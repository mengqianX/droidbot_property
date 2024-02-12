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
        policy_name="pbt",
        timeout=-1,
        build_model_timeout=-1,
        number_of_events_that_restart_app=100,
    ):
        super().__init__(
            apk_path,
            device_serial=device_serial,
            output_dir=output_dir,
            policy_name=policy_name,
            timeout=timeout,
            build_model_timeout=build_model_timeout,
            number_of_events_that_restart_app=number_of_events_that_restart_app,
        )
    @initialize()
    def set_up(self):
        if self.device(text="ALLOW").exists():
            self.device(text="ALLOW").click()
            time.sleep(1)
        elif self.device(text="Allow").exists():
            self.device(text="Allow").click()
            time.sleep(1)
            
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
    apk_path="./apk/amaze/amaze-3.4.3.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/1872/random_100/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
