import string
from main import *
import time
import sys
import re

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
            resourceId="net.gsantner.markor:id/fab_add_new_item"
        ).exists()
    )
    @rule()
    def rule_add_note(self):
        self.device(resourceId="net.gsantner.markor:id/fab_add_new_item").click()
        time.sleep(1)
        name = st.text(alphabet=string.ascii_letters,min_size=1, max_size=6).example()
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
        
    @precondition(lambda self: self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").exists() and self.device(resourceId="net.gsantner.markor:id/action_search").exists())
    @rule()
    def search_in_the_file(self):
        content = self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").info['text']
        time.sleep(1)
        words = content.split(" ")
        search_word = random.choice(words)
        print("search word: "+str(search_word))
        self.device(resourceId="net.gsantner.markor:id/action_search").click()
        time.sleep(1)
        self.device(text="Search").set_text(search_word)
        time.sleep(1)
        search_result = self.device(resourceId="android:id/text1")
        search_result_count = search_result.count
        print("search result count: "+str(search_result_count))
        assert search_result_count > 0
        search_result_text = search_result.info['text']
        assert search_word in str(search_result_text)

    @precondition(
        lambda self: self.device(
            resourceId="net.gsantner.markor:id/fab_add_new_item"
        ).exists()
    )
    @rule()
    def rule_rename_file(self):
        file_count = self.device(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title").count
        print("file count: "+str(file_count))
        if file_count == 0:
            print("no file to rename")
            return
        file_index = random.randint(0, file_count - 1)
        selected_file = self.device(resourceId="net.gsantner.markor:id/opoc_filesystem_item__title")[file_index]
        file_name = selected_file.info['text']
        file_name_suffix = file_name.split(".")[-1]
        print("file name: "+str(file_name))
        selected_file.long_click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/action_rename_selected_item").click()
        time.sleep(1)
        name = st.text(alphabet=string.ascii_letters,min_size=1, max_size=6).example()
        new_name  = name+"."+file_name_suffix
        print("new file name: "+str(new_name))
        self.device(resourceId="net.gsantner.markor:id/new_name").set_text(new_name)
        time.sleep(1)
        self.device(text="OK").click()
        assert self.device(text=new_name).exists()



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
