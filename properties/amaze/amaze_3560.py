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

    @precondition(lambda self: self.device(resourceId="com.amaze.filemanager:id/sd_main_fab").exists() and self.device(description="More options").exists() and self.device(resourceId="com.amaze.filemanager:id/firstline").count < 7 and not self.device(resourceId="com.amaze.filemanager:id/donate").exists())
    @rule()
    def action_create_folder(self):
        print("time: " + str(time.time() - start_time))
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
        assert self.device(resourceId="com.amaze.filemanager:id/firstline",text=folder_name).exists(), "create folder failed with folder_name: " + folder_name

    # bug #3560  
    @precondition(lambda self: self.device(resourceId="com.amaze.filemanager:id/firstline").exists() and self.device(text="Folders").exists() and self.device(resourceId="com.amaze.filemanager:id/sd_main_fab").exists() and not self.device(resourceId="com.amaze.filemanager:id/donate").exists() and not self.device(resourceId="com.amaze.filemanager:id/check_icon").exists() and not self.device(text="Type to search…").exists())
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
    apk_path="./apk/amaze-3.8.4.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/3560/1",
    explore_event_count=500,
    diverse_event_count=500,
    policy_name="random",
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
