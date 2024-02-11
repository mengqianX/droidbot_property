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
        self.device(resourceId="it.feio.android.omninotes:id/next").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/next").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/next").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/next").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/next").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/done").click()
        time.sleep(1)
        # 打开设置-在navigation 中显示没有被分类的Notes
        # self.device(description="drawer open").click()
        # time.sleep(1)
        # self.device(text="Settings").click()
        # time.sleep(1)
        # self.device(text="Navigation").click()
        # time.sleep(1)
        # self.device(text="Group not categorized").click()
        # time.sleep(1)
        # self.device(description="Navigate up").click()
        # time.sleep(1)
        # self.device(description="Navigate up").click()
        # time.sleep(1)
        # self.device.press("back")
        # time.sleep(1)
        # # 创建一个新的Note
        # self.device(resourceId="it.feio.android.omninotes:id/fab_expand_menu_button").click()
        # time.sleep(1)
        # self.device(text="Text note").click()
        # time.sleep(1)
        # self.device(resourceId="it.feio.android.omninotes:id/detail_title").set_text("test")
        # time.sleep(1)
        # self.device(resourceId="it.feio.android.omninotes:id/detail_content").set_text("#bb")
        # time.sleep(1)
        # # 添加新的category
        # self.device(resourceId="it.feio.android.omninotes:id/menu_category").click()
        # time.sleep(1)
        # self.device(resourceId="it.feio.android.omninotes:id/md_buttonDefaultPositive").click()
        # time.sleep(1)
        # category_name = st.text(alphabet=string.printable,min_size=1, max_size=10).example()
        # self.device(resourceId="it.feio.android.omninotes:id/category_title").set_text(category_name)
        # time.sleep(1)
        # self.device(text="OK").click()
        # self.device(description="drawer closed").click()
    
    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/note_title").exists() and self.device(text="Notes").exists() and not self.device(text="Settings").exists())
    @rule()
    def rule_trash_note_cannot_be_searched(self):
        print("time: " + str(time.time() - start_time))
        if not self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").exists():
            return
        note_count = int(self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").count)
        selected_note = random.randint(0, note_count - 1)
        selected_note_name = self.device(resourceId="it.feio.android.omninotes:id/note_title")[selected_note].info['text']
        print("selected_note: " + str(selected_note))
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root")[selected_note].long_click()
        time.sleep(1)
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Trash").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/toolbar").child(className="android.widget.ImageButton").click()
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        # 再去search 列表中查找
        self.device(resourceId="it.feio.android.omninotes:id/menu_search").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/search_src_text").set_text(selected_note_name)
        time.sleep(1)
        self.device.send_action("search")
        time.sleep(1)
        assert not self.device(text=selected_note_name,resourceId="it.feio.android.omninotes:id/note_title").exists()
        # 点击checklist 看能否找到
        self.device(resourceId="it.feio.android.omninotes:id/menu_uncomplete_checklists").click()
        time.sleep(1)
        assert not self.device(text=selected_note_name,resourceId="it.feio.android.omninotes:id/note_title").exists()
   
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
    apk_path="./apk/omninotes/OmniNotes-6.1.0.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/886/random_100/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
