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
        self.device(description="drawer open").click()
        time.sleep(1)
        self.device(text="Settings").click()
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
        self.device(text="ADD CATEGORY").click()
        time.sleep(1)
        category_name = st.text(alphabet=string.printable,min_size=1, max_size=10).example()
        self.device(resourceId="it.feio.android.omninotes:id/category_title").set_text(category_name)
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        self.device.press("back")
    
    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/menu_attachment").exists() and self.device(resourceId="it.feio.android.omninotes:id/menu_share").exists() and self.device(resourceId="it.feio.android.omninotes:id/menu_tag").exists() )
    @rule()
    def count_char_in_note(self):
        print("time: " + str(time.time() - start_time))
        # title = st.text(alphabet=string.ascii_letters,min_size=0, max_size=3).example()
        # self.device(resourceId="it.feio.android.omninotes:id/detail_title").set_text(title)
        # time.sleep(1)
        # content = st.text(alphabet=string.ascii_letters,min_size=0, max_size=3).example()
        # self.device(resourceId="it.feio.android.omninotes:id/detail_content").set_text(content)
        time.sleep(1)
        title = self.device(resourceId="it.feio.android.omninotes:id/detail_title").get_text()
        print("title: " + title)
        content = self.device(resourceId="it.feio.android.omninotes:id/detail_content").get_text()
        print("content: " + content)
        if content  is None:
            content = ""
        import re
        number_of_char = len(re.findall(".",title)) + len(re.findall(".",content))
        print("number of char: " + str(number_of_char))
        time.sleep(1)
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Info").click()
        time.sleep(1)
        chars = int(self.device(resourceId="it.feio.android.omninotes:id/note_infos_chars").get_text())
        print("chars calculated by omninotes: " + str(chars))
        time.sleep(1)
        assert number_of_char == chars

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
    apk_path="./apk/omninotes/OmniNotes-6.3.0.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/800/1",
    explore_event_count=500,
    diverse_event_count=500,
    policy_name="random",
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
