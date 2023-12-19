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
        lambda self: self.device(text="Activity Diary").exists() and self.device(resourceId="de.rampro.activitydiary:id/select_card_view").exists() and not self.device(text="Settings").exists()
    )
    @rule()
    def long_click_activity_should_edit_it(self):
        # random select an activity
        activity_count = self.device(resourceId="de.rampro.activitydiary:id/select_card_view").count
        random_index = random.randint(0, activity_count - 1)
        selected_activity = self.device(resourceId="de.rampro.activitydiary:id/select_card_view")[random_index]
        activity_name = selected_activity.child(resourceId="de.rampro.activitydiary:id/activity_name").get_text()
        print("activity name: " + activity_name)
        time.sleep(1)
        selected_activity.long_click()
        time.sleep(1)
        current_activity_name = self.device(resourceId="de.rampro.activitydiary:id/edit_activity_name").get_text()
        assert current_activity_name == activity_name, "activity name not match "+ str(activity_name) + " " + str(current_activity_name)
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
    output_dir="output/activitydiary/176/1",
    explore_event_count=500,
    diverse_event_count=500,
    policy_name="random",
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
