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
        self.device(description="Open menu").click()
        time.sleep(1)
        self.device(resourceId="de.danoeh.antennapod:id/txtvTitle", text="Add podcast").click()
        time.sleep(1)
        self.device(resourceId="de.danoeh.antennapod:id/discover_error_retry_btn").click()
        time.sleep(1)
        self.device(resourceId="de.danoeh.antennapod:id/discovery_cover", description="Morrison Mysteries - NBC News").click()
        time.sleep(1)
        self.device(resourceId="de.danoeh.antennapod:id/subscribeButton").click()
        time.sleep(1)
        self.device.xpath('//*[@resource-id="de.danoeh.antennapod:id/recyclerView"]/android.widget.FrameLayout[1]/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.ImageView[1]').click()
        time.sleep(10)
        self.device(resourceId="com.android.systemui:id/back").click()

    @precondition(
        lambda self: self.device(resourceId="de.danoeh.antennapod:id/action_favorites").exists()
    )
    @rule()
    def rule1(self):
        child_count = int(self.device(resourceId="de.danoeh.antennapod:id/recyclerView").info['childCount'])
        select_child = random.randint(0, child_count - 1)
        select_child_name = self.device(resourceId="de.danoeh.antennapod:id/container")[select_child].child(resourceId="de.danoeh.antennapod:id/txtvTitle").info['text']
        self.device(resourceId="de.danoeh.antennapod:id/container")[select_child].long_click()
        remove_or_add = True
        if self.device(text="Remove from queue").exists():
            self.device(text="Remove from queue").click()
        else:
            self.device(text="Add to queue").click()
            remove_or_add = False
        time.sleep(1)
        self.device(description="Open menu").click()
        self.device(text="Queue").click()
        time.sleep(1)
        if remove_or_add:
            assert not self.device(text=select_child_name).exists()
        else:
            assert self.device(text=select_child_name).exists()


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
