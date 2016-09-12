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

import KBD_element as el

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

class KBD_regression_test(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4'
        desired_caps['deviceName'] = 'sch_i535-1919e009'
        desired_caps['app'] = PATH('./KBD_apk/kBatteryDoctor_5.30_5300009_20160826_121217-world-release.apk')
        desired_caps['appPackage'] = 'com.ijinshan.kbatterydoctor_en'

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        #end the session
        self.driver.quit()

    def test_find_elements(self):
        getDrainnumA = ""
        getDrainnumB = "35"

        #Click Save Tab
        try:
            currently_waiting_for = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, el.SaveTab)))
            clickKBDSaveTab = self.driver.find_element_by_id(el.SaveTab).click()
            print("Click Save Tab done.")
        except TimeoutException:
            print("Click Save Tab Timeout Error")
        
        #Get draining apps count (Home page)
        try:
            currently_waiting_for = WebDriverWait(self.driver,15).until(EC.visibility_of_element_located((By.ID, el.SaveTabDrainnumA)))
            getDrainnumA = self.driver.find_element_by_id(el.SaveTabDrainnumA).text
            print("Query and Get Home Page Drain num A done. getDrainnumA = " + getDrainnumA)
        except TimeoutException:
            print("Query and Get Home Page Drain num A Timeout Error")
        
        #Click Save Tab Optimize button
        try:
            currently_waiting_for = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID, el.SaveTabOptimize)))
            clickOptimize = self.driver.find_element_by_id(el.SaveTabOptimize).click()
            print("Click Optimize done.")
        except TimeoutException:
            print("Click Optimize Timeout Error")

        #Get draining apps count (scanning page)
        try:
            currently_waiting_for = WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.ID, el.ScanPageDrainnumB)))
            getDrainnumB = self.driver.find_element_by_id(el.ScanPageDrainnumB).text
            print("Query and Get Scan Page Drain num B done. getDrainnumB = " + getDrainnumB)
        except TimeoutException:
            print("Query and Get Scan Page Drain num B Timeout Error")
        
        #Open a new file to record draining apps count
        file = open(str(PATH('./KBD_log/' + str(time.strftime("%Y%m%d") + '.txt'))) ,"w")
        #Write count into log file (scanning page)
        file = open(str(PATH('./KBD_log/' + str(time.strftime("%Y%m%d") + '.txt'))) ,"a")
        if getDrainnumA == "":
            print("[DEBUG]getDrainnumA is NULL")
        else:
            file.write("Drainging apps count(Home page, getDrainnumA) = " + str(getDrainnumA) + "\n")
        if getDrainnumB == "":
            print("[DEBUG]getDrainnumB is NULL")
        else:
            file.write("Drainging apps count(scanning page, getDrainnumB) = " + str(getDrainnumB) + "\n")
        
        #Compare draining apps count (Home page & scanning page)
        if getDrainnumA == "":
            print("[Compare]Query and Get Home Page Drain num A Timeout Error")
            raise ValueError('[Compare]Home Page Drain num A is NULL')
        elif getDrainnumB == "":
            print("[Compare]Query and Get Scan Page Drain num B Timeout Error")
            raise ValueError('[Compare]Scan Page Drain num B is NULL')
        else:
            DrainnumA = getDrainnumA.split()
            Drainnum = ''
            for a in DrainnumA[0]:
                if a != "+":
                    Drainnum = Drainnum + a
            Drainnum = int(Drainnum)
            getDrainnumB = int(getDrainnumB)
            if (Drainnum <= getDrainnumB) and ((getDrainnumB - Drainnum) <= 4):
                print(str(Drainnum) + " v.s " + str(getDrainnumB) + " = PASS")
                file.write(str(Drainnum) + "v.s" + str(getDrainnumB) + " = PASS" + "\n")
            else:
                print(str(Drainnum) + " v.s " + str(getDrainnumB) + " = FAIL")
                file.write(str(Drainnum) + "v.s" + str(getDrainnumB) + " = FAIL" + "\n")

        file.close()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(KBD_regression_test)
    unittest.TextTestRunner(verbosity=2).run(suite)