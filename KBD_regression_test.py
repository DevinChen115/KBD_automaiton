import os
import time
import subprocess
import unittest
from appium import webdriver

import KBD_util as ul
import KBD_element as el
import Other_element as el_other
import HTMLTestRunner

# Returns abs path relative to this file and not cwd
# PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))


def PATH(p):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), p))


def checkFolder():
        if not os.path.exists(os.getcwd() + "/KBD_result"):
            os.makedirs(os.getcwd() + "/KBD_result")


# Result = dict (Manufacturer,Model,Brand,Androidversion,SDKversion,SerialNo)
Result = ul.device_registration.getDeviceStatus()


class KBD_regression_test(unittest.TestCase):
    def setUp(self):
        apk = subprocess.getoutput('ls ' + os.getcwd() + "\KBD_apk")
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = Result["Androidversion"]
        desired_caps['deviceName'] = Result["SerialNo"]
        desired_caps['app'] = PATH('./KBD_apk/' + apk)
        desired_caps['appPackage'] = 'com.ijinshan.kbatterydoctor_en'

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.kbdutil = ul.Util(self.driver, os.getcwd() + "/screenshots")

    def tearDown(self):
        self.driver.quit()

    def test_SaveTab_HWbutton(self):
        try:
            savePowerEle = self.kbdutil.waitUntilAndGetElement("id", el.BatteryDoctor["SaveTab"], "ClickSaveTab", 20)
            savePowerEle.click()
            HWButtonWiFi = self.kbdutil.scrollUntilGetElement("id", el.SaveTab["SwitchWifi"], "ClickSwitchWiFiButton")
            subprocess.call("adb shell am start -n com.android.settings/.wifi.WifiStatusTest")
            WiFiStatusA = self.kbdutil.getTextEL(el_other.WifiStatusTest["State"])
            self.driver.back()
            HWButtonWiFi.click()
            subprocess.call("adb shell am start -n com.android.settings/.wifi.WifiStatusTest")
            WiFiStatusB = self.kbdutil.getTextEL(el_other.WifiStatusTest["State"])
            self.driver.back()
            if str(WiFiStatusB) == "Disabled":
                HWButtonWiFiOn = self.kbdutil.waitUntilAndGetElement("id", el.SaveTab["SwitchWifi"], "ClickSwitchWiFiButtonLetWiFiOn", 5)
                HWButtonWiFiOn.click()
            self.assertNotEqual(WiFiStatusA, WiFiStatusB, "[FAIL][Home Page] Compare WiFi Status A/B Fail.")
        except:
            self.kbdutil.screenshot("test_SaveTabHWbutton")
            self.assertTrue(False)

    def test_firstExecute_have_rating(self):
        try:
            savePowerEle = self.kbdutil.waitUntilAndGetElement("id", el.BatteryDoctor["SaveTab"], "ClickSaveTab", 20)
            savePowerEle.click()
            oneTapSavePowerBtnEle = self.kbdutil.waitUntilAndGetElement("id", el.SaveTab["Optimize"], "ClickOptimize")
            oneTapSavePowerBtnEle.click()
            guide_btn_close = self.kbdutil.waitUntilAndGetElement("id", el.ResultPage["PopupWindowX"], "ClickPopupWindowX", 10)
            guide_btn_close.click()
            backEle = self.kbdutil.waitUntilAndGetElement("id", el.ResultPage["Backkey"], "ClickBackKey")
            backEle.click()
            result = self.kbdutil.checkElVisible(el.SaveTab["FloatingFull"])
            self.assertTrue(result, "[FAIL][Home Page] Home page does not have rating dialog after first time execute optimize ")
        except:
            self.kbdutil.screenshot("firstTimeOptimizeNeedHaveRating")
            self.assertTrue(False)

    def test_availableTimecanClickAndGoToItsPage(self):
        try:
            savePowerEle = self.kbdutil.waitUntilAndGetElement("id", el.BatteryDoctor["SaveTab"], "ClickSaveTab", 20)
            savePowerEle.click()
            test = self.kbdutil.scrollUntilGetElement("id", el.SaveTab["AvailableTimeMovie"], "ClickAvailableTimeArea")
            test.click()
            result = self.kbdutil.checkElVisible(el.Availabletime['2GIcon'])
            self.assertTrue(result, "[FAIL][Home Page] Click Available time area can not go to Available time page")
        except:
            self.kbdutil.screenshot("goToAvailableTimePage")
            self.assertTrue(False)


if __name__ == '__main__':
    checkFolder()
    suite = unittest.TestLoader().loadTestsFromTestCase(KBD_regression_test)
    # unittest.TextTestRunner(verbosity=2).run(suite)
    file = open(str(PATH('./KBD_result/' + str(time.strftime("%Y%m%d") + '.html'))), "wb")
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=file,
        title="[KBD Automation] [Python+Appium] [Device: " + ' ' + Result["Manufacturer"] + ' ' + Result["Model"] + ' ' + Result["Brand"] + ']',
        description="[Platform Version: " + Result["Androidversion"] + ']' + "[SDK version: " + Result["SDKversion"] + ']' + "[Device S/N: " + Result["SerialNo"] + ']')
    runner.run(suite)
    file.close()
