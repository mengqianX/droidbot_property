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
        # lock note
        # self.device(description="More options").click()
        # time.sleep(1)
        # self.device(text="Lock").click()
        # time.sleep(1)
        # self.device(resourceId="it.feio.android.omninotes:id/password").set_text("1")
        # time.sleep(1)
        # self.device(resourceId="it.feio.android.omninotes:id/password_check").set_text("1")
        # time.sleep(1)
        # self.device(resourceId="it.feio.android.omninotes:id/question").set_text("1")
        # time.sleep(1)
        # self.device(resourceId="it.feio.android.omninotes:id/answer").set_text("1")
        # time.sleep(1)
        # self.device(resourceId="it.feio.android.omninotes:id/answer_check").set_text("1")
        # time.sleep(1)
        # self.device(scrollable=True).fling()
        # time.sleep(1)
        # self.device(text="OK").click()
        # time.sleep(2)
        self.device.press("back")
    # action
    @precondition(lambda self:  self.device(resourceId="it.feio.android.omninotes:id/count").exists() and self.device(text="Settings").exists())
    @rule()
    def action_category_deletion(self):
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

    @precondition(
        lambda self: self.device(text="Notes").exists() and self.device(resourceId="it.feio.android.omninotes:id/menu_sort").exists() and not self.device(text="Settings").exists() and self.device(resourceId="it.feio.android.omninotes:id/note_title").count < 6
    )
    @rule()
    def action_add_note(self):
        title = st.text(alphabet=string.ascii_letters+string.digits,min_size=1, max_size=10).example()
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
    # bug #598
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
    
    # action #598
    @precondition(lambda self: self.device(description="More options").exists() and self.device(resourceId="it.feio.android.omninotes:id/menu_attachment").exists())
    @rule()
    def action_lock_a_note(self):
        title = st.text(alphabet=string.printable,min_size=1, max_size=10).example()
        print("title: " + title)
        self.device(resourceId="it.feio.android.omninotes:id/detail_title").set_text(title)
        time.sleep(1)
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Lock").click()
        time.sleep(1)
        if self.device(text="Insert password").exists():
            self.device(resourceId="it.feio.android.omninotes:id/password_request").set_text("1")
            time.sleep(1)
            self.device(text="OK").click()
            time.sleep(3)
            self.device.press("back")
        else:
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
            time.sleep(3)
            self.device.press("back")
    
    # bug #625
    @precondition(lambda self: self.device(text="Categorize as").exists())
    @rule()
    def rule_add_category_should_change_number(self):
        print("time: " + str(time.time() - start_time))
        self.device(text="ADD CATEGORY").click()
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
        #assert self.device(resourceId="it.feio.android.omninotes.alpha:id/md_contentRecyclerView").child_by_text(category_name,allow_scroll_search=True).exists()
        assert self.device(text=category_name).exists(), "category_name: " + category_name
        time.sleep(1)
        assert self.device(text=category_name).right(resourceId="it.feio.android.omninotes:id/count").get_text() == "1"
    
    # bug #381
    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/toolbar").child(text="Trash").exists() and self.device(resourceId="it.feio.android.omninotes:id/root").exists() and not self.device(text="SETTINGS").exists())
    @rule()
    def restore_note_from_trash_should_work(self):
        print("time: " + str(time.time() - start_time))
        note_count = int(self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").count)
        selected_note = random.randint(0, note_count - 1)
        print("selected_note: " + str(selected_note))
        time.sleep(1)
        selected_note = self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root")[selected_note].child(resourceId="it.feio.android.omninotes:id/card_layout")
        time.sleep(1)
        note_title = selected_note.child(resourceId="it.feio.android.omninotes:id/note_title").get_text()
        print("note_title: " + note_title)
        time.sleep(1)
        is_archive = selected_note.child(resourceId="it.feio.android.omninotes:id/archivedIcon").exists()
        print("is_archive: " + str(is_archive))
        time.sleep(1)
        selected_note.long_click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/menu_sort").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/toolbar").child(className="android.widget.ImageButton").click()
        time.sleep(1)
        if is_archive:
            
            assert self.device(text="Archive").exists(),"Archive should appear in drawer item"
            time.sleep(1)
            self.device(text="Archive").click()
            assert self.device(resourceId="it.feio.android.omninotes:id/list").child_by_text(note_title,allow_scroll_search=True).exists(),"note should appear in Archive"
        else:
            self.device(text="Notes").click()
            time.sleep(1)
            assert self.device(resourceId="it.feio.android.omninotes:id/list").child_by_text(note_title,allow_scroll_search=True).exists(),"note should appear in Notes"
    
    # bug #340
    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/count").exists() and self.device(text="Settings").exists())
    @rule()
    def delete_category_should_remove_immediately(self):
        print("time: " + str(time.time() - start_time))
        category_count = self.device(resourceId="it.feio.android.omninotes:id/count").count
        selected_category_index = random.randint(0, category_count - 1)
        selected_category = self.device(resourceId="it.feio.android.omninotes:id/count")[selected_category_index].left(resourceId="it.feio.android.omninotes:id/title")
        selected_category_name = selected_category.get_text()
        print("selected_category_name: " + selected_category_name)
        time.sleep(1)
        selected_category.long_click()
        time.sleep(1)
        self.device(text="DELETE").click()
        time.sleep(1)
        self.device(text="CONFIRM").click()
        time.sleep(1)
        assert not self.device(text=selected_category_name).exists()

    # bug #237
    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/menu_attachment").exists() and self.device(resourceId="it.feio.android.omninotes:id/menu_share").exists() and self.device(resourceId="it.feio.android.omninotes:id/menu_tag").exists() )
    @rule()
    def hash_tag_with_number_start_shouldbe_recognized(self):
        print("time: " + str(time.time() - start_time))
        text = st.text(alphabet=string.ascii_letters+string.digits,min_size=1, max_size=5).example()
        tag = "#"+ text
        print("tag: " + tag)
        self.device(resourceId="it.feio.android.omninotes:id/detail_content").set_text(tag)
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/toolbar").child(className="android.widget.ImageButton").click()
        time.sleep(1)

        note_count = int(self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").count)
        selected_note = random.randint(0, note_count - 1)
        selected_note_name = self.device(resourceId="it.feio.android.omninotes:id/note_title")[selected_note].info['text']
        print("selected_note: " + str(selected_note_name))
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root")[selected_note].click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/menu_tag").click()
        time.sleep(1)
        assert self.device(resourceId="it.feio.android.omninotes:id/md_title",textContains=text).exists()

    # bug #104
    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/menu_attachment").exists() and self.device(resourceId="it.feio.android.omninotes:id/detail_title").get_text() != "Title")
    @rule()
    def remove_password_should_not_affect_notes(self):
        print("time: " + str(time.time() - start_time))
        note_title = self.device(resourceId="it.feio.android.omninotes:id/detail_title").get_text()
        print("title: " + str(note_title))
        time.sleep(1)
        content = self.device(resourceId="it.feio.android.omninotes:id/detail_content").get_text()
        print("content: " + str(content))
        time.sleep(1)
        self.device(description="More options").click()
        time.sleep(1)
        if self.device(text="Lock").exists():
            self.device(text="Lock").click()
            time.sleep(1)
            if self.device(resourceId="it.feio.android.omninotes:id/password_request").exists():
                self.device(resourceId="it.feio.android.omninotes:id/password_request").set_text("1")
                time.sleep(1)
                self.device(text="OK").click()
            else:    
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
            
        else:
            print("the note has been lock, return")
            self.device(text="Unlock").click()
            return
        time.sleep(2)
        self.device.press("back")

        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/toolbar").child(className="android.widget.ImageButton").click()
        time.sleep(1)
        self.device(text="Settings").click()
        time.sleep(1)
        self.device(text="Data").click()
        time.sleep(1)
        self.device(text="Password").click()
        time.sleep(1)
        self.device(text="REMOVE PASSWORD").click()
        time.sleep(1)
        if not self.device(text="Insert password").exists():
            print("password is not set, return")
            return 
        self.device(resourceId="it.feio.android.omninotes:id/password_request").set_text("1")
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(2)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        assert self.device(text=note_title).exists()," note title should exists the same as before "+note_title
        self.device(text=note_title).click()
        assert str(self.device(resourceId="it.feio.android.omninotes:id/detail_content").get_text()) == content," note content should exists the same as before "+content
        self.device.press("back")

    # bug #886
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
        if self.device(resourceId="it.feio.android.omninotes:id/password_request").exists():
            self.device(resourceId="it.feio.android.omninotes:id/password_request").set_text("1")
            time.sleep(1)
            self.device(text="OK").click()
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

    # # bug #812
    # @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/menu_search").exists() and self.device(resourceId="it.feio.android.omninotes:id/note_title").exists() and self.device(text="Notes").exists() and not self.device(text="SETTINGS").exists())
    # @rule()
    # def rule_restore_backup_shouldnot_change_note(self):
    #     print("time: " + str(time.time() - start_time))
    #     #首先选择一个note，记录下note的title，content，是否有attachment
    #     note_count = int(self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").count)
    #     selected_note = random.randint(0, note_count - 1)
    #     print("selected_note: " + str(selected_note))
    #     time.sleep(1)
    #     selected_note = self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root")[selected_note].child(resourceId="it.feio.android.omninotes:id/card_layout")
    #     time.sleep(1)
    #     note_title = selected_note.child(resourceId="it.feio.android.omninotes:id/note_title").get_text()
    #     print("note_title: " + note_title)
    #     time.sleep(1)
    #     note_content = selected_note.child(resourceId="it.feio.android.omninotes:id/note_content").get_text()
    #     print("note_content: " + note_content)
    #     time.sleep(1)
    #     has_attachment = selected_note.child(resourceId="it.feio.android.omninotes:id/attachmentThumbnail").exists()
    #     print("has_attachment: " + str(has_attachment))
    #     # 然后去设置中点击备份然后恢复备份
    #     self.device(resourceId="it.feio.android.omninotes:id/toolbar").child(className="android.widget.ImageButton").click()
    #     time.sleep(1)
    #     self.device(text="Settings").click()
    #     time.sleep(1)
    #     self.device(text="Data").click()
    #     time.sleep(1)
    #     self.device(text="Sync and Backups").click()
    #     time.sleep(1)
    #     self.device(text="Backup").click()
    #     time.sleep(1)
    #     back_up_name = self.device(resourceId="it.feio.android.omninotes:id/export_file_name").get_text()
    #     self.device(text="CONFIRM").click()
    #     time.sleep(1)
    #     self.device(text="Restore or delete backups").click()
    #     time.sleep(1)
    #     self.device(text=back_up_name).click()
    #     time.sleep(1)
    #     self.device(text="CONFIRM").click()
    #     time.sleep(1)
    #     self.device.press("back")
    #     time.sleep(1)
    #     self.device.press("back")
    #     time.sleep(1)
    #     self.device.press("back")
    #     time.sleep(1)
    #     self.device.press("back")
    #     time.sleep(1)
    #     # 检查note的title，content，是否有attachment是否发生了变化
    #     assert selected_note.exists(), "selected note not exists"
    #     assert selected_note.child(resourceId="it.feio.android.omninotes:id/note_title").get_text() == note_title, "note_title: "  + selected_note.child(resourceId="it.feio.android.omninotes:id/note_title").get_text()
    #     assert selected_note.child(resourceId="it.feio.android.omninotes:id/note_content").get_text() == note_content, "note_content: " + selected_note.child(resourceId="it.feio.android.omninotes:id/note_content").get_text()
    #     assert selected_note.child(resourceId="it.feio.android.omninotes:id/attachmentThumbnail").exists() == has_attachment, "has_attachment: " + str(selected_note.child(resourceId="it.feio.android.omninotes:id/attachmentThumbnail").exists())

    # bug #801
    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/note_title").exists() and self.device(text="Notes").exists() and not self.device(text="Settings").exists() and self.device(resourceId="it.feio.android.omninotes:id/lockedIcon").exists())
    @rule()
    def swipe_locked_note(self):
        print("time: " + str(time.time() - start_time))
        selected_note = self.device(resourceId="it.feio.android.omninotes:id/lockedIcon").up(resourceId="it.feio.android.omninotes:id/note_title")
        selected_note_text = selected_note.get_text()
        print("selected_note_text: " + selected_note_text)
        time.sleep(1)
        selected_note.scroll.horiz.forward(steps=100)
        time.sleep(3)
        self.device.press("recent")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        assert self.device(text=selected_note_text).exists()

    # bug #786_634
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
        select_tag_box = self.device(resourceId="it.feio.android.omninotes:id/md_control")[selected_tag_number]
        select_tag_name = select_tag_box.right(resourceId="it.feio.android.omninotes:id/md_title").info["text"].split(" ")[0]
        # select_tag_name = self.device(resourceId="it.feio.android.omninotes:id/title")[selected_tag_number+1].info["text"].split(" ")[0]
        print("selected_tag_number: " + str(selected_tag_number))
        print("selected_tag_name: " + str(select_tag_name))
        select_tag_name = "#"+select_tag_name
        time.sleep(1)
        select_tag_box.click()
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)

        assert not self.device(textContains=select_tag_name).exists()    
        new_content = self.device(resourceId="it.feio.android.omninotes:id/detail_content").info["text"].strip().replace("Content", "")
        print("new_content: " + str(new_content))
        origin_content_exlude_tag = origin_content.replace(select_tag_name, "").strip()
        print("origin_content_exlude_tag: " + str(origin_content_exlude_tag))
        time.sleep(1)
        assert new_content == origin_content_exlude_tag

    # bug #283
    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/search_query").exists() and self.device(resourceId="it.feio.android.omninotes:id/root").exists() and not self.device(text="SETTINGS").exists())
    @rule()
    def search_result_should_not_contain_other_notes(self):
        print("time: " + str(time.time() - start_time))
        text = self.device(resourceId="it.feio.android.omninotes:id/search_query").get_text().split(" ")[1]
        print("search text: " + text)
        if not self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").exists():
            return
        note_count = int(self.device(resourceId="it.feio.android.omninotes:id/list").child(resourceId="it.feio.android.omninotes:id/root").count)
        selected_note_number = random.randint(0, note_count - 1)
        selected_note = self.device(resourceId="it.feio.android.omninotes:id/root")[selected_note_number]
        print("selected_note: " + str(selected_note_number))
        selected_note.click()
        title = self.device(resourceId="it.feio.android.omninotes:id/detail_title").get_text()
        print("title: " + title)
        content = self.device(resourceId="it.feio.android.omninotes:id/detail_content").get_text()
        print("content: " + content)
        assert text in title or text in content
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
    apk_path="./apk/OmniNotes-6.3.0.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/6_3_0/1",
    explore_event_count=500,
    diverse_event_count=500,
    policy_name="random",
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
