from main import *
import time

reach_time_list = []


class Test(AndroidCheck):
    def __init__(
        self,
        apk_path,
        device_serial="emulator-5554",
        output_dir="output",
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
            event_count=event_count,
            xml_path=xml_path,
            source_activity=source_activity,
            target_activity=target_activity,
            policy_name=policy_name,
        )

    @initialize()
    def set_up(self):
        self.click(text="OK")
        self.click(text="ALLOW")

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
        t = time.time()
        reach_time_list.append(t - start_time)

    @rule()
    def rule3(self):
        print("reach rule 3")


start_time = time.time()
t = Test(
    apk_path=".\\apk\\AnkiDroid-2.15.2.apk",
    device_serial="emulator-5554",
    output_dir=".\\output\\anki\\random4",
    event_count=1000,
    xml_path=".\\xml_graph\\Anki_CTG.xml",
    source_activity="DeckPicker",
    target_activity="Preferences",
    policy_name="random",
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
