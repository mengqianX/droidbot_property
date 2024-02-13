import string
from main import *
import time
import sys
import re

class Test(AndroidCheck):
    def __init__(
        self,
        apk_path,
        device_serial="emulator-5554",
        output_dir="output",
        policy_name="pbt",
        timeout=-1,
        build_model_timeout=-1,
        number_of_events_that_restart_app=100,
    ):
        super().__init__(
            apk_path,
            device_serial=device_serial,
            output_dir=output_dir,
            policy_name=policy_name,
            timeout=timeout,
            build_model_timeout=build_model_timeout,
            number_of_events_that_restart_app=number_of_events_that_restart_app,
        )

    @initialize()
    def set_up(self):
        # self.device(resourceId="net.gsantner.markor:id/next").click()
        # time.sleep(1)
        # self.device(resourceId="net.gsantner.markor:id/next").click()
        # time.sleep(1)
        # self.device(resourceId="net.gsantner.markor:id/next").click()
        # time.sleep(1)
        # self.device(resourceId="net.gsantner.markor:id/next").click()
        # time.sleep(1)
        # self.device(text="DONE").click()
        # time.sleep(1)
        
        if self.device(text="OK").exists():
            self.device(text="OK").click()
        # time.sleep(1)
        # self.device(resourceId="net.gsantner.markor:id/action_sort").click()
        # time.sleep(1)
        # self.device(text="Date").click()
        # time.sleep(1)
        # self.device(resourceId="net.gsantner.markor:id/action_sort").click()
        # time.sleep(1)
        # self.device(text="Reverse order").click()
        # time.sleep(1)
        # self.device(resourceId="net.gsantner.markor:id/action_sort").click()
        # time.sleep(1)
        # self.device(text="Folder first").click()
        
    
    # bug #457
    @precondition(lambda self: self.device(resourceId="net.gsantner.markor:id/nav_notebook").exists() and self.device(resourceId="net.gsantner.markor:id/nav_notebook").info["selected"])
    @rule()
    def swipe_should_update_title(self):
        self.device.swipe_ext("left")
        assert self.device(resourceId="net.gsantner.markor:id/nav_todo").info["selected"] and self.device(resourceId="net.gsantner.markor:id/toolbar").child(text="Todo").exists()

start_time = time.time()

# args = sys.argv[1:]
# apk_path = args[0]
# device_serial = args[1]
# output_dir = args[2]
# xml_path = args[3]
# main_path_path = args[4]
# source_activity = args[5]
# target_activity = args[6]
# policy_name = args[7]
# t = Test(
#     apk_path="./apk/AnkiDroid-2.15.2.apk",
#     device_serial="emulator-5554",
#     output_dir="output/anki/random2",
#     event_count=1000,
#     xml_path="./xml_graph/Anki_CTG.xml",
#     source_activity="DeckPicker",
#     target_activity="Preferences",
#     policy_name="random", dfs_greedy
# )
t = Test(
    apk_path="./apk/markor/1.5.1.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/457/random_10/1",
    policy_name="21600",
    number_of_events_that_restart_app = 10
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
