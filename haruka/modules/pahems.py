from haruka import dispatcher, MESSAGE_DUMP, LOGGER
from haruka.modules.disable import DisableAbleCommandHandler
from haruka.modules.helper_funcs.filters import CustomFilters
from telegram import ParseMode, Update, Bot
from telegram.ext import run_async, MessageHandler
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# CUST_FILTER_HANDLER = MessageHandler(CustomFilters.has_text, reply_filter)
def pahedl(bot: Bot, update: Update):
    msg = update.effective_message.text
    MovieLink = 'https://pahe.ph/'+str(msg.split('https://pahe.ph/')[-1])

    # Printing The Name Of The Movie You Want To Download
    print("\n" + 'Getting link For ' + str(MovieLink) + ' To Download')

    # Openining The Browser & Getting To Pahe.in
    options = webdriver.FirefoxOptions()
    options.log.level = "trace"
    options.add_argument("-remote-debugging-port=9224")
    options.add_argument("-headless")
    options.add_argument("-disable-gpu")
    options.add_argument("-no-sandbox")

    binary = FirefoxBinary(os.environ.get('FIREFOX_BIN'))
    driver = webdriver.Firefox(firefox_binary=binary, executable_path=os.environ.get('GECKODRIVER_PATH'), options=options)
    driver.get(MovieLink)
    time.sleep(5)
    print(driver.title)
    res = ""

    # Getting File Name
    Name = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/div[1]/article/div/h1/span').text
    print("Name: ", Name)
    res += str(Name) + '\n'

    #here we go
    nameDiv = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/div[1]/article/div/div[2]/div[2]/div')
    cText = nameDiv.text
    vers = cText.split(" MG ")
    driver.quit()
    time.sleep(5)

    for i in range(len(vers)-1):
        print("Running for ", i, "th round")
        ver = ""
        ver = str(vers[i].split(" | ")[0].split("\n")[-1])
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
                GoogleDriveLink = WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH,'//*[@class="shortc-button small red "]')))
                GoogleDriveLink.location_once_scrolled_into_view
                GoogleDriveLink = driver.find_elements_by_xpath('//*[@class="shortc-button small red "]')
                GoogleDriveLink[i].click()
        except:
            break

        # Switching To The Newly Opened Tab
        print("Finally here!")
        # Adding 15 Second Pause For Loading The Page
        time.sleep(15)

        #Clicking Diasagree for coockies
        try:
            WebDriverWait(driver, 100).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/button[1]'))).click()
        except:
            pass
        #driver.find_element_by_xpath("//button[contains(., 'DISAGREE')]").click()
        # Clicking I Am Not A Robot Button
        Robot = WebDriverWait(driver, 1000000).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div[1]/div/form/div/div[2]/center/img')))
        Robot.location_once_scrolled_into_view
        Robot.click()
        print("Robot Passed")

        # Adding 15 Second Pause For Loading The Page
        time.sleep(15)

        # Clicking Generate Link Button
        print("Generating Link")
        GenerateLink = driver.find_element_by_xpath('//*[@id="generater"]')
        GenerateLink.click()

        # Adding 15 Second Pause For Loading The Page
        time.sleep(15)

        # Clicking Download To Get Redirected To Spacetica
        print("Clicking Download button!:/")
        Down = driver.find_element_by_xpath('//img[@id="showlink"]')
        Down.click()

        # Adding 15 Second Pause For Loading The Page
        time.sleep(15)

        ind = 1
        for i in range(1, len(driver.window_handles)):
            driver.switch_to.window(driver.window_handles[i])
            if "linegee.net" in str(driver.current_url):
                ind = i

        # Switching To The Newly Opened Tab linegee.net
        window_after = driver.window_handles[ind]
        driver.switch_to.window(window_after)
        print("On new tab")
        print(driver.title, driver.current_url)

        # Addin 5 Second Pause To Load The Page Properly
        time.sleep(5)

        # Clicking Continue Button On Spacetica
        try:
            Con = WebDriverWait(driver, 100).until( EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/section[2]/div/div/div[1]/div/div[1]/div[3]/center/p/a')))
        except:
            print("No Continue Button")
            break
        Con.location_once_scrolled_into_view
        # Con = driver.find_element_by_xpath('/html/body/div[2]/section[2]/div/div/div[1]/div/div[1]/div[3]/center/p/a')
        Con.click()
        print("Clicked Continue")
        time.sleep(5)
        print(ver, " : ", driver.current_url)
        res += '[' + str(ver) + '](' + str(driver.current_url) + ')\n'
        driver.quit()
        time.sleep(5)
        print("This round is done!")
    '''update.effective_message.reply_text(
            res, parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=False
        )'''
    bot.send_message(chat_id=-1001581805288, text=res, parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True)


@run_async
def clook(bot: Bot, update: Update):
    if update.effective_chat.type == "private":
        msg = update.effective_message.text
        if 'https://pahe.ph/' in msg:
            if 'Season' in msg:
                # TV Show
                pass
            else:
                pahedl(bot, update)


LINK_HANDLER = MessageHandler(CustomFilters.has_text, clook)
dispatcher.add_handler(LINK_HANDLER, group=12)