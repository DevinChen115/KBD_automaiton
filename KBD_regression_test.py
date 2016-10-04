import os, time
#import sys, fnmatch, smtplib, shutil, subprocess
#from time import sleep
#from datetime import date
import unittest
from appium import webdriver

#from selenium.webdriver.common.by import By
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.common.exceptions import TimeoutException

import KBD_util as ul
import KBD_element as el
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
        self.kbdutil = ul.Util(self.driver,os.getcwd()+"/screenshots")
    
    def tearDown(self):
        #end the session
        self.driver.quit()
    
    def test_SaveTabOptimize(self):
        getDrainnumA = ""
        #getDrainnumB = ""
        ResultPageFCText = ""
        HomePagePercent = ""

        #Click Save Tab
        if self.kbdutil.checkElClickable(el.BatteryDoctor["SaveTab"]) == True:
            self.kbdutil.clickEl(el.BatteryDoctor["SaveTab"])
            print("[PASS][Home Page]Check Save Tab done.")
        else:
            self.assertTrue(False,"[FAIL][Home Page]Check Save Tab fail.")

        #Get draining apps count A (Home page)
        if self.kbdutil.checkElVisible(el.SaveTab["DrainnumA"]) == True:
            getDrainnumA = self.kbdutil.getTextEL(el.SaveTab["DrainnumA"])
            print("[PASS][Home Page]Get Home Page Drain num A done. getDrainnumA = " + str(getDrainnumA))
        else:
            self.assertTrue(False,"[FAIL][Home Page]Get Home Page Drain num A fail.")

        #Click Save Tab Optimize button
        if self.kbdutil.checkElClickable(el.SaveTab["Optimize"]) == True:
            self.kbdutil.clickEl(el.SaveTab["Optimize"])
            print("[PASS][Home Page]Click Optimize button done.")
        else:
            self.assertTrue(False,"[FAIL][Home Page]Click Optimize button fail.")
        
        #Check and Click X of floating window if need
        if self.kbdutil.checkElClickable(el.ResultPage["PopupWindowTryitnow"]) == True:
            self.kbdutil.clickEl(el.ResultPage["PopupWindowTryitnow"])
            print("[PASS][Result Page]Check and Click floating window Tryitnow done. It's 1st time enter to Result Page.")
        else:
            print("[PASS][Result Page]Floating window didn't exist. It's 2nd time above enter to Result Page.")

        #Make sure KBD in Result Page
        if self.kbdutil.checkElVisible(el.ResultPage["FisrtCardText"]) == True:
            ResultPageFCText = self.kbdutil.getTextEL(el.ResultPage["FisrtCardText"])
            self.assertTrue(True,"[PASS][Result Page]Get First Card Text done. ResultPageFCText = " + str(ResultPageFCText))
        else:
            self.assertTrue(False,"[FAIL][Result Page]Get Result Page First Card Text fail.")
        
        #Press Back to Home page
        if self.kbdutil.checkElClickable(el.ResultPage["Backkey"]) == True:
            self.kbdutil.clickEl(el.ResultPage["Backkey"])
            print("[PASS][Result Page]Click Back key to Home done.")
        else:
            self.assertTrue(False,"[FAIL][Result Page]Click Back key to Home fail.")

        #Check and Click X of Home floating window if need
        if self.kbdutil.checkElClickable(el.SaveTab["FloatingX"]) == True:
            self.kbdutil.clickEl(el.SaveTab["FloatingX"])
            print("[PASS][Home Page]Check and Click floating window X done. It's 1st time enter to Home Page.")
        else:
            print("[PASS][Home Page]Floating window X didn't exist. It's 2nd time above enter to Home Page.")

        #Check test case back to KBD Home successfully (Percentage show up)
        if self.kbdutil.checkElVisible(el.SaveTab["Percent"]) == True:
            HomePagePercent = self.kbdutil.getTextEL(el.SaveTab["Percent"])
            print("[PASS][Home Page]Get Battery Percentage done. HomePagePercent = " + str(HomePagePercent))
        else:
            self.assertTrue(False,"[FAIL][Home Page]Get Battery Percentage fail.")

    def test_SaveTabHWbutton(self):
            
        #Click Save Tab
        if self.kbdutil.checkElClickable(el.BatteryDoctor["SaveTab"]) == True:
            self.kbdutil.clickEl(el.BatteryDoctor["SaveTab"])
            print("[PASS][Home Page]Check Save Tab done.")
        else:
            self.assertTrue(False,"[FAIL][Home Page]Check Save Tab fail.")

        #Check test case back to KBD Home successfully (Percentage show up)
        if self.kbdutil.checkElVisible(el.SaveTab["Percent"]) == True:
            HomePagePercent = self.kbdutil.getTextEL(el.SaveTab["Percent"])
            print("[PASS][Home Page]Get Battery Percentage done. HomePagePercent = " + str(HomePagePercent))
        else:
            self.assertTrue(False,"[FAIL][Home Page]Get Battery Percentage fail.")

        #Scroll to Wifi Switch button
        if self.kbdutil.scrollTo(el.SaveTab["SwitchWifi"]) == True:
            print("[PASS][Home Page]Scroll to Get Switch WiFi button done.")
        else:
            self.assertTrue(False,"[FAIL][Home Page]Scroll to Get Switch WiFi button fail.")

        #Test WiFi button
        if self.kbdutil.checkElVisible(el.SaveTab["SwitchWifi"]) == True:
            self.kbdutil.clickEl(el.SaveTab["SwitchWifi"])
            print("[PASS][Home Page]Scroll to Get Switch WiFi button done.")
        else:
            self.assertTrue(False,"[FAIL][Home Page]Scroll to Get Switch WiFi button fail.")

    def test_firstExecute_have_rating(self):
        try:
            savePowerEle = self.kbdutil.waitUntilAndGetElement("id",el.BatteryDoctor["SaveTab"],20)
            savePowerEle.click()
            oneTapSavePowerBtnEle = self.kbdutil.waitUntilAndGetElement("id",el.SaveTab["Optimize"])
            oneTapSavePowerBtnEle.click()
            guide_btn_close = self.kbdutil.waitUntilAndGetElement("id",el.ResultPage["PopupWindowX"],5)
            guide_btn_close.click()
            backEle = self.kbdutil.waitUntilAndGetElement("id",el.ResultPage["Backkey"])
            backEle.click()
            if self.kbdutil.checkElVisible(el.SaveTab["FloatingFull"]) == True:
                self.assertTrue(True)
        except:
            self.assertTrue(False)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(KBD_regression_test)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    file = open(str(PATH('./KBD_result/' + str(time.strftime("%Y%m%d") + '.html'))) ,"wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=file,title="[KBD Automation] [Python+Appium] [Device: " + ' ' + Result["Manufacturer"] + ' ' + Result["Model"] + ' ' + Result["Brand"] + ']',description="[Platform Version: " + Result["Androidversion"] + ']' + '\n' + "[SDK version: " + Result["SDKversion"] + ']' + '\n' + "[Device S/N: " + Result["SerialNo"] + ']')
    runner.run(suite)
    file.close()
