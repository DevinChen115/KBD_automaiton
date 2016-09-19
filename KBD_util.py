import os, sys, time, fnmatch, smtplib, shutil, subprocess
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

class device_registration():
    def getDeviceStatus():
        getadbState = subprocess.getoutput("adb get-state")
        while getadbState != "device":
            print("adb connection is unavailable to use. getadbState = " + getadbState)
            getadbKillServer = subprocess.getoutput("adb kill-server")
            getadbState = subprocess.getoutput("adb get-state")
        print("adb connection is available to use. getadbState = " + getadbState)
        getPropManufacturer = subprocess.getoutput("adb shell getprop ro.product.manufacturer")
        getPropModel = subprocess.getoutput("adb shell getprop ro.product.model")
        getPropBrand = subprocess.getoutput("adb shell getprop ro.product.brand")
        getPropAndroidversion = subprocess.getoutput("adb shell getprop ro.build.version.release")
        getPropSDKversion = subprocess.getoutput("adb shell getprop ro.build.version.sdk")
        getPropSerialNo = subprocess.getoutput("adb shell getprop ro.boot.serialno")
        Result = dict (Manufacturer=getPropManufacturer,Model=getPropModel,Brand=getPropBrand,Androidversion=getPropAndroidversion,SDKversion=getPropSDKversion,SerialNo=getPropSerialNo)
        return Result

class Util:
    def __init__(self, mDevice):
        self.driver = mDevice

    def checkElClickable(self, rid):
        try:
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.ID, rid)))
            return True
        except TimeoutException:
            print("Check element " + str(rid) + " clickable fail.")
            return False
    
    def checkElPresence(self, rid):
        try:
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.ID, rid)))
            return True
        except TimeoutException:
            print("Check element " + str(rid) + " presence fail.")
            return False

    def checkElVisible(self, rid):
        try:
            WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.ID, rid)))
            return True
        except TimeoutException:
            print("Check element " + str(rid) + " visible fail.")
            return False

    def clickEl(self, rid):
        try:
            self.driver.find_element_by_id(rid).click()
        except TimeoutException:
            print("Click element " + str(rid) + " Error.")

    def getTextEL(self, rid):
        try:
            return self.driver.find_element_by_id(rid).text
        except TimeoutException:
            print("Get element " + str(rid) + " Text Error.")