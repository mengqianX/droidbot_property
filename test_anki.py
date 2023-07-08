from main import *
import time

reach_time_list = []


class Test(AndroidCheck):
    def __init__(
        self,
        apk_path,
        event_count=100,
    ):
        super().__init__(apk_path, event_count=event_count)

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
t = Test(apk_path=".\\apk\\AnkiDroid-2.15.2.apk", event_count=300)
t.start()
for item in reach_time_list:
    print(item)
