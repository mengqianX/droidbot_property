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
        if self.device(text="OK").exists():
            self.device(text="OK").click()
        # time.sleep(1)
        # self.device(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        # content = st.text(alphabet=string.ascii_letters,min_size=1, max_size=10).example()
        # self.device(resourceId="nl.mpcjanssen.simpletask:id/taskText").set_text(content)
        # time.sleep(1)
        # self.device(resourceId="nl.mpcjanssen.simpletask:id/btnProject").click()
        # time.sleep(1)
        # tag_name = st.text(alphabet=string.ascii_letters,min_size=1, max_size=6).example()
        # print("tag name: "+str(tag_name))
        # self.device(resourceId="nl.mpcjanssen.simpletask:id/new_item_text").set_text(tag_name)
        # time.sleep(1)
        # self.device(text="OK").click()
        # time.sleep(1)
        # self.device(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()

    @precondition(
        lambda self: int(self.device(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count) > 1 and not self.device(resourceId="nl.mpcjanssen.simpletask:id/filter_text").exists() and not self.device(text="Quick filter").exists() and not self.device(text="Settings").exists() and not self.device(text="Saved filters").exists()
    )
    @rule()
    def closing_task_should_not_influence_other_tasks(self):
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
        content = self.device(resourceId="nl.mpcjanssen.simpletask:id/taskText").get_text()
        print("content: "+str(content))
        self.device(description="Navigate up").click()
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        
        new_selected_task_index = random.randint(0, task_count - 1)
        while new_selected_task_index == selected_task:
            new_selected_task_index = random.randint(0, task_count - 1)
        print("new selected task: "+str(new_selected_task_index))
        new_selected_task = self.device(resourceId="nl.mpcjanssen.simpletask:id/tasktext")[new_selected_task_index]
        new_selected_task_name = new_selected_task.get_text()
        print("selected task name: "+str(new_selected_task_name))
        new_selected_task.click()
        time.sleep(1)
        self.device(resourceId="nl.mpcjanssen.simpletask:id/update").click()
        time.sleep(1)
        new_content = self.device(resourceId="nl.mpcjanssen.simpletask:id/taskText").get_text()
        print("new content: "+str(new_content))
        assert content not in new_content, "content should not be in new content"

        
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
    apk_path="./apk/simpletask/9.0.1.apk",
    device_serial="emulator-5554",
    output_dir="output/simpletask/738/random_100/1",
    policy_name="random",
    timeout=21600,
    number_of_events_that_restart_app = 100
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
