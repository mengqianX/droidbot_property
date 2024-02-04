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
        # self.device(description="drawer open").click()
        # time.sleep(1)
        # self.device(text="SETTINGS").click()
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
        # self.device(resourceId="it.feio.android.omninotes:id/buttonDefaultPositive").click()
        # time.sleep(1)
        # category_name = st.text(alphabet=string.printable,min_size=1, max_size=10).example()
        # self.device(resourceId="it.feio.android.omninotes:id/category_title").set_text(category_name)
        # time.sleep(1)
        # self.device(text="OK").click()
        # time.sleep(1)
        # self.device.press("back")
    
    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/menu_attachment").exists() and self.device(resourceId="it.feio.android.omninotes:id/menu_share").exists() and self.device(resourceId="it.feio.android.omninotes:id/menu_tag").exists() )
    @rule()
    def rule_remove_tag_from_note_shouldnot_affect_content(self):
        print("time: " + str(time.time() - start_time))
        origin_content = self.device(resourceId="it.feio.android.omninotes:id/detail_content").info["text"]
        print("origin_content: " + str(origin_content))
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/menu_tag").click()
        time.sleep(1)
        if not self.device(className="android.widget.CheckBox").exists():
            print("no tag in tag list")
            return
        tag_list_count = int(self.device(className="android.widget.CheckBox").count)
        #tag_list_count = int(self.device(resourceId="it.feio.android.omninotes:id/md_control").count)
        tagged_notes = []
        for i in range(tag_list_count):
            # if self.device(resourceId="it.feio.android.omninotes:id/md_control")[i].info["checked"]:
            if self.device(className="android.widget.CheckBox")[i].info["checked"]:
                tagged_notes.append(i)
        if len(tagged_notes) == 0:
            print("no tag selected in tag list, random select one")
            selected_note_number = random.randint(0, tag_list_count - 1)
            self.device(className="android.widget.CheckBox")[selected_note_number].click()
            time.sleep(1)
            return
        selected_tag_number = random.choice(tagged_notes)
        select_tag_box = self.device(resourceId="it.feio.android.omninotes:id/control")[selected_tag_number]
        select_tag_name = self.device(resourceId="it.feio.android.omninotes:id/title")[selected_tag_number+1].info["text"].split(" ")[0]
        print("selected_tag_number: " + str(selected_tag_number))
        print("selected_tag_name: " + str(select_tag_name))
        select_tag_name = "#"+select_tag_name
        time.sleep(1)
        select_tag_box.click()
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)

        assert not self.device(textContains=select_tag_name).exists(), "tag should be removed from note" 
        new_content = self.device(resourceId="it.feio.android.omninotes:id/detail_content").info["text"].strip()
        print("new_content: " + str(new_content))
        origin_content_exlude_tag = origin_content.replace(select_tag_name, "").strip()
        print("origin_content_exlude_tag: " + str(origin_content_exlude_tag))
        time.sleep(1)
        assert new_content == origin_content_exlude_tag, "content should not be affected by removing tag"
    
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
    apk_path="./apk/omninotes/OmniNotes-5.4.0.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/786/1",
    policy_name="mutate_main_path",
    timeout=7200
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
