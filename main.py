import os
import random
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    Union,
    overload,
)
import traceback
import attr
import uiautomator2 as u2
from droidbot import env_manager, input_manager
from droidbot.droidbot import DroidBot
import inspect
from copy import copy
from uiautomator2.exceptions import UiObjectNotFoundError

import time

from droidbot.guide import Guide

from hypothesis import given, strategies as st
from hypothesis.errors import NonInteractiveExampleWarning
import warnings

warnings.filterwarnings("ignore", category=NonInteractiveExampleWarning)
# from uiobject import MyUiObject


RULE_MARKER = "tool_rule"
INITIALIZE_RULE_MARKER = "tool_initialize_rule"
PRECONDITIONS_MARKER = "tool_preconditions"
INVARIANT_MARKER = "tool_invariant"


@attr.s()
class Rule:
    function = attr.ib()
    preconditions = attr.ib()


def rule() -> Callable:
    def accept(f):
        precondition = getattr(f, PRECONDITIONS_MARKER, ())
        rule = Rule(function=f, preconditions=precondition)

        def rule_wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        setattr(rule_wrapper, RULE_MARKER, rule)
        return rule_wrapper

    return accept


def precondition(precond: Callable[[Any], bool]) -> Callable:
    def accept(f):
        def precondition_wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        rule = getattr(f, RULE_MARKER, None)
        if rule is not None:
            new_rule = attr.evolve(rule, preconditions=rule.preconditions + (precond,))
            setattr(precondition_wrapper, RULE_MARKER, new_rule)
        else:
            setattr(
                precondition_wrapper,
                PRECONDITIONS_MARKER,
                getattr(f, PRECONDITIONS_MARKER, ()) + (precond,),
            )
        return precondition_wrapper

    return accept


# TODO
def initialize():
    '''
    An initialize decorator behaves like a rule, but all ``@initialize()`` decorated
    methods will be called before any ``@rule()`` decorated methods, in an arbitrary
    order.  Each ``@initialize()`` method will be called exactly once per run, unless
    one raises an exception.
    '''

    def accept(f):
        def initialize_wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        rule = Rule(function=f, preconditions=())
        setattr(initialize_wrapper, INITIALIZE_RULE_MARKER, rule)
        return initialize_wrapper

    return accept


