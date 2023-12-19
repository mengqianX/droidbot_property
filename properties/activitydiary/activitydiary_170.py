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


    @precondition(
        lambda self: self.device(text="Settings").exists() and self.device(text="Behavior").exists()
    )
    @rule()
    def import_an_backup_should_take_effect(self):
        # first backup
        self.device(scrollable=True).scroll.to(text="Export database")
        time.sleep(1)
        self.device(text="Export database").click()
        backup_title = st.text(alphabet=string.ascii_letters,min_size=1, max_size=5).example()
        print("backup title: " + backup_title)
        self.device(text="ActivityDiary_Export.sqlite3").set_text(backup_title)
        time.sleep(1)
        self.device(text="SAVE").click()
        time.sleep(1)
        self.device.press("back")
        # then delete an activity
        # random select an activity
        activity_count = self.device(resourceId="de.rampro.activitydiary:id/select_card_view").count
        random_index = random.randint(0, activity_count - 1)
        selected_activity = self.device(resourceId="de.rampro.activitydiary:id/select_card_view")[random_index]
        
        time.sleep(1)
        selected_activity.click()
        time.sleep(1)
        activity_name = selected_activity.child(resourceId="de.rampro.activitydiary:id/activity_name").get_text()
        print("activity name: " + activity_name)
        selected_activity.long_click()
        time.sleep(1)
        self.device(resourceId="de.rampro.activitydiary:id/action_edit_delete").click()
        time.sleep(1)
        # then import
        self.device(description="Open navigation").click()
        time.sleep(1)
        self.device(text="Settings").click()
        time.sleep(1)
        self.device(scrollable=True).scroll.to(text="Import database")
        time.sleep(1)
        self.device(text="Import database").click()
        time.sleep(1)
        self.device(text=backup_title).click()
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        assert self.device(text=activity_name).exists(), "activity not exist after import" + str(activity_name)
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
    apk_path="./apk/activitydiary/1.2.5.apk",
    device_serial="emulator-5554",
    output_dir="output/activitydiary/170/1",
    explore_event_count=500,
    diverse_event_count=500,
    policy_name="random",
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
