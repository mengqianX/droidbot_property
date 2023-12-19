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

    # bug #253
    @precondition(
        lambda self: self.device(text="Activity Diary").exists() and not self.device(text="<No Activity>").exists() and self.device(description="Statistics").info["selected"] and not self.device(text="Settings").exists()
    )
    @rule()
    def click_content_should_enter_diary_entry(self):
        activity_name = self.device(resourceId="de.rampro.activitydiary:id/activity_name").get_text() 
        self.device(resourceId="de.rampro.activitydiary:id/duration_label").click()
        time.sleep(1)
        assert self.device(text="Diary entry").exists(), "not enter diary entry"
        time.sleep(1)
        current_activity_name = self.device(resourceId="de.rampro.activitydiary:id/activity_name").get_text()
        assert current_activity_name == activity_name, "activity name changed from "+ activity_name + " to " + current_activity_name

    # bug #176
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

    # bug #170
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

    # bug #118
    @precondition(
        lambda self: self.device(text="Diary").exists() and self.device(resourceId="de.rampro.activitydiary:id/picture").exists()
    )
    @rule()
    def delete_pics_should_work(self):
        pic_count = self.device(resourceId="de.rampro.activitydiary:id/picture").count
        print("pic count: " + str(pic_count))
        # random select a pic
        random_index = random.randint(0, pic_count - 1)
        selected_pic = self.device(resourceId="de.rampro.activitydiary:id/picture")[random_index]
        selected_pic_name = selected_pic.up(resourceId="de.rampro.activitydiary:id/activity_name").get_text()
        print("selected pic name: " + selected_pic_name)
        time.sleep(1)
        selected_pic.long_click()
        time.sleep(2)
        self.device(text="OK").click()
        time.sleep(1)
        after_pic_count = self.device(resourceId="de.rampro.activitydiary:id/picture").count 
        print("after pic count: " + str(after_pic_count))
        assert after_pic_count == pic_count - 1, "pic not deleted"
        for i in range(after_pic_count):
            pic_name = self.device(resourceId="de.rampro.activitydiary:id/picture")[i].up(resourceId="de.rampro.activitydiary:id/activity_name").get_text()
            assert pic_name != selected_pic_name, "pic not deleted "+pic_name+" "+selected_pic_name

    # bug #109
    @precondition(
        lambda self: self.device(text="New activity").exists() and self.device(resourceId="de.rampro.activitydiary:id/edit_activity_name").exists()
    )
    @rule()
    def new_activity_name(self):
        name = st.text(alphabet=string.digits + string.ascii_letters + string.punctuation,min_size=1, max_size=5).example()
        print(name)
        self.device(resourceId="de.rampro.activitydiary:id/edit_activity_name").set_text(name)
        time.sleep(1)
        if self.device(resourceId="de.rampro.activitydiary:id/textinput_error").exists():
            self.device(description="Navigate up").click()
            time.sleep(1)
            assert self.device(resourceId="de.rampro.activitydiary:id/activity_name",text=name).exists() , "activity name not exists"
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
    apk_path="./apk/activitydiary/1.4.2.apk",
    device_serial="emulator-5554",
    output_dir="output/activitydiary/new/1",
    explore_event_count=500,
    diverse_event_count=500,
    policy_name="random",
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
