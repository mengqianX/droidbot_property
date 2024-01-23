import string
import sys
import json
import logging
import random
import copy
from threading import Timer
import time
from .utils import Time, safe_get_dict
from abc import abstractmethod
from .input_event import (
    InputEvent,
    KEY_RotateDeviceNeutralEvent,
    KEY_RotateDeviceRightEvent,
    KeyEvent,
    IntentEvent,
    RotateDevice,
    RotateDeviceNeutralEvent,
    RotateDeviceRightEvent,
    TouchEvent,
    ManualEvent,
    SetTextEvent,
    KillAppEvent,
    UIEvent,
)
from hypothesis import given, strategies as st
from .utg import UTG

# Max number of restarts
MAX_NUM_RESTARTS = 5
# Max number of steps outside the app
MAX_NUM_STEPS_OUTSIDE = 5
MAX_NUM_STEPS_OUTSIDE_KILL = 10
# Max number of replay tries
MAX_REPLY_TRIES = 5

# Some input event flags
EVENT_FLAG_STARTED = "+started"
EVENT_FLAG_START_APP = "+start_app"
EVENT_FLAG_STOP_APP = "+stop_app"
EVENT_FLAG_EXPLORE = "+explore"
EVENT_FLAG_NAVIGATE = "+navigate"
EVENT_FLAG_TOUCH = "+touch"

# Policy taxanomy
POLICY_MUTATE = "mutate"
POLICY_BUILD_MODEL = "build_model"
POLICY_RANDOM = "random"
POLICY_RANDOM_TWO = "random_two"
POLICY_NAIVE_DFS = "dfs_naive"
POLICY_GREEDY_DFS = "dfs_greedy"
POLICY_NAIVE_BFS = "bfs_naive"
POLICY_GREEDY_BFS = "bfs_greedy"
POLICY_REPLAY = "replay"
POLICY_MANUAL = "manual"
POLICY_MONKEY = "monkey"
POLICY_NONE = "none"
POLICY_MEMORY_GUIDED = "memory_guided"  # implemented in input_policy2

# explore mode
GUIDE = "guide"
DIVERSE = "diverse"
MAX_NUM_STEPS_OUTSIDE_THE_SHORTEST_PATH = 10


class InputInterruptedException(Exception):
    pass


class InputPolicy(object):
    """
    This class is responsible for generating events to stimulate more app behaviour
    It should call AppEventManager.send_event method continuously
    """

    def __init__(self, device, app, android_check=None):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.time_recoder = Time()
        
        self.device = device
        self.app = app
        self.action_count = 0
        self.master = None
        self.android_check = android_check
        self.input_manager = None

        self.time_needed_to_satisfy_precondition = []
        self.time_needed_to_trigger_bug = []

    def run_initial_rules(self):
        if len(self.android_check.initialize_rules()) == 0:
            self.logger.info("No initialize rules")
        else:
            result = self.android_check.execute_rules(
                self.android_check.initialize_rules()
            )
            if result:
                self.logger.info("-------initialize successfully-----------")
            else:
                self.logger.error("-------initialize failed-----------")

    def start(self, input_manager):
        """
        start producing events
        :param input_manager: instance of InputManager
        """
        self.action_count = 0
        self.input_manager = input_manager       
        while (
            input_manager.enabled
            and self.action_count
            < input_manager.diverse_event_count + input_manager.explore_event_count
        ):
            try:
                # # make sure the first event is go to HOME screen
                # # the second event is to start the app
                # if self.action_count == 0 and self.master is None:
                #     event = KeyEvent(name="HOME")
                # elif self.action_count == 1 and self.master is None:
                #     event = IntentEvent(self.app.get_start_intent())
                self.device.u2.set_fastinput_ime(True)
                self.logger.info("action count: %d" % self.action_count)
                if self.action_count == 0 and self.master is None:
                    event = KillAppEvent(app=self.app)
                elif self.action_count == 1 and self.master is None:
                    event = IntentEvent(self.app.get_start_intent())
                else:
                    event = self.generate_event()
                input_manager.add_event(event)
            except KeyboardInterrupt:
                break
            except InputInterruptedException as e:
                self.logger.info("stop sending events: %s" % e)
                self.logger.info("action count: %d" % self.action_count)
                break
            # except RuntimeError as e:
            #     self.logger.warning(e.message)
            #     break
            except RuntimeError as e:
                self.logger.info("RuntimeError: %s, stop sending events" % e)
                break
            except Exception as e:
                self.logger.warning("exception during sending events: %s" % e)
                import traceback

                traceback.print_exc()
                continue
            self.action_count += 1
        self.tear_down()

    @abstractmethod    
    def tear_down(self):
        """
        输出一些统计信息
        """
        pass
    @abstractmethod
    def generate_event(self):
        """
        generate an event
        @return:
        """
        pass

    @abstractmethod
    def explore_app(self):
        """
        generate an event
        @return:
        """
        pass

class UtgBasedInputPolicy(InputPolicy):
    """
    state-based input policy
    """

    def __init__(self, device, app, random_input, android_check=None, guide=None):
        super(UtgBasedInputPolicy, self).__init__(device, app, android_check)
        self.random_input = random_input
        self.script = None
        self.master = None
        self.script_events = []
        self.last_event = None
        self.last_state = None
        self.current_state = None
        self.guide = guide
        self.utg = UTG(
            device=device, app=app, random_input=random_input, guide=self.guide
        )
        self.script_event_idx = 0
        if self.device.humanoid is not None:
            self.humanoid_view_trees = []
            self.humanoid_events = []

    def check_rule_with_precondition(self):
        rules_to_check = self.android_check.get_rules_that_pass_the_preconditions()
        if len(rules_to_check) == 0:
            print("No rules match the precondition")
            if hasattr(self,"not_reach_precondition_path_number"):
                self.not_reach_precondition_path_number.append(self.path_index)
            return
            # continue
        if hasattr(self,"reach_precondition_path_number"):
            self.reach_precondition_path_number.append(self.path_index)
        rule_to_check = random.choice(rules_to_check)

        if rule_to_check is not None:
            self.logger.info("-------check rule : %s------" % rule_to_check)
            result = self.android_check.execute_rule(rule_to_check)
            if result:
                self.logger.info("-------check rule : pass------")
                self.logger.info("-------time from start : %s-----------" % str(self.time_recoder.get_time_duration()))
                
                if hasattr(self, 'pass_rule_path_number'):
                  self.pass_rule_path_number.append(self.path_index)
            else:
                self.logger.error("-------rule execute failed-----------")
                self.logger.info("-------time from start : %s-----------" % str(self.time_recoder.get_time_duration()))
                self.time_needed_to_trigger_bug.append(self.time_recoder.get_time_duration())
                if hasattr(self, 'fail_rule_path_number'):
                    self.fail_rule_path_number.append(self.path_index)

    def check_rule_without_precondition(self):
        rules_to_check = self.android_check.get_rules_without_preconditions()
        if len(rules_to_check) > 0:
            result = self.android_check.execute_rules(
                self.android_check.get_rules_without_preconditions()
            )
            if result:
                print("-------rule_without_precondition execute success-----------")
            else:
                print("-------rule_without_precondition execute failed-----------")
        else:
            print("-------no rule_without_precondition to execute-----------")

    def stop_app_events(self):
        # self.logger.info("reach the target state, restart the app")
        stop_app_intent = self.app.get_stop_intent()
        stop_event = IntentEvent(stop_app_intent)
        self.logger.info("stop the app and go back to the main activity")
        return stop_event

    def generate_event(self):
        """
        generate an event
        @return:
        """
        # 在app 启动后执行定义好的初始化事件
        if self.action_count == 2:
            self.run_initial_rules()
        # Get current device state
        self.current_state = self.device.get_current_state()
        if self.current_state is None:
            import time

            time.sleep(5)
            return KeyEvent(name="BACK")

        self.__update_utg()

        event = None

        # first explore the app, then test the properties
        if self.action_count < self.input_manager.explore_event_count:
            self.logger.info("Explore the app")
            event = self.explore_app()
        elif self.action_count == self.input_manager.explore_event_count:
            event = KillAppEvent(app=self.app)
        else:
            self.logger.info("Test the app")
            event = self.generate_event_based_on_utg()

        self.last_state = self.current_state
        self.last_event = event
        return event

    def __update_utg(self):
        self.utg.add_transition(self.last_event, self.last_state, self.current_state)

    @abstractmethod
    def generate_event_based_on_utg(self):
        """
        generate an event based on UTG
        :return: InputEvent
        """
        pass

