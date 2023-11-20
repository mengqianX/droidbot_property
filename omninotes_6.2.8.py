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
        content = st.text(alphabet=string.printable,min_size=0, max_size=10).example()
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
                self.device(resourceId="it.feio.android.omninotes:id/md_contentRecyclerView").child(className="android.widget.LinearLayout")[random.randint(0,tag_count-1)].click()
                self.device(text="OK").click()
        self.device(description="drawer open").click()
        time.sleep(1)
        assert self.device(text=title).exists()

    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/menu_search").exists() & self.device(text="Notes").exists() and not self.device(text="Settings").exists())
    @rule()
    def rule_search_one(self):
        if not self.device(resourceId="it.feio.android.omninotes:id/note_title").exists():
            return
        note_count = int(self.device(resourceId="it.feio.android.omninotes:id/note_title").count)
        selected_note = random.randint(0, note_count - 1)
        selected_note_name = self.device(resourceId="it.feio.android.omninotes:id/note_title")[selected_note].info['text']
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/menu_search").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/search_src_text").set_text(selected_note_name)
        time.sleep(1)
        self.device.send_action("search")
        time.sleep(1)
        print("selected_note_name: " + selected_note_name)
        assert self.device(text=selected_note_name).exists()

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

    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/menu_search").exists() & self.device(text="Notes").exists() & self.device(description="drawer open").exists())
    @rule()
    def rule_select_uncategorized_note(self):
        self.device(description="drawer open").click()
        self.device(text="Uncategorized").click()
        if self.device(text="Notes").exists():
            self.device.press("back")
        time.sleep(1)
        note_count = int(self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").count)
        if note_count == 0:
            return
        selected_note = random.randint(0, note_count - 1)
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root")[selected_note].click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/menu_category").click()
        time.sleep(1)
        if not self.device(resourceId="it.feio.android.omninotes:id/md_contentRecyclerView").child(className ="android.widget.LinearLayout" )[0].exists():
            return 
        select_category = self.device(resourceId="it.feio.android.omninotes:id/md_contentRecyclerView").child(className ="android.widget.LinearLayout" )[0]
        select_category_name = self.device(resourceId="it.feio.android.omninotes:id/md_contentRecyclerView").child(className ="android.widget.LinearLayout" )[0].child(resourceId="it.feio.android.omninotes:id/title").info["text"]
        select_category_count = int(select_category.child(resourceId="it.feio.android.omninotes:id/count").info["text"])
        select_category.click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/menu_category").click()
        time.sleep(1)
        select_category_count_after = int(select_category.child(resourceId="it.feio.android.omninotes:id/count").info["text"])
        print("select_category_name: " + select_category_name)
        time.sleep(1)
        assert select_category_count_after == select_category_count + 1

    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/menu_search").exists() & self.device(text="Notes").exists() & self.device(description="drawer open").exists() and not self.device(text="Settings").exists())
    @rule()
    def action_enter_setting(self):
        self.device(description="drawer open").click()
        time.sleep(1)
        self.device(text="Settings").click()

    @precondition(lambda self: self.device(text="Categorize as").exists())
    @rule()
    def rule_add_category(self):
        self.device(resourceId="it.feio.android.omninotes:id/md_buttonDefaultPositive").click()
        time.sleep(1)
        category_name = st.text(alphabet=string.printable,min_size=1, max_size=10).example()
        self.device(resourceId="it.feio.android.omninotes:id/category_title").set_text(category_name)
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/menu_category").click()
        time.sleep(1)
        print("category_name: " + category_name)
        time.sleep(1)
        assert self.device(resourceId="it.feio.android.omninotes.alpha:id/md_contentRecyclerView").child_by_text(category_name,allow_scroll_search=True).exists()

    @precondition(lambda self:  self.device(resourceId="it.feio.android.omninotes:id/count").exists() and self.device(text="Settings").exists())
    @rule()
    def rule_category_deletion(self):
        category_count = int(self.device(resourceId="it.feio.android.omninotes:id/count").count)
        if category_count == 0:
            print("no category")
            return
        selected_category = random.randint(0, category_count - 1)
        print("selected_category: " + str(selected_category))
        selected_category_count = int(self.device(resourceId="it.feio.android.omninotes:id/count")[selected_category].get_text())
        print("category_count: " + str(selected_category_count))
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/count")[selected_category].long_click()
        time.sleep(1)
        selected_category_name = self.device(resourceId="it.feio.android.omninotes:id/category_title").get_text()
        print("selectec_category_name: " + selected_category_name)
        self.device(text="DELETE").click()
        time.sleep(1)
        if self.device(text="CONFIRM").exists():
            self.device(text="CONFIRM").click()
        time.sleep(1)
        assert not self.device(text=selected_category_name).exists() 
    
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

    # @precondition(lambda self: self.device(text="Uncategorized").exists() and self.device(text="Settings").exists())
    # @rule()
    # def rule_uncategory_should_contain_notes(self):
    #     self.device(text="Uncategorized",resourceId="it.feio.android.omninotes:id/title").click()
    #     time.sleep(1)
    #     assert self.device(resourceId="it.feio.android.omninotes:id/root").exists()

    # @precondition(lambda self: self.device(text="Trash").exists() and self.device(text="Settings").exists())
    # @rule()
    # def rule_trash_should_contain_notes(self):
    #     self.device(text="Trash",resourceId="it.feio.android.omninotes:id/title").click()
    #     time.sleep(1)
    #     assert self.device(resourceId="it.feio.android.omninotes:id/root").exists()

    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/note_title").exists())
    @rule()
    def action_archive_note(self):
        if not self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").exists():
            return
        note_count = int(self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").count)
        selected_note = random.randint(0, note_count - 1)
        print("selected_note: " + str(selected_note))
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root")[selected_note].long_click()
        time.sleep(1)
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Archive").click()
        
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

    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/note_title").exists() and self.device(resourceId="it.feio.android.omninotes:id/alarmIcon").exists())
    @rule()
    def rule_reminder_note_list(self):
        select_note  = self.device(resourceId="it.feio.android.omninotes:id/alarmIcon").up(resourceId="it.feio.android.omninotes:id/note_title")
        select_note_name = select_note.info["text"]
        self.device(description="drawer open").click()
        self.device(text="Reminders").click()
        assert self.device(text=select_note_name).exists()

    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/menu_attachment").exists() and self.device(resourceId="it.feio.android.omninotes:id/menu_share").exists() and self.device(resourceId="it.feio.android.omninotes:id/menu_tag").exists() )
    @rule()
    def rule_remove_tag_from_note(self):
        self.device(resourceId="it.feio.android.omninotes:id/menu_tag").click()
        time.sleep(1)
        if not self.device(resourceId="it.feio.android.omninotes:id/md_title").exists():
            print("no tag in tag list")
            return
        tag_list_count = int(self.device(resourceId="it.feio.android.omninotes:id/md_control").count)
        tagged_notes = []
        for i in range(tag_list_count):
            if self.device(resourceId="it.feio.android.omninotes:id/md_control")[i].info["checked"]:
                tagged_notes.append(i)
        if len(tagged_notes) == 0:
            print("no tag selected in tag list, random select one")
            selected_note_number = random.randint(0, tag_list_count - 1)
            self.device(resourceId="it.feio.android.omninotes:id/md_control")[selected_note_number].click()
            time.sleep(1)
            return
        selected_tag_number = random.choice(tagged_notes)
        select_tag_box = self.device(resourceId="it.feio.android.omninotes:id/md_control")[selected_tag_number]
        select_tag_name = self.device(resourceId="it.feio.android.omninotes:id/md_title")[selected_tag_number+1].info["text"].split(" ")[0]
        print("selected_tag_number: " + str(selected_tag_number))
        print("selected_tag_name: " + str(select_tag_name))
        select_tag_name = "#"+select_tag_name
        time.sleep(1)
        select_tag_box.click()
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)

        assert not self.device(textContains=select_tag_name).exists()     

    # @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/reminder_layout").exists())
    # @rule()
    # def add_reminder(self):
    #     self.device(resourceId="it.feio.android.omninotes:id/reminder_layout").click()
    #     time.sleep(1)
    #     self.device(text="OK").click()
    #     time.sleep(1)
    #     reminder_text = self.device(resourceId="it.feio.android.omninotes:id/datetime").get_text()
    #     assert "Reminder set for" in reminder_text
    

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
