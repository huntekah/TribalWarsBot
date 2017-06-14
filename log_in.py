#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
from selenium import webdriver
import random
import time
import datetime


def alert_every_n_seconds(future, n):
    print("Building at", future)
    while future > datetime.datetime.today():
        t = datetime.datetime.today()
        seconds = min((future - t).total_seconds(), n)
        print("sleeping for ", time.strftime('%H:%M:%S', time.gmtime(seconds)))
        time.sleep(seconds)
        print(datetime.datetime.today(), "remaining",
              time.strftime('%H:%M:%S', time.gmtime((future - datetime.datetime.today()).total_seconds())))
        if seconds < n:
            break


def login(username, password):
    # driver = webdriver.PhantomJS("E:\GIT_repos\TribalWarsBot\phantomjs-2.1.1-windows\bin\phantomjs.exe")
    driver = webdriver.Chrome('./chromedriver/chromedriver.exe');
    driver.get("https://www.plemiona.pl/")

    # logging in
    driver.find_element_by_id("user").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_css_selector("a.btn-login").click()
    driver.implicitly_wait(random.randint(1, 7))
    driver.find_element_by_xpath("//a[@class='world-select']/*[contains(text(), '117')]").click()
    driver.implicitly_wait(random.randint(1, 7))
    try:
        driver.find_element_by_xpath("//a[@class='popup_box_close']").click()
        driver.find_element_by_xpath("//button[@class='evt-confirm-btn]").click()
    except:
        print("no campaign popup to click")
    try:
        driver.find_element_by_xpath("//button[@class='Button-close']").click()
        driver.find_element_by_xpath("//button[@class='evt-confirm-btn]").click()
    except:
        print("no button to close")
    driver.implicitly_wait(random.randint(1, 3))
    driver.find_element_by_xpath("//*[@id='menu_row2_village']/a").click()
    driver.find_element_by_xpath("//tr[@id='l_main']//a").click()
    return driver


def build(building_id, time, username, password):
    t = datetime.datetime.today()
    # delta = datetime.timedelta(minutes=7, seconds=1)
    future = time
    alert_every_n_seconds(future, 599)
    t = datetime.datetime.today()
    print("I have woken up!\n its", t, "already!")
    driver = login(username, password)
    try:
        driver.find_element_by_xpath("//a[@class='popup_box_close']").click()
        driver.find_element_by_xpath("//button[@class='evt-confirm-btn]").click()
    except:
        print("no campaign popup to click")
    try:
        string_xpath = "//table[@id='buildings']//tr[@id='{0}']//a[@class='btn btn-build']".format(building_id)
        driver.find_element_by_xpath(string_xpath).click()
    except:
        print(sys.exc_info())
        print("no visible button aviable")
    finally:
        driver.implicitly_wait(random.randint(1, 3))
        driver.close()

def load_queue():
    pass


if __name__ == "__main__":
    t = datetime.datetime.today()
    # delta = datetime.timedelta(minutes=7, seconds=1)
    future = datetime.datetime(t.year, t.month, t.day + 1, 4, 20, 00)
    alert_every_n_seconds(future, 150)
    t = datetime.datetime.today()
    print("I have woken up!\n its", t, "already!")
    driver = login("", "")
    try:
        driver.find_element_by_xpath("//a[@class='popup_box_close']").click()
    except:
        print("no campaign popup to click")
    driver.find_element_by_xpath(
        "//table[@id='buildings']//tr[@id='main_buildrow_main']//a[@class='btn btn-build']").click()

# //table[@id='buildings']//tr[@id='main_buildrow_iron']//a[@class='btn btn-build']


# //tr[@id='l_main']//a # ratusz
# //tr[@id='l_main']//td/text() # jego poziom

# //tr[@id='l_barracks']//a # koszary
# //tr[@id='l_smith']//a # kuźna
# //tr[@id='l_place']//a # plac
# //tr[@id='l_market']//a # rynek
# //tr[@id='l_wood']//a # tartak
# //tr[@id='l_stone']//a # cegielnia
# //tr[@id='l_iron']//a # huta żelaza
# //tr[@id='l_farm']//a # spichlerz
# //tr[@id='l_storage']//a # Mur
