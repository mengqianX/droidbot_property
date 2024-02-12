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
        self.device(description="Navigate up").click()
        time.sleep(1)
        self.device(scrollable=True).scroll(steps=10)
        time.sleep(1)
        self.device(text="Settings").click()
        time.sleep(1)
        self.device(scrollable=True).scroll.to(text="Back navigation")
        time.sleep(2)
        self.device(text="Back navigation").right(className="android.widget.Switch").click()
        time.sleep(1)
        self.device.press("back")


    @precondition(lambda self: self.device(text="Go Back").exists() and self.device(resourceId="com.amaze.filemanager:id/second").exists())
    @rule()
    def rule_go_back(self):
        print("time: " + str(time.time() - start_time))
        original_path = self.device(resourceId="com.amaze.filemanager:id/fullpath").get_text()
        print("original path: "+str(original_path))
        time.sleep(1)
        self.device(text="Go Back",resourceId="com.amaze.filemanager:id/secondLine").click()
        time.sleep(1)
        after_path = self.device(resourceId="com.amaze.filemanager:id/fullpath").get_text()
        print("after path: "+str(after_path))
        expected_path = '/'.join(original_path.split("/")[:-1])
        print("expected path: "+str(expected_path))
        assert after_path == expected_path

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
    apk_path="./apk/amaze-3.3.0RC10.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/1499/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
