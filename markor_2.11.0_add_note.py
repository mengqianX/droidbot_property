import string
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
        self.device(resourceId="net.gsantner.markor:id/next").click()
        self.device(resourceId="net.gsantner.markor:id/next").click()
        self.device(resourceId="net.gsantner.markor:id/next").click()
        self.device(resourceId="net.gsantner.markor:id/next").click()
        time.sleep(1)
        self.device(text="DONE").click()
        time.sleep(1)
        
        if self.device(text="OK").exists():
            self.device(text="OK").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/action_sort").click()
        time.sleep(1)
        self.device(text="Date").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/action_sort").click()
        time.sleep(1)
        self.device(text="Reverse order").click()
        

    @precondition(
        lambda self: self.device(
            resourceId="net.gsantner.markor:id/new_file_dialog__name"
        ).exists()
    )
    @rule()
    def rule1(self):
        
        
        time.sleep(1)
        name = st.text(alphabet=string.printable,min_size=1, max_size=10).example()
        self.device(resourceId="net.gsantner.markor:id/new_file_dialog__name").set_text(
            name
        )
        time.sleep(1)
        print("file name: "+str(name))
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        content = st.text(min_size=1, max_size=10).example()
        self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").set_text(content)
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/action_save").click()
        self.device.press("back")
        if self.device(resourceId="net.gsantner.markor:id/action_save").exists():
            self.device.press("back")
        time.sleep(1)
        name = name+".md"
        assert self.device(text=name).exists()
        

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