class AndroidCheck(object):
    _rules_per_class: Dict[type, List[classmethod]] = {}
    _initializers_per_class: Dict[type, List[classmethod]] = {}

    def __init__(
        self,
        apk_path,
        device_serial="emulator-5554",
        output_dir="output",
        xml_path=None,
        main_path_path=None,
        source_activity=None,
        target_activity=None,
        is_emulator=True,
        policy_name=input_manager.DEFAULT_POLICY,
        random_input=True,
        script_path=None,
        event_interval=input_manager.DEFAULT_EVENT_INTERVAL,
        timeout=input_manager.DEFAULT_TIMEOUT,
        diverse_event_count=input_manager.DEFAULT_EVENT_COUNT,
        explore_event_count=0,
        cv_mode=None,
        debug_mode=None,
        keep_app=None,
        keep_env=None,
        profiling_method=None,
        grant_perm=True,
        enable_accessibility_hard=None,
        master=None,
        humanoid=None,
        ignore_ad=None,
        replay_output=None,
    ):
        self.apk_path = apk_path
        self.device_serial = device_serial
        self.guide = Guide(
            xml_path=xml_path,
            source_activity=source_activity,
            target_activity=target_activity,
        )
        self.droidbot = DroidBot(
            app_path=apk_path,
            device_serial=device_serial,
            is_emulator=is_emulator,
            output_dir=output_dir,
            env_policy=env_manager.POLICY_NONE,
            policy_name=policy_name,
            random_input=random_input,
            script_path=script_path,
            event_interval=event_interval,
            timeout=timeout,
            diverse_event_count=diverse_event_count,
            explore_event_count=explore_event_count,
            cv_mode=cv_mode,
            debug_mode=debug_mode,
            keep_app=keep_app,
            keep_env=keep_env,
            profiling_method=profiling_method,
            grant_perm=grant_perm,
            enable_accessibility_hard=enable_accessibility_hard,
            master=master,
            humanoid=humanoid,
            ignore_ad=ignore_ad,
            replay_output=replay_output,
            android_check=self,
            guide=self.guide,
            main_path_path=main_path_path
        )
        self.device = u2.connect(self.device_serial)
        self.device.implicitly_wait(5)  # set default element wait timeout = 5 seconds
        self._initialize_rules_to_run = copy(self.initialize_rules())
        if not self.rules():
            raise Exception(f"Type {type(self).__name__} defines no rules")
        self.current_rule = None
        self.execute_event = None

    def start(self):
        try:
            self.droidbot.start()
        except Exception:
            traceback.print_exc()

    @classmethod
    def initialize_rules(cls):
        try:
            return cls._initializers_per_class[cls]
        except KeyError:
            pass

        cls._initializers_per_class[cls] = []
        for _, v in inspect.getmembers(cls):
            r = getattr(v, INITIALIZE_RULE_MARKER, None)
            if r is not None:
                cls._initializers_per_class[cls].append(r)
        return cls._initializers_per_class[cls]

    @classmethod
    def rules(cls):
        try:
            return cls._rules_per_class[cls]
        except KeyError:
            pass

        cls._rules_per_class[cls] = []
        for _, v in inspect.getmembers(cls):
            r = getattr(v, RULE_MARKER, None)
            if r is not None:
                cls._rules_per_class[cls].append(r)
        return cls._rules_per_class[cls]

    def execute_initializers(self):
        for initializer in self._initialize_rules_to_run:
            initializer.function(self)

    def execute_rules(self, rules):
        '''random choose a rule, if the rule has preconditions, check the preconditions.
        if the preconditions are satisfied, execute the rule.'''
        if len(rules) == 0:
            return True
        rule_to_check = random.choice(rules)
        self.current_rule = rule_to_check
        return self.execute_rule(rule_to_check)

    def execute_rule(self, rule):
        if len(rule.preconditions) > 0:
            if not all(precond(self) for precond in rule.preconditions):
                return True
        # try to execute the rule and catch the exception if assertion error throws
        result = True
        try:
            time.sleep(1)
            result = rule.function(self)
            time.sleep(1)
        except UiObjectNotFoundError:
            print("Could not find the UI object.")
            return False
        except AssertionError:
            print("Assertion error.")
            # write_rule_result(
            #     f"Assertion error::{rule.function.__name__} failed",
            #     self.fuzzing.current_event,
            #     self.fuzzing.current_rule_event,
            #     self.execute_event,
            #     self.fuzzing.read_trace,
            # )
            # write_bug_record(
            #     self.fuzzing.current_testcase,
            #     self.fuzzing.current_event,
            #     self.fuzzing.current_rule_event,
            #     self.execute_event,
            #     self.fuzzing.bug_record_path,
            #     self.fuzzing.bug_num,
            # )
            # self.fuzzing.device.save_rule_state(
            #     self.fuzzing.result_path,
            #     self.fuzzing.current_testcase,
            #     self.fuzzing.current_event,
            #     self.fuzzing.current_rule_event,
            # )
            # self.fuzzing.current_rule_event = 0
            # self.fuzzing.find_bug = True
            # # self.fuzzing.current_event = self.fuzzing.current_event + 1
            return False
        finally:
            result = True

        return result

    def get_rules_that_pass_the_preconditions(self) -> List:
        '''Check all rules and return the list of rules that meet the preconditions.'''
        rules_to_check = self.rules()
        rules_meeting_preconditions = []
        for rule_to_check in rules_to_check:
            if len(rule_to_check.preconditions) > 0:
                if all(precond(self) for precond in rule_to_check.preconditions):
                    rules_meeting_preconditions.append(rule_to_check)
        return rules_meeting_preconditions

    def get_rules_without_preconditions(self):
        '''Return the list of rules that do not have preconditions.'''
        rules_to_check = self.rules()
        rules_without_preconditions = []
        for rule_to_check in rules_to_check:
            if len(rule_to_check.preconditions) == 0:
                rules_without_preconditions.append(rule_to_check)
        return rules_without_preconditions

    # def execute_method_by_lines(self, method):
    #     source = inspect.getsource(method)
    #     lines = source.splitlines()
    #     for line in lines:
    #         # exec(line, method.__globals__)
    #         print("executing line: ", line)

    def teardown(self):
        """Called after a run has finished executing to clean up any necessary
        state.
        Does nothing by default.
        """
        ...

    def click(self, **kwargs):
        # get name of the caller
        caller_frame = inspect.currentframe().f_back
        caller_name = caller_frame.f_code.co_name
        print(f"---------The calling function is {caller_name}----------")
        # Click on the device
        # self.device(**kwargs).click()
        # time.sleep(1)
        uiobject = self.device(**kwargs)
        if not uiobject.exists:
            raise UiObjectNotFoundError
        else:
            # time.sleep(1)
            current_rule_screenshot_path = self.fuzzing.device.save_rule_state(
                self.fuzzing.result_path,
                self.fuzzing.current_testcase,
                self.fuzzing.current_event,
                self.fuzzing.current_rule_event,
            )
            my_uiobject = MyUiObject(uiobject.info)
            view = View(my_uiobject.to_line(), [])
            time.sleep(1)
            uiobject.click()
            # print("info:  "+str(uiobject.info))
            # print("toline: "+my_uiobject.to_line())
            # print("uiobject:"+uiobject.get_text())
            self.execute_event = Event(
                view, "click", self.device, self.fuzzing.current_rule_event
            )
            draw_event(self.execute_event, current_rule_screenshot_path)
            write_rule_event(
                caller_name,
                self.fuzzing.current_event,
                self.fuzzing.current_rule_event,
                self.execute_event,
                self.fuzzing.read_trace,
            )
            print(
                "----------execute Rule::"
                + caller_name
                + "::"
                + self.execute_event.action
                + "------------"
            )
            self.fuzzing.current_rule_event += 1
            # current_rule_screenshot_path = self.fuzzing.device.save_rule_state(
            # self.fuzzing.result_path,
            # self.fuzzing.current_testcase,
            # self.fuzzing.current_event,
            # self.fuzzing.current_rule_event
            # )

    def long_click(self, **kwargs):
        # get name of the caller
        caller_frame = inspect.currentframe().f_back
        caller_name = caller_frame.f_code.co_name
        print(f"---------The calling function is {caller_name}----------")
        # Long click on the device
        # time.sleep(1)
        uiobject = self.device(**kwargs)
        if not uiobject.exists:
            raise UiObjectNotFoundError
        else:
            # time.sleep(1)
            current_rule_screenshot_path = self.fuzzing.device.save_rule_state(
                self.fuzzing.result_path,
                self.fuzzing.current_testcase,
                self.fuzzing.current_event,
                self.fuzzing.current_rule_event,
            )
            my_uiobject = MyUiObject(uiobject.info)
            view = View(my_uiobject.to_line(), [])
            time.sleep(1)
            uiobject.long_click()
            # print("info:  "+str(uiobject.info))
            # print("toline: "+my_uiobject.to_line())
            # print("uiobject:"+uiobject.get_text())
            self.execute_event = Event(
                view, "longclick", self.device, self.fuzzing.current_rule_event
            )
            draw_event(self.execute_event, current_rule_screenshot_path)
            write_rule_event(
                caller_name,
                self.fuzzing.current_event,
                self.fuzzing.current_rule_event,
                self.execute_event,
                self.fuzzing.read_trace,
            )
            print(
                "----------execute Rule::"
                + caller_name
                + "::"
                + self.execute_event.action
                + "------------"
            )
            self.fuzzing.current_rule_event += 1

    def double_click(self, **kwargs):
        # Double click on the device
        self.device(**kwargs).double_click()

    def swipe(self, **kwargs):
        # Swipe on the device
        self.device(**kwargs).swipe()

    def drag(self, **kwargs):
        # Drag on the device
        self.device(**kwargs).drag()

    def exists(self, **kwargs):
        # Check if the element exists
        return self.device(**kwargs).exists()


# t = AndroidCheck("droidbot\\apk\\amaze_3.4.3.apk").start()
