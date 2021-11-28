from haruka import dispatcher, MESSAGE_DUMP, LOGGER
from haruka.modules.disable import DisableAbleCommandHandler
from telegram import ParseMode, Update, Bot
from telegram.ext import run_async
import datetime
import requests
from bs4 import BeautifulSoup as BS
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import selenium
import time
import pyperclip
import re
import os


def getFromInter(link: str):
    megaLink = ""
    print("Starting new driver")
    options = webdriver.FirefoxOptions()
    options.log.level = "trace"
    options.add_argument("-remote-debugging-port=9224")
    options.add_argument("-headless")
    options.add_argument("-disable-gpu")
    options.add_argument("-no-sandbox")
    binary = FirefoxBinary(os.environ.get('FIREFOX_BIN'))
    tDriver = webdriver.Firefox(firefox_binary=binary, executable_path=os.environ.get('GECKODRIVER_PATH'),
                                options=options)
    tDriver.get(link)
    time.sleep(5)
    print("Finally here!", tDriver.current_url)

    # Clicking Diasagree for coockies
    try:
        WebDriverWait(tDriver, 15).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/button[1]'))).click()
    except:
        pass
    # driver.find_element_by_xpath("//button[contains(., 'DISAGREE')]").click()
    # Clicking I Am Not A Robot Button
    Robot = WebDriverWait(tDriver, 100).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[1]/div/form/div/div[2]/center/img')))
    Robot.location_once_scrolled_into_view
    Robot.click()
    print("Robot Passed")

    # Adding 15 Second Pause For Loading The Page
    time.sleep(15)

    # Clicking Generate Link Button
    print("Generating Link")
    GenerateLink = tDriver.find_element_by_xpath('//*[@id="generater"]')
    GenerateLink.click()

    # Adding 15 Second Pause For Loading The Page
    time.sleep(15)

    # Clicking Download To Get Redirected To Spacetica
    print("Clicking Download button!:/")
    Down = tDriver.find_element_by_xpath('//img[@id="showlink"]')
    Down.click()

    # Adding 15 Second Pause For Loading The Page
    time.sleep(15)

    # ind = -1
    print("len", len(tDriver.window_handles))
    '''for i in range(0, len(tDriver.window_handles)):
        tDriver.switch_to.window(tDriver.window_handles[i])
        print("checking", tDriver.current_url)
        if "linegee.net" in str(tDriver.current_url) or "spacetica.com" in str(tDriver.current_url):
            ind = i
            print("ind", ind)
            break'''

    # Switching To The Newly Opened Tab linegee.net
    window_after = tDriver.window_handles[-1]
    tDriver.switch_to.window(window_after)
    print("On new tab")

    # Addin 5 Second Pause To Load The Page Properly
    time.sleep(3)
    print(tDriver.title, tDriver.current_url)

    # Clicking Continue Button On Spacetica
    try:
        if "Linegee" in tDriver.title:
            Con = WebDriverWait(tDriver, 60).until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/section[2]/div/div/div[1]/div/div[1]/div[3]/center/p/a')))
        else:
            Con = WebDriverWait(tDriver, 60).until(EC.element_to_be_clickable(
                (By.XPATH, '/html/body/section/div/div/div/div[3]/a')
            ))
    except:
        print("No Continue Button")
        return "NA"
    Con.location_once_scrolled_into_view
    # Con = driver.find_element_by_xpath('/html/body/div[2]/section[2]/div/div/div[1]/div/div[1]/div[3]/center/p/a')
    Con.click()
    print("Clicked Continue")
    time.sleep(5)
    tDriver.switch_to.window(tDriver.window_handles[-1])
    megaLink = tDriver.current_url
    print(megaLink)
    tDriver.quit()
    return megaLink


