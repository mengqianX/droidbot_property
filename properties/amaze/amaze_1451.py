import string
import sys
import time
sys.path.append("..")
from main import *

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
        if self.device(text="ALLOW").exists():
            self.device(text="ALLOW").click()
            time.sleep(1)
            
    @precondition(lambda self: self.device(text="Recent files").exists() and self.device(text="Images").exists())
    @rule()
    def rule_open_recent_files(self):
        print("time: " + str(time.time() - start_time))
        self.device(text="Recent files").click()
        time.sleep(1)
        number_of_files = self.device(resourceId="com.amaze.filemanager:id/second").count
        print("number of files: "+str(number_of_files))
        self.device(description="Navigate up").click()
        time.sleep(1)
        self.device(text="Recent files").click()
        time.sleep(1)
        new_number_of_files = self.device(resourceId="com.amaze.filemanager:id/second").count
        print("new number of files: "+str(new_number_of_files))
        assert number_of_files == new_number_of_files

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
    apk_path="./apk/amaze/amaze-3.3.0RC6.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/1451/random_100/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
