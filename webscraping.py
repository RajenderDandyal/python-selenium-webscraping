from re import search
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
import time
import ast
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import ssl
# mongodb
myclient = pymongo.MongoClient(
    "mongodb+srv://energiapp_dev:WcTsPubiwSuGjRKG@energiapp.x8suh.mongodb.net/energiapp-smt-api-data?retryWrites=true&w=majority", ssl_cert_reqs=ssl.CERT_NONE)
mydb = myclient["energiapp-smt-api-data"]
collection = mydb["rep_prices"]
collection2 = mydb['rep_details']
rep_companies_not_scraped = mydb['rep_companies_not_scraped']
# print(collection2.count_documents({'Website': None}))
# doc = collection.find_one({"puctno": '10105'})
# print(doc)
# driver


# https://www.powertochoose.org/en-us


###########################################
# just energy
###########################################
def justEnergy(puct_no, name, website):
    print('started: ', name, puct_no)
    driver = startDriver()
    driver.get(website)

    see_plans = driver.find_element_by_id('postalCode1')
    see_plans.send_keys('75019')
    see_plans.send_keys(Keys.RETURN)

    try:
        select = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.ID, "formly_16_providerselectiondropdown_providerselectiondropdown1_1"))
        )
        # print(select)
        select_object = Select(select)
        select_object.select_by_index(1)

        driver.find_element_by_id('formly_16_button_NextIni_2').click()
        h4 = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "currency-unit"))
        )
        print("h4:---===---===---===", h4)
        time.sleep(4)
        price = driver.find_elements_by_xpath(
            '/html/body/app-root/app-launcher/div/div/div/form/formly-form/formly-field[2]/app-stepper/mat-horizontal-stepper/div[2]/div[2]/formly-field/formly-group/formly-field[12]/app-formly-wrapper-panel/div/div/formly-group/formly-field[2]/app-formly-wrapper-panel/div/div/formly-group/formly-field[2]/app-product-selection/div/app-product-row[1]/div/div/div[2]/div[1]/app-product-row-price/div/h4')
        final_price = ''
        for element in price:
            final_price = element.get_attribute("innerHTML").split("¢")[0]

        driver.quit()

        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)

        print('finished', name, final_price)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


################################################
# 4change energy
################################################
def fourChangeEnergy(puct_no, name, website):
    print('started: ', name, puct_no)
    driver = startDriver()
    driver.get(website)
    get_my_rates = driver.find_element_by_name('AddressDisplayValue')
    get_my_rates.send_keys('75019')
    get_my_rates.send_keys(Keys.RETURN)

    try:
        select = driver.find_element_by_xpath(
            '/html/body/div[1]/main/section/form/ul/li[2]/input')
        select.click()
        continuee = driver.find_element_by_xpath(
            '/html/body/div[1]/main/section/form/div/nav/button')
        continuee.click()
        time.sleep(5)
        price = driver.find_element_by_xpath(
            '/html/body/div[1]/main/div[2]/div[1]/section/div/div/div/div/div/div[1]/div[1]/div/div[2]/div/div[1]/h2')

        final_price = price.get_attribute("innerHTML").split('<')[0]
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print('Finished: ', name, final_price)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


################################################
# amigo energy
# ##############################################
def amigoEnergy(puct_no, name, website):
    print('started: ', name, puct_no)
    driver = startDriver()
    driver.get(website)

    see_plans = driver.find_element_by_id('z')
    see_plans.send_keys('75019')
    see_plans.send_keys(Keys.RETURN)

    try:
        select = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.ID, "formly_16_providerselectiondropdown_providerselectiondropdown1_1"))
        )
        # print(select)
        select_object = Select(select)
        select_object.select_by_index(1)
        driver.find_element_by_id('formly_16_button_NextIni_2').click()
        h4 = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "currency-unit"))
        )
        #print("h4:---===---===---===", h4)
        price = driver.find_elements_by_xpath(
            '/html/body/app-root/app-launcher/div/div/div/form/formly-form/formly-field[2]/app-stepper/mat-horizontal-stepper/div[2]/div[2]/formly-field/formly-group/formly-field[12]/app-formly-wrapper-panel/div/div/formly-group/formly-field[2]/app-formly-wrapper-panel/div/div/formly-group/formly-field[2]/app-product-selection/div/app-product-row[1]/div/div/div[2]/div[1]/app-product-row-price/div/h4')
        final_price = ''
        for element in price:
            final_price = element.get_attribute("innerHTML").split("¢")[0]

        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print('finished: ', name, final_price)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


