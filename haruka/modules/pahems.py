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
from bs4 import BeautifulSoup as SOUP
import requests as HTTP
from queue import Queue
q = Queue(maxsize=10)
drake = False

# CUST_FILTER_HANDLER = MessageHandler(CustomFilters.has_text, reply_filter)
def pahedl(bot: Bot, update: Update):
    msg = update.effective_message.text
    MovieLink = 'https://pahe.li/' + str(msg.split('https://pahe.li/')[-1])
    if str(update.effective_chat.id) == "-1001581805288":
        MovieLink = MovieLink.split('\n')[0]

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
    driver = webdriver.Firefox(firefox_binary=binary, executable_path=os.environ.get('GECKODRIVER_PATH'),
                               options=options)
    driver.get(MovieLink)
    time.sleep(5)
    print(driver.title)
    res = ""

    # Getting File Name
    if str(update.effective_chat.id) != "-1001581805288":
        Name = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/div[1]/article/div/h1/span').text
        print("Name: ", Name)
        res += str(Name) + '\n'

        POSTER = str(driver.find_element_by_xpath('//img[@class="imdbwp__img"]').get_attribute('src'))
    # res += str(driver.find_element_by_xpath('//div[@class="imdbwp__meta"]').text) + '\n'

    # here we go
    try:
        nameDiv = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/div[1]/article/div/div[2]/div[2]/div')
    except:
        nameDiv = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/div[1]/article/div/div[2]/div[1]/div')
    cText = nameDiv.text
    vers = cText.split("MG")
    driver.quit()
    time.sleep(5)

    for i in range(len(vers) - 1):
        print("Running for ", i, "th round")
        ver = ""
        if ' | ' in str(vers[i]):
            ver = str(vers[i].split(" | ")[0].split("\n")[-1])
        else:
            # ver = str(vers[i].split("\n")[0])
            for v in vers[i].split("\n"):
                if len(v.strip()) > 3:
                    ver = v
                    break
        print(ver)
        if '480p' in ver:
            continue
        elif str(update.effective_chat.id) == "-1001581805288" and '1080p' in ver:
            break
        options = webdriver.FirefoxOptions()
        options.log.level = "trace"
        options.add_argument("-remote-debugging-port=9224")
        options.add_argument("-headless")
        options.add_argument("-disable-gpu")
        options.add_argument("-no-sandbox")
        binary = FirefoxBinary(os.environ.get('FIREFOX_BIN'))
        try:
            driver = webdriver.Firefox(firefox_binary=binary, executable_path=os.environ.get('GECKODRIVER_PATH'),
                                   options=options)
        except Exception:
            print("Retrying init driver")
            driver = webdriver.Firefox(firefox_binary=binary, executable_path=os.environ.get('GECKODRIVER_PATH'),
                                       options=options)
        driver.get(MovieLink)
        print("Getting link")
        time.sleep(5)
        try:
            for o in range(0, 2):
                print("Finding red button")
                try:
                    GoogleDriveLink = driver.find_elements_by_xpath('//*[@class="shortc-button small red "]')[i]
                    GoogleDriveLink.location_once_scrolled_into_view
                    GoogleDriveLink.click()
                    print("Clicked red button")
                except:
                    pass

            # on intercelestial
            time.sleep(10)
            try:
                WebDriverWait(driver, 100).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/button[1]'))).click()
                print("Disagreed")
            except:
                pass
            # driver.find_element_by_xpath("//button[contains(., 'DISAGREE')]").click()
            # Clicking I Am Not A Robot Button
            try:
                Robot = WebDriverWait(driver, 100).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '/html/body/div[2]/div/div[1]/div/form/div/div[2]/center/img')))
            except:
                print("Robot not found")
                driver.quit()
                raise Exception("No Mega Link")
            Robot.location_once_scrolled_into_view
            Robot.click()
            print("Robot Passed")

            # Adding 15 Second Pause For Loading The Page
            time.sleep(15)

            # Clicking Generate Link Button
            print("Generating Link")
            try:
                # //*[@id="generater"]
                GenerateLink = WebDriverWait(driver, 100).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '/html/body/div[1]/div/div[1]/div/div[2]/div[3]/a/img')))
            except:
                driver.quit()
                raise Exception("No Generate Link Button")
            GenerateLink.click()

            # Adding 15 Second Pause For Loading The Page
            time.sleep(15)

            # Clicking Download To Get Redirected To Spacetica
            print("Clicking Download button!:/")
            Down = driver.find_element_by_xpath('//img[@id="showlink"]')
            Down.click()

            time.sleep(15)
            print("len", len(driver.window_handles))
            # Switching To The Newly Opened Tab linegee.net
            window_after = driver.window_handles[-1]
            driver.switch_to.window(window_after)
            print("On new tab")

            time.sleep(3)
            print(driver.title, driver.current_url)

            # Clicking Continue Button On Spacetica
            try:
                if "Linegee" in driver.title:
                    Con = WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
                        (By.XPATH, '/html/body/div[2]/section[2]/div/div/div[1]/div/div[1]/div[3]/center/p/a')))
                else:
                    Con = WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
                        (By.XPATH, '/html/body/section/div/div/div/div[3]/a')
                    ))
            except:
                print("No Continue Button")
                raise Exception("No Mega")
            Con.location_once_scrolled_into_view
            # Con = driver.find_element_by_xpath('/html/body/div[2]/section[2]/div/div/div[1]/div/div[1]/div[3]/center/p/a')
            try:
                Con.click()
            except:
                time.sleep(5)
                Con.click()
            print("Clicked Continue")
            time.sleep(5)
            # tDriver.switch_to.window(tDriver.window_handles[-1])
            mLink = str(driver.current_url)
            print(mLink)
            driver.quit()
        except Exception as e:
            try:
                driver.quit()
            except:
                pass
            print(e)
            break

        time.sleep(5)
        if str(update.effective_chat.id) != "-1001581805288":
            res += '[' + str(ver) + '](' + str(mLink) + ')\n'
        else:
            update.effective_message.reply_text(
                str(mLink), parse_mode=ParseMode.HTML,
                disable_web_page_preview=True
            )
        print("res", res)
        print("This round is done!")
    if str(update.effective_chat.id) != "-1001581805288":
        update.effective_message.reply_photo(
            POSTER,
            res, parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
    # driver.quit()
    '''bot.send_message(chat_id=-100-1001581805288, text=res, parse_mode=ParseMode.MARKDOWN,
                     disable_web_page_preview=True)'''


def pahesh(bot: Bot, update: Update):
    msg = update.effective_message.text
    MovieLink = 'https://pahe.li/' + str(msg.split('https://pahe.li/')[-1])
    if str(update.effective_chat.id) == "-1001581805288":
        MovieLink = MovieLink.split('\n')[0]

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
    driver = webdriver.Firefox(firefox_binary=binary, executable_path=os.environ.get('GECKODRIVER_PATH'),
                               options=options)
    driver.get(MovieLink)
    time.sleep(5)
    print(driver.title)
    res = ""

    # Getting File Name
    if str(update.effective_chat.id) != "-1001581805288":
        Name = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div/div[1]/div[1]/article/div/h1/span').text
        print("Name: ", Name)
        res += str(Name) + '\n'
        POSTER = str(driver.find_element_by_xpath('//img[@class="imdbwp__img"]').get_attribute('src'))
    navTabs = driver.find_elements_by_xpath('//ul[@class="tabs-nav"]')
    print("There are ", len(navTabs), " columns")
    for x in range(len(navTabs)):
        allLi = driver.find_elements_by_xpath(
            '/html/body/div[1]/div[2]/div/div[1]/div[1]/article/div/div[2]/div[' + str(x + 2) + ']/ul/li')
        print("There are ", len(allLi), " rows")
        driver.quit()
        time.sleep(5)
        try:
            driver.quit()
            time.sleep(5)
        except:
            pass
        button = 0
        for y in range(len(allLi)):
            options = webdriver.FirefoxOptions()
            options.log.level = "trace"
            options.add_argument("-remote-debugging-port=9224")
            options.add_argument("-headless")
            options.add_argument("-disable-gpu")
            options.add_argument("-no-sandbox")

            binary = FirefoxBinary(os.environ.get('FIREFOX_BIN'))
            try:
                driver = webdriver.Firefox(firefox_binary=binary, executable_path=os.environ.get('GECKODRIVER_PATH'),
                                       options=options)
            except Exception:
                print("retrying init driver")
                driver = webdriver.Firefox(firefox_binary=binary, executable_path=os.environ.get('GECKODRIVER_PATH'),
                                           options=options)
            driver.get(MovieLink)
            time.sleep(5)
            print(button)
            cLi = WebDriverWait(driver, 100).until(
                EC.element_to_be_clickable((By.XPATH,
                                            '/html/body/div[1]/div[2]/div/div[1]/div[1]/article/div/div[2]/div[' + str(
                                                x + 2) + ']/ul/li[' + str(
                                                y + 1) + ']')))
            cLi.location_once_scrolled_into_view
            cLi = driver.find_element_by_xpath(
                '/html/body/div[1]/div[2]/div/div[1]/div[1]/article/div/div[2]/div[' + str(x + 2) + ']/ul/li[' + str(
                    y + 1) + ']')
            print(cLi.text)
            res += cLi.text + '\n'
            cLi.click()
            driver.execute_script("arguments[0].click();", cLi)
            print(driver.find_element_by_xpath('//li[@class="current"]').text)

            # code
            del cLi
            print("getting division text")
            nameDiv = driver.find_elements_by_xpath(
                '/html/body/div[1]/div[2]/div/div[1]/div[1]/article/div/div[2]/div[' + str(x + 2) + ']/div')[y]
            cText = nameDiv.text
            vers = cText.split("MG")
            print(vers[0])
            driver.quit()
            if len(vers) == 1:
                break
            if '480p' in vers[0] and len(vers) == 2:
                button = 1
                continue

            for i in range(len(vers)):
                print("Running for ", i, "th round")
                if i == len(vers) - 1:
                    print("this is last round")
                    button += len(vers) - 1
                    print(button)
                    break
                ver = ""
                if ' | ' in vers[i]:
                    ver = str(vers[i].split(" | ")[0].split("\n")[-1])
                else:
                    for v in vers[i].split("\n"):
                        if len(v.strip()) > 3:
                            ver = v
                            break
                if '480p' in ver:
                    continue
                elif str(update.effective_chat.id) == "-1001581805288" and '1080p' in ver:
                    break
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
                time.sleep(5)
                print(button)
                cLi = WebDriverWait(driver, 100).until(
                    EC.element_to_be_clickable((By.XPATH,
                                                '/html/body/div[1]/div[2]/div/div[1]/div[1]/article/div/div[2]/div[' + str(
                                                    x + 2) + ']/ul/li[' + str(
                                                    y + 1) + ']')))
                cLi.location_once_scrolled_into_view
                cLi = driver.find_element_by_xpath(
                    '/html/body/div[1]/div[2]/div/div[1]/div[1]/article/div/div[2]/div[' + str(
                        x + 2) + ']/ul/li[' + str(
                        y + 1) + ']')
                print(cLi.text)
                cLi.click()
                driver.execute_script("arguments[0].click();", cLi)
                print("Finding red button")
                print("clicking", button + i, "th button")
                # try:
                for o in range(0, 2):
                    print("Finding red button")
                    try:
                        GoogleDriveLink = driver.find_elements_by_xpath('//*[@class="shortc-button small red "]')[button + i]
                        GoogleDriveLink.location_once_scrolled_into_view
                        GoogleDriveLink.click()
                        print("Clicked red button")
                    except:
                        pass

                # on intercelestial
                time.sleep(5)
                try:
                    WebDriverWait(driver, 15).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, '/html/body/div[1]/div/div/div/div[2]/div/button[1]'))).click()
                except:
                    pass
                # driver.find_element_by_xpath("//button[contains(., 'DISAGREE')]").click()
                # Clicking I Am Not A Robot Button
                try:
                    Robot = WebDriverWait(driver, 100).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, '/html/body/div[2]/div/div[1]/div/form/div/div[2]/center/img')))
                except:
                    driver.quit()
                    continue
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

                time.sleep(15)
                print("len", len(driver.window_handles))
                # Switching To The Newly Opened Tab linegee.net
                window_after = driver.window_handles[-1]
                for win in driver.window_handles:
                    driver.switch_to.window(win)
                    if 'inegee.' in str(driver.current_url):
                        break
                # driver.switch_to.window(window_after)
                print("On new tab")

                time.sleep(3)
                print(driver.title, driver.current_url)

                # Clicking Continue Button On Spacetica
                try:
                    if "Linegee" in driver.title:
                        Con = WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
                            (By.XPATH, '/html/body/div[2]/section[2]/div/div/div[1]/div/div[1]/div[3]/center/p/a')))
                    else:
                        Con = WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
                            (By.XPATH, '/html/body/section/div/div/div/div[3]/a')
                        ))
                except:
                    print("No Continue Button")
                    driver.quit()
                    continue
                Con.location_once_scrolled_into_view
                # Con = driver.find_element_by_xpath('/html/body/div[2]/section[2]/div/div/div[1]/div/div[1]/div[3]/center/p/a')
                try:
                    Con.click()
                except:
                    time.sleep(5)
                    Con.click()
                print("Clicked Continue")
                time.sleep(5)
                # tDriver.switch_to.window(tDriver.window_handles[-1])
                mLink = driver.current_url
                print(ver, mLink)
                if str(update.effective_chat.id) != "-1001581805288":
                    res += '[' + str(ver) + '](' + str(mLink) + ')\n'
                else:
                    update.effective_message.reply_text(
                        str(mLink), parse_mode=ParseMode.HTML,
                        disable_web_page_preview=True
                    )
                driver.quit()
                time.sleep(5)
                #mLink = getFromInter(GoogleDriveLink.get_attribute('href'))
                '''if mLink == "NA":
                    raise Exception('NO Cont button')
                except:
                    print("Mega button not found.:/")
                    break'''

                # print(ver, " : ", mLink)
                # print("Back on", driver.current_url)
            # driver.quit()
            print("This round is done!")

    # here we go
    # driver.quit()
    if str(update.effective_chat.id) != "-1001581805288":
        update.effective_message.reply_photo(
            POSTER,
            res, parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )
    '''bot.send_message(chat_id=-1001581805288, text=res, parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True)'''


@run_async
def clook(bot: Bot, update: Update):
    if update.effective_chat.type == "private" or str(update.effective_chat.id) == "-1001581805288":
        global drake
        global q
        msg = update.effective_message.text
        if msg is not None:
            if 'https://pahe.li/' in msg:
                print("Getting file with message:\n", msg)
                q.put(update)
                while not drake and not q.empty():
                    drake = True
                    cupdate = q.get()
                    if 'Season' in cupdate.effective_message.text:
                        print("It's TV Show")
                        pahesh(bot, cupdate)
                    else:
                        print("It's Movie")
                        pahedl(bot, cupdate)
                    drake = False


LINK_HANDLER = MessageHandler(CustomFilters.has_text, clook)
dispatcher.add_handler(LINK_HANDLER, group=12)