@run_async
def pahedl(bot: Bot, update: Update):
    msg = update.effective_message
    MovieName = msg.text[6:]
    res = ""

    # Getting User Input
    # print("Enter file name-gdrive name-password")
    # print('Enter The Name Of The Movie You Want To Download' )
    # MovieName = input()

    # Enter Your GDrive/Gmail Email and Password For The Account You Want To Use
    # Email = 'YOUR_EMAIL_ADRESS'
    # Password = 'YOUR_PASSWORD'

    # Printing The Name Of The Movie You Want To Download
    print("\n" + 'Getting link For ' + str(MovieName) + ' To Download')

    # Openining The Browser & Getting To Pahe.in
    options = webdriver.FirefoxOptions()
    options.log.level = "trace"
    options.add_argument("-remote-debugging-port=9224")
    options.add_argument("-headless")
    options.add_argument("-disable-gpu")
    options.add_argument("-no-sandbox")

    binary = FirefoxBinary(os.environ.get('FIREFOX_BIN'))
    driver = webdriver.Firefox(firefox_binary=binary, executable_path=os.environ.get('GECKODRIVER_PATH'), options=options)
    driver.get('https://pahe.ph/')
    time.sleep(3)
    print(driver.title)

    # Finding The SearchBox
    searchbox = driver.find_element_by_xpath('//*[@id="s-header"]')
    driver.execute_script("arguments[0].click();", searchbox)
    #searchbox.click()

    # Removing The 'Search' From The Search Bar
    for i in range(0, 6):
        searchbox.send_keys(Keys.BACK_SPACE)

    # Searching Movie Name And Returning Result
    searchbox.send_keys(MovieName)
    searchbox.send_keys(Keys.ENTER)

    # Adding 7 Second Pause
    time.sleep(7)

    # Opening The Movie Page
    cLink = driver.find_elements_by_xpath('//h2//a')
    print("l1: ", cLink[1].text)
    cLink = driver.find_element_by_xpath('//*[@id="main-content"]/div[1]/div[2]/div/div/ul[1]/li/div[1]/h2/a')
    print("l2: ", cLink.text)
    MovieLink = cLink.get_attribute('href')
    cLink.click()

    # Adding 5 Second Pause
    time.sleep(5)

    # Getting File Name
    Name = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/div[1]/article/div/h1/span')
    print("Name: ", Name.text)
    res += str(Name.text) + '\n'

    # here we go
    cText = ""
    nameDivs = driver.find_elements_by_xpath('//*[@class="box download  "]')
    for i in range(len(nameDivs)):
        nameDiv = driver.find_elements_by_xpath('//*[@class="box download  "]')[i]
        cText += nameDiv.text
        cText += '\n'
    vers = cText.split("MG")
    driver.quit()
    time.sleep(5)

    for i in range(len(vers) - 1):
        print("Running for ", i, "th round")
        ver = ""
        ver = str(vers[i].split(" | ")[0].split("\n")[-1])
        print(ver)
        options = webdriver.FirefoxOptions()
        options.log.level = "trace"
        options.add_argument("-remote-debugging-port=9224")
        options.add_argument("-headless")
        options.add_argument("-disable-gpu")
        options.add_argument("-no-sandbox")
        binary = FirefoxBinary(os.environ.get('FIREFOX_BIN'))
        driver = webdriver.Firefox(firefox_binary=binary, executable_path=os.environ.get('GECKODRIVER_PATH'),
                                   options=options)
        driver.get(MovieLink)
        print("Getting link")
        time.sleep(5)
        try:
            for o in range(0, 2):
                print("Finding red button")
                GoogleDriveLink = WebDriverWait(driver, 100).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@class="shortc-button small red "]')))
                GoogleDriveLink.location_once_scrolled_into_view
                GoogleDriveLink = driver.find_elements_by_xpath('//*[@class="shortc-button small red "]')
                # GoogleDriveLink[i].click()
            linktc = GoogleDriveLink[i].get_attribute('href')
            driver.quit()
            time.sleep(5)
            mLink = getFromInter(linktc)
            if mLink == "NA":
                raise Exception('NO MEGA LINK')
        except:
            break

        res += '[' + str(ver) + '](' + str(mLink) + ')\n'
        print("This round is done!")
    update.effective_message.reply_text(
            res, parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )


PAHE_HANDLER = DisableAbleCommandHandler("pahe", pahedl)
dispatcher.add_handler(PAHE_HANDLER)