class MutatePolicy(UtgBasedInputPolicy):
    """
    测试人员提供一条main path, 然后在main path上进行变异
    """

    def __init__(self, device, app, random_input, android_check=None, guide=None,main_path_path=None):
        super(MutatePolicy, self).__init__(
            device, app, random_input, android_check, guide
        )
        self.logger = logging.getLogger(self.__class__.__name__)
        self.main_path_path = main_path_path
        self.__nav_target = None
        self.__nav_num_steps = -1
        self.__num_restarts = 0
        self.__num_steps_outside = 0
        self.__event_trace = ""
        self.__missed_states = set()
        self.__random_explore = False
        # used in execute main path
        self.main_path = self.get_main_path()
        self.main_path_list = copy.deepcopy(self.main_path)
        self.execute_main_path = True
        # used in mutate phase
        self.mutate_node_index_on_main_path = -2
        self.start_mutate_on_the_node = False
        self.shortest_path_states = None
        self.max_number_of_mutate_steps_on_single_node = 20
        self.current_number_of_mutate_steps_on_single_node = 0
        self.stop_mutate = False
        self.step_on_the_path = 0  # 用于记录在main path 上执行了几个event,方便引导app到达目标base node

        # used in diverse phase
        self.path_index = -1  # currently explore path index
        self.paths = []  # paths from start state to target state
        self.not_reach_precondition_path_number = []
        self.reach_precondition_path_number = []
        self.pass_rule_path_number = []
        self.fail_rule_path_number = []
        self.step_in_each_path = 0
        # 在我们计算diverse path的时候，是在G图上进行计算，还是G2. True 代表G， False 代表G2
        self.compute_diverse_path_on_G_or_G2 = True

    def get_main_path(self):
        import json
        if self.main_path_path is None:
            raise Exception("main path path is None")
        f = open(self.main_path_path, "r")
        event_list = json.load(f)
        return event_list

    def generate_event(self):
        """
        首先按照用户指定的path走一遍,然后在path上进行变异
        """
        self.current_state = self.device.get_current_state(self.action_count)

        self.__update_utg()

        event = self.check_the_app_on_foreground()
        if event is not None:
            self.last_state = self.current_state
            self.last_event = event
            return event
        # 在app 启动后执行定义好的初始化事件
        if self.action_count == 2:
            self.run_initial_rules()
            time.sleep(2)
            return None
        if self.action_count == 3:
            self.utg.first_state_after_initialization = self.current_state

        if self.execute_main_path:
            # 首先，根据用户指定的path，生成一条路径到达Precondition
            event = self.get_main_path_event()
            if event:
                self.last_state = self.current_state
                self.last_event = event
                return event
            else:
                self.execute_main_path = False
                # 如果探索到了target activity，则设置好对应的target state，方便后面直接引导过去
                rules_satisfy_precondition = (
                    self.android_check.get_rules_that_pass_the_preconditions()
                )
                if len(rules_satisfy_precondition) > 0:
                    self.logger.info("has rule that matches the precondition")
                    self.utg.set_target_state(self.current_state)
                else:
                    self.logger.info("no rule matches the precondition")


        # 如果变异停止了，则根据model开始生成diverse path 来测property
        if self.stop_mutate:
            event = self.generate_events_from_diverse_paths()
        else:
            event = self.mutate_the_main_path()

        self.last_state = self.current_state
        self.last_event = event
        return event

    def get_main_path_event(self):
        """
        依次返回main path上的event
        """
        if len(self.main_path_list) == 0:
            return None
        event_dict = self.main_path_list.pop(0)
        event = self.get_event_from_dict(event_dict)
        return event

    def get_event_from_dict(self, event_dict):
        # 如果是set_text事件，则需要先获取view，然后再生成任意字符串的set_text事件
        if event_dict["event_type"] == "set_text":
            view = self.current_state.get_view_by_attribute(event_dict["ui_element"])
            if view is None:
                return None
            event = SetTextEvent(
                view=view,
                text=st.text(
                    alphabet=string.ascii_letters, min_size=1, max_size=5
                ).example(),
            )
            return event
        view = self.current_state.get_view_by_attribute(event_dict["ui_element"])
        if view is None:
            return None
        event = TouchEvent(view=view)
        return event

    def mutate_the_main_path(self):
        event = None
        if self.mutate_node_index_on_main_path == -2:
            self.mutate_node_index_on_main_path = len(self.main_path) - 1
            return self.stop_app_events()
        # 意味着停止变异
        if self.mutate_node_index_on_main_path == -1:
            self.logger.info("finish mutate the main path")
            self.start_mutate_on_the_node = False
            self.current_number_of_mutate_steps_on_single_node = 0
            self.stop_mutate = True
            return self.stop_app_events()
        # 首先判断是否开始在主路径上进行变异，如果还没开始，则首先要将app引导到开始变异的那个节点
        if not self.start_mutate_on_the_node:

            if self.step_on_the_path == self.mutate_node_index_on_main_path:
                self.start_mutate_on_the_node = True
                self.logger.info(
                    "reach the node and start mutate on the node: %d"
                    % self.mutate_node_index_on_main_path
                )
                self.step_on_the_path = 0
            # 如果还没到达目标node，则继续引导app到目标node
            else:
                view = self.main_path[self.step_on_the_path]
                event = self.get_event_from_dict(view)
                self.step_on_the_path += 1
                return event

        # 如果已经开始在主路径上进行变异，则继续变异
        # 只允许最多变异N步，如果超过N步，则重新启动app,选择下一个变异的Node
        if (
            self.current_number_of_mutate_steps_on_single_node
            > self.max_number_of_mutate_steps_on_single_node
        ):
            self.logger.info(
                "reach the max number of mutate steps on single node, restart the app"
            )
            self.start_mutate_on_the_node = False
            self.mutate_node_index_on_main_path -= 1
            self.current_number_of_mutate_steps_on_single_node = 0
            return self.stop_app_events()
        else:
            self.logger.info(
                "mutate on the node: %d" % self.mutate_node_index_on_main_path
            )
            self.current_number_of_mutate_steps_on_single_node += 1
            event = self.explore_app()
            return event

    def explore_app(self) -> InputEvent:
        """
        generate an event based on current UTG
        @return: InputEvent
        """
        current_state = self.current_state
        self.logger.info("Current state: %s" % current_state.state_str)
        if current_state.state_str in self.__missed_states:
            self.__missed_states.remove(current_state.state_str)

        if current_state.get_app_activity_depth(self.app) < 0:
            # If the app is not in the activity stack
            start_app_intent = self.app.get_start_intent()

            # It seems the app stucks at some state, has been
            # 1) force stopped (START, STOP)
            #    just start the app again by increasing self.__num_restarts
            # 2) started at least once and cannot be started (START)
            #    pass to let viewclient deal with this case
            # 3) nothing
            #    a normal start. clear self.__num_restarts.

            if self.__event_trace.endswith(
                EVENT_FLAG_START_APP + EVENT_FLAG_STOP_APP
            ) or self.__event_trace.endswith(EVENT_FLAG_START_APP):
                self.__num_restarts += 1
                self.logger.info(
                    "The app had been restarted %d times.", self.__num_restarts
                )
            else:
                self.__num_restarts = 0

            # pass (START) through
            if not self.__event_trace.endswith(EVENT_FLAG_START_APP):
                if self.__num_restarts > MAX_NUM_RESTARTS:
                    # If the app had been restarted too many times, enter random mode
                    msg = "The app had been restarted too many times. Entering random mode."
                    self.logger.info(msg)
                    self.__random_explore = True
                else:
                    # Start the app
                    self.__event_trace += EVENT_FLAG_START_APP
                    self.logger.info("Trying to start the app...")
                    return IntentEvent(intent=start_app_intent)

        elif current_state.get_app_activity_depth(self.app) > 0:
            # If the app is in activity stack but is not in foreground
            self.__num_steps_outside += 1

            if self.__num_steps_outside > MAX_NUM_STEPS_OUTSIDE:
                # If the app has not been in foreground for too long, try to go back
                if self.__num_steps_outside > MAX_NUM_STEPS_OUTSIDE_KILL:
                    stop_app_intent = self.app.get_stop_intent()
                    go_back_event = IntentEvent(stop_app_intent)
                else:
                    go_back_event = KeyEvent(name="BACK")
                self.__event_trace += EVENT_FLAG_NAVIGATE
                self.logger.info("Going back to the app...")
                return go_back_event
        else:
            # If the app is in foreground
            self.__num_steps_outside = 0

        # Get all possible input events
        possible_events = current_state.get_possible_input()

        if self.random_input:
            random.shuffle(possible_events)

        possible_events.append(KeyEvent(name="BACK"))
        # if self.search_method == POLICY_GREEDY_DFS:
        #     possible_events.append(KeyEvent(name="BACK"))
        # elif self.search_method == POLICY_GREEDY_BFS:
        #     possible_events.insert(0, KeyEvent(name="BACK"))

        # first try to select the actions that lead to activity transition. e.g., open drawer and click item on it.
        # for input_event in possible_events:
        #     if not self.utg.is_event_explored(
        #         event=input_event, state=current_state
        #     ) and self.is_event_contains_drawer(input_event):
        #         self.logger.info("find the drawer event ")
        #         return input_event

        # If there is an unexplored event, try the event first
        for input_event in possible_events:
            if not self.utg.is_event_explored(event=input_event, state=current_state):
                self.logger.info("Trying an unexplored event.")
                self.__event_trace += EVENT_FLAG_EXPLORE
                return input_event

        target_state = self.__get_nav_target(current_state)
        if target_state:
            navigation_steps = self.utg.get_navigation_steps(
                from_state=current_state, to_state=target_state
            )
            if navigation_steps and len(navigation_steps) > 0:
                self.logger.info(
                    "Navigating to %s, %d steps left."
                    % (target_state.state_str, len(navigation_steps))
                )
                self.__event_trace += EVENT_FLAG_NAVIGATE
                return navigation_steps[0][1]

        if self.__random_explore:
            self.logger.info("Trying random event.")
            random.shuffle(possible_events)
            return possible_events[0]

        # If couldn't find a exploration target, stop the app
        stop_app_intent = self.app.get_stop_intent()
        self.logger.info("Cannot find an exploration target. Trying to restart app...")
        self.__event_trace += EVENT_FLAG_STOP_APP
        return IntentEvent(intent=stop_app_intent)

    def generate_events_from_diverse_paths(self):
        next_event = None

        # 如果还没开始进行diverse phase,则选择最短的path先进行探索
        if self.path_index == -1:
            # 获取从first state 到 target state的path
            self.paths = self.utg.get_paths_mutate_on_the_main_path(state_str_or_structure=self.compute_diverse_path_on_G_or_G2)
            # augument_path = self.utg.get_paths_with_loop_mutate_on_base_path()
            # self.paths.extend(augument_path)
            # 重新安装app，防止之前的状态影响当前的探索
            self.device.uninstall_app(self.app)
            self.device.install_app(self.app)
            self.need_initialize = True
            self.path_index = 0
            self.step_in_each_path = 0
            start_app_intent = self.app.get_start_intent()
            return IntentEvent(intent=start_app_intent)
        if self.need_initialize:
            self.run_initial_rules()
            self.need_initialize = False
            return None     

        # 还没有到达target state，则继续探索当前path
        if self.path_index < len(self.paths):
            if self.paths[self.path_index] is None:
                self.logger.info("path is None")
                self.path_index += 1
                self.step_in_each_path = 0
                return self.stop_app_events()
            if self.step_in_each_path == len(self.paths[self.path_index]):
                # 说明已经走到最后一个state了，check property
                self.check_rule_with_precondition()
            # 如果当前step 大于等于path的长度，则结束当前path
            if self.step_in_each_path >= len(self.paths[self.path_index]):
                self.logger.info("finish current path: %d, " % self.path_index)
                self.path_index += 1
                self.step_in_each_path = 0
                return self.stop_app_events()
            
            self.logger.info(
                "current path length %d " % len(self.paths[self.path_index])
            )
            # 老方法：按照当前state的structure和path上的state的structure进行比较，找到下一个event，
            # 不太靠谱，因为抽象的原因导致这种方式匹配state不准确
            # 新方法：不匹配state信息，只匹配event信息。也就是说，直接在当前state上查找是否能找到event对应的view。
            # 如果能找到，则返回这个view对于的event
            next_event = self.paths[self.path_index][self.step_in_each_path][2]
            if isinstance(next_event, UIEvent):
                view_in_next_event = next_event.view
                if self.current_state.is_view_exist(view_in_next_event):
                    self.logger.info("find next event in the %d path" % self.path_index)
                    self.step_in_each_path += 1
                    return next_event
                else:
                    # 如果没有找到下一个事件，说明当前path走不通，就放弃当前path,走下一条path
                    self.logger.info("cannot find next event in the %d path" % self.path_index)
                    self.not_reach_precondition_path_number.append(self.path_index)
                    self.path_index += 1
                    self.logger.info("start next path: %d" % self.path_index)
                    self.step_in_each_path = 0
                    return self.stop_app_events()
            else:
                self.step_in_each_path += 1
                return next_event
        else:
            raise InputInterruptedException("finish explore all paths")
        return None
    
    def tear_down(self):
        self.logger.info("All paths number: %d", len(self.paths))
        self.logger.info("finish explore paths: %d", self.path_index)
        self.logger.info(
            "number of reach precondition paths: %d",
            len(self.reach_precondition_path_number),
        )
        self.logger.info(
            "number of not reach precondition paths: %d",
            len(self.not_reach_precondition_path_number),
        )
        self.logger.info(
            "number of pass rule paths: %d", len(self.pass_rule_path_number)
        )
        self.logger.info(
            "number of fail rule paths: %d", len(self.fail_rule_path_number)
        )

    def __get_nav_target(self, current_state):
        # If last event is a navigation event
        if self.__nav_target and self.__event_trace.endswith(EVENT_FLAG_NAVIGATE):
            navigation_steps = self.utg.get_navigation_steps(
                from_state=current_state, to_state=self.__nav_target
            )
            if navigation_steps and 0 < len(navigation_steps) <= self.__nav_num_steps:
                # If last navigation was successful, use current nav target
                self.__nav_num_steps = len(navigation_steps)
                return self.__nav_target
            else:
                # If last navigation was failed, add nav target to missing states
                self.__missed_states.add(self.__nav_target.state_str)

        reachable_states = self.utg.get_reachable_states(current_state)
        if self.random_input:
            random.shuffle(reachable_states)

        for state in reachable_states:
            # Only consider foreground states
            if state.get_app_activity_depth(self.app) != 0:
                continue
            # Do not consider missed states
            if state.state_str in self.__missed_states:
                continue
            # Do not consider explored states
            if self.utg.is_state_explored(state):
                continue
            self.__nav_target = state
            navigation_steps = self.utg.get_navigation_steps(
                from_state=current_state, to_state=self.__nav_target
            )
            if navigation_steps is not None and len(navigation_steps) > 0:
                self.__nav_num_steps = len(navigation_steps)
                return state

        self.__nav_target = None
        self.__nav_num_steps = -1
        return None

    def check_the_app_on_foreground(self):
        if self.current_state.get_app_activity_depth(self.app) < 0:
            # If the app is not in the activity stack
            start_app_intent = self.app.get_start_intent()

            # It seems the app stucks at some state, has been
            # 1) force stopped (START, STOP)
            #    just start the app again by increasing self.__num_restarts
            # 2) started at least once and cannot be started (START)
            #    pass to let viewclient deal with this case
            # 3) nothing
            #    a normal start. clear self.__num_restarts.

            if self.__event_trace.endswith(
                EVENT_FLAG_START_APP + EVENT_FLAG_STOP_APP
            ) or self.__event_trace.endswith(EVENT_FLAG_START_APP):
                self.__num_restarts += 1
                self.logger.info(
                    "The app had been restarted %d times.", self.__num_restarts
                )
            else:
                self.__num_restarts = 0

            # pass (START) through
            if not self.__event_trace.endswith(EVENT_FLAG_START_APP):
                if self.__num_restarts > MAX_NUM_RESTARTS:
                    # If the app had been restarted too many times, enter random mode
                    msg = "The app had been restarted too many times. Entering random mode."
                    self.logger.info(msg)
                    self.__random_explore = True
                else:
                    # Start the app
                    self.__event_trace += EVENT_FLAG_START_APP
                    self.logger.info("Trying to start the app...")
                    return IntentEvent(intent=start_app_intent)

        elif self.current_state.get_app_activity_depth(self.app) > 0:
            # If the app is in activity stack but is not in foreground
            self.__num_steps_outside += 1

            if self.__num_steps_outside > MAX_NUM_STEPS_OUTSIDE:
                # If the app has not been in foreground for too long, try to go back
                if self.__num_steps_outside > MAX_NUM_STEPS_OUTSIDE_KILL:
                    stop_app_intent = self.app.get_stop_intent()
                    go_back_event = IntentEvent(stop_app_intent)
                else:
                    go_back_event = KeyEvent(name="BACK")
                self.__event_trace += EVENT_FLAG_NAVIGATE
                self.logger.info("Going back to the app...")
                return go_back_event
        else:
            # If the app is in foreground
            self.__num_steps_outside = 0

    def stop_app_events(self):
        # self.logger.info("reach the target state, restart the app")
        stop_app_intent = KillAppEvent(app=self.app)
        # stop_event = IntentEvent(stop_app_intent)

        self.__event_trace += EVENT_FLAG_STOP_APP
        self.logger.info("stop the app and go back to the main activity")
        return stop_app_intent

    def __update_utg(self):
        self.utg.add_transition(self.last_event, self.last_state, self.current_state)

