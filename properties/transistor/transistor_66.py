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
        pass

    @precondition(
        lambda self: self.device(resourceId="org.y20k.transistor:id/list_item_more_button").exists()
    )
    @rule()
    def rename_station_should_work(self):
        original_station_count = int(self.device(resourceId="org.y20k.transistor:id/list_item_textview").count)
        print("original_station_count: " + str(original_station_count))
        self.device(resourceId="org.y20k.transistor:id/list_item_more_button").click()
        time.sleep(1)
        self.device(text="Rename").click()
        time.sleep(1)
        original_name = self.device(resourceId="org.y20k.transistor:id/dialog_rename_station_input").get_text()
        print("original_name: " + original_name)
        new_name = st.text(alphabet=string.ascii_lowercase,min_size=1, max_size=6).example()
        print("new_name: " + new_name)
        self.device(resourceId="org.y20k.transistor:id/dialog_rename_station_input").set_text(new_name)
        time.sleep(1)
        self.device(text="RENAME").click()

        assert self.device(text=new_name).exists(), "NEW NAME DOES NOT EXIST"
        assert not self.device(text=original_name).exists(), "OLD NAME STILL EXISTS"
        new_station_count = int(self.device(resourceId="org.y20k.transistor:id/list_item_textview").count)
        print("new_station_count: " + str(new_station_count))
        assert original_station_count == new_station_count, "station count changed"

        



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
    apk_path="./apk/transistor/1.2.4.apk",
    device_serial="emulator-5554",
    output_dir="output/transistor/66/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
