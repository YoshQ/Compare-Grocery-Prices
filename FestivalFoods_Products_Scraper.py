from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.expected_conditions import element_to_be_clickable
from selenium.webdriver.support.expected_conditions import url_changes
from selenium.webdriver.common.action_chains import *
from decimal import Decimal
from Product import Product
from selenium.common.exceptions import TimeoutException
import re
import time
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import *
from fractions import Fraction
import random

def scrape_FestivalFoods_search_results(list_of_products, product):

#   Code taken from here: https://stackoverflow.com/questions/59787776/how-to-set-chrome-experimental-option-same-site-by-default-cookie-in-python-sele    
#   Code taken from here: https://www.selenium.dev/documentation/en/
    
    chrome_options = webdriver.ChromeOptions()
    experimentalFlags = ['same-site-by-default-cookies@1','cookies-without-same-site-must-be-secure@1']
    chromeLocalStatePrefs = { 'browser.enabled_labs_experiments' : experimentalFlags}
    chrome_options.add_experimental_option('localState',chromeLocalStatePrefs)
    driver = webdriver.Chrome(options=chrome_options, executable_path=r'chromedriver.exe')
    driver.get("https://www.festfoods.com/shop#!/?q={}".format(product))
    #driver.get("https://www.festfoods.com/my-store/store-locator")
    
    price_line = re.compile('\$[0-9]+\.[0-9][0-9]$')
    size_letters_and_numbers = re.compile('\S*(\S*([a-zA-Z]\S*[0-9])|([0-9]\S*[a-zA-Z]))\S*')
    trailing_periods = re.compile('\.(?!\d)')
    
    wait = WebDriverWait(driver, 30)
    #print("I have just declared the wait and am now about to wait until the first div on the page is present")
    element_present = expected_conditions.presence_of_all_elements_located((By.XPATH, "/html/body/div[1]"))    
    
    try:
        wait.until(element_present);
        #print("found the page contents")
    except TimeoutException:
        print("Could not scan FestivalFoods for:", end = " ")
        print("the first div on the page")
        print(product)
        print("\n")
        #time.sleep(100) #sleep here
        driver.close()        
                
    
    #wait.until(expected_conditions.presence_of_all_elements_located((By.XPATH, "/html/body/div[1]/div/header/div/nav/section[1]/div/div/div[6]/div/span[3]/a[1]"))); # sign in 
    wait.until(expected_conditions.presence_of_all_elements_located((By.XPATH, "/html/body/div[3]/div[3]/div[2]/div/div/div[2]/div/form/div[3]/a"))); # sign in   
    #/html/body/div[3]/div[3]/div[2]/div/div/div[2]/div/form/div[3]/a


    #sign_in = driver.find_element_by_xpath("/html/body/div[1]/div/header/div/nav/section[1]/div/div/div[6]/div/span[3]/a[1]")
    sign_in = driver.find_element_by_xpath("/html/body/div[3]/div[3]/div[2]/div/div/div[2]/div/form/div[3]/a")  
    
    driver.execute_script("arguments[0].click();", sign_in) #click sign in    
    #wait.until(expected_conditions.presence_of_all_elements_located((By.XPATH, "/html/body/div[1]/div/main/div/div[2]/article/ul/li/div/div/div[3]/div/div/form/div[1]/div[2]/label/input"))); #username
    wait.until(expected_conditions.presence_of_all_elements_located((By.XPATH, "/html/body/div[1]/div/div[2]/section/div[2]/div[2]/div/div/div/div/div/div/div/div/div[3]/div/div[1]/form/div[1]/label/input"))); #username
    #username = driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div[2]/article/ul/li/div/div/div[3]/div/div/form/div[1]/div[2]/label/input")
    username = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/section/div[2]/div[2]/div/div/div/div/div/div/div/div/div[3]/div/div[1]/form/div[1]/label/input")
    username.send_keys('xyoshqx@hotmail.com')
    #password = driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div[2]/article/ul/li/div/div/div[3]/div/div/form/div[1]/div[3]/label[1]/input")
    password = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/section/div[2]/div[2]/div/div/div/div/div/div/div/div/div[3]/div/div[1]/form/div[2]/label[1]/input")
    password.send_keys('festivalfoods')
    #sign_in2 = driver.find_element_by_xpath("/html/body/div[1]/div/main/div/div[2]/article/ul/li/div/div/div[3]/div/div/form/div[2]/button")
    sign_in2 = driver.find_element_by_xpath("/html/body/div[1]/div/div[2]/section/div[2]/div[2]/div/div/div/div/div/div/div/div/div[3]/div/div[1]/form/div[3]/button")
    driver.execute_script("arguments[0].click();", sign_in2)
    #time.sleep(100) #sleep here
    
    
    try:
        soup = BeautifulSoup(driver.page_source, 'lxml')
        store_cards = soup.find_all('div', class_='all-stores-info col-md-4 col-sm-12')
        for store in store_cards:
            if store.find('h3').getText() == "Madison":
                make_this_my_store_button = driver.find_elements_by_xpath("//button[@class='btn btn-small btn-make-store']")
                driver.execute_script("arguments[0].click();", make_this_my_store_button[18])
        #print("store has been selected")
    except TimeoutException:
        print("store selection failed")
        #return
        driver.close()        
    
    #testing going to a specific page
    #driver.get("https://www.festfoods.com/shop#!/?limit=48&page=168")
    #testing searching for a specific product
    driver.get("https://www.festfoods.com/shop#!/?limit=48&q=quaker%20oats%20rolled%20overnight%20oats&search_option_id=product")
    
    # click Shop
    # try: 
        # shop = driver.find_element_by_xpath("/html/body/div[1]/div/header/div/nav/section[2]/section[1]/div/div/div[4]/section/a/div[2]")
        # driver.execute_script("arguments[0].click();", shop)
        # per_page_string = "/html/body/div[1]/div/main/section/div[6]/div/div[1]/div/div/div[3]/label[1]/span[2]/button/span[1]"
        # wait.until(expected_conditions.presence_of_all_elements_located((By.XPATH, per_page_string)));
        # per_page = driver.find_element_by_xpath(per_page_string)       
        # driver.execute_script("arguments[0].click();", per_page)
        # forty_eight = driver.find_element_by_xpath("/html/body/div[1]/div/main/section/div[6]/div/div[1]/div/div/div[3]/label[1]/span[2]/span/span/span[5]/a")
        # driver.execute_script("arguments[0].click();", forty_eight)
        # #print("shop has been clicked")
    # except TimeoutException:
        # print("shop could not be clicked")
        # driver.close()
      
        
    #element_present = expected_conditions.presence_of_all_elements_located((By.XPATH, "/html/body/div[1]/div/main/section/div[6]/div/div[3]/div[2]/div[2]/ul/li[1]/div/div[2]/div[2]/div[1]/a")) #product list
    element_present = expected_conditions.presence_of_all_elements_located((By.XPATH, "/html/body/div[1]/div/section/article/section/div/div[2]/div/div/div[1]/div/div/div[5]/div[3]/div[2]/div[2]/ul/li[1]/div/div[2]/div[1]/a/img")) #product list
    
    try:
        wait.until(element_present);      
        #print("found product list")
    except TimeoutException:
        print("Could not scan FestivalFoods for:", end = " ")
        print("the product results")
        print(product)
        print("\n")
        driver.close()  
    
    time.sleep(3)
    
    #mydivs = soup.findAll("div", {"class": "fp-btn-icon fp-btn-next"})
    
    soup = BeautifulSoup(driver.page_source, 'lxml')
    products_not_on_sale = soup.select('li', class_="fp-item     ")
    products_on_sale = soup.select('li', class_="fp-item    fp-item-fixed_price ")    
        
    count = 0
    
    for product in products_not_on_sale:        
        
        items = product.select('div[class="fp-item-detail"]')        
        
        if len(items) > 0:
            
            for item in items:
                count += 1
                #print('I am in the first page of results about to get the products (not on sale)')
                new_product = Product()
                new_product.name = item.select('a')[0].getText()
                #print("the product name in first page (not on sale) is: " + new_product.name)
                price = item.select('span[class="fp-item-base-price"]')[0].getText().replace('$', '').split("for")
                if len(price) == 1:
                    new_product.price = Decimal(price[0])
                else: 
                    new_product.price = (Decimal(price[0]) / Decimal(price[1]))
                    #print("new_product.price in else statement is: " + new_product.price)
                    print("new_product.price in else statement is: " + str(new_product.price))
                #need to handle "5 for $5.00".
                size = item.select('span[class="fp-item-size"]')[0].getText().split(" ")
                
                #print("my link is as follows: ")                                
                new_product.url = "https://www.festfoods.com" + item.select('a')[0].get('href')
                #print(item.select('a')[0].get('href'))                
                
                #todo: handle if more than 2 elements. example: "144 fl oz".
                if len(size) == 1:
                    new_product.size = [Decimal(1), size[0]]
                else:
                    new_product.size = [Decimal(size[0]), size[1]]
                new_product.price_per = [round(new_product.price / new_product.size[0], 2), new_product.size[1]]                
                new_product.price_per = str(new_product.price_per).replace('Decimal', '').replace('\'', '').replace('[', '').replace(']', '').replace(')', '').replace('(', '').replace(',', '/')
                new_product.size = str(new_product.size).replace('Decimal', '').replace('\'', '').replace('[', '').replace(']', '').replace(')', '').replace('(', '').replace(',', '')
                #print('I am in the first page of results about to click next (not on sale)')
                new_product.website = 'FestivalFoods'
                list_of_products.append(new_product)
    
    count = 0
    
    for product in products_on_sale:        
        
        items_list = product.select('div[class="fp-item-detail fp-is-item-detail-sale"]')

        #print("I have just tried to populate items_list")
        
        if len(items_list) > 0:
            
            for item in items_list:
                count += 1
                #print('I am in the first page of results about to get the products (on sale)')
                new_product = Product()                
                new_product.name = item.select('a')[0].getText()
                #print("the product name in first page (on sale) is: " + new_product.name)
                price = item.select('span', class_='fp-item-sale-date')[0].getText()
                price_split = price.split(' (')
                
                new_product.url = "https://www.festfoods.com" + item.select('a')[0].get('href')
                
                if len(price_split) == 2:
                    price = price_split[0]
                    if not price_line.match(price):
                        continue
                else:
                    continue
                new_product.price = Decimal(price.replace('$', ''))
                #print("the product price in first page (on sale) is: " + str(new_product.price))
                size = item.select('span[class="fp-item-size"]')[0].getText().split(" ")
                #print("I am about to go into if statement (on sale page 1)")
                #print("the size in first page before if statement (on sale) is: " + str(size))
                
                if len(size) == 1:
                    #print("I am in if statement (on sale page 1)")
                    new_product.size = [Decimal(1), size[0]]
                else:
                    #print("I am in else statement (on sale page 1)")
                    new_product.size = [Decimal(size[0]), size[1]]                    
                    
                #print("the size in first page (on sale) is: " + str(size)) # ['lb']                
                new_product.price_per = [round(new_product.price / new_product.size[0], 2), new_product.size[1]]                
                new_product.price_per = str(new_product.price_per).replace('Decimal', '').replace('\'', '').replace('[', '').replace(']', '').replace(')', '').replace('(', '').replace(',', '/')                
                new_product.size = str(new_product.size).replace('Decimal', '').replace('\'', '').replace('[', '').replace(']', '').replace(')', '').replace('(', '').replace(',', '')
                #print("the product size in first page (on sale) is: " + str(new_product.size))
                #print("the product price per in first page (on sale) is: " + str(new_product.price_per))
                #print('I am in the first page of results about to click next (on sale)')
                new_product.website = 'FestivalFoods'
                list_of_products.append(new_product)
                
    #nextButtonLink = driver.find_element_by_xpath('/html/body/div[1]/div/main/section/div[6]/div/div[3]/div[3]/div/div/ul/li[11]/a')    
    nextButtonLink = driver.find_element_by_xpath('/html/body/div[1]/div/section/article/section/div/div[2]/div/div/div[1]/div/div/div[5]/div[3]/div[3]/div/div/ul/li[11]/a')  
    

    
    #pageCount = 2
    pageCount = 169 #testing
    
    #time.sleep(10)    
    
    while True:        
        
        # go to the next page
        try: 
            nextPageLink = driver.find_element_by_link_text(str(pageCount))
            #signUpForOurMobileClubButton = driver.find_element_by_xpath("/html/body/div[1]/div/footer/div[1]/div/div[2]/ul/li[1]/button/span")
            gasRewards = driver.find_element_by_xpath("/html/body/div[1]/div/footer/div[1]/div/div/div[3]/div/ul/li[1]/a")
                        
            # click next
            #time.sleep(random.uniform(1.5, 15.5)) # detected on page 68
            #time.sleep(random.uniform(1.5, 60)) # detected at page 12
            time.sleep(random.uniform(10, 60))
            #ActionChains(driver).move_to_element(signUpForOurMobileClubButton).click(nextPageLink).perform() 
            ActionChains(driver).move_to_element(gasRewards).click(nextPageLink).perform() 
            
            #if pageCount == 3:
            if pageCount == 100:
                driver.refresh()
                time.sleep(10)
            elif pageCount == 120:
                driver.refresh()
                time.sleep(10)
            elif pageCount == 140:
                driver.refresh()
                time.sleep(10)
            elif pageCount == 160:
                driver.refresh()
                time.sleep(10)
            elif pageCount == 180:
                driver.refresh()
                time.sleep(10)
            elif pageCount == 200:
                driver.refresh()
                time.sleep(10)
            elif pageCount == 300:
                driver.refresh()
                time.sleep(10)
            elif pageCount == 400:
                driver.refresh()
                time.sleep(10)
            elif pageCount == 500:
                driver.refresh()
                time.sleep(10)
            elif pageCount == 600:
                driver.refresh()
                time.sleep(10)
            
            print('I have just clicked next')
            
        #except TimeoutException:  
        
        #except InvalidSessionIdException as sessionE:          
            #print("I may be seeing no products. Error: " + sessionE)
            #driver.refresh()
            #time.sleep(10)
        
        except NoSuchElementException:
            #time.sleep(10)            
            print("I've either reached the end of the products or I had some trouble finding the page link.")
            driver.close() 
            
        #time.sleep(10)
        #element_present = expected_conditions.presence_of_all_elements_located((By.XPATH, "/html/body/div[1]/div/main/section/div[6]/div/div[3]/div[2]/div[2]/ul/li[1]/div/div[2]/div[2]/div[1]/a")) # product list
        element_present = expected_conditions.presence_of_all_elements_located((By.XPATH, "/html/body/div[1]/div/section/article/section/div/div[2]/div/div/div[1]/div/div/div[5]/div[3]/div[2]/div[2]/ul/li[1]/div/div[2]/div[1]/a/img")) # product list        
    
        try:
            wait.until(element_present);
            #print("found product list")
        except TimeoutException:
            print("Could not scan FestivalFoods for page:", end = " ")
            print(str(pageCount))
            driver.close()  
        
        pageCount += 1
        print("next button found in while statement and I'm on page " + str(pageCount))
        
        time.sleep(3)
        
        soup = BeautifulSoup(driver.page_source, 'lxml')
        products_not_on_sale = soup.select('li', class_="fp-item     ")
        products_on_sale = soup.select('li', class_="fp-item    fp-item-fixed_price ")    
            
        #time.sleep(10)
        #print('I have just slept for 10 seconds')
        count = 0
        
        for product in products_not_on_sale:        
                        
            items = product.select('div[class="fp-item-detail"]')
            
            if len(items) > 0:
                #time.sleep(10)
                
                for item in items:
                    count += 1
                    #print('I am on the second page of results')
                    new_product = Product()
                    new_product.name = item.select('a')[0].getText()
                    #print('the product name in 2nd page (not on sale) is: ' + new_product.name)
                    #print('the product price in 2nd page (not on sale) just from XPath is: ' + item.select('span[class="fp-item-base-price"]')[0].getText().replace('$', ''))
                    
                    price = item.select('span[class="fp-item-base-price"]')[0].getText().replace('$', '')                                
                    price_regex = re.findall("for", price)
                    if price_regex:
                        #print("the product price in 2nd page (not on sale) in price variable inside if statement is: "  + price)
                        new_product.price = price.replace('for', '').split(" ")
                        new_product.price = str([round(Decimal(new_product.price[0]) / Decimal(new_product.price[2]), 2)]).replace('Decimal', '').replace('\'', '').replace('[', '').replace(']', '').replace(')', '').replace('(', '') # divide the first item in the array by the third and remove the word 'Decimal', (), '', and [].
                        #print("the product price in 2nd page (not on sale) inside if statement is: " + new_product.price)
                        new_product.price = Decimal(new_product.price)
                    else:
                        #print("the product price in 2nd page (not on sale) in price variable inside if statement else block statement is: "  + price) #
                        new_product.price = Decimal(price)                    
                    
                    #print("The product price in second page not on sale is: " + str(new_product.price))
                    
                    new_product.url = "https://www.festfoods.com" + item.select('a')[0].get('href')
                    
                    try:
                        size = item.select('span[class="fp-item-size"]')[0].getText().split(" ")
                    except IndexError:
                       #size = []
                       #size = ["ct"]
                       #size[0] = "ct"
                       size = ["ct"]
                                        
                    if size[0].endswith("."):
                       #print("I'm inside if block")
                       old = "."
                       new = ""
                       maxreplace = 1
                       size[0] = new.join(size[0].rsplit(old, maxreplace))
                       
                    #if not size[0].isnumeric():
                    if size_letters_and_numbers.match(size[0]):                    
                       size = re.split('(\d+)',size[0])
                       #size.pop(0)
                       size[0] = size[1]
                       size[1] = size[2]
                    
                    #print("size in not on sale is: " + str(size))
                    
                    if '/' in size[0] and '.' in size[0]:                    
                       #print("regex matched")
                       size_temp = re.split('/',size[0])                      
                       #print("size[0] before multiplication is: " + size[0])
                       #print("size_temp is: " + str(size0))                      
                       size[0] = Decimal(size_temp[0]) * Decimal(size_temp[1])
                       #print("size[0] after multiplication is: " + str(size[0]))
                    
                    if '/' in size[0]:
                       #print("I'm inside symbol if block")
                       size[0] = float(sum(Fraction(s) for s in size[0].split()))
                       size[0] = Decimal(size[0])
                    
                    if len(size) == 1:
                        
                        new_product.size = [Decimal(1), size[0]]
                    else:
                        new_product.size = [Decimal(size[0]), size[1]]
                    #print("the product size on second page from new_product.size[0] is: " + str(new_product.size[0]))   
                    
                    new_product.price_per = [round(new_product.price / new_product.size[0], 2), new_product.size[1]]
                    new_product.price_per = str(new_product.price_per).replace('Decimal', '').replace('\'', '').replace('[', '').replace(']', '').replace(')', '').replace('(', '').replace(',', '/')
                    new_product.size = str(new_product.size).replace('Decimal', '').replace('\'', '').replace('[', '').replace(']', '').replace(')', '').replace('(', '').replace(',', '')
                    new_product.website = 'FestivalFoods'
                    list_of_products.append(new_product)
        
            
        count = 0
        
        for product in products_on_sale:
                    
            #time.sleep(10)
            items_list = product.select('div[class="fp-item-detail fp-is-item-detail-sale"]')
            
            if len(items_list) > 0:
                #time.sleep(10)
                
                for item in items_list:
                    count += 1
                    #print('I am on the second page of results')
                    new_product = Product()
                    new_product.name = item.select('div[class="fp-item-name notranslate"]')[0].select('a')[0].getText()
                    # print(new_product.name)
                    price = item.select('span', class_='fp-item-sale-date')[0].getText()
                    price_split = price.split(' (')
                    
                    new_product.url = "https://www.festfoods.com" + item.select('a')[0].get('href')
                    
                    if len(price_split) == 2:
                        price = price_split[0]
                        if not price_line.match(price):
                            continue
                    else:
                        continue
                    new_product.price = Decimal(price.replace('$', ''))
                                        
                    try:
                        size = item.select('span[class="fp-item-size"]')[0].getText().split(" ")
                    except IndexError:                                                                        
                        size = ["ct"]
                        
                    if size[0].endswith("."):
                       #print("I'm inside if block trailing period for size, on sale")
                       old = "."
                       new = ""
                       maxreplace = 1
                       size[0] = new.join(size[0].rsplit(old, maxreplace))
                                        
                    if size_letters_and_numbers.match(size[0]):
                       size = re.split('(\d+)',size[0])
                       size[0] = size[1]
                       size[1] = size[2]                        
                       
                    if '/' in size[0] and '.' in size[0]:                    
                       #print("regex matched")
                       size_temp = re.split('/',size[0])                      
                       #print("size[0] before multiplication is: " + size[0])
                       #print("size_temp is: " + str(size0))                      
                       size[0] = Decimal(size_temp[0]) * Decimal(size_temp[1])
                       #print("size[0] after multiplication is: " + str(size[0]))
                    
                    if '/' in size[0]:
                       #print("I'm inside symbol if block")
                       size[0] = float(sum(Fraction(s) for s in size[0].split()))
                       size[0] = Decimal(size[0])
                    
                    if len(size) == 1:
                        new_product.size = [Decimal(1), size[0]]
                    else:
                        new_product.size = [Decimal(size[0]), size[1]]                    
                    
                    new_product.price_per = [round(new_product.price / new_product.size[0], 2), new_product.size[1]]
                    new_product.price_per = str(new_product.price_per).replace('Decimal', '').replace('\'', '').replace('[', '').replace(']', '').replace(')', '').replace('(', '').replace(',', '/')
                    new_product.size = str(new_product.size).replace('Decimal', '').replace('\'', '').replace('[', '').replace(']', '').replace(')', '').replace('(', '').replace(',', '')
                    
                    new_product.website = 'FestivalFoods'
                    list_of_products.append(new_product)
    
    
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'X-Requested-With': 'XMLHttpRequest',}