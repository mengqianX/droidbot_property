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

    @precondition(lambda self: self.device(text="Folders").exists() and self.device(resourceId="com.amaze.filemanager:id/search").exists() and not self.device(text="Internal Storage").exists())
    @rule()
    def search_folder_should_be_opened(self):
        print("time: " + str(time.time() - start_time))
        folder = self.device(text="Folders").down(resourceId="com.amaze.filemanager:id/firstline")
        print("folder: "+str(folder.get_text()))
        self.device(resourceId="com.amaze.filemanager:id/search").click()
        time.sleep(1)
        self.device(resourceId="com.amaze.filemanager:id/search_edit_text").set_text(folder.get_text())
        time.sleep(1)
        self.device.set_fastinput_ime(False) # 切换成正常的输入法
        self.device.send_action("search") # 模拟输入法的搜索
        time.sleep(1)
        self.device.set_fastinput_ime(True)
        time.sleep(1)
        assert self.device(text=folder.get_text()).exists(), "search folder failed with folder name: "+str(folder.get_text())
        folder.click()
        time.sleep(1)
        assert not self.device(text="Open As").exists(), "open folder failed with folder name: "+str(folder.get_text())


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
    apk_path="./apk/amaze-3.4.3.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/1872/1",
    explore_event_count=500,
    diverse_event_count=500,
    policy_name="random",
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