class BuildModelPolicy(UtgBasedInputPolicy):
    """
    DFS/BFS (according to search_method) strategy to explore UFG (new)
    这个类用于: 用户没有提供base path,因此:
    1. 工具首先要进行探索，构建一个模型
    2. 基于这个模型，生成多条路径，然后执行这些路径
    """

    def __init__(
        self, device, app, random_input, search_method, android_check=None, guide=None, build_model_timeout=0
    ):
        super(BuildModelPolicy, self).__init__(
            device, app, random_input, android_check, guide
        )
        self.logger = logging.getLogger(self.__class__.__name__)
        self.search_method = search_method

        self.preferred_buttons = [
            "yes",
            "ok",
            "activate",
            "detail",
            "more",
            "access",
            "allow",
            "check",
            "agree",
            "try",
            "go",
            "next",
        ]

        self.__nav_target = None
        self.__nav_num_steps = -1
        self.__num_restarts = 0
        self.__num_steps_outside = 0
        self.__event_trace = ""
        self.__missed_states = set()
        self.__random_explore = False

        self.guide = guide
        # yiheng: add a new variable to record the current explore mode
        # if mode = GUIDE, it means we didn't encounter the target state,
        #   so we choose to guide the exploration to the target state.
        # if mode = DIVERSE, it means we have encountered the target state,
        #   we choose to explore the app in order to generate more states to encounter the target state.
        self.explore_mode = GUIDE
        self.number_of_steps_outside_the_shortest_path = 0
        self.reached_state_on_the_shortest_path = []

        self.reach_target_during_exploration = False

        # used in diverse phase
        self.path_index = -1  # currently explore path index
        self.paths = []  # paths from start state to target state
        # whether reach target state, if true, we start next paths.
        # self.reach_target_after_last_event = False
        self.not_reach_precondition_path_number = []
        self.reach_precondition_path_number = []
        self.pass_rule_path_number = []
        self.fail_rule_path_number = []
        self.step_in_each_path = 0

        # 在我们计算diverse path的时候，是在G图上进行计算，还是G2. True 代表G， False 代表G2
        self.compute_diverse_path_on_G_or_G2 = True
        self.enable_buide_model = True
        self.build_model_timeout = build_model_timeout
        if self.build_model_timeout > 0:
            self.logger.info("build model timeout: %d" % self.build_model_timeout)
            self.timer = Timer(self.build_model_timeout, self.stop_build_model)
            self.timer.start()

        # 记录没有走通的paths的前缀,在每一次执行一条path之前，都会检查当前path是否是之前走过的失败的path的前缀，如果是，则跳过这条path
        self.not_reach_precondition_path_prefix = set()
        self.skip_path = []

    def stop_build_model(self):
        # 使用一个计时器，如果超过一定时间则停止构建模型
        self.enable_buide_model = False

    def generate_event(self):   
        """
        generate an event
        @return:
        """
        # Get current device state
        self.current_state = self.device.get_current_state(self.action_count)
        if self.current_state is None:
            import time

            time.sleep(5)
            return KeyEvent(name="BACK")

        self.__update_utg()

        # event = self.check_the_app_on_foreground()
        # if event is not None:
        #     self.last_state = self.current_state
        #     self.last_event = event
        #     return event
        
        # 在app 启动后执行定义好的初始化事件
        if self.action_count == 2:
            
            self.run_initial_rules()
            import time
            time.sleep(2)
            return None
        
        if self.action_count == 3:
            self.utg.first_state_after_initialization = self.current_state

        # first explore the app, then generate diverse paths to test the properties
        if self.action_count < self.input_manager.explore_event_count and self.enable_buide_model:
            self.logger.info("Explore the app")
            event = self.explore_app() 
        elif self.action_count == self.input_manager.explore_event_count:
            event = KillAppEvent(app=self.app)
        else:
            self.logger.info("Test the app")
            event = self.generate_event_based_on_utg()

        self.last_state = self.current_state
        self.last_event = event
        return event
    
    def generate_event_based_on_utg(self):
        """
        generate an event based on current UTG
        @return: InputEvent
        """
        current_state = self.current_state
        self.logger.info("Current state: %s" % current_state.state_str)
        if current_state.state_str in self.__missed_states:
            self.__missed_states.remove(current_state.state_str)

        if current_state.get_app_activity_depth(self.app) < 0:
            # If the app is not in the activity stack
            start_app_intent = self.app.get_start_intent()

            # It seems the app stucks at some state, has been
            # 1) force stopped (START, STOP)
            #    just start the app again by increasing self.__num_restarts
            # 2) started at least once and cannot be started (START)
            #    pass to let viewclient deal with this case
            # 3) nothing
            #    a normal start. clear self.__num_restarts.

            if self.__event_trace.endswith(
                EVENT_FLAG_START_APP + EVENT_FLAG_STOP_APP
            ) or self.__event_trace.endswith(EVENT_FLAG_START_APP):
                self.__num_restarts += 1
                self.logger.info(
                    "The app had been restarted %d times.", self.__num_restarts
                )
            else:
                self.__num_restarts = 0

            # pass (START) through
            # if not self.__event_trace.endswith(EVENT_FLAG_START_APP):
            # if self.__num_restarts > MAX_NUM_RESTARTS:
            #     # If the app had been restarted too many times, enter random mode
            #     msg = "The app had been restarted too many times."
            #     self.logger.info(msg)
            #     self.__random_explore = True
            # else:
            # Start the app
            self.__event_trace += EVENT_FLAG_START_APP
            self.logger.info("Trying to start the app...")
            return IntentEvent(intent=start_app_intent)

        elif current_state.get_app_activity_depth(self.app) > 0:
            # If the app is in activity stack but is not in foreground
            self.__num_steps_outside += 1

            if self.__num_steps_outside > MAX_NUM_STEPS_OUTSIDE:
                # If the app has not been in foreground for too long, try to go back
                if self.__num_steps_outside > MAX_NUM_STEPS_OUTSIDE_KILL:
                    stop_app_intent = self.app.get_stop_intent()
                    go_back_event = IntentEvent(stop_app_intent)
                else:
                    go_back_event = KeyEvent(name="BACK")
                self.__event_trace += EVENT_FLAG_NAVIGATE
                self.logger.info("Going back to the app...")
                return go_back_event
        else:
            # If the app is in foreground
            self.__num_steps_outside = 0

        if self.reach_target_during_exploration:
            event = self.generate_events_from_diverse_paths()
            return event
        else:
            print("didnot reach target state, continue to explore")

        # Get all possible input events
        possible_events = current_state.get_possible_input()

        if self.random_input:
            random.shuffle(possible_events)

        if self.search_method == POLICY_GREEDY_DFS:
            possible_events.append(KeyEvent(name="BACK"))
        elif self.search_method == POLICY_GREEDY_BFS:
            possible_events.insert(0, KeyEvent(name="BACK"))

        # If there is an unexplored event, try the event first
        for input_event in possible_events:
            if not self.utg.is_event_explored(event=input_event, state=current_state):
                self.logger.info("Trying an unexplored event.")
                self.__event_trace += EVENT_FLAG_EXPLORE
                return input_event

        target_state = self.__get_nav_target(current_state)
        if target_state:
            navigation_steps = self.utg.get_navigation_steps(
                from_state=current_state, to_state=target_state
            )
            if navigation_steps and len(navigation_steps) > 0:
                self.logger.info(
                    "Navigating to %s, %d steps left."
                    % (target_state.state_str, len(navigation_steps))
                )
                self.__event_trace += EVENT_FLAG_NAVIGATE
                return navigation_steps[0][1]

        if self.__random_explore:
            self.logger.info("Trying random event.")
            random.shuffle(possible_events)
            return possible_events[0]

        # If couldn't find a exploration target, stop the app
        stop_app_intent = self.app.get_stop_intent()
        self.logger.info("Cannot find an exploration target. Trying to restart app...")
        self.__event_trace += EVENT_FLAG_STOP_APP
        return IntentEvent(intent=stop_app_intent)
    
    def generate_events_from_diverse_paths(self):
        next_event = None

        # 如果还没开始进行diverse phase,则选择最短的path先进行探索
        if self.path_index == -1:
            # 获取从first state 到 target state的path
            self.paths = self.utg.get_paths_mutate_on_the_main_path(state_str_or_structure=self.compute_diverse_path_on_G_or_G2,number_of_meet_target=0)
            paths_2 = self.utg.get_paths_mutate_on_the_main_path(state_str_or_structure=self.compute_diverse_path_on_G_or_G2,number_of_meet_target=-1)
            # 重新安装app，防止之前的状态影响当前的探索
            self.device.uninstall_app(self.app)
            self.device.install_app(self.app)
            self.need_initialize = True
            self.path_index = 0
            self.step_in_each_path = 0
            start_app_intent = self.app.get_start_intent()
            return IntentEvent(intent=start_app_intent)
        
        if self.need_initialize:
            self.run_initial_rules()
            self.need_initialize = False
            return None
        

        # 还没有探索完所有的path，则继续
        if self.path_index < len(self.paths):
            if self.paths[self.path_index] is None:
                self.logger.info("path is None")
                self.path_index += 1
                self.step_in_each_path = 0
                return self.stop_app_events()
            
            if self.step_in_each_path >=len(self.paths[self.path_index]):
                # 说明已经走到最后一个state了，check property
                rules_to_check = self.android_check.get_rules_that_pass_the_preconditions()
                if len(rules_to_check) > 0:
                    self.time_needed_to_satisfy_precondition.append(self.time_recoder.get_time_duration())
                    self.check_rule_with_precondition()
                else:
                    self.not_reach_precondition_path_number.append(self.path_index)
                self.logger.info("finish current path: %d, " % self.path_index)
                self.path_index += 1
                self.step_in_each_path = 0

                return self.stop_app_events()

            self.logger.info(
                "current path length %d " % len(self.paths[self.path_index])
            )
            # 在每条path开始之前检查一下当前path是否是之前走过的失败的path的前缀，如果是，则跳过这条path
            if self.step_in_each_path == 0 and len(self.not_reach_precondition_path_prefix) > 0:
                for i in range(len(self.paths[self.path_index])):
                    if tuple(self.paths[self.path_index][:i+1]) in self.not_reach_precondition_path_prefix:
                        self.logger.info("skip the path: %d" % self.path_index)
                        self.skip_path.append(self.path_index)
                        self.path_index += 1
                        self.step_in_each_path = 0
                        return self.stop_app_events()
                


            # 老方法：按照当前state的structure和path上的state的structure进行比较，找到下一个event，
            # 不太靠谱，因为抽象的原因导致这种方式匹配state不准确
            # 新方法：不匹配state信息，只匹配event信息。也就是说，直接在当前state上查找是否能找到event对应的view。
            # 如果能找到，则返回这个view对于的event
            next_event = self.paths[self.path_index][self.step_in_each_path][2]
            if isinstance(next_event, UIEvent):
                view_in_next_event = next_event.view
                if self.current_state.is_view_exist(view_in_next_event):
                    self.logger.info("find next event in the %d path" % self.path_index)
                    self.step_in_each_path += 1
                    return next_event
            else:
                self.step_in_each_path += 1
                return next_event

            # 如果没有找到下一个事件，说明当前path走不通，就放弃当前path,走下一条path
            self.logger.info("cannot find next event in the %d path" % self.path_index)
            self.not_reach_precondition_path_number.append(self.path_index)
            self.not_reach_precondition_path_prefix.add(tuple(self.paths[self.path_index][:self.step_in_each_path+1]))
            self.path_index += 1
            self.logger.info("start next path: %d" % self.path_index)
            self.step_in_each_path = 0
            return self.stop_app_events()
        else:
            raise InputInterruptedException("finish explore all paths")
        return None

    def explore_app(self) -> InputEvent:
        """
        generate an event based on current UTG
        @return: InputEvent
        """
        current_state = self.current_state
        self.logger.info("Current state: %s" % current_state.state_str)
        if current_state.state_str in self.__missed_states:
            self.__missed_states.remove(current_state.state_str)

        if current_state.get_app_activity_depth(self.app) < 0:
            # If the app is not in the activity stack
            start_app_intent = self.app.get_start_intent()

            # It seems the app stucks at some state, has been
            # 1) force stopped (START, STOP)
            #    just start the app again by increasing self.__num_restarts
            # 2) started at least once and cannot be started (START)
            #    pass to let viewclient deal with this case
            # 3) nothing
            #    a normal start. clear self.__num_restarts.

            if self.__event_trace.endswith(
                EVENT_FLAG_START_APP + EVENT_FLAG_STOP_APP
            ) or self.__event_trace.endswith(EVENT_FLAG_START_APP):
                self.__num_restarts += 1
                self.logger.info(
                    "The app had been restarted %d times.", self.__num_restarts
                )
            else:
                self.__num_restarts = 0

            # pass (START) through
            if not self.__event_trace.endswith(EVENT_FLAG_START_APP):
                if self.__num_restarts > MAX_NUM_RESTARTS:
                    # If the app had been restarted too many times, enter random mode
                    msg = "The app had been restarted too many times. Entering random mode."
                    self.logger.info(msg)
                    self.__random_explore = True
                else:
                    # Start the app
                    self.__event_trace += EVENT_FLAG_START_APP
                    self.logger.info("Trying to start the app...")
                    return IntentEvent(intent=start_app_intent)

        elif current_state.get_app_activity_depth(self.app) > 0:
            # If the app is in activity stack but is not in foreground
            self.__num_steps_outside += 1

            if self.__num_steps_outside > MAX_NUM_STEPS_OUTSIDE:
                # If the app has not been in foreground for too long, try to go back
                if self.__num_steps_outside > MAX_NUM_STEPS_OUTSIDE_KILL:
                    stop_app_intent = self.app.get_stop_intent()
                    go_back_event = IntentEvent(stop_app_intent)
                else:
                    go_back_event = KeyEvent(name="BACK")
                self.__event_trace += EVENT_FLAG_NAVIGATE
                self.logger.info("Going back to the app...")
                return go_back_event
        else:
            # If the app is in foreground
            self.__num_steps_outside = 0

        if not self.reach_target_during_exploration:
        # 如果探索到了target activity，则设置好对应的target state，方便后面直接引导过去
            rules_satisfy_precondition = (
                self.android_check.get_rules_that_pass_the_preconditions()
            )
            if len(rules_satisfy_precondition) > 0:
                self.logger.info("has rule that matches the precondition")
                self.reach_target_during_exploration = True
                self.utg.set_target_state(self.current_state)
            else:
                self.logger.info("no rule matches the precondition")

        # Get all possible input events
        possible_events = current_state.get_possible_input()

        if self.random_input:
            random.shuffle(possible_events)
            
        possible_events.append(KeyEvent(name="BACK"))
        if self.search_method == POLICY_GREEDY_DFS:
            possible_events.append(KeyEvent(name="BACK"))
        elif self.search_method == POLICY_GREEDY_BFS:
            possible_events.insert(0, KeyEvent(name="BACK"))

        # first try to select the actions that lead to activity transition. e.g., open drawer and click item on it.
        for input_event in possible_events:
            if not self.utg.is_event_explored(
                event=input_event, state=current_state
            ) and self.is_event_contains_drawer(input_event):
                self.logger.info("find the drawer event ")
                return input_event

        # If there is an unexplored event, try the event first
        for input_event in possible_events:
            if not self.utg.is_event_explored(event=input_event, state=current_state):
                self.logger.info("Trying an unexplored event.")
                self.__event_trace += EVENT_FLAG_EXPLORE
                return input_event

        target_state = self.__get_nav_target(current_state)
        if target_state:
            navigation_steps = self.utg.get_navigation_steps(
                from_state=current_state, to_state=target_state
            )
            if navigation_steps and len(navigation_steps) > 0:
                self.logger.info(
                    "Navigating to %s, %d steps left."
                    % (target_state.state_str, len(navigation_steps))
                )
                self.__event_trace += EVENT_FLAG_NAVIGATE
                return navigation_steps[0][1]

        if self.__random_explore:
            self.logger.info("Trying random event.")
            random.shuffle(possible_events)
            return possible_events[0]

        # If couldn't find a exploration target, stop the app
        stop_app_intent = self.app.get_stop_intent()
        self.logger.info("Cannot find an exploration target. Trying to restart app...")
        self.__event_trace += EVENT_FLAG_STOP_APP
        return IntentEvent(intent=stop_app_intent)

    def is_event_contains_drawer(self, event) -> bool:
        if hasattr(event, "view"):
            # anki: drawer: description: navigate up
            if safe_get_dict(event.view, "content_description") == "Navigate up":
                return True
        return False

    def __update_utg(self):
        self.utg.add_transition(self.last_event, self.last_state, self.current_state)

    def __get_nav_target(self, current_state):
        # If last event is a navigation event
        if self.__nav_target and self.__event_trace.endswith(EVENT_FLAG_NAVIGATE):
            navigation_steps = self.utg.get_navigation_steps(
                from_state=current_state, to_state=self.__nav_target
            )
            if navigation_steps and 0 < len(navigation_steps) <= self.__nav_num_steps:
                # If last navigation was successful, use current nav target
                self.__nav_num_steps = len(navigation_steps)
                return self.__nav_target
            else:
                # If last navigation was failed, add nav target to missing states
                self.__missed_states.add(self.__nav_target.state_str)

        reachable_states = self.utg.get_reachable_states(current_state)
        if self.random_input:
            random.shuffle(reachable_states)

        for state in reachable_states:
            # Only consider foreground states
            if state.get_app_activity_depth(self.app) != 0:
                continue
            # Do not consider missed states
            if state.state_str in self.__missed_states:
                continue
            # Do not consider explored states
            if self.utg.is_state_explored(state):
                continue
            self.__nav_target = state
            navigation_steps = self.utg.get_navigation_steps(
                from_state=current_state, to_state=self.__nav_target
            )
            if navigation_steps is not None and len(navigation_steps) > 0:
                self.__nav_num_steps = len(navigation_steps)
                return state

        self.__nav_target = None
        self.__nav_num_steps = -1
        return None

    def __get_nav_target_on_the_shortest_path(self, current_state):
        # If last event is a navigation event
        if self.__nav_target and self.__event_trace.endswith(EVENT_FLAG_NAVIGATE):
            navigation_steps = self.utg.get_navigation_steps(
                from_state=current_state, to_state=self.__nav_target
            )
            if navigation_steps and 0 < len(navigation_steps) <= self.__nav_num_steps:
                # If last navigation was successful, use current nav target
                self.__nav_num_steps = len(navigation_steps)
                return self.__nav_target
            else:
                # If last navigation was failed, add nav target to missing states
                self.__missed_states.add(self.__nav_target.state_str)
        # yiheng: get the reachable states on the graph
        reachable_states = self.utg.get_reachable_states(current_state)
        # yiheng: get the states on the shortest path
        shortest_path_states = self.utg.get_states_on_shortest_path()
        if shortest_path_states is not None:
            reachable_states = list(
                set(reachable_states).intersection(set(shortest_path_states))
            )
            # yiheng: remove the states that have been reached on the shortest path
            # in order to push the exploration to the target states
            reachable_states = list(
                set(reachable_states).difference(
                    set(self.reached_state_on_the_shortest_path)
                )
            )
        else:
            self.logger.info("No shortest path states found")
        if self.random_input:
            random.shuffle(reachable_states)

        for state in reachable_states:
            # Only consider foreground states
            if state.get_app_activity_depth(self.app) != 0:
                continue
            # Do not consider missed states
            if state.state_str in self.__missed_states:
                continue
            # Do not consider explored states
            if self.utg.is_state_explored(state):
                continue
            self.__nav_target = state
            navigation_steps = self.utg.get_navigation_steps(
                from_state=current_state, to_state=self.__nav_target
            )
            if navigation_steps is not None and len(navigation_steps) > 0:
                self.__nav_num_steps = len(navigation_steps)
                return state

        self.__nav_target = None
        self.__nav_num_steps = -1
        return None
    def check_the_app_on_foreground(self):
        if self.current_state.get_app_activity_depth(self.app) < 0:
            # If the app is not in the activity stack
            start_app_intent = self.app.get_start_intent()

            # It seems the app stucks at some state, has been
            # 1) force stopped (START, STOP)
            #    just start the app again by increasing self.__num_restarts
            # 2) started at least once and cannot be started (START)
            #    pass to let viewclient deal with this case
            # 3) nothing
            #    a normal start. clear self.__num_restarts.

            if self.__event_trace.endswith(
                EVENT_FLAG_START_APP + EVENT_FLAG_STOP_APP
            ) or self.__event_trace.endswith(EVENT_FLAG_START_APP):
                self.__num_restarts += 1
                self.logger.info(
                    "The app had been restarted %d times.", self.__num_restarts
                )
            else:
                self.__num_restarts = 0

            # pass (START) through
            if not self.__event_trace.endswith(EVENT_FLAG_START_APP):
                if self.__num_restarts > MAX_NUM_RESTARTS:
                    # If the app had been restarted too many times, enter random mode
                    msg = "The app had been restarted too many times. Entering random mode."
                    self.logger.info(msg)
                    self.__random_explore = True
                else:
                    # Start the app
                    self.__event_trace += EVENT_FLAG_START_APP
                    self.logger.info("Trying to start the app...")
                    return IntentEvent(intent=start_app_intent)

        elif self.current_state.get_app_activity_depth(self.app) > 0:
            # If the app is in activity stack but is not in foreground
            self.__num_steps_outside += 1

            if self.__num_steps_outside > MAX_NUM_STEPS_OUTSIDE:
                # If the app has not been in foreground for too long, try to go back
                if self.__num_steps_outside > MAX_NUM_STEPS_OUTSIDE_KILL:
                    stop_app_intent = self.app.get_stop_intent()
                    go_back_event = IntentEvent(stop_app_intent)
                else:
                    go_back_event = KeyEvent(name="BACK")
                self.__event_trace += EVENT_FLAG_NAVIGATE
                self.logger.info("Going back to the app...")
                return go_back_event
        else:
            # If the app is in foreground
            self.__num_steps_outside = 0
    
    def tear_down(self):
        self.logger.info("all paths length: %d", len(self.paths))
        self.logger.info(
            "number of fail paths: %d", len(self.not_reach_precondition_path_number)
        )
        self.logger.info(
            "number of skip paths: %d", len(self.skip_path)
        )
        if self.reach_target_during_exploration:
            self.logger.info("------------ reach the target state during exploration")
        else:
            self.logger.info(
                "------------ not reach the target state during exploration"
            )
        self.logger.info(
            "number of reach precondition paths: %d",
            len(self.reach_precondition_path_number),
        )
        self.logger.info(
            "number of not reach precondition paths: %d",
            len(self.not_reach_precondition_path_number),
        )
        self.logger.info(
            "number of pass rule paths: %d", len(self.pass_rule_path_number)
        )
        self.logger.info(
            "number of fail rule paths: %d", len(self.fail_rule_path_number)
        )
        self.logger.info("----------------------------------------")
        if len(self.time_needed_to_satisfy_precondition)>0:

            self.logger.info("the first time needed to satisfy the precondition: %s" % self.time_needed_to_satisfy_precondition[0])
            self.logger.info("How many times satisfy the precondition: %s" % len(self.time_needed_to_satisfy_precondition))
            self.logger.info("the time needed to satisfy the precondition: %s" % self.time_needed_to_satisfy_precondition)
        else:
            self.logger.info("did not satisfy the precondition")
            return

        if len(self.time_needed_to_trigger_bug) > 0:
            self.logger.info("the first time needed to trigger the bug: %s" % self.time_needed_to_trigger_bug[0])
            self.logger.info("How many times trigger the bug: %s" % len(self.time_needed_to_trigger_bug)) 
            self.logger.info("the time needed to trigger the bug: %s" % self.time_needed_to_trigger_bug)
        else:
            self.logger.info("did not trigger the bug")
            return

