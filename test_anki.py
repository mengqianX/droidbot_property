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
        event_count=100,
        xml_path=None,
        source_activity=None,
        target_activity=None,
        policy_name="dfs_greedy",
    ):
        super().__init__(
            apk_path,
            device_serial=device_serial,
            output_dir=output_dir,
            explore_event_count=explore_event_count,
            event_count=event_count,
            xml_path=xml_path,
            source_activity=source_activity,
            target_activity=target_activity,
            policy_name=policy_name,
        )

    @initialize()
    def set_up(self):
        pass
        # self.device(resourceId="net.gsantner.markor:id/next").click()
        # self.device(resourceId="net.gsantner.markor:id/next").click()
        # self.device(resourceId="net.gsantner.markor:id/next").click()
        # self.device(resourceId="net.gsantner.markor:id/next").click()
        # self.device(text="DONE").click()
        # self.device(text="OK").click()

    @precondition(
        lambda self: self.device.app_current()['activity'].split('.')[-1]
        == "DeckPicker"
    )
    @rule()
    def rule2(self):
        print("reach rule 2")
        print(
            "current activity: " + self.device.app_current()['activity'].split('.')[-1]
        )

    @rule()
    def rule3(self):
        print("reach rule 3")


start_time = time.time()

args = sys.argv[1:]
apk_path = args[0]
device_serial = args[1]
output_dir = args[2]
xml_path = args[3]
source_activity = args[4]
target_activity = args[5]
policy_name = args[6]
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
    explore_event_count=200,
    event_count=200,
    xml_path=xml_path,
    source_activity=source_activity,
    target_activity=target_activity,
    policy_name=policy_name,
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
