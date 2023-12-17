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
        self.add_file_names = []
    @initialize()
    def set_up(self):
        self.device(description="More options").click()
        time.sleep(1)
        self.device(resourceId="com.amaze.filemanager:id/submenuarrow").click()
        time.sleep(1)
        self.device(text="Directory Sort Mode").click()
        time.sleep(1)
        self.device(text="None On Top").click()
        time.sleep(1)
        self.device(description="More options").click()
        time.sleep(1)
        self.device(resourceId="com.amaze.filemanager:id/submenuarrow").click()
        time.sleep(1)
        self.device(text="Sort By").click()
        time.sleep(1)
        self.device(text="Last Modified").click()
        time.sleep(1)
        self.device(text="DESCENDING").click()
        return

    @precondition(lambda self: self.device(resourceId="com.amaze.filemanager:id/sd_main_fab").exists() and self.device(resourceId="com.amaze.filemanager:id/search").exists() and not self.device(resourceId="com.amaze.filemanager:id/instagram").exists())
    @rule()
    def add_file(self):
        self.device(resourceId="com.amaze.filemanager:id/sd_main_fab").click()
        time.sleep(1)
        self.device(text="File").click()
        time.sleep(1)
        file_name = st.text(alphabet=string.ascii_lowercase,min_size=1, max_size=6).example()+".txt"
        print("file name: "+str(file_name))

        self.device(resourceId="com.amaze.filemanager:id/singleedittext_input").set_text(file_name)
        time.sleep(1)
        self.device(text="CREATE").click()
        time.sleep(1)
        self.add_file_names.append(file_name)
        assert self.device(text=file_name).exists()

    @precondition(lambda self: self.device(text="Type to search…").exists())
    @rule()
    def rule_search(self):
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
        assert characters in selected_file_name

    @precondition(lambda self: self.device(resourceId="com.amaze.filemanager:id/firstline").exists() and self.device(resourceId="com.amaze.filemanager:id/sd_main_fab").exists() and not self.device(resourceId="com.amaze.filemanager:id/donate").exists())
    @rule()
    def rule_rename(self):
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
        new_file_name = st.text(alphabet=string.ascii_letters,min_size=1, max_size=5).example()
        print("new file name: "+str(new_file_name))
        self.device(resourceId="com.amaze.filemanager:id/singleedittext_input").set_text(new_file_name)
        time.sleep(1)
        self.device(text="SAVE").click()
        time.sleep(1)
        assert self.device(text=new_file_name).exists()

    @precondition(lambda self: self.device(textContains=".zip").exists() and not self.device(text="Exit").exists() and not self.device(resourceId="com.amaze.filemanager:id/donate").exists())
    @rule()
    def rule_extract_zip(self):
        zip_count = int(self.device(textContains=".zip").count)
        print("zip count: "+str(zip_count))
        index = random.randint(0, zip_count - 1)
        selected_zip = self.device(textContains=".zip")[index]
        print("selected zip: "+str(selected_zip.get_text()))
        file_name = str(selected_zip.get_text()).rsplit(".zip")[0]
        print("file name: "+str(file_name))
        selected_zip.click()
        time.sleep(1)
        self.device(text="EXTRACT").click()
        time.sleep(1)
        assert self.device(text=file_name).exists()

    @precondition(lambda self: self.device(resourceId="com.amaze.filemanager:id/firstline").exists() and self.device(text="Folders").exists() and self.device(resourceId="com.amaze.filemanager:id/sd_main_fab").exists() and not self.device(resourceId="com.amaze.filemanager:id/donate").exists())
    @rule()
    def rule_open_folder(self):
        count = self.device(resourceId="com.amaze.filemanager:id/firstline").count
        print("count: "+str(count))
        index = random.randint(0, count-1)
        print("index: "+str(index))
        selected_file = self.device(resourceId="com.amaze.filemanager:id/firstline")[index]
        selected_file_name = selected_file.get_text()
        print("selected file or dir name: "+str(selected_file_name))
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

    @precondition(lambda self: self.device(resourceId="com.amaze.filemanager:id/firstline").exists() and self.device(resourceId="com.amaze.filemanager:id/sd_main_fab").exists() and not self.device(resourceId="com.amaze.filemanager:id/donate").exists())
    @rule()
    def rule_hide_unhide_file(self):
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
        assert self.device(text=selected_file_name).exists()

    @precondition(lambda self: self.device(text="Recent files").exists()  and self.device(resourceId="com.amaze.filemanager:id/instagram").exists())
    @rule()
    def rule_recent_file(self):
        self.device(text="Recent files").click()
        time.sleep(1)
        recent_added_file = self.add_file_names[-1]
        print("recent added file: "+str(recent_added_file))
        assert self.device(text=recent_added_file).exists()

    @precondition(lambda self: self.device(resourceId="com.amaze.filemanager:id/pathname").exists() and not self.device(resourceId="com.amaze.filemanager:id/instagram").exists())
    @rule()
    def rule_file_folder_count(self):
        file_folder_txt = self.device(resourceId="com.amaze.filemanager:id/pathname").get_text() 
        print("file folder text: "+str(file_folder_txt))
        file_folder_count = int(file_folder_txt.split(" ")[0])+int(file_folder_txt.split(" ")[3])
        print("file folder count: "+str(file_folder_count))
        # 当前页面统计出来的文件夹和文件的数量
        current_file_folder_count = int(self.device(resourceId="com.amaze.filemanager:id/firstline").count)
        print("current file folder count: "+str(current_file_folder_count))
        assert file_folder_count >= current_file_folder_count
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
    explore_event_count=1000,
    diverse_event_count=1000,
    xml_path=xml_path,
    main_path_path=main_path_path,
    source_activity=source_activity,
    target_activity=target_activity,
    policy_name=policy_name,
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
