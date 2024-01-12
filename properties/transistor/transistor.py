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
        self.device(text="Settings").click()
        time.sleep(1)
        self.device(scrollable=True).scroll.to(text="Edit Stations")
        time.sleep(1)
        self.device(text="Edit Stations").click()
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device(text="Add new station").click()
        time.sleep(1)
        station_name_prefix = ["bbc", "new", "swi","chn"]
        selected_station_name_prefix = random.choice(station_name_prefix)
        self.device(resourceId="org.y20k.transistor:id/search_src_text").set_text(selected_station_name_prefix)
        time.sleep(3)
        random_selected_station = random.choice(self.device(resourceId="org.y20k.transistor:id/station_name"))
        random_selected_station.click()
        time.sleep(1)
        self.device(text="Add").click()

    # bug 9
    @precondition(
        lambda self: self.device(text="Add new station").exists and self.device(resourceId="org.y20k.transistor:id/station_name").count < 3
    )
    @rule()
    def add_station(self):
        self.device(text="Add new station").click()
        time.sleep(1)
        station_name_prefix = ["bbc", "new", "swi","chn"]
        selected_station_name_prefix = random.choice(station_name_prefix)
        self.device(resourceId="org.y20k.transistor:id/search_src_text").set_text(selected_station_name_prefix)
        time.sleep(3)
        random_selected_station = random.choice(self.device(resourceId="org.y20k.transistor:id/station_name"))
        random_selected_station.click()
        time.sleep(1)
        self.device(text="Add").click()


    # bug 239
    @precondition(
        lambda self: self.device(resourceId="org.y20k.transistor:id/station_name").exists() and not self.device(text="Find Station").exists()
    )
    @rule()
    def delete_should_work(self):
        station_count = int(self.device(resourceId="org.y20k.transistor:id/station_name").count)
        print("station_count: " + str(station_count))
        random_index = random.randint(0, station_count - 1)
        selected_station = self.device(resourceId="org.y20k.transistor:id/station_name")[random_index]
        station_name = selected_station.get_text()
        print("station_name: " + station_name)
        selected_station.swipe("left")
        time.sleep(1)
        delete_message = self.device(resourceId="android:id/message").get_text()
        print("delete_message: " + delete_message)
        self.device(text="Remove").click()
        time.sleep(1)
        new_station_count = int(self.device(resourceId="org.y20k.transistor:id/station_name").count)
        print("new_station_count: " + str(new_station_count))
        assert station_count - 1 == new_station_count, "delete does not work"
        assert not self.device(text=station_name).exists(), "delete station still exists"

    # bug 363
    @precondition(
        lambda self: self.device(resourceId="org.y20k.transistor:id/station_card").exists() and self.device(resourceId="org.y20k.transistor:id/station_card").count > 1 and self.device(resourceId="org.y20k.transistor:id/player_play_button").exists()
    )
    @rule()
    def notification_button_should_work(self):
        station_name = self.device(resourceId="org.y20k.transistor:id/player_station_name").get_text()
        print("station_name: " + station_name)
        self.device(resourceId="org.y20k.transistor:id/player_play_button").click()
        time.sleep(2)
        self.device.open_notification()
        time.sleep(1)
        self.device(resourceId="android:id/action0")[2].click()
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        new_station_name = self.device(resourceId="org.y20k.transistor:id/player_station_name").get_text()
        print("new_station_name: " + new_station_name)
        assert station_name != new_station_name, "notification next button does not work"

    #bug 234
    @precondition(
        lambda self: self.device(resourceId="org.y20k.transistor:id/station_card").exists()
    )
    @rule()
    def rename_station_should_work(self):
        station_count = int(self.device(resourceId="org.y20k.transistor:id/station_name").count)
        print("station_count: " + str(station_count))
        random_selected_station = random.choice(self.device(resourceId="org.y20k.transistor:id/station_name"))
        station_name = random_selected_station.get_text()
        print("random_selected_station: " + str(station_name))
        random_selected_station.long_click()
        time.sleep(1)
        new_name = st.text(alphabet=string.ascii_lowercase,min_size=1, max_size=6).example()
        print("new_name: " + new_name)
        self.device(resourceId="org.y20k.transistor:id/edit_station_name").set_text(new_name)
        time.sleep(1)
        self.device(text="Save Changes").click()
        time.sleep(2)
        assert self.device(text=new_name).exists(), "NEW NAME DOES NOT EXIST"
        assert not self.device(text=station_name).exists(), "OLD NAME STILL EXISTS"
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
    apk_path="./apk/transistor/4.1.7.apk",
    device_serial="emulator-5554",
    output_dir="output/transistor/new/1",
    explore_event_count=500,
    diverse_event_count=500,
    policy_name="random",
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
