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
        self.add_file_names = []
    

    @precondition(lambda self: self.device(text="Recent files").exists()  and self.device(text="Internal Storage").exists() and len(self.add_file_names) > 0)
    @rule()
    def rule_recent_file(self):
        print("time: " + str(time.time() - start_time))
        self.device(text="Recent files").click()
        time.sleep(1)
        recent_added_file = self.add_file_names[-1]
        print("recent added file: "+str(recent_added_file))
        assert self.device(text=recent_added_file).exists()

    @precondition(lambda self: self.device(resourceId="com.amaze.filemanager:id/sd_main_fab").exists() and self.device(resourceId="com.amaze.filemanager:id/search").exists() and not self.device(resourceId="com.amaze.filemanager:id/instagram").exists())
    @rule()
    def add_file(self):
        print("time: " + str(time.time() - start_time))
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
    output_dir="output/amaze/1916/1",
    explore_event_count=500,
    diverse_event_count=500,
    policy_name="random",
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
