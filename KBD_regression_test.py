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

    def test_SaveTabOptimize(self):
        #Result = dict (IQT_Result='Pass',FC='',Output='')
        getDrainnumA = ""
        getDrainnumB = "35"

        #Click Save Tab
        self.kbdutil.checkElClickable(el.SaveTab)
        print("Check Save Tab done.")
        self.kbdutil.clickEl(el.SaveTab)
        print("Click Save Tab done.")

        #Get draining apps count A (Home page)
        self.kbdutil.checkElVisible(el.SaveTabDrainnumA)
        print("Query Home Page Drain num A done.")
        getDrainnumA = self.kbdutil.getTextEL(el.SaveTabDrainnumA)
        print("Get Home Page Drain num A done.")

        #Click Save Tab Optimize button
        self.kbdutil.checkElClickable(el.SaveTabOptimize)
        print("Check Optimize button done.")
        self.kbdutil.clickEl(el.SaveTabOptimize)
        print("Click Optimize button done.")

        #Get draining apps count B (scanning page)
        if self.kbdutil.checkElPresence(el.ScanPageDrainnumB) == True:
            getDrainnumB = self.kbdutil.getTextEL(el.ScanPageDrainnumB)
            print("[PASS]Get Scan Page Drain num B done. getDrainnumB = " + str(getDrainnumB))
        else:
            print("[FAIL]Get Scan Page Drain num B fail.")

        #self.assertEqual()

    def tearDown(self)2
        #end the session
        self.driver.quit()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(KBD_regression_test)
    unittest.TextTestRunner(verbosity=2).run(suite)
    #file = open(str(PATH('./KBD_result/' + str(time.strftime("%Y%m%d") + '.html'))) ,"wb")
    #runner = HTMLTestRunner.HTMLTestRunner(stream=file,title="test",description="first time test")
    #runner.run(suite)
