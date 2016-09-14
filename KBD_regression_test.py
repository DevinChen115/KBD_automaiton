import os, sys, time, fnmatch, smtplib, shutil
from time import sleep
from datetime import date
import unittest
from appium import webdriver

from selenium.webdriver.common.by import By
#from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import KBD_util as ul
import KBD_element as el
import HTMLTestRunner

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

class KBD_regression_test(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4'
        desired_caps['deviceName'] = 'sch_i535-1919e009'
        desired_caps['app'] = PATH('./KBD_apk/kBatteryDoctor_5.31_5310007_20160902_152436-world-release.apk')
        desired_caps['appPackage'] = 'com.ijinshan.kbatterydoctor_en'

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        self.kbdutil = ul.Util(self.driver)
    
    def tearDown(self):
        #end the session
        self.driver.quit()

    def test_SaveTabOptimize(self):
        getDrainnumA = ""
        getDrainnumB = ""
        ResultPageFCText = ""
        HomePagePercent = ""

        #Click Save Tab
        if self.kbdutil.checkElClickable(el.SaveTab) == True:
            self.kbdutil.clickEl(el.SaveTab)
            print("[PASS][Home Page]Check Save Tab done.")
        else:
            self.assertTrue(False,"[FAIL][Home Page]Check Save Tab fail.")

        #Get draining apps count A (Home page)
        if self.kbdutil.checkElVisible(el.SaveTabDrainnumA) == True:
            getDrainnumA = self.kbdutil.getTextEL(el.SaveTabDrainnumA)
            print("[PASS][Home Page]Get Home Page Drain num A done. getDrainnumA = " + str(getDrainnumA))
        else:
            self.assertTrue(False,"[FAIL][Home Page]Get Home Page Drain num A fail.")

        #Click Save Tab Optimize button
        if self.kbdutil.checkElClickable(el.SaveTabOptimize) == True:
            self.kbdutil.clickEl(el.SaveTabOptimize)
            print("[PASS][Home Page]Click Optimize button done.")
        else:
            self.assertTrue(False,"[FAIL][Home Page]Click Optimize button fail.")
        
        """
        #Get draining apps count B (scanning page)
        try:
            if self.kbdutil.checkElPresence(el.ScanPageDrainnumB) == True:
                getDrainnumB = self.kbdutil.getTextEL(el.ScanPageDrainnumB)
                self.assertTrue(True,"[PASS][Scan Page]Get Drain num B done. getDrainnumB = " + str(getDrainnumB))
            else:
                self.assertTrue(False,"[FAIL][Scan Page]Get Drain num B fail.")
        except:
            self.assertTrue(False,"[FAIL][Scan Page]Get getDrainnumB Text fail.")
        """

        #Check and Click X of floating window if need
        if self.kbdutil.checkElClickable(el.ResultPagePopupWindowTryitnow) == True:
            self.kbdutil.clickEl(el.ResultPagePopupWindowTryitnow)
            print("[PASS][Result Page]Check and Click floating window Tryitnow done. It's 1st time enter to Result Page.")
        else:
            print("[PASS][Result Page]Floating window didn't exist. It's 2nd time above enter to Result Page.")

        #Make sure KBD in Result Page
        if self.kbdutil.checkElVisible(el.ResultPageFisrtCardText) == True:
            ResultPageFCText = self.kbdutil.getTextEL(el.ResultPageFisrtCardText)
            self.assertTrue(True,"[PASS][Result Page]Get First Card Text done. ResultPageFCText = " + str(ResultPageFCText))
        else:
            self.assertTrue(False,"[FAIL][Result Page]Get Result Page First Card Text fail.")
        
        #Press Back to Home page
        if self.kbdutil.checkElClickable(el.ResultPageBackkey) == True:
            self.kbdutil.clickEl(el.ResultPageBackkey)
            print("[PASS][Result Page]Click Back key to Home done.")
        else:
            self.assertTrue(False,"[FAIL][Result Page]Click Back key to Home fail.")

        #Check and Click X of Home floating window if need
        if self.kbdutil.checkElClickable(el.SaveTabFloatingX) == True:
            self.kbdutil.clickEl(el.SaveTabFloatingX)
            print("[PASS][Home Page]Check and Click floating window X done. It's 1st time enter to Home Page.")
        else:
            print("[PASS][Home Page]Floating window X didn't exist. It's 2nd time above enter to Home Page.")

        #Check test case back to KBD Home successfully (Percentage show up)
        if self.kbdutil.checkElVisible(el.SaveTabPercent) == True:
            HomePagePercent = self.kbdutil.getTextEL(el.SaveTabPercent)
            print("[PASS][Home Page]Get Battery Percentage done. HomePagePercent = " + str(HomePagePercent))
        else:
            self.assertTrue(False,"[FAIL][Home Page]Get Battery Percentage fail.")
            
    def test_SaveTabHWbutton(self):
        self.assertTrue(True)
        """
        #Click Save Tab
        self.kbdutil.checkElClickable(el.SaveTab)
        print("Check Save Tab done.")
        self.kbdutil.clickEl(el.SaveTab)
        print("Click Save Tab done.")
        
        #Get draining apps count A (Home page)
        self.kbdutil.checkElVisible(el.SaveTabDrainnumA)
        print("Query Home Page Drain num A done.")
        getDrainnumA = self.kbdutil.getTextEL(el.SaveTabDrainnumA)
        print("Get Home Page Drain num A done. getDrainnumA = " + str(getDrainnumA))
        
        element_to_tap = self.driver.find_element_by_xpath(<xpath_to_element_near_bottom_of_screen>)
        element_to_drag_to = self.driver.find_element_by_xpath(<xpath_to_element_near_top_of_screen>)
        self.driver.scroll(element_to_tap, element_to_drag_to)
        """

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(KBD_regression_test)
    #unittest.TextTestRunner(verbosity=2).run(suite)
    file = open(str(PATH('./KBD_result/' + str(time.strftime("%Y%m%d") + '.html'))) ,"wb")
    runner = HTMLTestRunner.HTMLTestRunner(stream=file,title="KBD Automation (Python+Appium)",description="Automation test")
    runner.run(suite)
    file.close()