################################################
# ALLIANCE POWER COMPANY LLC
################################################
def alliancePower(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        price = driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[1]/div/article/div/table/tbody/tr[2]/td[4]')

        final_price = float(price.get_attribute("innerHTML")[1:])*100
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print('Finished: ', name, final_price)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


################################################
# AMBIT TEXAS LLC
################################################
def ambitTexas(puct_no, name, website):
    print('started: ', name, puct_no)
    driver = startDriver()

    driver.get(website)
    see_our_rates = driver.find_element_by_xpath(
        '/html/body/div[1]/div[3]/div[2]/div[1]/a')
    see_our_rates.click()

    try:
        input_zipcode = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.ID, "zip"))
        )
        input_zipcode.send_keys('75019')
        input_zipcode.send_keys(Keys.RETURN)

        customer_type = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.ID, "residential"))
        )
        #print('customer_type', customer_type)
        # driver.implicitly_wait(10)
        time.sleep(3)
        customer_type.click()
        dwelling_type = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.ID, "house"))
        )
        time.sleep(3)
        #dwelling_type = driver.find_element_by_id('house')
        #print('dwelling_type', dwelling_type)
        dwelling_type.click()

        show_my_rates = driver.find_element_by_xpath(
            '/html/body/div[1]/div[3]/div[1]/div/div[1]/form/input[2]')
        #print('show_my_rates', show_my_rates)
        show_my_rates.click()
        utility_provider = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.ID, "287"))
        )
        time.sleep(3)
        #print('utility_provider', utility_provider)
        utility_provider.click()
        price = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.ID, "EPlanRate[13173]"))
        )
        time.sleep(3)
        final_price = price.get_attribute("innerHTML")[:4]
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print('Finished: ', name, final_price)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


