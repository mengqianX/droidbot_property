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
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/action_sort").click()
        time.sleep(1)
        self.device(text="Date").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/action_sort").click()
        time.sleep(1)
        self.device(text="Reverse order").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/action_sort").click()
        time.sleep(1)
        self.device(text="Folder first").click()
        

    @precondition(
        lambda self: self.device(
            resourceId="net.gsantner.markor:id/fab_add_new_item"
        ).exists() and int(self.device(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title").count) < 7
    )
    @rule()
    def rule_add_note(self):
        self.device(resourceId="net.gsantner.markor:id/fab_add_new_item").click()
        time.sleep(1)
        name = st.text(alphabet=string.ascii_letters,min_size=1, max_size=6).example()
        suffix = self.device(resourceId="net.gsantner.markor:id/new_file_dialog__ext").get_text()
        
        self.device(resourceId="net.gsantner.markor:id/new_file_dialog__name").set_text(
            name
        )
        name = name+suffix
        time.sleep(1)
        print("file name: "+str(name))
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        content = st.text(alphabet=string.printable,min_size=1, max_size=10).example()
        self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").set_text(content)
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/action_save").click()
        self.device.press("back")
        if self.device(resourceId="net.gsantner.markor:id/action_save").exists():
            self.device.press("back")
        time.sleep(1)
        assert self.device(text=name).exists()
    
    # bug #1961
    @precondition(lambda self: self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").exists() and self.device(resourceId="net.gsantner.markor:id/action_search").exists())
    @rule()
    def search_in_the_file(self):
        content = self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").info['text']
        if content is None:
            print("no content")
            return
        time.sleep(1)
        words = content.split(" ")
        search_word = random.choice(words)
        print("search word: "+str(search_word))
        self.device(resourceId="net.gsantner.markor:id/action_search").click()
        time.sleep(1)
        self.device(text="Search").set_text(search_word)
        time.sleep(1)
        search_result = self.device(resourceId="android:id/text1")
        search_result_count = search_result.count
        print("search result count: "+str(search_result_count))
        assert search_result_count > 0
        search_result_text = search_result.info['text']
        print("search result text: "+str(search_result_text))
        assert search_word in str(search_result_text)

    # bug #1481
    @precondition(
        lambda self: self.device(
            resourceId="net.gsantner.markor:id/fab_add_new_item"
        ).exists()
    )
    @rule()
    def rule_rename_file(self):
        file_count = self.device(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title").count
        print("file count: "+str(file_count))
        if file_count == 0:
            print("no file to rename")
            return
        file_index = random.randint(0, file_count - 1)
        selected_file = self.device(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title")[file_index]
        file_name = selected_file.info['text']
        is_file = True
        if "." not in file_name:
            is_file = False
            print("not a file")
            return
        file_name_suffix = file_name.split(".")[-1]
        print("file name: "+str(file_name))
        selected_file.long_click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/action_rename_selected_item").click()
        time.sleep(1)
        name = st.text(alphabet=string.ascii_letters,min_size=1, max_size=6).example()
        if is_file:
            name = name+"."+file_name_suffix
        print("new file name: "+str(name))
        self.device(resourceId="net.gsantner.markor:id/new_name").set_text(name)
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        assert self.device(text=name).exists()

    # bug #331
    @precondition(lambda self: self.device(resourceId="net.gsantner.markor:id/action_save").exists() and self.device(resourceId="net.gsantner.markor:id/action_save").info["enabled"] == True)
    @rule()
    def rule_save_file(self):
        file_name = self.device(resourceId="net.gsantner.markor:id/note__activity__text_note_title").get_text()
        origin_content = self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").get_text()
        print("origin_content: " + origin_content)
        self.device(resourceId="net.gsantner.markor:id/action_save").click()
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        if not self.device(text=file_name+".md").exists():
            print("do not find the file")
            return
        self.device(text=file_name+".md").click()
        time.sleep(1)
        content = self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").get_text()
        print("content: " + content)
        assert content == origin_content

    # bug #10
    @precondition(lambda self: self.device(resourceId="net.gsantner.markor:id/action_preview").exists())
    @rule()
    def rule_preview_should_not_change_content(self):
        origin_content = self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").get_text()
        self.device(resourceId="net.gsantner.markor:id/action_preview").click()
        time.sleep(1)
        if not self.device(resourceId="net.gsantner.markor:id/action_edit").exists():
            print("don't find edit button")
            return
        self.device(resourceId="net.gsantner.markor:id/action_edit").click()
        time.sleep(1)
        content = self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").get_text()
        assert content == origin_content, "content changed after preview"

    # bug #1985
    @precondition(lambda self: self.device(resourceId="net.gsantner.markor:id/fab_add_new_item").exists() and not self.device(text="Settings").exists() and not self.device(text="Date").exists())
    @rule()
    def click_FAB_should_work(self):
        self.device(resourceId="net.gsantner.markor:id/fab_add_new_item").click()
        time.sleep(1)
        assert self.device(text="OK", resourceId="android:id/button1").exists()

    # bug #1729
    @precondition(lambda self: self.device(resourceId="net.gsantner.markor:id/action_preview").exists() and not self.device(resourceId="net.gsantner.markor:id/action_edit").exists())
    @rule()
    def added_text_can_be_shown_in_preview(self):
        original_content = self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").get_text()
        print("original_content: " + str(original_content))
        content = st.text(alphabet=string.ascii_lowercase,min_size=1, max_size=10).example()
        print("add content: "+content)
        self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").set_text(str(original_content)+" "+content)
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/action_preview").click()
        time.sleep(1)
        for i in range(int(self.device(className="android.webkit.WebView").child(className="android.view.View").count)):
            print("content: "+self.device(className="android.webkit.WebView").child(className="android.view.View")[i].info["contentDescription"])
            if content in str(self.device(className="android.webkit.WebView").child(className="android.view.View")[i].info["contentDescription"]):
                return True
        # new_content = self.device(resourceId="net.gsantner.markor:id/document__placeholder_fragment").child(className="android.view.View").info["contentDescription"]
        # print("new_content: " + new_content)
        assert False, "added text can not be shown in preview"

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

    # bug #1149
    @precondition(
        lambda self: self.device(resourceId="net.gsantner.markor:id/action_preview").exists() and not self.device(text="Save").exists()
        )
    @rule()
    def change_view_mode_should_not_change_position(self):
        content = self.device(className="android.widget.EditText").get_text()
        if content is None:
            content = ""
        print("content: " + content)
        added_content = st.text(alphabet=string.ascii_lowercase,min_size=1, max_size=6).example()
        print("added_content: " + added_content)
        self.device(className="android.widget.EditText").set_text(content + " "+ added_content)
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/action_preview").click()
        time.sleep(1)
        for i in range(int(self.device(className="android.webkit.WebView").child(className="android.view.View").count)):
            print("content: "+self.device(className="android.webkit.WebView").child(className="android.view.View")[i].info["contentDescription"])
            if added_content in str(self.device(className="android.webkit.WebView").child(className="android.view.View")[i].info["contentDescription"]):
                return True
        assert False
    
    #bug 1220
    # @precondition(
    #     lambda self: self.device(resourceId="net.gsantner.markor:id/fab_add_new_item").exists() and not self.device(text="Settings").exists() and not self.device(text="Date").exists() and not self.device(resourceId="net.gsantner.markor:id/action_rename_selected_item").exists()
    #     )
    # @rule()
    # def change_file_format_should_work(self):
    #     file_count = self.device(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title").count
    #     print("file count: "+str(file_count))
    #     if file_count == 0:
    #         print("no file ")
    #         return
    #     file_index = random.randint(0, file_count - 1)
    #     selected_file = self.device(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title")[file_index]
    #     file_name = selected_file.info['text']
        
    #     if "." not in file_name or ".." in file_name:
    #         print("not a file")
    #         return
    #     print("file name: "+str(file_name))
    #     selected_file.click()
    #     time.sleep(1)
    #     self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").set_text("# test")
    #     time.sleep(1)
    #     self.device(description="More options").click()
    #     time.sleep(1)
    #     self.device(text="File settings").click()
    #     time.sleep(1)
    #     self.device(text="Format").click()
    #     time.sleep(1)
    #     self.device(text="Markdown").click()
    #     time.sleep(1)
    #     self.device(resourceId="net.gsantner.markor:id/action_preview").click()
    #     time.sleep(1)
    #     assert "#" not in self.device(className="android.webkit.WebView").child(className="android.view.View").info["contentDescription"], "1 markdown format failed"
    #     time.sleep(1)
    #     self.device.press("back")
    #     time.sleep(1)
    #     self.device.press("back")
    #     time.sleep(1)
    #     self.device(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title")[file_index].click()
    #     time.sleep(1)
    #     assert "#" not in self.device(className="android.webkit.WebView").child(className="android.view.View").info["contentDescription"], "2 markdown format failed"

    # bug #1020
    # @precondition(
    #     lambda self: self.device(resourceId="net.gsantner.markor:id/new_file_dialog__name").exists() 
    #     )
    # @rule()
    # def file_type_should_be_the_same(self):
    #     file_type = self.device(resourceId="net.gsantner.markor:id/new_file_dialog__type").child(className="android.widget.TextView").get_text()
    #     print("file_type: " + file_type)
    #     file_name_suffix = self.device(resourceId="net.gsantner.markor:id/new_file_dialog__ext").get_text()
    #     print("file_name_suffix: " + file_name_suffix)
    #     if file_type == "Markdown":
    #         assert file_name_suffix == ".md"
    #     elif file_type == "Plain Text":
    #         assert file_name_suffix == ".txt"
    #     elif file_type == "todo.txt":
    #         assert file_name_suffix == ".todo.txt"
    #     elif file_type == "AsciiDoc":
    #         assert file_name_suffix == ".adoc"
    #     elif file_type == "CSV":
    #         assert file_name_suffix == ".csv"
    #     elif file_type == "OrgMode":
    #         assert file_name_suffix == ".org"
    #     elif file_type == "Wikitext":
    #         assert file_name_suffix == ".txt"
    #     else:
    #         assert file_name_suffix == ".md"

    #bug 994
    @precondition(
        lambda self: self.device(resourceId="net.gsantner.markor:id/fab_add_new_item").exists() and not self.device(text="Settings").exists() and not self.device(text="Date").exists() and not self.device(resourceId="net.gsantner.markor:id/action_rename_selected_item").exists()
        )
    @rule()
    def create_file_with_same_name_should_not_overwrite(self):
        file_count = self.device(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title").count
        print("file count: "+str(file_count))
        if file_count == 0:
            print("no file ")
            return
        file_index = random.randint(0, file_count - 1)
        selected_file = self.device(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title")[file_index]
        file_name = selected_file.info['text']
        file_name_suffix = file_name.split(".")[-1]
        file_name_prefix = file_name.split(".")[0]
        if "." not in file_name or ".." in file_name:
            print("not a file")
            return
        print("file name: "+str(file_name))
        selected_file.click()
        time.sleep(1)
        original_content = self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").get_text()
        print("original content: "+str(original_content))
        self.device.press("back")
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/fab_add_new_item").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/new_file_dialog__name").set_text(file_name_prefix)
        self.device(resourceId="net.gsantner.markor:id/new_file_dialog__ext").set_text("."+file_name_suffix)
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        new_content = self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").get_text()
        print("new content: "+str(new_content))
        assert original_content == new_content, "create file with same name should not overwrite"
        
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
    apk_path="./apk/markor/2.11.1.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/new/1",
    explore_event_count=500,
    diverse_event_count=500,
    policy_name="random",
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
