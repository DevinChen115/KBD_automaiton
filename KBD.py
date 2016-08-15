import os
from time import sleep

import unittest

from appium import webdriver

import KBD_element as el

# Returns abs path relative to this file and not cwd
PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

class KBD_regression_test(unittest.TestCase):
    def setUp(self):
        desired_caps = {}
        desired_caps['platformName'] = 'Android'
        desired_caps['platformVersion'] = '4.4'
        desired_caps['deviceName'] = 'sch_i535-1919e009'
        desired_caps['app'] = PATH('./KBD_apk/kBatteryDoctor_5.26_5260009_20160803_150815-world-release.apk')
        desired_caps['appPackage'] = 'com.ijinshan.kbatterydoctor_en'

        self.driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)

#    def tearDown(self):
        # end the session
#        self.driver.quit()

    def test_find_elements(self):
        sleep(15)
        clickKBDSaveTab = self.driver.find_element_by_id(el.KBDSaveTab).click()
        sleep(3)
        clickKBDChargeTab = self.driver.find_element_by_id(el.KBDChargeTab).click()
        sleep(3)
        clickKBDModeTab = self.driver.find_element_by_id(el.KBDModeTab).click()
        sleep(3)
        clickKBDRankTab = self.driver.find_element_by_id(el.KBDRankTab).click()
        sleep(3)
#       self.assertIsNotNone(el)

        self.driver.back()
        sleep(0.5)
        self.driver.back()
        sleep(3)
"""
        el = self.driver.find_element_by_accessibility_id("App")
        self.assertIsNotNone(el)

        els = self.driver.find_elements_by_android_uiautomator("new UiSelector().clickable(true)")
        self.assertGreaterEqual(12, len(els))

        self.driver.find_element_by_android_uiautomator('text("API Demos")')


    def test_simple_actions(self):
        el = self.driver.find_element_by_accessibility_id('Graphics')
        el.click()

        el = self.driver.find_element_by_accessibility_id('Arcs')
        el.click()

        self.driver.find_element_by_android_uiautomator('new UiSelector().text("Graphics/Arcs")')
"""

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(KBD_regression_test)
    unittest.TextTestRunner(verbosity=2).run(suite)
