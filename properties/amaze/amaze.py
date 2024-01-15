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
        self.device(description="Navigate up").click()
        time.sleep(1)
        self.device(scrollable=True).scroll(steps=10)
        time.sleep(1)
        self.device(text="Settings").click()
        time.sleep(1)
        self.device(text="Interface").click()
        time.sleep(2)
        self.device(text="Back navigation").right(className="android.widget.Switch").click()
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")


    @precondition(lambda self: self.device(resourceId="com.amaze.filemanager:id/sd_main_fab").exists() and self.device(description="More options").exists() and self.device(resourceId="com.amaze.filemanager:id/firstline").count < 7 and not self.device(resourceId="com.amaze.filemanager:id/donate").exists() and not self.device(resourceId="com.amaze.filemanager:id/check_icon").exists())
    @rule()
    def action_create_folder(self):
        self.device(resourceId="com.amaze.filemanager:id/sd_main_fab").click()
        time.sleep(1)
        self.device(text="Folder").click()
        time.sleep(1)
        folder_name = st.text(alphabet=string.printable,min_size=1, max_size=5).example()
        print("folder_name: " + folder_name)
        self.device(resourceId="com.amaze.filemanager:id/singleedittext_input").set_text(folder_name)
        time.sleep(1)
        self.device(text="CREATE").click()
        time.sleep(1)
        assert self.device(resourceId="com.amaze.filemanager:id/listView").child_by_text(folder_name, allow_scroll_search=True).exists(), "create folder failed with folder_name: " + folder_name

    # bug #3560  
    @precondition(lambda self: self.device(resourceId="com.amaze.filemanager:id/firstline").exists() and self.device(text="Folders").exists() and self.device(resourceId="com.amaze.filemanager:id/sd_main_fab").exists() and not self.device(resourceId="com.amaze.filemanager:id/donate").exists() and not self.device(resourceId="com.amaze.filemanager:id/check_icon").exists() and not self.device(text="Type to search…").exists() and not self.device(text="Cloud Connection").exists())
    @rule()
    def rule_open_folder(self):
        print("time: " + str(time.time() - start_time))
        count = self.device(resourceId="com.amaze.filemanager:id/firstline").count
        print("count: "+str(count))
        index = random.randint(0, count-1)
        print("index: "+str(index))
        selected_file = self.device(resourceId="com.amaze.filemanager:id/firstline")[index]
        selected_file_name = selected_file.get_text()
        print("selected file or dir name: "+str(selected_file_name))
        if selected_file_name == "..":
            print("not a folder")
            return
        selected_file.right(resourceId="com.amaze.filemanager:id/properties").click()
        time.sleep(1)
        if self.device(text="Open with").exists():
            print("its a file, not a folder")
            return
        self.device.press("back")
        time.sleep(1)
        selected_file.click()
        time.sleep(1)
        full_path = self.device(resourceId="com.amaze.filemanager:id/fullpath").get_text()
        print("full path: "+str(full_path))     
        assert selected_file_name in full_path
        self.device.press("back")

    # bug #2910
    @precondition(lambda self: self.device(resourceId="com.amaze.filemanager:id/action_mode_close_button").exists() and self.device(resourceId="com.amaze.filemanager:id/check_icon").exists() and self.device(resourceId="com.amaze.filemanager:id/cpy").exists())
    @rule()
    def rotate_should_persist_selected_item(self):
        print("time: " + str(time.time() - start_time))
        self.device.set_orientation('l')
        time.sleep(1)
        self.device.set_orientation('n')
        time.sleep(1)
        assert self.device(resourceId="com.amaze.filemanager:id/check_icon").exists(), "rotate_should_persist_selected_item failed"

    # bug #2687
    @precondition(lambda self: self.device(resourceId="com.amaze.filemanager:id/firstline").exists() and self.device(resourceId="com.amaze.filemanager:id/sd_main_fab").exists() and not self.device(resourceId="com.amaze.filemanager:id/donate").exists() and not self.device(resourceId="com.amaze.filemanager:id/check_icon").exists() and not self.device(text="Cloud Connection").exists())
    @rule()
    def rule_hide_unhide_file(self):
        print("time: " + str(time.time() - start_time))
        # 先去hide 一个文件或者文件夹
        count = self.device(resourceId="com.amaze.filemanager:id/firstline").count
        print("count: "+str(count))
        index = random.randint(0, count-1)
        print("index: "+str(index))
        selected_file = self.device(resourceId="com.amaze.filemanager:id/firstline")[index]
        selected_file_name = selected_file.get_text()
        print("selected file name: "+str(selected_file_name))
        selected_file.long_click()
        time.sleep(1)
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Hide").click()
        time.sleep(1)
        assert not self.device(text=selected_file_name).exists()
        time.sleep(1)
        # 再去unhide 一个文件或者文件夹
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Hidden Files").click()
        time.sleep(1)
        self.device(text=selected_file_name).right(resourceId="com.amaze.filemanager:id/delete_button").click()
        time.sleep(1)
        self.device(text="CLOSE").click()
        time.sleep(1)
        assert self.device(resourceId="com.amaze.filemanager:id/listView").child_by_text(selected_file_name, allow_scroll_search=True).exists(), "unhide file failed with file name: " + str(selected_file_name)

    # bug #2518
    @precondition(lambda self: self.device(text="App Manager").exists() and self.device(description="More options").exists())
    @rule()
    def click_exist_button_should_work(self):
        print("time: " + str(time.time() - start_time))
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Exit").click()
        time.sleep(1)
        assert not self.device(text="App Manager").exists()
    
    # bug #2498
    @precondition(lambda self: self.device(text="App Manager").exists() and self.device(description="More options").exists())
    @rule()
    def click_sort_should_work(self):
        print("time: " + str(time.time() - start_time))
        self.device(resourceId="com.amaze.filemanager:id/sort").click()
        time.sleep(1)
        assert self.device(text="Sort By").exists()

    # bug #2477
    @precondition(lambda self: self.device(text="Color").exists() and self.device(text="Customize").exists())
    @rule()
    def back_should_not_go_to_main_setting(self):
        print("time: " + str(time.time() - start_time))
        self.device.press.back()
        time.sleep(1)
        assert not self.device(text="Settings").exists()

    # bug #2128
    @precondition(lambda self:  self.device(text="Amaze").exists() and self.device(resourceId="com.amaze.filemanager:id/fullpath").exists() and not self.device(resourceId="com.amaze.filemanager:id/item_count").exists() and self.device(resourceId="com.amaze.filemanager:id/search").exists() and not self.device(resourceId="com.amaze.filemanager:id/donate").exists() and not self.device(resourceId="com.amaze.filemanager:id/sd_label").exists())
    @rule()
    def rule_FAB_should_appear(self):
        print("time: " + str(time.time() - start_time))
        assert self.device(resourceId="com.amaze.filemanager:id/sd_main_fab").exists(), "FAB should appear"
        self.device(resourceId="com.amaze.filemanager:id/sd_main_fab").click()
        time.sleep(1)
        assert self.device(resourceId="com.amaze.filemanager:id/sd_label").exists()

    # bug #2113_1556
    @precondition(lambda self: self.device(resourceId="com.amaze.filemanager:id/firstline").exists() and self.device(resourceId="com.amaze.filemanager:id/sd_main_fab").exists() and not self.device(resourceId="com.amaze.filemanager:id/donate").exists() and not self.device(text="Cloud Connection").exists() and not self.device(resourceId="com.amaze.filemanager:id/check_icon").exists())
    @rule()
    def rule_rename(self):
        print("time: " + str(time.time() - start_time))
        count = self.device(resourceId="com.amaze.filemanager:id/firstline").count
        print("count: "+str(count))
        index = random.randint(0, count-1)
        print("index: "+str(index))
        selected_file = self.device(resourceId="com.amaze.filemanager:id/firstline")[index]
        selected_file_name = selected_file.get_text()
        print("selected file name: "+str(selected_file_name))
        selected_file.right(resourceId="com.amaze.filemanager:id/properties").click()
        time.sleep(1)
        self.device(text="Rename").click()
        time.sleep(1)
        new_file_name = st.text(alphabet=string.printable,min_size=1, max_size=5).example()
        print("new file name: "+str(new_file_name))
        self.device(resourceId="com.amaze.filemanager:id/singleedittext_input").set_text(new_file_name)
        time.sleep(1)
        self.device(text="SAVE").click()
        time.sleep(1)
        assert self.device(resourceId="com.amaze.filemanager:id/listView").child_by_text(new_file_name, allow_scroll_search=True).exists(), "rename failed with new_file_name: " + new_file_name

    # bug #1872
    @precondition(lambda self: self.device(text="Folders").exists() and self.device(resourceId="com.amaze.filemanager:id/search").exists() and not self.device(text="Internal Storage").exists())
    @rule()
    def search_folder_should_be_opened(self):
        print("time: " + str(time.time() - start_time))
        # 先随机选择一个folder
        folder_count = self.device(resourceId="com.amaze.filemanager:id/firstline").count
        print("folder count: "+str(folder_count))
        folder_index = random.randint(0, folder_count-1)
        print("folder index: "+str(folder_index))
        folder = self.device(resourceId="com.amaze.filemanager:id/firstline")[folder_index]
        folder_name = folder.get_text()
        print("folder: "+str(folder_name))
        if "." in folder_name:
            print("may not be a folder ")
            return
        # 再去搜索这个folder
        self.device(resourceId="com.amaze.filemanager:id/search").click()
        time.sleep(1)
        self.device(resourceId="com.amaze.filemanager:id/search_edit_text").set_text(folder_name)
        time.sleep(1)
        self.device.set_fastinput_ime(False) # 切换成正常的输入法
        self.device.send_action("search") # 模拟输入法的搜索
        time.sleep(1)
        self.device.set_fastinput_ime(True)
        time.sleep(1)
        assert self.device(text=folder_name).exists(), "search folder failed with folder name: "+str(folder_name)
        self.device(text=folder_name).click()
        time.sleep(1)
        assert not self.device(text="Open As").exists(), "open folder failed with folder name: "+str(folder_name)

    # bug #1834
    @precondition(lambda self: self.device(textContains=".zip").exists() and not self.device(text="Internal Storage").exists() and not self.device(resourceId="com.amaze.filemanager:id/donate").exists() and not self.device(text="Cloud Connection").exists() and not self.device(resourceId="com.amaze.filemanager:id/check_icon").exists())
    @rule()
    def extract_zip_file_shouldnot_need_password(self):
        print("time: " + str(time.time() - start_time))
        zip_file = self.device(textContains=".zip")
        folder_name = zip_file.get_text().split(".")[0]
        print("zip_file: "+str(zip_file.get_text()))
        zip_file.click()
        time.sleep(1)
        self.device(text="EXTRACT").click()
        time.sleep(1)
        assert self.device(resourceId="com.amaze.filemanager:id/listView").child_by_text(folder_name,allow_scroll_search=True,resourceId="com.amaze.filemanager:id/firstline").exists(), "extract zip file failed with zip file name: "+str(zip_file.get_text())

    # bug #1797
    @precondition(lambda self: self.device(text="Type to search…").exists() )
    @rule()
    def rule_search(self):
        print("time: " + str(time.time() - start_time))
        characters = st.text(alphabet=string.ascii_lowercase,min_size=1, max_size=2).example()
        print("characters: "+str(characters))
        self.device(text="Type to search…").set_text(characters)
        time.sleep(1)
        self.device.set_fastinput_ime(False)
        time.sleep(1)
        self.device.send_action("search")
        time.sleep(1)
        self.device.set_fastinput_ime(True)
        file_name = self.device(resourceId="com.amaze.filemanager:id/firstline")
        if file_name.count == 0:
            print("no file found")
            return
        selected_file = file_name[random.randint(0, file_name.count - 1)]
        selected_file_name = selected_file.get_text()
        print("selected file name: "+str(selected_file_name))
        assert characters in selected_file_name

    # bug #1499
    @precondition(lambda self: self.device(text="Go Back").exists() and self.device(resourceId="com.amaze.filemanager:id/second").exists() and self.device(resourceId="com.amaze.filemanager:id/fullpath").get_text() != "/storage/emulated/0" and not self.device(resourceId="com.amaze.filemanager:id/donate").exists() and not self.device(text="Cloud Connection").exists() and not self.device(resourceId="com.amaze.filemanager:id/check_icon").exists() and not self.device(resourceId="com.amaze.filemanager:id/search_edit_text").exists())
    @rule()
    def rule_go_back(self):
        print("time: " + str(time.time() - start_time))
        original_path = self.device(resourceId="com.amaze.filemanager:id/fullpath").get_text()
        print("original path: "+str(original_path))
        time.sleep(1)
        self.device(text="Go Back",resourceId="com.amaze.filemanager:id/date").click()
        time.sleep(1)
        after_path = self.device(resourceId="com.amaze.filemanager:id/fullpath").get_text()
        print("after path: "+str(after_path))
        expected_path = '/'.join(original_path.split("/")[:-1])
        print("expected path: "+str(expected_path))
        assert after_path == expected_path

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
    apk_path="./apk/amaze/amaze-3.8.4.apk",
    device_serial="emulator-5582",
    output_dir="output/amaze/new/15",
    explore_event_count=1000,
    diverse_event_count=1000,
    policy_name="random",
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
