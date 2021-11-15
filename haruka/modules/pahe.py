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


@run_async
def pahedl(bot: Bot, update: Update):
    msg = update.effective_message
    msg = msg.text[6:]
    start_time = time.time()

    # Getting User Input
    # print("Enter file name-gdrive name-password")
    MovieName, Email, Password = str(msg).split("-")
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

    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", str(update.effective_user.id))
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/x-gzip")
    driver = webdriver.Firefox(firefox_binary=binary, executable_path=os.environ.get('GECKODRIVER_PATH'), options=options)
    driver.get('https://pahe.ph/')

    # Finding The SearchBox
    searchbox = driver.find_element_by_xpath('//*[@id="s-header"]')
    searchbox.click()

    # Removing The 'Search' From The Search Bar
    for i in range(0, 6):
        searchbox.send_keys(Keys.BACK_SPACE)

    # Searching Movie Name And Returning Result
    searchbox.send_keys(MovieName)
    searchbox.send_keys(Keys.ENTER)

    # Adding 7 Second Pause
    time.sleep(7)

    # Opening The Movie Page
    MovieLink = driver.find_elements_by_xpath('//h2//a')
    MovieLink[1].click()

    # Adding 5 Second Pause
    time.sleep(5)

    # Creating Download Dir
    tmp_directory_for_each_user = str(update.effective_user.id)
    if not os.path.isdir(tmp_directory_for_each_user):
        os.makedirs(tmp_directory_for_each_user)

    # Getting File Name
    Name = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/div[1]/article/div/h1/span')
    print("Name: ", Name.text)
    download_directory = tmp_directory_for_each_user + "/"

    # Opeing The GDrive Links/First GDLink In 720p Section
    for o in range(0, 2):
        GoogleDriveLink = WebDriverWait(driver, 1000000).until(EC.element_to_be_clickable((By.XPATH,'//*[@class="shortc-button small purple "]')))
        GoogleDriveLink.location_once_scrolled_into_view
        GoogleDriveLink = driver.find_elements_by_xpath('//*[@class="shortc-button small purple "]')
        print(GoogleDriveLink)
        GoogleDriveLink[1].click()

    # Switching To The Newly Opened Tab
    window_after = driver.window_handles[1]
    driver.switch_to.window(window_after)

    # Adding 30 Second Pause For Loading The Page
    time.sleep(30)

    # Clicking I Am Not A Robot Button
    Robot = driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/form/div/div[2]')
    Robot.click()

    # Adding 15 Second Pause For Loading The Page
    time.sleep(15)

    # Clicking Generate Link Button
    GenerateLink = driver.find_element_by_xpath('//*[@id="generater"]')
    GenerateLink.click()

    # Adding 15 Second Pause For Loading The Page
    time.sleep(15)

    # Clicking Download To Get Redirected To Spacetica
    Down = driver.find_element_by_xpath('//*[@id="showlink"]')
    Down.click()

    # Adding 15 Second Pause For Loading The Page
    time.sleep(15)

    # Switching To The Newly Opened Tab
    window_after = driver.window_handles[2]
    driver.switch_to.window(window_after)

    # Addin 10 Second Pause To Load The Page Properly
    time.sleep(10)

    # Clicking Continue Button On Spacetica
    Con = driver.find_element_by_xpath('/html/body/section/div/div/div/div[3]/p/a')
    Con.click()

    # Switching To Klop Login
    window_after = driver.window_handles[3]
    driver.switch_to.window(window_after)

    # Opeing A New Tab For StackOverflow To Bypass Gmail Login Security Issue Due To Autoamtion
    print("Stack Overflow ByPass")
    NewTab = driver.find_element_by_tag_name('body')
    NewTab.send_keys(Keys.CONTROL + 't')

    # Switching To The New Tab
    window_after = driver.window_handles[4]
    driver.switch_to.window(window_after)

    # Getting StackOverflow SignUp Page For Logging In Gmail
    driver.get('https://stackoverflow.com/users/signup?ssrc=head&returnurl=%2fusers%2fstory%2fcurrent')

    # Adding 5 Second Sleep
    time.sleep(5)

    # Clicking The Signin With Gmail Button
    SignUp = driver.find_element_by_xpath('/html/body/div[4]/div[2]/div/div[2]/div[2]/button[1]')
    SignUp.click()

    # Typing Email On Gmail For Login
    EmailField = driver.find_element_by_xpath('//input[@id="identifierId"]')
    EmailField.send_keys(Email)

    # Adding 5 Second Pause To Load Page Properly
    time.sleep(5)

    # Clicking The Next Button To Get Forwarded To Entering The Password
    EmailForward = driver.find_element_by_xpath(
        '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/span/span')
    EmailForward.click()

    # Adding 2 Second Sleep In Case
    time.sleep(2)

    # Typing Password On Gmail For Login
    PasswordField = driver.find_element_by_xpath(
        '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input')
    PasswordField.send_keys(Password)

    # Adding 2 Second Sleep
    time.sleep(2)

    # Clicking The Next Button To Get Forwarded To The Permission Page For GDrive
    PasswordForward = driver.find_element_by_xpath('//*[@id="passwordNext"]')
    PasswordForward.click()

    # Switching Back To The Previous Tab
    window_after = driver.window_handles[3]
    driver.switch_to.window(window_after)

    # Adding 5 Second Pause To Load The Page Properly
    time.sleep(5)

    # Clicking Allow Button For Permission
    for p in range(0, 2):
        abc = driver.find_element_by_xpath('/html/body/div/div/div[2]/form/center/button')
        abc.click()

    # Adding 5 Second Sleep
    time.sleep(5)

    # Clicking Get Code Button For Getting The Authenticated Code For KLOP
    for q in range(0, 2):
        GetCode = driver.find_element_by_xpath('/html/body/div/form/div/div[2]/center/button[2]')
        GetCode.click()

    # Adding 5 Second Pause
    time.sleep(5)

    # Switching To The Code Tab
    window_after = driver.window_handles[4]
    driver.switch_to.window(window_after)

    # Adding 3 Second Pause
    time.sleep(3)

    # Clicking The Account Logged In Before
    EmailField = driver.find_element_by_xpath(
        '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/div/ul/li[1]/div')
    EmailField.click()

    # Adding 5 Second Pause
    time.sleep(7)

    # Clicking Allow For Drive Permissions
    Allow = driver.find_element_by_xpath('/html/body/div[5]/div/div[2]/div[3]/div[1]')
    Allow.click()

    # Adding 5 Second Pause
    time.sleep(5)

    # Click Allow Again For Editing Drive Contents
    Allo = driver.find_element_by_xpath('//*[@id="submit_approve_access"]')
    Allo.click()

    # Adding 5 Second Pause
    time.sleep(5)

    # Getting Conformation Code And Copying It To ClipBoard
    ConformationCode = driver.find_element_by_xpath(
        '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div/div/div/div/div')
    ConformationCode.click()

    # Adding 3 Second Pause
    time.sleep(3)

    # Switching Back To Klop For Entering Conformation Code
    window_after = driver.window_handles[3]
    driver.switch_to.window(window_after)

    # Clicking Code Input Field & Pasting The Conformation Code
    CodeInput = driver.find_element_by_xpath('/html/body/div/form/div/div[2]/div/div/input')
    CodeInput.click()
    Key = pyperclip.paste()
    CodeInput.send_keys(pyperclip.paste())

    # Adding 3 Second Pause
    time.sleep(3)

    # Conforming The Copied Code To Login In KLOP
    Confirm = driver.find_element_by_xpath('/html/body/div/form/div/div[2]/center/button[1]')
    Confirm.click()

    # Adding 2 Second Pause
    time.sleep(2)

    # Clicking Generate Download Link Button
    for r in range(0, 2):
        GenerateDownloadLink = driver.find_element_by_xpath('/html/body/div/div/div[2]/form/center/button')
        GenerateDownloadLink.click()

    # Adding 2 Second Pause
    time.sleep(2)

    # Clicking Download File Button To Get Redirected To GDrive Link
    for s in range(0, 2):
        DownloadFile = driver.find_element_by_xpath('/html/body/div/div/div[2]/center/button')
        DownloadFile.click()

    # Switching To GDrive Link Page
    window_after = driver.window_handles[4]
    driver.switch_to.window(window_after)

    # Adding 10 Second Pause To Load The Page Properly
    time.sleep(10)

    # Clicking Download Button To Go The Download File Page
    GDownload = driver.find_element_by_xpath('/html/body/div[4]/div[3]/div/div[3]/div[2]/div[2]/div[3]')
    GDownload.click()

    # Switching To Download File Tab
    window_after = driver.window_handles[5]
    driver.switch_to.window(window_after)

    # Adding 10 Second Pause To Load Page Properly
    time.sleep(10)

    # Clicking The Final Download Button To Get The Prompt To Save The File & Start Download
    for t in range(0, 2):
        GDownloadFinal = driver.find_element_by_xpath('//*[@id="uc-download-link"]')
        GDownloadFinal.click()

    # Printing The Total Time Elapsed
    elapsed_time = time.time() - start_time
    print(time.strftime("%H:%M:%S", time.gmtime(elapsed_time)))

    # getting downloaded fle
    rootdir = "./" + str(update.effective_user.id)
    regex = re.compile(MovieName[0] + '.*')

    for root, dirs, files in os.walk(rootdir):
        for file in files:
            if regex.match(file):
                download_directory += file

    bot.send_document(
        chat_id=update.message.chat.id,
        document=download_directory,
        caption=Name,
        parse_mode="HTML",
        reply_to_message_id=update.message.reply_to_message.message_id
    )


PAHE_HANDLER = DisableAbleCommandHandler("pahe", pahedl)
dispatcher.add_handler(PAHE_HANDLER)
