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
        explore_event_count=0,
        diverse_event_count=100,
        main_path_path=None,
        xml_path="None",
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

    @precondition(lambda self: self.device(resourceId="nl.mpcjanssen.simpletask:id/fab").exists() and not self.device(text="Saved filters").exists() and not self.device(text="Quick filter").exists())
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

    @precondition(lambda self: self.device(description="More options").exists() and self.device(text="Simpletask").exists() and not self.device(text="Settings").exists() and not self.device(text="Saved filters").exists() and not self.device(text="Quick filter").exists() and not self.device(text="Help").exists())
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

    # bug #1060
    @precondition(
        lambda self: self.device(text="Quick filter").exists() and self.device(text="CLEAR FILTER").exists() and self.device(resourceId="android:id/text1",className="android.widget.CheckedTextView").exists()
    )
    @rule()
    def filter_by_tag(self):
        self.device(text="CLEAR FILTER").click()
        time.sleep(1)
        check_box_count = int(self.device(resourceId="android:id/text1",className="android.widget.CheckedTextView").count)
        print("check box count: "+str(check_box_count))
        selected_check_box = random.randint(0, check_box_count - 1)
        print("selected check box: "+str(selected_check_box))
        selected_check_box = self.device(resourceId="android:id/text1",className="android.widget.CheckedTextView")[selected_check_box]
        selected_check_box_name = selected_check_box.get_text()
        print("selected check box name: "+str(selected_check_box_name))
        if selected_check_box_name == "-":
            print("not select list or tag, return")
            return
        selected_check_box.click()
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        filter_text = self.device(resourceId="nl.mpcjanssen.simpletask:id/filter_text").get_text()
        print("filter text: "+str(filter_text))
        number = filter_text.split("/")[1][0]
        if number == "0":
            print("no task, return")
            return
        
        assert self.device(resourceId="nl.mpcjanssen.simpletask:id/tasktext").exists(), "no task"
        time.sleep(1)
        self.device(resourceId="nl.mpcjanssen.simpletask:id/tasktext").click()
        time.sleep(1)
        self.device(resourceId="nl.mpcjanssen.simpletask:id/update").click()
        time.sleep(1)
        content = self.device(resourceId="nl.mpcjanssen.simpletask:id/taskText").get_text()
        print("content: "+str(content))
        assert selected_check_box_name in content, "content doesn't have selected items"

    # bug #993
    @precondition(
        lambda self: int(self.device(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count) > 0 and not self.device(text="Quick filter").exists() and not self.device(text="Settings").exists() and not self.device(text="Saved filters").exists())
    @rule()
    def save_reopen_task_should_not_change_number(self):
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
        
        content = st.text(alphabet=string.ascii_letters,min_size=0, max_size=3).example()
        print("content: "+str(content))
        self.device(resourceId="nl.mpcjanssen.simpletask:id/taskText").set_text(content)
        time.sleep(1)
        self.device(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()
        time.sleep(1)
        new_count = int(self.device(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count)
        print("new count: "+str(new_count))
        assert task_count == new_count, "task count should be the same"

    # bug #941
    @precondition(
        lambda self: int(self.device(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count) > 10 and not self.device(text="Settings").exists() and not self.device(text="Saved filters").exists())
    @rule()
    def enter_task_and_back_should_keep_position(self):
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
        self.device(resourceId="nl.mpcjanssen.simpletask:id/btnSave").click()
        time.sleep(1)
        assert self.device(text=selected_task_name).exists(), "selected_task_name not exists"

    # bug #907_708
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
        self.device.set_fastinput_ime(False)
        time.sleep(1)
        self.device(resourceId="com.google.android.inputmethod.latin:id/key_pos_ime_action").click()
        time.sleep(1)
        self.device.set_fastinput_ime(True)
        time.sleep(1)
        self.device(text="OK").click()
        content = self.device(resourceId="nl.mpcjanssen.simpletask:id/taskText").get_text()
        print("content: "+str(content))
        time.sleep(1)
        assert tag_name in content
    
    # bug #843
    @precondition(
        lambda self: self.device(text="Add Task").exists() and self.device(resourceId="nl.mpcjanssen.simpletask:id/taskText").exists()
    )
    @rule()
    def rotate_device_should_keep_text(self):
        content = self.device(resourceId="nl.mpcjanssen.simpletask:id/taskText").get_text()
        print("content: "+str(content))
        self.device.set_orientation("l")
        time.sleep(1)
        self.device.set_orientation("n")
        time.sleep(1)
        new_content = self.device(resourceId="nl.mpcjanssen.simpletask:id/taskText").get_text()
        print("new content: "+str(new_content))
        assert content == new_content

    # bug #839
    @precondition(
        lambda self: int(self.device(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count) > 0 and not self.device(resourceId="nl.mpcjanssen.simpletask:id/filter_text").exists() and not self.device(text="Quick filter").exists() and not self.device(text="Settings").exists() and not self.device(text="Saved filters").exists()
    )
    @rule()
    def unclick_filter_should_work(self):
        self.device(resourceId="nl.mpcjanssen.simpletask:id/filter").click()
        time.sleep(1)
        filter_count = int(self.device(resourceId="android:id/text1").count)
        print("filter count: "+str(filter_count))
        selected_filter_index = random.randint(0, filter_count - 1)
        print("selected filter: "+str(selected_filter_index))
        self.device(resourceId="android:id/text1")[selected_filter_index].click()
        time.sleep(1)
        self.device(resourceId="nl.mpcjanssen.simpletask:id/menu_filter_action").click()
        time.sleep(1)
        assert self.device(resourceId="nl.mpcjanssen.simpletask:id/filter_text").exists(), "filter text should exist"
        time.sleep(1)

        self.device(resourceId="nl.mpcjanssen.simpletask:id/filter").click()
        time.sleep(1)
        self.device(resourceId="android:id/text1")[selected_filter_index].click()
        time.sleep(1)
        self.device(resourceId="nl.mpcjanssen.simpletask:id/menu_filter_action").click()
        time.sleep(1)
        assert not self.device(resourceId="nl.mpcjanssen.simpletask:id/filter_text").exists(), "filter text should not exist"

    # bug #753_739
    @precondition(
        lambda self: int(self.device(resourceId="nl.mpcjanssen.simpletask:id/tasktext").count) > 0 and not self.device(resourceId="nl.mpcjanssen.simpletask:id/filter_text").exists() and not self.device(text="Quick filter").exists() and not self.device(text="Settings").exists() and not self.device(text="Saved filters").exists()
    )
    @rule()
    def task_prefilled_when_filtered(self):
        self.device(resourceId="nl.mpcjanssen.simpletask:id/filter").click()
        time.sleep(1)
        # 随机选择tag or list
        if random.randint(0, 1) == 0:
            self.device(text="LIST").click()
        else:
            self.device(text="TAG").click()
        time.sleep(1)
        # 随机选择是否点击invert filter
        invert_filter = random.randint(0, 1) == 0
        if invert_filter:
            self.device(resourceId="nl.mpcjanssen.simpletask:id/checkbox").click()
        filter_count = int(self.device(resourceId="android:id/text1").count)
        print("filter count: "+str(filter_count))
        selected_filter_index = random.randint(0, filter_count - 1)
        selected_filer_name = self.device(resourceId="android:id/text1")[selected_filter_index].get_text()
        print("selected filter: "+str(selected_filer_name))
        self.device(resourceId="android:id/text1")[selected_filter_index].click()
        time.sleep(1)
        self.device(resourceId="nl.mpcjanssen.simpletask:id/menu_filter_action").click()
        time.sleep(1)
        assert self.device(resourceId="nl.mpcjanssen.simpletask:id/filter_text").exists(), "filter text should exist"
        time.sleep(1)
        self.device(resourceId="nl.mpcjanssen.simpletask:id/fab").click()
        time.sleep(1)
        content = str(self.device(resourceId="nl.mpcjanssen.simpletask:id/taskText").get_text())
        print("content: "+str(content))
        if selected_filer_name == "-":
            assert content == "None", "task text should be empty"
        else:
            print("content: "+str(content))
            if invert_filter:
                assert selected_filer_name not in content, "selected_filer_name should not be in content"
            else:
                assert selected_filer_name in content, "selected_filer_name should be in content"

    # bug #738
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
    apk_path="./apk/simpletask/11.0.1.apk",
    device_serial="emulator-5554",
    output_dir="output/simpletask/new/1",
    explore_event_count=500,
    diverse_event_count=500,
    policy_name="random",
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
