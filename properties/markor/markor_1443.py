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
        
    
    @precondition(
        lambda self: self.device(text="Settings").exists() and self.device(text="More").exists() 
    )
    @rule()
    def change_language_to_other_should_not_influence_functionality(self):
        self.device(text="Settings").click()
        time.sleep(1)
        self.device(scrollable=True).scroll.to(text="Language")
        time.sleep(1)
        self.device(text="Language").click()
        time.sleep(1)
        self.device(scrollable=True).scroll.to(text="Turkish (Türkçe)")
        time.sleep(1)
        self.device(text="Turkish (Türkçe)").click()
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.press("back")
        time.sleep(1)
        self.device.app_start("net.gsantner.markor")
        time.sleep(1)
        self.device(resourceId="net.gsantner.markor:id/nav_more").click()
        time.sleep(1)
        self.device(text="Ayarlar").click()
        time.sleep(1)
        assert self.device(text="Genel").exists()

start_time = time.time()


t = Test(
    apk_path="./apk/markor/2.8.0.apk",
    device_serial="emulator-5554",
    output_dir="output/markor/1443/1",
    policy_name="random",
    timeout=7200
)
t.start()
execution_time = time.time() - start_time
print("execution time: " + str(execution_time))
