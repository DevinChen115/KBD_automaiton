import os, sys, time
from time import sleep
from datetime import date
import unittest
from appium import webdriver

from selenium.webdriver.common.by import By
#from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from selenium.common.exceptions import TimeoutException

import KBD_element as el

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

class KBD_regression_test(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4'
        desired_caps['deviceName'] = 'sch_i535-1919e009'
        desired_caps['app'] = PATH('./KBD_apk/kBatteryDoctor_5.28_5280010_20160815_114952-world-release.apk')
        desired_caps['appPackage'] = 'com.ijinshan.kbatterydoctor_en'

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

    def tearDown(self):
        #end the session
        self.driver.quit()

    def test_find_elements(self):
        #Open a new file to record draining apps count
        file = open(str(PATH('./KBD_log/' + str(time.strftime("%Y%m%d") + '.txt'))) ,"w")
        file.close()

        try:
            currently_waiting_for = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable((By.ID, el.SaveTab)))
            clickKBDSaveTab = self.driver.find_element_by_id(el.SaveTab).click()
            print("Click Save Tab done." + str(currently_waiting_for))
        except TimeoutError:
            print("Click Save Tab Timeout Error")

        """
        if (webdriver.wait_activity(self, el.SaveTab, 60, interval=5) == True):
            #Go to Save Tab(Home page)
            clickKBDSaveTab = self.driver.find_element_by_id(el.SaveTab).click()
            print("Click Save Tab done.")
        """

        try:
            currently_waiting_for = WebDriverWait(self.driver,15).until(EC.presence_of_element_located((By.ID, el.SaveTabDrainnumA)))
            #Get draining apps count (Home page)
            getDrainnumA = self.driver.find_element_by_id(el.SaveTabDrainnumA).text
            print("Query and Get Scan Page Drain num A done. getDrainnumA = " + getDrainnumA)
        except TimeoutError:
            print("Query and Get Scan Page Drain num A Timeout Error")
        
        try:
            currently_waiting_for = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, el.SaveTabOptimize)))
            clickOptimize = self.driver.find_element_by_id(el.SaveTabOptimize).click()
            print("Click Optimize done.")
        except TimeoutError:
            print("Click Optimize Timeout Error")

        try:
            currently_waiting_for = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, el.ScanPageDrainnumText)))
            print("Get Scan page Back key done." + str(currently_waiting_for))
            #Get draining apps count (scanning page)
            getDrainnumB = self.driver.find_element_by_id(el.ScanPageDrainnumB).text
            print("Query and Get Scan Page Drain num B done. getDrainnumB = " + getDrainnumB)
        except TimeoutError:
            print("Query and Get Scan Page Drain num B Timeout Error")
        
        #Write count into log file (scanning page)
        file = open(str(PATH('./KBD_log/' + str(time.strftime("%Y%m%d") + '.txt'))) ,"a")
        file.write("Drainging apps count(Home page, getDrainnumA) = " + str(getDrainnumA) + "\n")
        file.write("Drainging apps count(scanning page, getDrainnumB) = " + str(getDrainnumB) + "\n")
        file.close()
        """
        sleep(8)

        #Go to Charging Tab
        clickKBDChargeTab = self.driver.find_element_by_id(el.ChargeTab).click()
        sleep(3)
        #Go to Mode Tab
        clickKBDModeTab = self.driver.find_element_by_id(el.ModeTab).click()
        sleep(3)
        #Go to Rank Tab
        clickKBDRankTab = self.driver.find_element_by_id(el.RankTab).click()
        sleep(3)
        
        self.driver.back()
        sleep(0.5)
        self.driver.back()
        sleep(3)
        """
    
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(KBD_regression_test)
    unittest.TextTestRunner(verbosity=2).run(suite)



"""
        WebDriverWait wait = new WebDriverWait(driver, 60);
            WebElement e= wait.until(new  ExpectedCondition<WebElement>() {
                    @Override
                    public WebElement apply(WebDriver d) {
                        return d.findElement(By.id("q"));
                    }
            })
"""