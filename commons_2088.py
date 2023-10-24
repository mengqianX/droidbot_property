from main import *
import time
import sys


class Test(AndroidCheck):
    def __init__(
        self,
        apk_path,
        device_serial="emulator-5554",
        output_dir="output",
        explore_event_count=0,
        diverse_event_count=100,
        main_path_path=None,
        xml_path=None,
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
        self.device.swipe_ext("left")
        self.device.swipe_ext("left")
        self.device.swipe_ext("left")
        self.device.swipe_ext("left")
        self.device(text="YES!").click()
        self.device(resourceId="fr.free.nrw.commons:id/loginUsername").set_text("testecnu")
        
        self.device(resourceId="fr.free.nrw.commons:id/loginPassword").set_text("testagain")
        self.device(text="LOG IN").click()
        time.sleep(3)

    @precondition(
        lambda self: self.device(resourceId="fr.free.nrw.commons:id/categoryImageView").exists() and self.device(text="Explore").exists()
    )
    @rule()
    def rule1(self):
        self.device(resourceId="fr.free.nrw.commons:id/categoryImageView").click()
        self.device.swipe_ext("up")
        self.device.swipe_ext("up")
        self.device(resourceId="fr.free.nrw.commons:id/mediaDetailCategoryContainer").click()
        self.device(text="PARENT CATEGORIES").click()
        assert self.device(resourceId="fr.free.nrw.commons:id/textView1").exists()
        # self.device(resourceId="com.ichi2.anki:id/action_add_new_note_type").click()
        # self.device(resourceId="com.ichi2.anki:id/dropdown_deck_name").click()
        # time.sleep(2)
        # self.device(text="Add: Basic (and reversed card)").click()
        # self.device(text="OK").click()
        # note_name = self.device(className="android.widget.EditText").info['text']
        # self.device(text="OK").click()

        # assert self.device(text=note_name).exists()


start_time = time.time()

args = sys.argv[1:]
apk_path = args[0]
device_serial = args[1]
output_dir = args[2]
xml_path = args[3]
main_path_path = args[4]
source_activity = args[5]
target_activity = args[6]
policy_name = args[7]
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
    apk_path=apk_path,
    device_serial=device_serial,
    output_dir=output_dir,
    explore_event_count=2000,
    diverse_event_count=2000,
    xml_path=xml_path,
    main_path_path=main_path_path,
    source_activity=source_activity,
    target_activity=target_activity,
    policy_name=policy_name,
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
