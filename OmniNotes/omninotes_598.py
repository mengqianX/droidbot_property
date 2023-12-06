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
        explore_event_count=0,
        diverse_event_count=100,
        main_path_path=None,
        xml_path="None",
        source_activity=None,
        target_activity=None,
        policy_name="pbt",
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
        )

    @initialize()
    def set_up(self):
        self.device.set_fastinput_ime(True)
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
        if self.device(text="OK").exists():
            self.device(text="OK").click()
            time.sleep(1)
        # 打开设置-在navigation 中显示没有被分类的Notes
        self.device(description="drawer open").click()
        time.sleep(1)
        self.device(text="SETTINGS").click()
        time.sleep(1)
        self.device(text="Navigation").click()
        time.sleep(1)
        self.device(text="Group not categorized").click()
        time.sleep(1)
        self.device(description="Navigate up").click()
        time.sleep(1)
        self.device(description="Navigate up").click()
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        # 创建一个新的Note
        self.device(resourceId="it.feio.android.omninotes:id/fab_expand_menu_button").click()
        time.sleep(1)
        self.device(text="Text note").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/detail_title").set_text("test")
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/detail_content").set_text("#bb")
        time.sleep(1)
        # 添加新的category
        self.device(resourceId="it.feio.android.omninotes:id/menu_category").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/buttonDefaultPositive").click()
        time.sleep(1)
        category_name = st.text(alphabet=string.printable,min_size=1, max_size=10).example()
        self.device(resourceId="it.feio.android.omninotes:id/category_title").set_text(category_name)
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        # lock note
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Lock").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/password").set_text("1")
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/password_check").set_text("1")
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/question").set_text("1")
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/answer").set_text("1")
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/answer_check").set_text("1")
        time.sleep(1)
        self.device(scrollable=True).fling()
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(2)
        self.device.press("back")
        
    
    @precondition(lambda self: self.device(text="Data").exists() and self.device(text="Password").exists())
    @rule()
    def remove_password_in_setting_should_effect(self):
        print("time: " + str(time.time() - start_time))
        self.device(text="Password").click()
        time.sleep(1)
        self.device(text="REMOVE PASSWORD").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/password_request").set_text("1")
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        # open note
        if not self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").exists():
            print("no note")
            return
        note_count = int(self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").count)
        selected_note = random.randint(0, note_count - 1)
        print("selected_note: " + str(selected_note))
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root")[selected_note].click()
        time.sleep(1)
        assert not self.device(text="PASSWORD FORGOTTEN").exists()
    
    precondition(lambda self: self.device(description="More options").exists() and self.device(resourceId="it.feio.android.omninotes:id/menu_attachment").exists())
    @rule()
    def action_lock_a_note(self):
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Lock").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/password").set_text("1")
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/password_check").set_text("1")
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/question").set_text("1")
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/answer").set_text("1")
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/answer_check").set_text("1")
        time.sleep(1)
        self.device(scrollable=True).fling()
        time.sleep(1)
        self.device(text="OK").click()
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
    apk_path="./apk/OmniNotes-5.5.3.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/598/1",
    explore_event_count=500,
    diverse_event_count=500,
    policy_name="random",
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
