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
        lambda self: int(self.device(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count) > 0 and not self.device(resourceId="nl.mpcjanssen.simpletask:id/filter_text").exists() and not self.device(text="Quick filter").exists() and not self.device(text="Settings").exists() and not self.device(text="Saved filters").exists()
    )
    @rule()
    def task_prefilled_when_filtered(self):
        self.device(resourceId="nl.mpcjanssen.simpletask:id/filter").click()
        time.sleep(1)
        # 随机选择tag or list
        if random.randint(0, 1) == 0:
            self.device(text="LIST").click()
        else:
            self.device(text="TAG").click()
        time.sleep(1)
        # 随机选择是否点击invert filter
        invert_filter = random.randint(0, 1) == 0
        if invert_filter:
            self.device(resourceId="nl.mpcjanssen.simpletask:id/checkbox").click()
        filter_count = int(self.device(resourceId="android:id/text1").count)
        print("filter count: "+str(filter_count))
        selected_filter_index = random.randint(0, filter_count - 1)
        selected_filer_name = self.device(resourceId="android:id/text1")[selected_filter_index].get_text()
        print("selected filter: "+str(selected_filer_name))
        self.device(resourceId="android:id/text1")[selected_filter_index].click()
        time.sleep(1)
        self.device(resourceId="nl.mpcjanssen.simpletask:id/menu_filter_action").click()
        time.sleep(1)
        assert self.device(resourceId="nl.mpcjanssen.simpletask:id/filter_text").exists(), "filter text should exist"
        time.sleep(1)
        self.device(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        time.sleep(1)
        if selected_filer_name == "-":
            assert self.device(resourceId="nl.mpcjanssen.simpletask:id/taskText").get_text() == "", "task text should be empty"
        else:
            content = self.device(resourceId="nl.mpcjanssen.simpletask:id/taskText").get_text()
            print("content: "+str(content))
            if invert_filter:
                assert selected_filer_name not in content, "selected_filer_name should not be in content"
            else:
                assert selected_filer_name in content, "selected_filer_name should be in content"
        
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
    apk_path="./apk/simpletask/9.0.2.apk",
    device_serial="emulator-5554",
    output_dir="output/simpletask/753/random_100/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
