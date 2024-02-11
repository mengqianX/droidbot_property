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
        policy_name="pbt",
        timeout=-1,
        build_model_timeout=-1,
        number_of_events_that_restart_app=100,
    ):
        super().__init__(
            apk_path,
            device_serial=device_serial,
            output_dir=output_dir,
            policy_name=policy_name,
            timeout=timeout,
            build_model_timeout=build_model_timeout,
            number_of_events_that_restart_app=number_of_events_that_restart_app,
        )

    @initialize()
    def set_up(self):
        self.device.set_fastinput_ime(True)
        self.device(text="Not now").click()
        time.sleep(1)
        # 创建一个新的Note
        self.device(resourceId="it.feio.android.omninotes:id/menu_add").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/detail_title").set_text("test")
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/detail_content").set_text("#bb")
        time.sleep(1)
        # lock
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Mask").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/password").set_text("1")
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/password_check").set_text("1")
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/question").set_text("1")
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/answer").set_text("1")
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/answer_check").set_text("1")
        time.sleep(1)
        self.device(text="Confirm").click()
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")

    @precondition(lambda self: self.device(resourceId="it.feio.android.omninotes:id/menu_attachment").exists())
    @rule()
    def remove_password_should_not_affect_notes(self):
        print("time: " + str(time.time() - start_time))
        note_title = st.text(alphabet=string.ascii_letters,min_size=1, max_size=10).example()
        print("title: " + note_title)
        self.device(resourceId="it.feio.android.omninotes:id/detail_title").set_text(note_title)
        time.sleep(1)
        content = st.text(alphabet=string.ascii_letters,min_size=1, max_size=10).example()
        print("content: " + content)
        self.device(resourceId="it.feio.android.omninotes:id/detail_content").set_text(content)
        time.sleep(1)
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Mask").click()
        time.sleep(1)
        if self.device(resourceId="it.feio.android.omninotes:id/password").exists():
            self.device(resourceId="it.feio.android.omninotes:id/password").set_text("1")
            time.sleep(1)
            self.device(resourceId="it.feio.android.omninotes:id/password_check").set_text("1")
            time.sleep(1)
            self.device(resourceId="it.feio.android.omninotes:id/question").set_text("1")
            time.sleep(1)
            self.device(resourceId="it.feio.android.omninotes:id/answer").set_text("1")
            time.sleep(1)
            self.device(resourceId="it.feio.android.omninotes:id/answer_check").set_text("1")
            time.sleep(1)
            self.device(text="Confirm").click()
            time.sleep(2)
            self.device.press("back")
            time.sleep(1)
            self.device.press("back")
        else:
            self.device(resourceId="it.feio.android.omninotes:id/password_request").set_text("1")
            time.sleep(1)
            self.device(text="Confirm").click()
        time.sleep(2)
        self.device.press("back")

        time.sleep(1)
        self.device(text="Notes").click()
        time.sleep(1)
        self.device(text="SETTINGS").click()
        time.sleep(1)
        self.device(text="Data").click()
        time.sleep(1)
        self.device(text="Password").click()
        time.sleep(1)
        self.device(text="Confirm").click()
        time.sleep(1)
        if not self.device(text="Insert password").exists():
            print("password is not set, return")
            return 
        self.device(resourceId="it.feio.android.omninotes:id/password_request").set_text("1")
        time.sleep(1)
        self.device(text="Confirm").click()
        time.sleep(1)
        self.device(text="Confirm").click()
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        assert self.device(text=note_title).exists()," note title should exists the same as before "+note_title
        assert self.device(text=content).exists()," note content should exists the same as before "+content

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
    apk_path="./apk/omninotes/OmniNotes-4.7.2.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/104/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
