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
        explore_event_count=5000,
        diverse_event_count=5000,
        main_path_path=None,
        xml_path="None",
        source_activity=None,
        target_activity=None,
        policy_name="pbt",
        timeout=-1,
        build_model_timeout=-1
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
            timeout=timeout,
            build_model_timeout=build_model_timeout
        )

    @precondition(lambda self: self.device(text="Type to search…").exists())
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
        assert characters in selected_file_name, "characters: " + characters + " selected_file_name: " + selected_file_name

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
    apk_path="./apk/amaze-3.5.0.apk",
    device_serial="emulator-5554",
    output_dir="output/amaze/1797/1",
    policy_name="random",
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
