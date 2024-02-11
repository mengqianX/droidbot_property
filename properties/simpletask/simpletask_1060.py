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
        if self.device(text="OK").exists():
            self.device(text="OK").click()
        # time.sleep(1)
        # self.device(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        # content = st.text(alphabet=string.ascii_letters,min_size=1, max_size=10).example()
        # self.device(resourceId="nl.mpcjanssen.simpletask:id/taskText").set_text(content)
        # time.sleep(1)
        # self.device(resourceId="nl.mpcjanssen.simpletask:id/btnProject").click()
        # time.sleep(1)
        # tag_name = st.text(alphabet=string.ascii_letters,min_size=1, max_size=6).example()
        # print("tag name: "+str(tag_name))
        # self.device(resourceId="nl.mpcjanssen.simpletask:id/new_item_text").set_text(tag_name)
        # time.sleep(1)
        # self.device(text="OK").click()
        # time.sleep(1)
        # self.device(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()

    @precondition(
        lambda self: self.device(text="Quick filter").exists() and self.device(text="CLEAR FILTER").exists() and self.device(resourceId="android:id/text1",className="android.widget.CheckedTextView").exists()
    )
    @rule()
    def filter_by_tag(self):
        self.device(text="CLEAR FILTER").click()
        time.sleep(1)
        check_box_count = int(self.device(resourceId="android:id/text1",className="android.widget.CheckedTextView").count)
        print("check box count: "+str(check_box_count))
        selected_check_box = random.randint(0, check_box_count - 1)
        print("selected check box: "+str(selected_check_box))
        selected_check_box = self.device(resourceId="android:id/text1",className="android.widget.CheckedTextView")[selected_check_box]
        selected_check_box_name = selected_check_box.get_text()
        print("selected check box name: "+str(selected_check_box_name))
        if selected_check_box_name == "-":
            print("not select list or tag, return")
            return
        selected_check_box.click()
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        filter_text = self.device(resourceId="nl.mpcjanssen.simpletask:id/filter_text").get_text()
        print("filter text: "+str(filter_text))
        number = filter_text.split("/")[1][0]
        if number == "0":
            print("no task, return")
            return
        
        assert self.device(resourceId="nl.mpcjanssen.simpletask:id/tasktext").exists(), "no task"
        time.sleep(1)
        self.device(resourceId="nl.mpcjanssen.simpletask:id/tasktext").click()
        time.sleep(1)
        self.device(resourceId="nl.mpcjanssen.simpletask:id/update").click()
        time.sleep(1)
        content = self.device(resourceId="nl.mpcjanssen.simpletask:id/taskText").get_text()
        print("content: "+str(content))
        assert selected_check_box_name in content, "content doesn't have selected items"
    

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
    apk_path="./apk/simpletask/10.5.2.apk",
    device_serial="emulator-5554",
    output_dir="output/simpletask/1060/random_100/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
