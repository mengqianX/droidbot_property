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
        main_path_path=None,
        xml_path="None",
        source_activity=None,
        target_activity=None,
        policy_name="pbt",
        timeout=-1,
        build_model_timeout=-1
    ):
        super().__init__(
            apk_path,
            device_serial=device_serial,
            output_dir=output_dir,
            xml_path=xml_path,
            main_path_path=main_path_path,
            source_activity=source_activity,
            target_activity=target_activity,
            policy_name=policy_name,
            timeout=timeout,
            build_model_timeout=build_model_timeout
        )

    @initialize()
    def set_up(self):
        self.device(resourceId="net.gsantner.markor:id/next").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/next").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/next").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/next").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/next").click()
        time.sleep(1)
        self.device(text="DONE").click()
        time.sleep(1)
        
        if self.device(text="OK").exists():
            self.device(text="OK").click()
        time.sleep(1)
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
        
    
    @precondition(
        lambda self: self.device(resourceId="net.gsantner.markor:id/action_preview").exists() and not self.device(text="Save").exists()
        )
    @rule()
    def change_view_mode_should_not_change_position(self):
        content = self.device(className="android.widget.EditText").get_text()
        print("content: " + str(content))
        added_content = st.text(alphabet=string.ascii_lowercase,min_size=1, max_size=6).example()
        print("added_content: " + str(added_content))
        self.device(className="android.widget.EditText").set_text(content + " "+ str(added_content))
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/action_preview").click()
        time.sleep(1)
        for i in range(int(self.device(className="android.webkit.WebView").child(className="android.view.View").count)):
            print(self.device(className="android.webkit.WebView").child(className="android.view.View")[i].info["contentDescription"])
            if content in str(self.device(className="android.webkit.WebView").child(className="android.view.View")[i].info["contentDescription"]):
                return True
        assert False, "content not found in preview"

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
    apk_path="./apk/markor/2.4.0.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/1149/1",
    policy_name="random",
    timeout=7200
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
