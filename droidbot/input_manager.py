import json
import logging
import subprocess
import time

from .input_event import EventLog
from .input_policy import (
    POLICY_MIX_RANDOM_MUTATE,
    POLICY_MUTATE_MAIN_PATH,
    POLICY_RANDOM_TWO,
    POLICY_RANDOM_100,
    Mix_random_and_mutate_policy,
    Mutate_Main_Path_Policy,
    MutatePolicy,
    POLICY_MUTATE,
    POLICY_BUILD_MODEL,
    POLICY_RANDOM,
    UtgBasedInputPolicy,
    UtgNaiveSearchPolicy,
    BuildModelPolicy,
    UtgRandomPolicy,
    POLICY_NAIVE_DFS,
    POLICY_GREEDY_DFS,
    POLICY_NAIVE_BFS,
    POLICY_GREEDY_BFS,
    POLICY_REPLAY,
    POLICY_MEMORY_GUIDED,
    POLICY_MANUAL,
    POLICY_MONKEY,
    POLICY_NONE,
)

DEFAULT_POLICY = POLICY_GREEDY_DFS
RANDOM_POLICY = POLICY_RANDOM
DEFAULT_EVENT_INTERVAL = 1
DEFAULT_EVENT_COUNT = 100000000
DEFAULT_TIMEOUT = -1


class UnknownInputException(Exception):
    pass


class InputManager(object):
    """
    This class manages all events to send during app running
    """

    def __init__(
        self,
        device,
        app,
        policy_name,
        random_input,
        event_interval,
        event_count=DEFAULT_EVENT_COUNT,  # the number of event generated in the explore phase.
        script_path=None,
        profiling_method=None,
        master=None,
        replay_output=None,
        android_check=None,
        guide=None,
        main_path_path=None,
        build_model_timeout=-1,
        number_of_events_that_restart_app=100,
    ):
        """
        manage input event sent to the target device
        :param device: instance of Device
        :param app: instance of App
        :param policy_name: policy of generating events, string
        :return:
        """
        self.logger = logging.getLogger('InputEventManager')
        self.enabled = True

        self.device = device
        self.app = app
        self.policy_name = policy_name
        self.random_input = random_input
        self.events = []
        self.policy = None
        self.script = None
        self.event_count = event_count
        self.event_interval = event_interval
        self.replay_output = replay_output

        self.monkey = None

        if script_path is not None:
            f = open(script_path, 'r')
            script_dict = json.load(f)
            from .input_script import DroidBotScript

            self.script = DroidBotScript(script_dict)

        self.android_check = android_check
        self.guide = guide
        self.main_path_path = main_path_path
        
        self.profiling_method = profiling_method
        self.build_model_timeout = build_model_timeout
        self.number_of_events_that_restart_app = number_of_events_that_restart_app
        self.policy = self.get_input_policy(device, app, master)

    def get_input_policy(self, device, app, master):
        if self.policy_name == POLICY_NONE:
            input_policy = None
        elif self.policy_name == POLICY_MONKEY:
            input_policy = None
        elif self.policy_name in [POLICY_NAIVE_DFS, POLICY_NAIVE_BFS]:
            input_policy = UtgNaiveSearchPolicy(
                device, app, self.random_input, self.policy_name
            )
        elif self.policy_name == POLICY_BUILD_MODEL:
            input_policy = BuildModelPolicy(
                device,
                app,
                self.random_input,
                self.policy_name,
                self.android_check,
                self.guide,
                self.build_model_timeout
            )
        elif self.policy_name == POLICY_MUTATE:
            input_policy = MutatePolicy(
                device,
                app,
                self.random_input,
                self.android_check,
                self.guide,
                main_path_path=self.main_path_path
            )
        elif self.policy_name == POLICY_RANDOM:
            input_policy = UtgRandomPolicy(device, app, random_input=self.random_input,android_check=self.android_check,number_of_events_that_restart_app = self.number_of_events_that_restart_app, clear_and_restart_app_data_after_100_events=True)
        elif self.policy_name == POLICY_RANDOM_TWO:
            input_policy = UtgRandomPolicy(device, app, random_input=self.random_input,android_check=self.android_check, restart_app_after_check_property=True)
        elif self.policy_name == POLICY_RANDOM_100:
            input_policy = UtgRandomPolicy(device, app, random_input=self.random_input,android_check=self.android_check, clear_and_restart_app_data_after_100_events=True)
        elif self.policy_name == POLICY_MUTATE_MAIN_PATH:
            input_policy = Mutate_Main_Path_Policy(device,app,random_input=self.random_input,android_check=self.android_check,restart_app_after_100_events=True)
        elif self.policy_name == POLICY_MIX_RANDOM_MUTATE:
            input_policy = Mix_random_and_mutate_policy(device,app,random_input=self.random_input,android_check=self.android_check,restart_app_after_100_events=True)
        elif self.policy_name == POLICY_MEMORY_GUIDED:
            from .input_policy2 import MemoryGuidedPolicy

            input_policy = MemoryGuidedPolicy(device, app, self.random_input)
        # elif self.policy_name == POLICY_REPLAY:
        #     input_policy = UtgReplayPolicy(device, app, self.replay_output)
        # elif self.policy_name == POLICY_MANUAL:
        #     input_policy = ManualPolicy(device, app)
        elif self.policy_name == POLICY_RANDOM:
            input_policy = UtgRandomPolicy(device, app, guide=self.guide)
        else:
            self.logger.warning(
                "No valid input policy specified. Using policy \"none\"."
            )
            input_policy = None
        if isinstance(input_policy, UtgBasedInputPolicy):
            input_policy.script = self.script
            input_policy.master = master
        return input_policy

    def add_event(self, event):
        """
        add one event to the event list
        :param event: the event to be added, should be subclass of AppEvent
        :return:
        """
        if event is None:
            return
        self.events.append(event)

        event_log = EventLog(self.device, self.app, event, self.profiling_method)
        event_log.start()
        while True:
            time.sleep(self.event_interval)
            if not self.device.pause_sending_event:
                break
        event_log.stop()

    def start(self):
        """
        start sending event
        """
        self.logger.info("start sending events, policy is %s" % self.policy_name)

        try:
            if self.policy is not None:
                self.policy.start(self)

        except KeyboardInterrupt:
            pass

        self.stop()
        self.logger.info("Finish sending events")

    def stop(self):
        """
        stop sending event
        """
        if self.monkey:
            if self.monkey.returncode is None:
                self.monkey.terminate()
            self.monkey = None
            pid = self.device.get_app_pid("com.android.commands.monkey")
            if pid is not None:
                self.device.adb.shell("kill -9 %d" % pid)
        self.enabled = False
