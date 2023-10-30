import string
from main import *
import time
import sys


class Test(AndroidCheck):
    def __init__(
        self,
        apk_path,
        device_serial="emulator-5554",
        output_dir="output",
        explore_event_count=0,
        diverse_event_count=100,
        main_path_path=None,
        xml_path=None,
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
        self.device(resourceId="it.feio.android.omninotes:id/md_buttonDefaultPositive").click()
        time.sleep(1)
        category_name = st.text(alphabet=string.printable,min_size=1, max_size=10).example()
        self.device(resourceId="it.feio.android.omninotes:id/category_title").set_text(category_name)
        time.sleep(1)
        self.device(text="OK").click()
        self.device(description="drawer closed").click()
        
    @precondition(
        lambda self: self.device(text="Notes").exists() and self.device(resourceId="it.feio.android.omninotes:id/menu_sort").exists() and not self.device(text="Settings").exists()
    )
    @rule()
    def rule_add_note(self):
        title = st.text(alphabet=string.printable,min_size=1, max_size=10).example()
        content = st.text(alphabet=string.printable,min_size=1, max_size=10).example()
        print("title "+title)
        self.device(resourceId="it.feio.android.omninotes:id/menu_sort").click()
        time.sleep(1)
        self.device(text="Creation date").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/fab_expand_menu_button").click()
        time.sleep(1)
        self.device(text="Text note").click()
        time.sleep(1)
        self.device(text="Title").set_text(title)
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/detail_content").set_text(content)
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/menu_tag").click()
        time.sleep(1)
        if self.device(resourceId="it.feio.android.omninotes:id/md_contentRecyclerView").exists():
            tag_count = int(self.device(resourceId="it.feio.android.omninotes:id/md_contentRecyclerView").info["childCount"])
            if tag_count > 0:
                self.device(resourceId="it.feio.android.omninotes:id/md_contentRecyclerView").child().click()
                self.device(text="OK").click()
        self.device(description="drawer open").click()
        time.sleep(1)
        assert self.device(text=title).exists()

    # @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/menu_search").exists() & self.device(text="Notes").exists() and not self.device(text="Settings").exists())
    # @rule()
    # def rule_search_one(self):
    #     if not self.device(resourceId="it.feio.android.omninotes:id/note_title").exists():
    #         return
    #     note_count = int(self.device(resourceId="it.feio.android.omninotes:id/note_title").count)
    #     selected_note = random.randint(0, note_count - 1)
    #     selected_note_name = self.device(resourceId="it.feio.android.omninotes:id/note_title")[selected_note].info['text']
    #     time.sleep(1)
    #     self.device(resourceId="it.feio.android.omninotes:id/menu_search").click()
    #     time.sleep(1)
    #     self.device(resourceId="it.feio.android.omninotes:id/search_src_text").set_text(selected_note_name)
    #     time.sleep(1)
    #     self.device.send_action("search")
    #     time.sleep(1)
    #     print("selected_note_name: " + selected_note_name)
    #     assert self.device(text=selected_note_name).exists()

    # @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/menu_search").exists() & self.device(text="Notes").exists() & self.device(description="drawer open").exists() and not self.device(text="Settings").exists())
    # @rule()
    # def rule_search_two(self):
    #     # 搜索untagged note，应该返回没有tag的note
    #     self.device(resourceId="it.feio.android.omninotes:id/menu_search").click()
    #     time.sleep(1)
    #     self.device(resourceId="it.feio.android.omninotes:id/menu_tags").click()
    #     time.sleep(1)
    #     self.device(resourceId="it.feio.android.omninotes:id/md_buttonDefaultPositive").click()
    #     note_count = int(self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").count)
    #     selected_note = random.randint(0, note_count - 1)
    #     time.sleep(1)
    #     self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root")[selected_note].click()
    #     time.sleep(1)
    #     self.device(resourceId="it.feio.android.omninotes:id/menu_tag").click()
    #     time.sleep(1)
    #     tag_count = int(self.device(resourceId="it.feio.android.omninotes:id/md_control").count)
    #     time.sleep(1)
    #     print("selected note "+ str(selected_note))
    #     for i in range(tag_count):
    #         assert str(self.device(resourceId="it.feio.android.omninotes:id/md_control")[i].info["checked"]) == "False"

    # @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/menu_search").exists() & self.device(text="Notes").exists() & self.device(description="drawer open").exists())
    # @rule()
    # def rule_select_uncategorized_note(self):
    #     self.device(description="drawer open").click()
    #     self.device(text="Uncategorized").click()
    #     if self.device(text="Notes").exists():
    #         self.device.press("back")
    #     time.sleep(1)
    #     note_count = int(self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").count)
    #     if note_count == 0:
    #         return
    #     selected_note = random.randint(0, note_count - 1)
    #     time.sleep(1)
    #     self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root")[selected_note].click()
    #     time.sleep(1)
    #     self.device(resourceId="it.feio.android.omninotes:id/menu_category").click()
    #     time.sleep(1)
    #     if not self.device(resourceId="it.feio.android.omninotes:id/md_contentRecyclerView").child(className ="android.widget.LinearLayout" )[0].exists():
    #         return 
    #     select_category = self.device(resourceId="it.feio.android.omninotes:id/md_contentRecyclerView").child(className ="android.widget.LinearLayout" )[0]
    #     select_category_name = self.device(resourceId="it.feio.android.omninotes:id/md_contentRecyclerView").child(className ="android.widget.LinearLayout" )[0].child(resourceId="it.feio.android.omninotes:id/title").info["text"]
    #     select_category_count = int(select_category.child(resourceId="it.feio.android.omninotes:id/count").info["text"])
    #     select_category.click()
    #     time.sleep(1)
    #     self.device(resourceId="it.feio.android.omninotes:id/menu_category").click()
    #     time.sleep(1)
    #     select_category_count_after = int(select_category.child(resourceId="it.feio.android.omninotes:id/count").info["text"])
    #     print("select_category_name: " + select_category_name)
    #     time.sleep(1)
    #     assert select_category_count_after == select_category_count + 1

    # @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/menu_search").exists() & self.device(text="Notes").exists() & self.device(description="drawer open").exists() and not self.device(text="Settings").exists())
    # @rule()
    # def action_enter_setting(self):
    #     self.device(description="drawer open").click()
    #     time.sleep(1)
    #     self.device(text="Settings").click()

    # @precondition(lambda self: self.device(text="Categorize as").exists())
    # @rule()
    # def rule_add_category(self):
    #     self.device(resourceId="it.feio.android.omninotes:id/md_buttonDefaultPositive").click()
    #     time.sleep(1)
    #     category_name = st.text(alphabet=string.printable,min_size=1, max_size=10).example()
    #     self.device(resourceId="it.feio.android.omninotes:id/category_title").set_text(category_name)
    #     time.sleep(1)
    #     self.device(text="OK").click()
    #     time.sleep(1)
    #     self.device(resourceId="it.feio.android.omninotes:id/menu_category").click()
    #     time.sleep(1)
    #     print("category_name: " + category_name)
    #     time.sleep(1)
    #     assert self.device(text=category_name).exists()

    # @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/menu_search").exists() & self.device(text="Notes").exists() & self.device(description="drawer open").exists() and not self.device(text="Settings").exists())
    # @rule()
    # def rule_check_category_note_number(self):
    #     note_count = int(self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").count)
    #     if note_count == 0:
    #         return
    #     selected_note = random.randint(0, note_count - 1)
    #     time.sleep(1)
    #     self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root")[selected_note].click()
    #     time.sleep(1)
    #     self.device(resourceId="it.feio.android.omninotes:id/menu_category").click()
    #     if not self.device(resourceId="it.feio.android.omninotes:id/md_contentRecyclerView").child(className ="android.widget.LinearLayout" )[0].exists():
    #         return 
    #     select_category = self.device(resourceId="it.feio.android.omninotes:id/md_contentRecyclerView").child(className ="android.widget.LinearLayout" )[0]
    #     select_category_name = self.device(resourceId="it.feio.android.omninotes:id/md_contentRecyclerView").child(className ="android.widget.LinearLayout" )[0].child(resourceId="it.feio.android.omninotes:id/title").info["text"]
    #     select_category_count = int(select_category.child(resourceId="it.feio.android.omninotes:id/count").info["text"])
    #     print("select_category_name: " + select_category_name)
    #     time.sleep(1)
    #     self.device.press("back")
    #     time.sleep(1)
    #     self.device(description="drawer open").click()
    #     time.sleep(1)
    #     if not self.device(description="More options").exists() and not self.device(description="drawer open").exists():
    #         return
    #     self.device(description="drawer open").click()
    #     category = self.device(text=select_category_name)
    #     if not category.exists():
    #         return
    #     category_count = int(category.sibling(resourceId="it.feio.android.omninotes:id/count").info["text"])
    #     assert category_count == select_category_count

    # @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/note_title").exists())
    # @rule()
    # def action_archive_note(self):
    #     if not self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").exists():
    #         return
    #     note_count = int(self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").count)
    #     selected_note = random.randint(0, note_count - 1)
    #     print("selected_note: " + str(selected_note))
    #     time.sleep(1)
    #     self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root")[selected_note].long_click()
    #     time.sleep(1)
    #     self.device(description="More options").click()
    #     time.sleep(1)
    #     self.device(text="Archive").click()
        
    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/note_title").exists() and self.device(text="Notes").exists() and not self.device(text="Settings").exists())
    @rule()
    def rule_archive_note(self):
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
        self.device(text="Archive").click()
        time.sleep(1)
        # 再去archive 列表中查找
        self.device(description="drawer open").click()
        time.sleep(1)
        self.device(text="Archive").click()
        time.sleep(1)
        assert self.device(text=selected_note_name).exists()

        
    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/note_title").exists() and self.device(text="Notes").exists() and not self.device(text="Settings").exists())
    @rule()
    def rule_trash_note(self):
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
        # 再去archive 列表中查找
        self.device(description="drawer open").click()
        time.sleep(1)
        self.device(text="Trash").click()
        time.sleep(1)
        assert self.device(text=selected_note_name).exists()

    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/menu_attachment").exists() and self.device(description="More options").exists() and self.device(resourceId="it.feio.android.omninotes:id/reminder_icon").exists())
    @rule()
    def action_pin_note(self):
        self.device(description="More options").click()
        time.sleep(1)
        if not self.device(text="Pin note").exists():
            return
        self.device(text="Pin note").click()
        time.sleep(1)

start_time = time.time()

args = sys.argv[1:]
apk_path = args[0]
device_serial = args[1]
output_dir = args[2]
xml_path = args[3]
main_path_path = args[4]
source_activity = args[5]
target_activity = args[6]
policy_name = args[7]
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
    apk_path=apk_path,
    device_serial=device_serial,
    output_dir=output_dir,
    explore_event_count=100,
    diverse_event_count=100,
    xml_path=xml_path,
    main_path_path=main_path_path,
    source_activity=source_activity,
    target_activity=target_activity,
    policy_name=policy_name,
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