class UtgRandomPolicy(UtgBasedInputPolicy):
    """
    random input policy based on UTG
    """

    def __init__(self, device, app, random_input=True, android_check=None, restart_app_after_check_property=False):
        super(UtgRandomPolicy, self).__init__(
            device, app, random_input, android_check
        )
        self.restart_app_after_check_property = restart_app_after_check_property
        self.logger = logging.getLogger(self.__class__.__name__)

        self.preferred_buttons = [
            "yes",
            "ok",
            "activate",
            "detail",
            "more",
            "access",
            "allow",
            "check",
            "agree",
            "try",
            "go",
            "next",
        ]
        self.__num_restarts = 0
        self.__num_steps_outside = 0
        self.__event_trace = ""
        self.__missed_states = set()
        self.number_of_steps_outside_the_shortest_path = 0
        self.reached_state_on_the_shortest_path = []

        self.last_rotate_events = KEY_RotateDeviceNeutralEvent

    def generate_event(self):
        """
        generate an event
        @return:
        """
        # 在app 启动后执行定义好的初始化事件
        if self.action_count == 2:
            self.run_initial_rules()
    
        # Get current device state
        self.current_state = self.device.get_current_state(self.action_count)
        if self.current_state is None:
            import time
            time.sleep(5)
            return KeyEvent(name="BACK")

        self.__update_utg()
    
        rules_to_check = self.android_check.get_rules_that_pass_the_preconditions()
        
        if len(rules_to_check) > 0:
            self.time_needed_to_satisfy_precondition.append(self.time_recoder.get_time_duration())
            self.logger.info("has rule that matches the precondition and the time duration is "+ self.time_recoder.get_time_duration())
            # 以50%的概率选择是否check rule
            if random.random() < 0.5:   
                self.logger.info(" check rule")
                self.check_rule_with_precondition()
                if self.restart_app_after_check_property:
                    self.logger.info("restart app after check property")
                    return KillAppEvent(app=self.app)
                return None
            else:
                self.logger.info("don't check rule")
        event = None

        if event is None:
            event = self.generate_event_based_on_utg()
        # 旋转屏幕事件。如果之前执行过旋转屏幕事件，那么下一次执行的旋转屏幕事件应该是相反的
        if isinstance(event, RotateDevice):
            if self.last_rotate_events == KEY_RotateDeviceNeutralEvent:
                self.last_rotate_events = KEY_RotateDeviceRightEvent
                event = RotateDeviceRightEvent()
            else:
                self.last_rotate_events = KEY_RotateDeviceNeutralEvent
                event = RotateDeviceNeutralEvent()

        self.last_state = self.current_state
        self.last_event = event
        return event


    def generate_event_based_on_utg(self):
        """
        generate an event based on current UTG
        @return: InputEvent
        """
        current_state = self.current_state
        self.logger.info("Current state: %s" % current_state.state_str)
        if current_state.state_str in self.__missed_states:
            self.__missed_states.remove(current_state.state_str)

        if current_state.get_app_activity_depth(self.app) < 0:
            # If the app is not in the activity stack
            start_app_intent = self.app.get_start_intent()

            # It seems the app stucks at some state, has been
            # 1) force stopped (START, STOP)
            #    just start the app again by increasing self.__num_restarts
            # 2) started at least once and cannot be started (START)
            #    pass to let viewclient deal with this case
            # 3) nothing
            #    a normal start. clear self.__num_restarts.

            if self.__event_trace.endswith(
                EVENT_FLAG_START_APP + EVENT_FLAG_STOP_APP
            ) or self.__event_trace.endswith(EVENT_FLAG_START_APP):
                self.__num_restarts += 1
                self.logger.info(
                    "The app had been restarted %d times.", self.__num_restarts
                )
            else:
                self.__num_restarts = 0

            # pass (START) through
            if not self.__event_trace.endswith(EVENT_FLAG_START_APP):
                if self.__num_restarts > MAX_NUM_RESTARTS:
                    # If the app had been restarted too many times, enter random mode
                    msg = "The app had been restarted too many times. Entering random mode."
                    self.logger.info(msg)
                    self.__random_explore = True
                else:
                    # Start the app
                    self.__event_trace += EVENT_FLAG_START_APP
                    self.logger.info("Trying to start the app...")
                    return IntentEvent(intent=start_app_intent)

        elif current_state.get_app_activity_depth(self.app) > 0:
            # If the app is in activity stack but is not in foreground
            self.__num_steps_outside += 1

            if self.__num_steps_outside > MAX_NUM_STEPS_OUTSIDE:
                # If the app has not been in foreground for too long, try to go back
                if self.__num_steps_outside > MAX_NUM_STEPS_OUTSIDE_KILL:
                    stop_app_intent = self.app.get_stop_intent()
                    go_back_event = IntentEvent(stop_app_intent)
                else:
                    go_back_event = KeyEvent(name="BACK")
                self.__event_trace += EVENT_FLAG_NAVIGATE
                self.logger.info("Going back to the app...")
                return go_back_event
        else:
            # If the app is in foreground
            self.__num_steps_outside = 0

        # if self.guide:
        #     event = self.guide_the_exploration()
        #     if event is not None:
        #         return event
        # if self.guide:
        #     if self.device.get_activity_short_name() == self.guide.target_activity:
        #         raise InputInterruptedException("Target state reached.")
        # Get all possible input events
        possible_events = current_state.get_possible_input()

        if self.random_input:
            random.shuffle(possible_events)
        possible_events.append(KeyEvent(name="BACK"))
        possible_events.append(RotateDevice())

        self.__event_trace += EVENT_FLAG_EXPLORE
        return random.choice(possible_events)
    
    def __update_utg(self):
        self.utg.add_transition(self.last_event, self.last_state, self.current_state)

    def tear_down(self):
        """
        输出一些统计信息
        """
        self.logger.info("----------------------------------------")
        if len(self.time_needed_to_satisfy_precondition)>0:

            self.logger.info("the first time needed to satisfy the precondition: %s" % self.time_needed_to_satisfy_precondition[0])
            self.logger.info("How many times satisfy the precondition: %s" % len(self.time_needed_to_satisfy_precondition))
            self.logger.info("the time needed to satisfy the precondition: %s" % self.time_needed_to_satisfy_precondition)
        else:
            self.logger.info("did not satisfy the precondition")
            return

        if len(self.time_needed_to_trigger_bug) > 0:
            self.logger.info("the first time needed to trigger the bug: %s" % self.time_needed_to_trigger_bug[0])
            self.logger.info("How many times trigger the bug: %s" % len(self.time_needed_to_trigger_bug)) 
            self.logger.info("the time needed to trigger the bug: %s" % self.time_needed_to_trigger_bug)
        else:
            self.logger.info("did not trigger the bug")
            return

