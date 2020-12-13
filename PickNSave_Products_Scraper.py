from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from decimal import Decimal
from Product import Product
from selenium.common.exceptions import TimeoutException
import re

def scrape_PickNSave_search_results(list_of_products, product):
    
    size_line = re.compile('([0-9]+(\.[0-9]+)* [A-Za-z]+|\$[0-9]+\.[0-9][0-9]/[A-Za-z]+)')
    price_line = re.compile('\$[0-9]+\.[0-9][0-9]')
    NoneType = type(None)
    
#   Code taken from here: https://stackoverflow.com/questions/59787776/how-to-set-chrome-experimental-option-same-site-by-default-cookie-in-python-sele    
#   Code taken from here: https://www.selenium.dev/documentation/en/
    
    chrome_options = webdriver.ChromeOptions()
    experimentalFlags = ['same-site-by-default-cookies@1','cookies-without-same-site-must-be-secure@1']
    chromeLocalStatePrefs = { 'browser.enabled_labs_experiments' : experimentalFlags}
    chrome_options.add_experimental_option('localState',chromeLocalStatePrefs)
    driver = webdriver.Chrome(options=chrome_options, executable_path=r'chromedriver.exe')
    driver.get("https://www.picknsave.com/")
    
#   Code taken from here: https://stackoverflow.com/questions/27652543/how-to-use-python-requests-to-fake-a-browser-visit
#   Code taken from here: https://stackoverflow.com/questions/55609049/python-beautifulsoup-selenium-scraper
    
    wait = WebDriverWait(driver, 10)
    
    confirm_button = driver.find_element_by_xpath("//button[@data-testid='DynamicTooltip-Button-confirm']")
    confirm_button.click()
    
    search_button = driver.find_element_by_xpath("//div[@class='SearchBar']")
    search_button.click()
    
    search_bar = driver.find_element_by_xpath("//input[@id='SearchBar-input-open']")
    search_bar.send_keys("{}".format(product) + Keys.RETURN)
    
    
    for x in range(1, 24):
        element_present = expected_conditions.presence_of_all_elements_located((By.XPATH, "//div[@data-qa='ProductCard-{}']".format(x)))
        try:
            wait.until(element_present);
        except TimeoutException:
            print("Could not scan PickNSave for:", end = " ")
            print(product)
            print("\n")
            driver.close()
            return
    
    soup = BeautifulSoup(driver.page_source, 'lxml')
    product_cards = soup.find_all('div', class_='ProductCard border-default-300 border-solid rounded-8 border w-full flex flex-col overflow-hidden w-full px-8 pb-12')

    for card in product_cards:
        
        escape = True
        
        new_product = Product()
        
#        print('\n')
#        print('\n')
#        print(card.prettify())
#        print('\n')
#        print('\n')
        
        price = card.find('data', class_="kds-Price")
        
        if isinstance(price, NoneType):
            continue
        else:
            price_split = price.getText().split(" ")
            for section in price_split:
                if price_line.match(section):
                    final_price = section.replace("$", "")
                    break
            new_product.price = Decimal(final_price)
        
        name = card.find('h3', class_="kds-Text--m text-default-800 mt-12 mb-4 font-500")
        
        name_search = name.getText().split(" ")
        
        for word in name_search:
            if product.upper() == word.upper():
                escape = False
            
        if escape:
#           TODO: Add function that shows people the items that were thrown out.
            continue
        
        if isinstance(name, NoneType):
            continue
        else:
            new_product.name = name.getText()
            
        size = card.find('div', class_="ProductCard-sellBy ProductCard-sellBy-unit")
        
        if isinstance(size, NoneType):
            new_product.website = "PickNSave"
            list_of_products.append(new_product)
            continue
        else:
            size = size.getText()
            if not size_line.match(size):
                print("Wrong size line detected:", end = " ")
                print(size)
                continue
            size = size.split(" ")                                
            
            if len(size) > 3:
                continue
            elif len(size) == 3:
                size = [Decimal(size[0]), size[1] + " " + size[2]]
            elif len(size) == 2:
                size = [Decimal(size[0]), size[1]]
            else:
                size = size[0].split("/")
                if len(size) == 1:
                    continue
            new_product.size = size
        
        if not size == "":
            new_product.price_per = [round(new_product.price / new_product.size[0], 2), new_product.size[1]]
            new_product.website = "PickNSave"
            list_of_products.append(new_product)
        else:
            continue

            
#    driver.close()
    
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'X-Requested-With': 'XMLHttpRequest',}