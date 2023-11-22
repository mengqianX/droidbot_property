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
        self.device.set_fastinput_ime(True)
        self.device(text="OK").click()
        time.sleep(1)
        self.device(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        content = st.text(alphabet=string.ascii_letters,min_size=1, max_size=10).example()
        self.device(resourceId="nl.mpcjanssen.simpletask:id/taskText").set_text(content)
        time.sleep(1)
        self.device(resourceId="nl.mpcjanssen.simpletask:id/btnProject").click()
        time.sleep(1)
        tag_name = st.text(alphabet=string.ascii_letters,min_size=1, max_size=6).example()
        print("tag name: "+str(tag_name))
        self.device(resourceId="nl.mpcjanssen.simpletask:id/new_item_text").set_text(tag_name)
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        self.device(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()

    @precondition(
        lambda self: int(self.device(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count) > 0 and not self.device(text="Quick filter").exists() and not self.device(text="Settings").exists() and not self.device(text="Saved filters").exists())
    @rule()
    def add_tag(self):
        task_count = int(self.device(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count)
        print("task count: "+str(task_count))
        selected_task = random.randint(0, task_count - 1)
        print("selected task: "+str(selected_task))
        selected_task = self.device(resourceId="nl.mpcjanssen.simpletask:id/tasktext")[selected_task]
        selected_task_name = selected_task.get_text()
        print("selected task name: "+str(selected_task_name))
        selected_task.click()
        time.sleep(1)
        self.device(resourceId="nl.mpcjanssen.simpletask:id/update").click()
        time.sleep(1)
        self.device(resourceId="nl.mpcjanssen.simpletask:id/btnProject").click()
        time.sleep(1)
        tag_name = st.text(alphabet=string.ascii_letters,min_size=1, max_size=6).example()
        print("tag name: "+str(tag_name))
        self.device(resourceId="nl.mpcjanssen.simpletask:id/new_item_text").set_text(tag_name)
        time.sleep(1)
        self.device(text="OK").click()
        content = self.device(resourceId="nl.mpcjanssen.simpletask:id/taskText").get_text()
        print("content: "+str(content))
        time.sleep(1)
        assert tag_name in content
    
    @precondition(
        lambda self: int(self.device(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count) > 0 and not self.device(text="Quick filter").exists() and not self.device(text="Settings").exists() and not self.device(text="Saved filters").exists())
    @rule()
    def add_list(self):
        task_count = int(self.device(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count)
        print("task count: "+str(task_count))
        selected_task = random.randint(0, task_count - 1)
        print("selected task: "+str(selected_task))
        selected_task = self.device(resourceId="nl.mpcjanssen.simpletask:id/tasktext")[selected_task]
        selected_task_name = selected_task.get_text()
        print("selected task name: "+str(selected_task_name))
        selected_task.click()
        self.device(resourceId="nl.mpcjanssen.simpletask:id/update").click()
        time.sleep(1)
        self.device(resourceId="nl.mpcjanssen.simpletask:id/btnContext").click()
        list_name = st.text(alphabet=string.ascii_letters,min_size=1, max_size=6).example()
        print("list name: "+str(list_name))
        self.device(resourceId="nl.mpcjanssen.simpletask:id/new_item_text").set_text(list_name)
        time.sleep(1)
        self.device(text="OK").click()
        content = self.device(resourceId="nl.mpcjanssen.simpletask:id/taskText").get_text()
        print("content: "+str(content))
        time.sleep(1)
        assert list_name in content

    @precondition(lambda self: self.device(resourceId="nl.mpcjanssen.simpletask:id/fab").exists())
    @rule()
    def add_task(self):
        count = self.device(resourceId="nl.mpcjanssen.simpletask:id/checkBox").count
        if count > 10:
            print("task count is more than 13, do not add task") 
            return
        self.device(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        content = st.text(alphabet=string.ascii_letters,min_size=1, max_size=10).example()
        print("content: "+str(content))
        self.device(resourceId="nl.mpcjanssen.simpletask:id/taskText").set_text(content)
        time.sleep(1)
        self.device(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()
        time.sleep(1)
        new_count = self.device(resourceId="nl.mpcjanssen.simpletask:id/checkBox").count
        print("new count: "+str(new_count))
        assert new_count == count + 1   

    @precondition(lambda self: self.device(description="More options").exists())
    @rule()
    def action_enter_setting(self):
        self.device(description="More options").click()
        time.sleep(1)
        self.device(text="Settings").click()

    @precondition(
        lambda self: int(self.device(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count) > 0 and not self.device(text="Quick filter").exists() and not self.device(text="Settings").exists() and not self.device(text="Saved filters").exists())
    @rule()
    def rule_delete_task(self):
        task_count = int(self.device(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count)
        if task_count == 0:
            print("task count is 0")
            return
        print("task count: "+str(task_count))
        selected_task = random.randint(0, task_count - 1)
        print("selected task: "+str(selected_task))
        selected_task = self.device(resourceId="nl.mpcjanssen.simpletask:id/tasktext")[selected_task]
        selected_task_name = selected_task.get_text()
        print("selected task name: "+str(selected_task_name))
        selected_task.click()
        time.sleep(1)
        self.device(resourceId="nl.mpcjanssen.simpletask:id/context_delete").click()
        time.sleep(1)
        self.device(text="OK").click()
        time.sleep(1)
        new_count = int(self.device(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count)
        print("new count: "+str(new_count))
        assert new_count == task_count - 1


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
    explore_event_count=1000,
    diverse_event_count=1000,
    xml_path=xml_path,
    main_path_path=main_path_path,
    source_activity=source_activity,
    target_activity=target_activity,
    policy_name=policy_name,
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
