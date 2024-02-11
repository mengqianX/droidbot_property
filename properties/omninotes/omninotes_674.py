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
        self.device(resourceId="it.feio.android.omninotes:id/next").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/next").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/next").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/next").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/next").click()
        time.sleep(1)
        self.device(resourceId="it.feio.android.omninotes:id/done").click()
        time.sleep(1)
        # # 打开设置-在navigation 中显示没有被分类的Notes
        # self.device(description="drawer open").click()
        # time.sleep(1)
        # self.device(text="SETTINGS").click()
        # time.sleep(1)
        # self.device(text="Navigation").click()
        # time.sleep(1)
        # self.device(text="Group not categorized").click()
        # time.sleep(1)
        # self.device(description="Navigate up").click()
        # time.sleep(1)
        # self.device(description="Navigate up").click()
        # time.sleep(1)
        # self.device.press("back")
        # time.sleep(1)
        # # 创建一个新的Note
        # self.device(resourceId="it.feio.android.omninotes:id/fab_expand_menu_button").click()
        # time.sleep(1)
        # self.device(text="Text note").click()
        # time.sleep(1)
        # self.device(resourceId="it.feio.android.omninotes:id/detail_title").set_text("test")
        # time.sleep(1)
        # self.device(resourceId="it.feio.android.omninotes:id/detail_content").set_text("#bb")
        # time.sleep(1)
        # # 添加新的category
        # self.device(resourceId="it.feio.android.omninotes:id/menu_category").click()
        # time.sleep(1)
        # self.device(resourceId="it.feio.android.omninotes:id/md_buttonDefaultPositive").click()
        # time.sleep(1)
        # category_name = st.text(alphabet=string.printable,min_size=1, max_size=10).example()
        # self.device(resourceId="it.feio.android.omninotes:id/category_title").set_text(category_name)
        # time.sleep(1)
        # self.device(text="OK").click()
        # self.device(description="drawer closed").click()
    
    
    @precondition(lambda self: self.device(text="Interface").exists() and self.device(text="Language").exists())
    @rule()
    def check_languge_selection(self):
        print("time: " + str(time.time() - start_time))
        self.device(text="Language").click()
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("العربية (Arabic)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "Arabic"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("Asturianu (Asturian)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "Asturian"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("Euskara (Basque)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "Basque"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("Català (Catalan)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "Catalan"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("中文 (Chinese Simplified)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "Chinese Simplified"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("臺灣話 (Chinese Traditional)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "Chinese Traditional"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("Hrvatski (Croatian)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "Croatian"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("Čeština (Czech)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "Czech"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("Nederlands (Dutch)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "Dutch"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("English (English)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "English"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("Suomi (Finnish)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "Finnish"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("Français (French)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "French"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("ភាសាខ្មែរ (Khmer)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "Khmer"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("Deutsch (German)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "German"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("Galego (Galician)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "Galician"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("ελληνικά (Greek)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "Greek"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("עברית (Hebrew)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "Hebrew"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("हिंदी (Hindi)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "Hindi"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("Magyar (Hungarian)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "Hungarian"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("Bahasa Indonesia (Indonesian)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "Indonesian"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("Italiano (Italian)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "Italian"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("日本語 (Japanese)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "Japanese"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("ສ​ປ​ປ​ລາວ (Lao)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "Lao"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("Latviešu valoda (Latvian)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "Latvian"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("Polszczyzna (Polish)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "Polish"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("Português (Portuguese Brazil)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "Portuguese Brazil"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("Português (Portuguese Portugal)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "Portuguese Portugal"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("Русский (Russian)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "Russian"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("Српски (Serbian Cyrillic)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "Serbian Cyrillic"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("Slovenčina (Slovak)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "Slovak"
        time.sleep(1)
        assert self.device(resourceId="android:id/select_dialog_listview").child_by_text("Slovenščina (Slovenian)",allow_scroll_search=True,className="android.widget.CheckedTextView").exists(), "Slovenian"
        time.sleep(1)
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
    apk_path="./apk/omninotes/OmniNotes-5.4.5.apk",
    device_serial="emulator-5554",
    output_dir="output/omninotes/674/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
