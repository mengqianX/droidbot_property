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
        explore_event_count=9999999,
        diverse_event_count=9999999,
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
            explore_event_count=explore_event_count,
            diverse_event_count=diverse_event_count,
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
        
    
    # bug #1569
    @precondition(lambda self: self.device(resourceId="net.gsantner.markor:id/toolbar").child(text="QuickNote").exists() and self.device(description="More options").exists())
    @rule()
    def share_file_to_quicknote_shouldnot_influence_original_content(self):
        original_content = self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").get_text()
        print("original content: " + original_content)
        self.device(text="Files").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/fab_add_new_item").click()
        time.sleep(1)
        title = st.text(alphabet=string.ascii_lowercase,min_size=1, max_size=6).example()
        print("title: " + title)
        self.device(resourceId="net.gsantner.markor:id/new_file_dialog__name").set_text(title)
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        shared_content = st.text(alphabet=string.printable,min_size=1, max_size=10).example()
        print("shared content: " + shared_content)
        self.device(className="android.widget.EditText").set_text(shared_content)
        time.sleep(1)
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Share").click()
        time.sleep(1)
        self.device(text="Plain Text").click()
        time.sleep(1)
        self.device(text="Markor").click()
        time.sleep(1)
        self.device(text="QuickNote").click()
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device(text="QuickNote").click()
        time.sleep(1)
        new_content = self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").get_text()
        print("new content: " + new_content)
        assert original_content in new_content, "original content should be in new content"
        assert shared_content in new_content, "shared content should be in new content"

start_time = time.time()

t = Test(
    apk_path="./apk/markor/2.8.5.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/1961/1",
    policy_name="random",
    timeout=7200
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
