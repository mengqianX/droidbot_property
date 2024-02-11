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
        self.device(resourceId="net.gsantner.markor:id/next").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/next").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/next").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/next").click()
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/next").click()
        time.sleep(1)
        self.device(text="DONE").click()
        time.sleep(1)
        
        if self.device(text="OK").exists():
            self.device(text="OK").click()
        # time.sleep(1)
        # self.device(resourceId="net.gsantner.markor:id/action_sort").click()
        # time.sleep(1)
        # self.device(text="Date").click()
        # time.sleep(1)
        # self.device(resourceId="net.gsantner.markor:id/action_sort").click()
        # time.sleep(1)
        # self.device(text="Reverse order").click()
        # time.sleep(1)
        # self.device(resourceId="net.gsantner.markor:id/action_sort").click()
        # time.sleep(1)
        # self.device(text="Folder first").click()
        
    
    # bug #1961
    @precondition(lambda self: self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").exists() and self.device(resourceId="net.gsantner.markor:id/action_search").exists())
    @rule()
    def search_in_the_file(self):
        content = self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").info['text']
        if content is None:
            random_text = st.text(alphabet=string.printable,min_size=1, max_size=10).example()
            print("random text: "+str(random_text))
            self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").set_text(random_text)
            content = self.device(resourceId="net.gsantner.markor:id/document__fragment__edit__highlighting_editor").info['text']
        time.sleep(1)
        words = content.split("")
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
        print("search result text: "+str(search_result_text))
        assert search_word in str(search_result_text)


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
    apk_path="./apk/markor/2.10.2.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/1961/1",
    policy_name="random",
    timeout=7200,
    number_of_events_that_restart_app = 100
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