class UtgNaiveSearchPolicy(UtgBasedInputPolicy):
    """
    depth-first strategy to explore UFG (old)
    """

    def __init__(self, device, app, random_input, search_method):
        super(UtgNaiveSearchPolicy, self).__init__(device, app, random_input)
        self.logger = logging.getLogger(self.__class__.__name__)

        self.explored_views = set()
        self.state_transitions = set()
        self.search_method = search_method

        self.last_event_flag = ""
        self.last_event_str = None
        self.last_state = None

        self.preferred_buttons = [
            "yes",
            "ok",
            "activate",
            "detail",
            "more",
            "access",
            "allow",
            "check",
            "agree",
            "try",
            "go",
            "next",
        ]

    def generate_event_based_on_utg(self):
        """
        generate an event based on current device state
        note: ensure these fields are properly maintained in each transaction:
          last_event_flag, last_touched_view, last_state, exploited_views, state_transitions
        @return: InputEvent
        """
        self.save_state_transition(
            self.last_event_str, self.last_state, self.current_state
        )

        if self.device.is_foreground(self.app):
            # the app is in foreground, clear last_event_flag
            self.last_event_flag = EVENT_FLAG_STARTED
        else:
            number_of_starts = self.last_event_flag.count(EVENT_FLAG_START_APP)
            # If we have tried too many times but the app is still not started, stop DroidBot
            if number_of_starts > MAX_NUM_RESTARTS:
                raise InputInterruptedException("The app cannot be started.")

            # if app is not started, try start it
            if self.last_event_flag.endswith(EVENT_FLAG_START_APP):
                # It seems the app stuck at some state, and cannot be started
                # just pass to let viewclient deal with this case
                self.logger.info(
                    "The app had been restarted %d times.", number_of_starts
                )
                self.logger.info("Trying to restart app...")
                pass
            else:
                start_app_intent = self.app.get_start_intent()

                self.last_event_flag += EVENT_FLAG_START_APP
                self.last_event_str = EVENT_FLAG_START_APP
                return IntentEvent(start_app_intent)

        # select a view to click
        view_to_touch = self.select_a_view(self.current_state)

        # if no view can be selected, restart the app
        if view_to_touch is None:
            stop_app_intent = self.app.get_stop_intent()
            self.last_event_flag += EVENT_FLAG_STOP_APP
            self.last_event_str = EVENT_FLAG_STOP_APP
            return IntentEvent(stop_app_intent)

        view_to_touch_str = view_to_touch['view_str']
        if view_to_touch_str.startswith('BACK'):
            result = KeyEvent('BACK')
        else:
            result = TouchEvent(view=view_to_touch)

        self.last_event_flag += EVENT_FLAG_TOUCH
        self.last_event_str = view_to_touch_str
        self.save_explored_view(self.current_state, self.last_event_str)
        return result

    def select_a_view(self, state):
        """
        select a view in the view list of given state, let droidbot touch it
        @param state: DeviceState
        @return:
        """
        views = []
        for view in state.views:
            if view['enabled'] and len(view['children']) == 0:
                views.append(view)

        if self.random_input:
            random.shuffle(views)

        # add a "BACK" view, consider go back first/last according to search policy
        mock_view_back = {
            'view_str': 'BACK_%s' % state.foreground_activity,
            'text': 'BACK_%s' % state.foreground_activity,
        }
        if self.search_method == POLICY_NAIVE_DFS:
            views.append(mock_view_back)
        elif self.search_method == POLICY_NAIVE_BFS:
            views.insert(0, mock_view_back)

        # first try to find a preferable view
        for view in views:
            view_text = view['text'] if view['text'] is not None else ''
            view_text = view_text.lower().strip()
            if (
                view_text in self.preferred_buttons
                and (state.foreground_activity, view['view_str'])
                not in self.explored_views
            ):
                self.logger.info("selected an preferred view: %s" % view['view_str'])
                return view

        # try to find a un-clicked view
        for view in views:
            if (state.foreground_activity, view['view_str']) not in self.explored_views:
                self.logger.info("selected an un-clicked view: %s" % view['view_str'])
                return view

        # if all enabled views have been clicked, try jump to another activity by clicking one of state transitions
        if self.random_input:
            random.shuffle(views)
        transition_views = {transition[0] for transition in self.state_transitions}
        for view in views:
            if view['view_str'] in transition_views:
                self.logger.info("selected a transition view: %s" % view['view_str'])
                return view

        # no window transition found, just return a random view
        # view = views[0]
        # self.logger.info("selected a random view: %s" % view['view_str'])
        # return view

        # DroidBot stuck on current state, return None
        self.logger.info("no view could be selected in state: %s" % state.tag)
        return None

    def save_state_transition(self, event_str, old_state, new_state):
        """
        save the state transition
        @param event_str: str, representing the event cause the transition
        @param old_state: DeviceState
        @param new_state: DeviceState
        @return:
        """
        if event_str is None or old_state is None or new_state is None:
            return
        if new_state.is_different_from(old_state):
            self.state_transitions.add((event_str, old_state.tag, new_state.tag))

    def save_explored_view(self, state, view_str):
        """
        save the explored view
        @param state: DeviceState, where the view located
        @param view_str: str, representing a view
        @return:
        """
        if not state:
            return
        state_activity = state.foreground_activity
        self.explored_views.add((state_activity, view_str))
