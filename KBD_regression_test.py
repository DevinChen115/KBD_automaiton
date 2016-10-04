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
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))
# Result = dict (Manufacturer,Model,Brand,Androidversion,SDKversion,SerialNo)
Result = ul.device_registration.getDeviceStatus()


class KBD_regression_test(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = Result["Androidversion"]
        desired_caps['deviceName'] = Result["SerialNo"]
        desired_caps['app'] = PATH('./KBD_apk/kBatteryDoctor_5.34_5340006_20160930_121658-world-release.apk')
        desired_caps['appPackage'] = 'com.ijinshan.kbatterydoctor_en'

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.kbdutil = ul.Util(self.driver, os.getcwd() + "/screenshots")

    def tearDown(self):
        self.driver.quit()

    def test_SaveTabOptimize(self):
        getDrainnumA = ""
        ResultPageFCText = ""
        HomePagePercent = ""

        if self.kbdutil.checkElClickable(el.BatteryDoctor["SaveTab"]) is True:
            self.kbdutil.clickEl(el.BatteryDoctor["SaveTab"])
            print("[PASS][Home Page]Check Save Tab done.")
        else:
            self.assertTrue(False, "[FAIL][Home Page]Check Save Tab fail.")

        if self.kbdutil.checkElVisible(el.SaveTab["DrainnumA"]) is True:
            getDrainnumA = self.kbdutil.getTextEL(el.SaveTab["DrainnumA"])
            print("[PASS][Home Page]Get Home Page Drain num A done. getDrainnumA = " + str(getDrainnumA))
        else:
            self.assertTrue(False, "[FAIL][Home Page]Get Home Page Drain num A fail.")

        if self.kbdutil.checkElClickable(el.SaveTab["Optimize"]) is True:
            self.kbdutil.clickEl(el.SaveTab["Optimize"])
            print("[PASS][Home Page]Click Optimize button done.")
        else:
            self.assertTrue(False, "[FAIL][Home Page]Click Optimize button fail.")

        if self.kbdutil.checkElClickable(el.ResultPage["PopupWindowTryitnow"]) is True:
            self.kbdutil.clickEl(el.ResultPage["PopupWindowTryitnow"])
            print("[PASS][Result Page]Check and Click floating window Tryitnow done. It's 1st time enter to Result Page.")
        else:
            print("[PASS][Result Page]Floating window didn't exist. It's 2nd time above enter to Result Page.")

        if self.kbdutil.checkElVisible(el.ResultPage["FisrtCardText"]) is True:
            ResultPageFCText = self.kbdutil.getTextEL(el.ResultPage["FisrtCardText"])
            self.assertTrue(True, "[PASS][Result Page]Get First Card Text done. ResultPageFCText = " + str(ResultPageFCText))
        else:
            self.assertTrue(False, "[FAIL][Result Page]Get Result Page First Card Text fail.")

        if self.kbdutil.checkElClickable(el.ResultPage["Backkey"]) is True:
            self.kbdutil.clickEl(el.ResultPage["Backkey"])
            print("[PASS][Result Page]Click Back key to Home done.")
        else:
            self.assertTrue(False, "[FAIL][Result Page]Click Back key to Home fail.")

        if self.kbdutil.checkElClickable(el.SaveTab["FloatingX"]) is True:
            self.kbdutil.clickEl(el.SaveTab["FloatingX"])
            print("[PASS][Home Page]Check and Click floating window X done. It's 1st time enter to Home Page.")
        else:
            print("[PASS][Home Page]Floating window X didn't exist. It's 2nd time above enter to Home Page.")

        if self.kbdutil.checkElVisible(el.SaveTab["Percent"]) is True:
            HomePagePercent = self.kbdutil.getTextEL(el.SaveTab["Percent"])
            print("[PASS][Home Page]Get Battery Percentage done. HomePagePercent = " + str(HomePagePercent))
        else:
            self.assertTrue(False, "[FAIL][Home Page]Get Battery Percentage fail.")

    def test_SaveTabHWbutton(self):
        if self.kbdutil.checkElClickable(el.BatteryDoctor["SaveTab"]) is True:
            self.kbdutil.clickEl(el.BatteryDoctor["SaveTab"])
            print("[PASS][Home Page]Check Save Tab done.")
        else:
            self.assertTrue(False, "[FAIL][Home Page]Check Save Tab fail.")

        if self.kbdutil.checkElVisible(el.SaveTab["Percent"]) is True:
            HomePagePercent = self.kbdutil.getTextEL(el.SaveTab["Percent"])
            print("[PASS][Home Page]Get Battery Percentage done. HomePagePercent = " + str(HomePagePercent))
        else:
            self.assertTrue(False, "[FAIL][Home Page]Get Battery Percentage fail.")

        if self.kbdutil.scrollTo(el.SaveTab["SwitchWifi"]) is True:
            print("[PASS][Home Page]Scroll to Get Switch WiFi button done.")
        else:
            self.assertTrue(False, "[FAIL][Home Page]Scroll to Get Switch WiFi button fail.")

        if self.kbdutil.checkElVisible(el.SaveTab["SwitchWifi"]) is True:
            subprocess.call("adb shell am start -n com.android.settings/.wifi.WifiStatusTest")
            WiFiStatusA = self.kbdutil.getTextEL(el_other.WifiStatusTest["State"])
            self.driver.back()
            self.kbdutil.clickEl(el.SaveTab["SwitchWifi"])
            subprocess.call("adb shell am start -n com.android.settings/.wifi.WifiStatusTest")
            WiFiStatusB = self.kbdutil.getTextEL(el_other.WifiStatusTest["State"])
            if WiFiStatusB == "Disabled":
                self.kbdutil.clickEl(el.SaveTab["SwitchWifi"])
            print("[PASS][Home Page]Test Switch WiFi button done.")
        else:
            self.assertTrue(False, "[FAIL][Home Page]Test Switch WiFi button fail.")

    def test_firstExecute_have_rating(self):
        try:
            savePowerEle = self.kbdutil.waitUntilAndGetElement("id", el.BatteryDoctor["SaveTab"], 20)
            savePowerEle.click()
            oneTapSavePowerBtnEle = self.kbdutil.waitUntilAndGetElement("id", el.SaveTab["Optimize"])
            oneTapSavePowerBtnEle.click()
            guide_btn_close = self.kbdutil.waitUntilAndGetElement("id", el.ResultPage["PopupWindowX"], 5)
            guide_btn_close.click()
            backEle = self.kbdutil.waitUntilAndGetElement("id", el.ResultPage["Backkey"])
            backEle.click()
            if self.kbdutil.checkElVisible(el.SaveTab["FloatingFull"]) is True:
                self.assertTrue(True)
        except:
            self.assertTrue(False)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(KBD_regression_test)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    file = open(str(PATH('./KBD_result/' + str(time.strftime("%Y%m%d") + '.html'))) ,"wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=file, title="[KBD Automation] [Python+Appium] [Device: " + ' ' + Result["Manufacturer"] + ' ' + Result["Model"] + ' ' + Result["Brand"] + ']', description="[Platform Version: " + Result["Androidversion"] + ']' + '\n' + "[SDK version: " + Result["SDKversion"] + ']' + '\n' + "[Device S/N: " + Result["SerialNo"] + ']')
    runner.run(suite)
    file.close()