################################################
# AP GAS & ELECTRIC (TX) LLC
################################################
def apGas(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        see_rates_today = driver.find_element_by_xpath(
            '/html/body/div[2]/div/div[5]/div/div/div/div/div/div/div[2]/a')
        see_rates_today.click()
        time.sleep(7)
        zip_code = driver.find_element_by_name('collect-zip-code-zip-code')
        zip_code.send_keys('75019')
        zip_code.send_keys(Keys.RETURN)
        time.sleep(4)
        select = driver.find_element_by_name('choose-ldc-ldc-code')
        # print(select)
        select_object = Select(select)
        select_object.select_by_index(1)

        nextButton = driver.find_element_by_id('choose-ldc-next')
        nextButton.click()

        time.sleep(4)
        price = driver.find_element_by_xpath(
            '/html/body/div/div/choose-offer/div/div/div[2]/form/div/div[1]/div/div[7]/span[1]')
        final_price = price.get_attribute("innerHTML").split('¢')[0]

        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print('Finished: ', name, final_price)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def branchEnergy(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        search = driver.find_element_by_id('find1')
        search.send_keys('515 Meadowview Ln, Coppel, TX, 75019')
        time.sleep(8)
        dropdown = driver.find_element_by_xpath(
            '//*[@id="hide-scrollbar"]/div/div[1]/div/div/div/div/div/div/div')
        dropdown.click()
        time.sleep(9)
        price = driver.find_element_by_css_selector('h2.bubble-element.Text')

        final_price = price.get_attribute("innerHTML").split(" ")[0]
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print('Finished: ', name, final_price)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def brookletEnergy(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        time.sleep(6)
        driver.find_element_by_css_selector(
            'label[for="customRadio1"]').click()
        driver.find_element_by_css_selector(
            'a.btn.btn-primary.tdu-submit').click()
        time.sleep(5)
        span = driver.find_elements_by_css_selector('span.average-price')[0]

        price = span.get_attribute("innerHTML").split('<')[0]
        # print(price)
        final_price = price
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print('Finished: ', name, final_price)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def bulbUS(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)

        # zipcode = driver.find_element_by_id('zipcode')
        # zipcode.send_keys('75019')
        # zipcode.send_keys(Keys.RETURN)
        time.sleep(9)
        text = driver.find_element_by_css_selector('h2.sc-dxgOiQ.ZnduC')
        text2 = text.get_attribute("innerHTML").split('</span>')[0]
        text3 = text2.split('>')[len(text2.split('>'))-1].split('¢')[0]

        price = text3
        # print(price)
        final_price = price
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print('Finished: ', name, final_price)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def constilationNewEnergy(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)

        select = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.ID, "electricity-provider"))
        )
        # print(select)
        select_object = Select(select)
        select_object.select_by_index(1)
        # time.sleep(9)
        button = driver.find_element_by_css_selector(
            'button#signUpFormStepOneSubmit')
        button.click()
        time.sleep(8)
        text = driver.find_element_by_xpath(
            '//*[@id="individual-electricity-options"]/ul/li[3]/div[1]/div[2]/div[1]/div[1]')

        price = text.get_attribute("innerHTML").split('¢')[0]

        final_price = price
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print("Finished: ", name, final_price)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def directEnergy(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        # time.sleep(7)
        zip_code = driver.find_element_by_xpath(
            '/html/body/section/div[1]/section[2]/div/div/div/div[1]/div/div[1]/div/div/div[2]/form/div[1]/input')
        zip_code.clear()
        zip_code.send_keys('75019')
        zip_code.send_keys(Keys.RETURN)
        time.sleep(20)
        tnmp = driver.find_element_by_xpath(
            '/html/body/section/div[1]/section[2]/app-order-cycle/app-shadow-container//div/div/ngb-modal-window/div/div/app-enrollment-dialog/div/div/div[1]/app-utility-select/div/div[4]/div[3]')
        tnmp.click()
        time.sleep(10)
        # select = WebDriverWait(driver, 20).until(
        #     EC.presence_of_element_located(
        #         (By.ID, "electricity-provider"))
        # )
        # # print(select)
        # select_object = Select(select)
        # select_object.select_by_index(1)
        # # time.sleep(9)
        # button = driver.find_element_by_css_selector(
        #     'button#signUpFormStepOneSubmit')
        # button.click()
        # time.sleep(8)
        # text = driver.find_element_by_xpath(
        #     '//*[@id="individual-electricity-options"]/ul/li[3]/div[1]/div[2]/div[1]/div[1]')

        # price = text.get_attribute("innerHTML").split('¢')[0]

        # final_price = price
        # driver.quit()
        # collection.update_one(
        #     {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        # print("Finished: ", name, final_price)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def firstChoicePower(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        # time.sleep(7)
        zip_code = driver.find_element_by_id('search')
        zip_code.clear()
        zip_code.send_keys('75019')
        zip_code.send_keys(Keys.RETURN)

        time.sleep(10)
        text = driver.find_element_by_xpath(
            '//*[@id="tab_75"]/div/div[1]/div/div/div[2]/h4/span')

        final_price = text.get_attribute("innerHTML")
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print("Finished: ", name, final_price)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def frontierUtilities(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        # time.sleep(7)
        zip_code = driver.find_element_by_id('txtPlanValue')
        zip_code.clear()
        zip_code.send_keys('75019')
        # zip_code.send_keys(Keys.RETURN)
        driver.find_element_by_id('btnTexasPlanSubmit_dt').click()
        time.sleep(7)
        text = driver.find_element_by_css_selector(
            'span.plan_price_value.ng-star-inserted')
        # print(text)
        text = text.get_attribute("innerHTML")

        final_price = text
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print("Finished: ", name, final_price)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def gexaEnergyx(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        time.sleep(7)
        zip_code = driver.find_element_by_id('txtZipCode3')
        zip_code.clear()
        zip_code.send_keys('75019')
        time.sleep(3)
        driver.find_element_by_css_selector('input[value="TNMP"]').click()
        driver.find_element_by_id('btAddress2').click()
        time.sleep(5)
        text = driver.find_element_by_xpath(
            '//*[@id="divInfo"]/div/div[2]/div/div/div[2]/span[1]')

        final_price = text.get_attribute("innerHTML")
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print("Finished: ", name, final_price)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def greenMountain(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        # time.sleep(7)
        text = driver.find_element_by_xpath(
            '//*[@id="gmec-product-price-75897"]/td[6]/div[1]/div[1]/div[1]')
        # print(text.get_attribute("innerHTML"))
        final_price = text.get_attribute("innerHTML").split('¢')[0]
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print("Finished: ", name, final_price)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def infuseEnergy(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        # time.sleep(7)
        zip_code = driver.find_element_by_id('Text1')
        zip_code.clear()
        zip_code.send_keys('75019')
        zip_code.send_keys(Keys.RETURN)
        time.sleep(6)
        driver.find_element_by_xpath(
            '//*[@id="MultipleTDSP"]/section/div/div/div/div/form/p[3]/span/input').click()
        driver.find_element_by_css_selector(
            'a[ng-click="selectNewTdspVal()"]').click()
        time.sleep(6)
        text = driver.find_element_by_xpath(
            '/html/body/section/div[3]/section/section/section/div[2]/div/div[2]/div/div[1]/div[3]/div/div[1]/div/div/span[1]')
        # print()
        # time.sleep(5)
        final_price = text.get_attribute("innerHTML")
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print("Finished: ", name, final_price)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def ironHorsePower(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        time.sleep(5)
        zip_code = driver.find_element_by_css_selector(
            'input[placeholder="zip code"]')
        zip_code.send_keys('75019')
        time.sleep(2)
        button = driver.find_element_by_css_selector(
            'input[value="View Plans"]')
        button.click()
        time.sleep(8)
        text = driver.find_element_by_xpath(
            '//*[@id="plans-div"]/div[2]/div/div[1]/div[2]/div/h4')
        # print(text.get_attribute("innerHTML"))
        # # # time.sleep(5)
        final_price = text.get_attribute("innerHTML").split('¢')[0]
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print("Finished: ", name, final_price)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def midAmericanEnergy(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        time.sleep(4)

        text = driver.find_element_by_xpath(
            '/html/body/div[4]/div/div/div[2]/div[2]/div[1]/div[5]/div[2]/div[3]')

        final_price = text.get_attribute("innerHTML").split('<sup>')[0].strip()
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print("Finished: ", name, final_price)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def pulsePower(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        time.sleep(4)
        zip_code = driver.find_element_by_id(
            'ctl00_MainContent_C015_txtZipCode')
        zip_code.send_keys('75019')
        zip_code.send_keys(Keys.RETURN)
        # driver.find_element_by_id(
        #     'ctl00_MainContent_C015_btnSubmitEnrollmentForm').click()
        time.sleep(5)
        select = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "select.radPreventDecorate"))
        )
        # print(select)
        select_object = Select(select)
        select_object.select_by_index(1)
        driver.find_element_by_css_selector(
            'button#ctl00_MainContent_C004_btnSaveTDSP').click()
        text = driver.find_element_by_xpath(
            '//*[@id="MainContent_C004_pnlRates"]/div[2]/div/div/div/div[2]/div/div[1]/div[2]')
        print(text.get_attribute("innerHTML").split(
            '</h4>')[1].split('¢')[0].strip())
        final_price = text.get_attribute(
            "innerHTML").split('</h4>')[1].split('¢')[0].strip()
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print("Finished: ", name, final_price)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def reliantEnergy(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        time.sleep(8)

        driver.find_element_by_css_selector('label[for="radioYes"]').click()
        zip_code = driver.find_element_by_css_selector('input#zipcode')
        zip_code.send_keys('75019')
        driver.find_element_by_id('changeaddressbtn').click()
        time.sleep(5)
        driver.find_element_by_css_selector('button[id="40051"]').click()
        text = driver.find_element_by_xpath(
            '//*[@id="51840011"]/div[1]/div[2]/div/div/div[1]/span/span[2]')
        print(text.get_attribute("innerHTML"))
        final_price = text.get_attribute("innerHTML").split('<sup>')[0].strip()
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print("Finished: ", name, final_price)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def rhytmOps(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        time.sleep(8)

        zip_code = driver.find_element_by_css_selector(
            'input#heroZipcodeLookup')
        zip_code.send_keys('75019')
        zip_code.send_keys(Keys.RETURN)
        time.sleep(4)
        street_address = driver.find_element_by_css_selector(
            'input[id="serviceAddress.addressLine1"]')
        street_address.send_keys('123123')
        street_city = driver.find_element_by_css_selector(
            'input[id="serviceAddress.city"]')
        street_city.send_keys('coppel')
        time.sleep(1)
        driver.find_element_by_css_selector('button[type="submit"]').click()
        time.sleep(3)
        driver.find_element_by_css_selector(
            'label[for="utility-choice-007929441"]').click()
        time.sleep(1)
        driver.find_element_by_css_selector('button[type="submit"]').click()

        time.sleep(6)
        text = driver.find_element_by_xpath(
            '/html/body/div[1]/main/div[1]/div[1]/div/div[2]/div/div[1]/div[5]/div[3]/div/div/h3')
        # print(text.get_attribute("innerHTML"))
        final_price = text.get_attribute("innerHTML").split('¢')[0].strip()
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print("Finished: ", name, final_price)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def xoomEnergy(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        # time.sleep(8)

        zip_code = driver.find_element_by_css_selector(
            'input[placeholder="ZIP"]')
        zip_code.send_keys('75019')
        zip_code.send_keys(Keys.RETURN)
        time.sleep(4)
        driver.find_element_by_xpath(
            '//*[@id="cpTopMain_cpMain_rptElectric_lnkUtility_1"]/div').click()

        time.sleep(4)
        text = driver.find_element_by_xpath(
            '//*[@id="rateData51839431"]/div[1]/div[3]/div[1]/div')

        # print(text.get_attribute("innerHTML"))
        final_price = text.get_attribute("innerHTML").split('¢')[0].strip()
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print("Finished: ", name, final_price)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def truePower(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        # time.sleep(8)

        zip_code = driver.find_element_by_css_selector(
            'input[placeholder="Enter Zip"]')
        zip_code.send_keys('75019')
        zip_code.send_keys(Keys.RETURN)
        time.sleep(20)
        # driver.find_element_by_xpath(
        #     '//*[@id="cpTopMain_cpMain_rptElectric_lnkUtility_1"]/div').click()

        text = driver.find_element_by_xpath(
            '/html/body/wrapper/main/app-root/app-user-journey/app-products-journey-section/div/div[2]/div[2]/div[1]/div[4]/div/div[4]/div')

        print(text.get_attribute("innerHTML").split('<span')[0])
        final_price = text.get_attribute("innerHTML").split('<span')[0].strip()
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print("Finished: ", name, final_price)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def streamSpe(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        # time.sleep(5)

        zip_code = driver.find_element_by_css_selector(
            'input[id="Typeahead-Input"]')
        zip_code.send_keys('75019')
        time.sleep(4)
        zip_code.send_keys(Keys.TAB)
        driver.find_element_by_css_selector(
            'label[for="serviceTypeNew"]').click()
        time.sleep(2)
        driver.find_element_by_xpath(
            '//*[@id="addressForm"]/button[1]').click()
        time.sleep(5)
        driver.find_element_by_css_selector(
            'label[for="LDC-code-D0003"]').click()
        time.sleep(1)
        driver.find_element_by_css_selector(
            'button.primary.continue_ele').click()
        time.sleep(4)
        text = driver.find_element_by_xpath(
            '//*[@id="utilityFlowPlans"]/div[2]/div/section/form/article/div[5]/table/tbody/tr[9]/td/div[2]/div[1]/span[2]')

        # print(text.get_attribute("innerHTML").split('¢')[0])
        final_price = text.get_attribute("innerHTML").split('¢')[0].strip()
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print("Finished: ", name, final_price)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def capitalEnergy(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        constilationNewEnergy(puct_no, name, website)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        # driver.quit()


def txuEnergyRetail(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        time.sleep(6)
        driver.find_elements_by_css_selector(
            'a.btn.btn-block.button')[0].click()

        time.sleep(6)
        clk = driver.find_elements_by_css_selector('span.modsmall')[2]
        clk.click()
        time.sleep(2)
        driver.find_elements_by_css_selector('label.txu-radio')[0].click()
        address = driver.find_element_by_id('main_0_txtTypeAhead')
        address.send_keys('75019')
        time.sleep(4)
        address.send_keys(Keys.UP)
        address.send_keys(Keys.RETURN)
        driver.find_elements_by_css_selector('label.txu-radio')[2].click()
        driver.find_element_by_id('main_0_btnProspect').click()
        time.sleep(6)
        text = driver.find_element_by_xpath(
            '//*[@id="maincontent_0_pnlOfferListing"]/section[3]/div/div[8]/div[8]/div[1]/h3/span')

        # print('Plan for homes clicked')
        # print(text.get_attribute("innerHTML"))
        final_price = text.get_attribute("innerHTML").split('¢')[0].strip()
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print("Finished: ", name, final_price)
        # time.sleep(800)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def trieagleEnergy(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        time.sleep(6)
        zip_code = driver.find_element_by_id('ctl00_txtZipCode')
        zip_code.send_keys('75019')
        zip_code.send_keys(Keys.RETURN)
        time.sleep(4)
        driver.find_element_by_id('RightContent_btnSavePromo').click()
        time.sleep(4)
        text = driver.find_element_by_xpath(
            '//*[@id="RightContent_lvRates_ctrl2_divRateBox_3"]/table[1]/tbody/tr/td/div[1]')

        # print(text.get_attribute("innerHTML"))
        final_price = text.get_attribute("innerHTML").split('¢')[0].strip()
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print("Finished: ", name, final_price)
        # time.sleep(800)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def tomorrowEnergy(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        time.sleep(6)
        zip_code = driver.find_element_by_css_selector('input[name="zip"]')
        zip_code.send_keys('75019')
        zip_code.send_keys(Keys.RETURN)
        time.sleep(10)
        text = driver.find_element_by_xpath(
            '//*[@id="energy_rates_widget-2"]/div/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]/div[3]/div[1]/div[2]/span[2]')
        # print(text.get_attribute("innerHTML"))
        final_price = text.get_attribute("innerHTML").strip()
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print("Finished: ", name, final_price)
        # time.sleep(800)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def corp300Energy(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        time.sleep(3)

        text = driver.find_element_by_id('lblPlan31PerKWH')
        # print(text.get_attribute("innerHTML"))
        final_price = text.get_attribute("innerHTML").strip()
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print("Finished: ", name, final_price)
        # time.sleep(800)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def directEnergyLLC(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        time.sleep(3)
        driver.find_element_by_css_selector(
            'a[href="/small-business/products-c"]').click()
        time.sleep(11)
        zip_code = driver.find_element_by_css_selector('input[id="zipCode"]')
        zip_code.send_keys('75019')
        time.sleep(4)
        driver.find_element_by_css_selector(
            'button[onclick="updateZip();"]').click()
        time.sleep(6)
        text = driver.find_element_by_xpath(
            '//*[@id="deb-products-controller-v3"]/div[3]/div[1]/div[1]/div[2]')
        # print(text.get_attribute("innerHTML"))
        final_price = text.get_attribute("innerHTML").split('¢')[0].strip()
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print("Finished: ", name, final_price)
        # time.sleep(800)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def windrosePower(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        time.sleep(3)
        zip_code = driver.find_element_by_css_selector('input[id="Zipcode2"]')
        zip_code.send_keys('75019')
        time.sleep(2)
        driver.find_element_by_id('viewratesbtn2').click()
        time.sleep(6)
        text = driver.find_element_by_xpath('//*[@id="127410"]/p[3]')

        # print(text.get_attribute("innerHTML"))
        final_price = text.get_attribute("innerHTML").split('¢')[0].strip()
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print("Finished: ", name, final_price)
        # time.sleep(800)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def v247Power(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        time.sleep(3)
        zip_code = driver.find_element_by_css_selector('input[id="zip"]')
        zip_code.send_keys('75019')
        zip_code.send_keys(Keys.RETURN)
        time.sleep(2)
        driver.find_element_by_css_selector(
            'div[onclick="chooseProvider(\'007929441\')"]').click()

        time.sleep(6)
        text = driver.find_element_by_xpath(
            '//*[@id="popular"]/div[4]/div/p[2]/span/strong/span')

        # print(text.get_attribute("innerHTML"))
        final_price = text.get_attribute("innerHTML").strip()
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print("Finished: ", name, final_price)
        # time.sleep(800)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def usRetailer(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        time.sleep(3)
        zip_code = driver.find_element_by_css_selector(
            'input[id="txtZipcode"]')
        zip_code.send_keys('75019')
        zip_code.send_keys(Keys.RETURN)
        time.sleep(6)
        driver.find_element_by_css_selector('label[for="40051_tdsp"]').click()
        time.sleep(2)
        driver.find_element_by_id('multiTDSPContinue').click()
        time.sleep(6)
        text = driver.find_element_by_xpath(
            '/html/body/div[2]/main/div/div/div/div[2]/div[3]/div[1]/div[3]/div[4]/div/span[1]')

        # print(text.get_attribute("innerHTML"))
        final_price = text.get_attribute("innerHTML").strip()
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print("Finished: ", name, final_price)
        # time.sleep(800)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def titanGas(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        time.sleep(3)
        zip_code = driver.find_element_by_css_selector(
            'input[id="zip"]')
        zip_code.send_keys('75019')
        zip_code.send_keys(Keys.RETURN)
        time.sleep(6)

        text = driver.find_element_by_xpath(
            '//*[@id="divPlanRates"]/div/div/span')

        # print(text.get_attribute("innerHTML"))
        final_price = text.get_attribute("innerHTML").split('¢')[0].strip()
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print("Finished: ", name, final_price)
        # time.sleep(800)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def taraEnergy(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        time.sleep(3)
        zip_code = driver.find_element_by_css_selector(
            'input[id="ZipCode"]')
        zip_code.send_keys('75019')
        zip_code.send_keys(Keys.RETURN)
        time.sleep(6)

        select = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.ID, "formly_16_providerselectiondropdown_providerselectiondropdown1_1"))
        )
        # print(select)
        select_object = Select(select)
        select_object.select_by_index(1)

        driver.find_element_by_id('formly_16_button_NextIni_2').click()
        h4 = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "currency-unit"))
        )
        #print("h4:---===---===---===", h4)
        time.sleep(4)
        price = driver.find_elements_by_xpath(
            '/html/body/app-root/app-launcher/div/div/div/form/formly-form/formly-field[2]/app-stepper/mat-horizontal-stepper/div[2]/div[2]/formly-field/formly-group/formly-field[12]/app-formly-wrapper-panel/div/div/formly-group/formly-field[2]/app-formly-wrapper-panel/div/div/formly-group/formly-field[2]/app-product-selection/div/app-product-row[1]/div/div/div[2]/div[1]/app-product-row-price/div/h4')
        final_price = ''
        for element in price:
            final_price = element.get_attribute(
                "innerHTML").split("¢")[0].strip()

        # print(final_price)
        final_price = final_price
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print("Finished: ", name, final_price)
        # time.sleep(800)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def summerEnergy(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        time.sleep(3)
        select = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.ID, "stateurls"))
        )
        # print(select)
        select_object = Select(select)
        select_object.select_by_index(1)
        time.sleep(4)
        zip_code = driver.find_element_by_css_selector(
            'input[id="ZipCodeData_Zip"]')
        zip_code.send_keys('75019')
        zip_code.send_keys(Keys.RETURN)
        time.sleep(4)
        driver.find_element_by_css_selector('input[value="5"]').click()
        time.sleep(2)
        driver.find_element_by_css_selector('input[type="submit"]').click()
        # print(final_price)
        # final_price = ''
        # driver.quit()
        # collection.update_one(
        #     {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        # print("Finished: ", name, final_price)
        # time.sleep(800)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def evolveRetailEnergy(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        time.sleep(3)
        text = driver.find_element_by_xpath(
            '/html/body/div[1]/main/div[1]/section[1]/div[2]/p/span')

        # print(text.get_attribute("innerHTML").split('¢')[0].strip())
        final_price = text.get_attribute("innerHTML").split('¢')[0].strip()
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print("Finished: ", name, final_price)
        # time.sleep(800)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def sparkEnergy(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        time.sleep(3)

        zip_code = driver.find_element_by_css_selector(
            'input[id="Zip"]')
        zip_code.send_keys('75019')
        zip_code.send_keys(Keys.RETURN)
        time.sleep(4)
        text = driver.find_element_by_xpath(
            '/html/body/div[5]/div[3]/div/div/div/div/div/article/div/div[1]/div[3]/ul/li[4]/header/div[1]/div[2]/div[2]/h1/span')
        # print(text.get_attribute("innerHTML").split('¢')[0].strip())
        final_price = text.get_attribute("innerHTML").split('¢')[0].strip()
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print("Finished: ", name, final_price)
        # time.sleep(800)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


def eligoEnergy(puct_no, name, website):
    try:
        print('started: ', name, puct_no)
        driver = startDriver()
        driver.get(website)
        time.sleep(5)

        zip_code = driver.find_element_by_css_selector(
            'input[id="txtZIP_CODE"]')
        zip_code.send_keys('75019')
        time.sleep(1)
        driver.find_element_by_id('btnProdLookup').click()

        time.sleep(4)
        driver.find_elements_by_css_selector(
            'button[id="btnProviderEnroll"]')[1].click()

        time.sleep(5)

        text = driver.find_element_by_xpath(
            '/html/body/div[1]/div[2]/div[3]/div[1]/div[2]/div[2]/div[4]/div/div[2]/div/div/div[2]/div/div/div/div/div[1]/p[3]/span/span/strong/span/span/span[1]/span')
        # print(text.get_attribute("innerHTML"))
        final_price = text.get_attribute("innerHTML").split('¢')[0].strip()
        driver.quit()
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "latest_price": final_price, "scraping_success": True}}, upsert=True,)
        print("Finished: ", name, final_price)
        # time.sleep(800)
    except Exception as e:
        print(name, e)
        collection.update_one(
            {"puctno": puct_no}, {"$set": {"company_name": name, "website": website, "scraping_success": False}}, upsert=True,)
        driver.quit()


companies_list = [
    {
        "name": "JUST ENERGY TEXAS LP",
        "website": "https://justenergy.com/",
        "inDb": True,
        "function": justEnergy,
        "puctno": '10052'
    },
    {
        "name": "4CHANGE ENERGY",
        "website": "https://www.4changeenergy.com/",
        "inDb": True,
        "function": fourChangeEnergy,
        "puctno": '10041'
    },
    {
        "name": "AMIGO ENERGY",
        "website": "https://amigoenergy.com/",
        "inDb": True,
        "function": amigoEnergy,
        "puctno": '10081'
    },
    {
        "name": "ALLIANCE POWER COMPANY LLC",
        "website": "https://alliance-power.com/residential/",
        "inDb": True,
        "function": alliancePower,
        "puctno": '10074'
    },
    {
        "name": "AMBIT TEXAS LLC",
        "website": "https://www.ambitenergy.com/",
        "inDb": True,
        "function": ambitTexas,
        "puctno": '10117'
    },
    {
        "name": "AP GAS & ELECTRIC (TX) LLC",
        "website": "https://www.apge.com/",
        "inDb": True,
        "function": apGas,
        "puctno": '10105'
    },
    {
        "name": "BRANCH ENERGY HOLDINGS INC",
        "website": "https://branchenergy.com/sign-up/address",
        "inDb": True,
        "function": branchEnergy,
        "puctno": '10290'
    },
    {
        "name": "BROOKLET ENERGY DISTRIBUTION LLC",
        "website": "https://www.acaciaenergy.com/enroll/?zip=75019",
        "inDb": True,
        "function": brookletEnergy,
        "puctno": '10137'
    },
    {
        "name": "BULB US LLC",
        "website": "https://join.bulb.com/plan?zipcode=75019",
        "inDb": True,
        "function": bulbUS,
        "puctno": '10266'
    },
    {
        "name": "CONSTELLATION NEWENERGY INC",
        "website": "https://www.constellation.com/content/constellation/en/solutions/for-your-home/residential-signup.html?zip=75019&promoCode=",
        "inDb": True,
        "function": constilationNewEnergy,
        "puctno": '10014'
    },
    {
        "name": "FIRST CHOICE POWER LLC",
        "website": "https://www.firstchoicepower.com/",
        "inDb": True,
        "function": firstChoicePower,
        "puctno": '10008'
    },
    {
        "name": "FRONTIER UTILITIES LLC",
        "website": "https://www.frontierutilities.com/",
        "inDb": True,
        "function": frontierUtilities,
        "puctno": '10169'
    },
    {
        "name": "GEXA ENERGY LP",
        "website": "https://newenroll.gexaenergy.com/?refid=1DEFAULT&ul=1000",
        "inDb": True,
        "function": gexaEnergyx,
        "puctno": '10027'
    },
    {
        "name": "GREEN MOUNTAIN ENERGY COMPANY",
        "website": "https://www.greenmountainenergy.com/home-energy-solutions/products/tnmp/",
        "inDb": True,
        "function": greenMountain,
        "puctno": '10009'
    },
    {
        "name": "INFUSE ENERGY LLC",
        "website": "https://www.infuseenergy.com/",
        "inDb": True,
        "function": infuseEnergy,
        "puctno": '10223'
    },
    {
        "name": "IRONHORSE POWER SERVICES LLC",
        "website": "http://www.ironhorsepowerservices.com/",
        "inDb": True,
        "function": ironHorsePower,
        "puctno": '10289'
    },
    {
        "name": "MIDAMERICAN ENERGY SERVICES LLC",
        "website": "https://www.midamericanenergyservices.com/ResidentialSmallBusiness/TexasVariableRates",
        "inDb": True,
        "function": midAmericanEnergy,
        "puctno": '10233'
    },
    {
        "name": "PULSE POWER LLC",
        "website": "https://www.pulsepowertexas.com/",
        "inDb": True,
        "function": pulsePower,
        "puctno": '10259'
    },
    {
        "name": "RELIANT ENERGY RETAIL SERVICES LLC",
        "website": "https://www.reliant.com/en/residential/electricity/electricity-plans/electricity-plans.jsp",
        "inDb": True,
        "function": reliantEnergy,
        "puctno": '10007'
    },
    {
        "name": "RHYTHM OPS LLC",
        "website": "https://www.gotrhythm.com/",
        "inDb": True,
        "function": rhytmOps,
        "puctno": '10279'
    },
    # {
    #     "name": "FULCRUM RETAIL ENERGY LLC",
    #     "website": "https://amigoenergy.com/",
    #     "inDb": True,
    #     "function": amigoEnergy,
    #     "puctno": '10081'
    # },
    {
        "name": "DIRECT ENERGY BUSINESS LLC",
        "website": "https://business.directenergy.com/",
        "inDb": True,
        "function": directEnergyLLC,  # directEnergy,
        "puctno": '10040'  # '10011'
    },
    # {
    #     "name": "JUST ENERGY TEXAS LP",
    #     "website": "https://justenergy.com/",
    #     "inDb": True,
    #     "function": justEnergy,
    #     "puctno": '10052'
    # },
    # {
    #     "name": "VALUE BASED BRANDS LLC",
    #     "website": "https://www.4changeenergy.com/",
    #     "inDb": True,
    #     "function": fourChangeEnergy,
    #     "puctno": '10041'
    # },
    {
        "name": "XOOM ENERGY TEXAS LLC",
        "website": "https://xoomenergy.com/en",
        "inDb": True,
        "function": xoomEnergy,
        "puctno": '10203'
    },
    {
        "name": "TRUE COMMODITIES LLC",
        "website": "https://truepower.com/",
        "inDb": True,
        "function": truePower,
        "puctno": '10287'
    },
    {
        "name": "STREAM SPE LTD",
        "website": "https://www.mystream.com/en/",
        "inDb": True,
        "function": streamSpe,
        "puctno": '10104'
    },
    {
        "name": "CAPITAL ENERGY PA LLC",
        "website": "https://www.constellation.com/content/constellation/en/solutions/for-your-home/residential-signup.html?zip=75019&promoCode=",
        "inDb": True,
        "function": capitalEnergy,
        "puctno": '10293'
    },
    {
        "name": "TXU ENERGY RETAIL COMPANY LLC",
        "website": "https://www.txu.com/",
        "inDb": True,
        "function": txuEnergyRetail,
        "puctno": '10004'
    },
    {
        "name": "TRIEAGLE ENERGY LP",
        "website": "https://www.trieagleenergy.com/",
        "inDb": True,
        "function": trieagleEnergy,
        "puctno": '10064'
    },
    {
        "name": "TOMORROW ENERGY CORP",
        "website": "https://tomorrowenergy.com/",
        "inDb": True,
        "function": tomorrowEnergy,
        "puctno": '10270'
    },
    {
        "name": "3000 Energy Corp",
        "website": "https://penstarpower.com/",
        "inDb": True,
        "function": corp300Energy,
        "puctno": '10087'
    },
    {
        "name": "DIRECT ENERGY BUSINESS LLC",
        "website": "https://business.directenergy.com/",
        "inDb": True,
        "function": directEnergyLLC,
        "puctno": '10011'
    },
    {
        "name": "WINDROSE POWER AND GAS LLC",
        "website": "https://www.windroseenergy.com/",
        "inDb": True,
        "function": windrosePower,
        "puctno": '10254'
    },
    {
        "name": "V247 POWER CORPORATION",
        "website": "https://v247power.com/",
        "inDb": True,
        "function": v247Power,
        "puctno": '10210'
    },
    {
        "name": "US RETAILERS LLC",
        "website": "https://www.discountpowertx.com/",
        "inDb": True,
        "function": usRetailer,
        "puctno": '10177'
    },
    {
        "name": "TITAN GAS LLC",
        "website": "https://cleanskyenergy.com/",
        "inDb": True,
        "function": titanGas,
        "puctno": '10268'
    },
    {
        "name": "TARA ENERGY LLC",
        "website": "https://taraenergy.com/",
        "inDb": True,
        "function": taraEnergy,
        "puctno": '10051'
    },
    {
        "name": "SUMMER ENERGY LLC",
        "website": "https://www.summerenergy.com/",
        "inDb": True,
        "function": summerEnergy,
        "puctno": '10205'
    },
    {
        "name": "SPARK ENERGY LLC",
        "website": "https://www.sparkenergy.com/for-home/fixed-price-energy-plan/",
        "inDb": True,
        "function": sparkEnergy,
        "puctno": '10046'
    },
    {
        "name": "Evolve Retail Energy LLC",
        "website": "https://octopusenergy.com/",
        "inDb": True,
        "function": evolveRetailEnergy,
        "puctno": '10262'
    },
    {
        "name": "ELIGO ENERGY TX LLC",
        "website": "https://eligoenergy.myaccount.energy/sigma/myeaccount/?connectName=SigmaELIGO&process=enroll",
        "inDb": True,
        "function": eligoEnergy,
        "puctno": '10246'
    },
]


def startDriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.headless = False
    driver = webdriver.Chrome(
        ChromeDriverManager().install(), options=chrome_options)
    return driver


def runScrapper():
    for company in companies_list:
        if company['inDb'] and company["puctno"] == '10117':
            time.sleep(2)
            company['function'](company['puctno'],
                                company['name'], company["website"])


findCompany = []
companies = []


def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1


def updateCollections():
    rep_details = list(collection2.find({}))
    # print(list(rep_details))
    in_list = False

    for rep in rep_details:
        if find(companies_list, 'puctno', rep['puctno']) < 0:
            rep_companies_not_scraped.update_one(
                {"puctno": rep["puctno"]}, {"$set": {"company_name": rep["CompanyName"], "website": rep["Website"], "scraping_success": False, "latest_price": None, "reason": "Website not found" if rep["Website"] == None or rep["Website"] == 'null' else "Rate plan not found"}}, upsert=True,)
        else:
            rep_companies_not_scraped.delete_one(
                {"puctno": rep["puctno"], "company_name": rep['CompanyName']})


print(len(companies_list))
runScrapper()
# updateCollections()
