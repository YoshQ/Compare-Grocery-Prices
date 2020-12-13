from bs4 import BeautifulSoup
from selenium import webdriver
from Product import Product
from decimal import Decimal
import re
import keyword
# import result
import json 
#from Scraper import product1
import time
    
product1 = "Potatoes"
    

def scrape_Amazon_search_results(list_of_products, product):
           
    NoneType = type(None)
    
    ratings_line = re.compile('[0-5]\.[0-9] out of 5 stars')
    num_reviews_line = re.compile('[0-9]+')
    price_line = re.compile('\$[0-9]+\.[0-9][0-9]\$[0-9]+\.[0-9][0-9]')
    price_per_line = re.compile('[(]\$[0-9]+\.[0-9][0-9][/](Fl Oz|Ounce|Count)[)]')
    availability_line = re.compile('^(In stock on|Only [0-9]+ left in stock)')
    earliest_arrival_line = re.compile('^(Get it as soon as)')
    shipping_costs_line = re.compile('(^(FREE Shipping|FREE Shipping by Amazon)|(\$[0-9]+\.[0-9][0-9] shipping))') # this only seems to be matching the first part before any of the pipes.
    ## begin josh added
    #dropped_lines = re.compile('^(FREE Shipping on orders over|Save 5% more|FREE delivery with Prime| \[data|Sponsored|These are ads for products you|Learn more about Sponsored Products|   |More Buying Choices|Only [0-9]+ left in stock]|\[data|metrics\.attach|Ad feedback|Save more with Subscribe & Save|Price and other details may vary based on size and color)')
    #dropped_lines = re.compile('^(FREE Shipping on orders over|Save 5% more|FREE delivery with Prime| \[data|Sponsored|These are ads for products you|Learn more about Sponsored Products|   |More Buying Choices|Only [0-9]+ left in stock]|\[data|metrics\.attach|Ad feedback|Save more with Subscribe & Save|Price and other details may vary based on size and color)')
    #dropped_names = re.compile('Sponsored|Price and other details may vary based on size and color') 
    dropped_names = re.compile('Sponsored') 
    #dropped_lines = re.compile('^(FREE Shipping on orders over|Save 5% more|FREE delivery with Prime| \[data|Sponsored|These are ads for products you|Learn more about Sponsored Products|   |More Buying Choices|Only [0-9]+ left in stock]|\[data|metrics\.attach|Ad feedback|Save more with Subscribe & Save)')    
    product_name = re.compile(product1)
    
    url = "https://www.amazon.com/s?k={}&ref=nb_sb_noss_2".format(product)
    driver = webdriver.Chrome(executable_path=r'chromedriver.exe')
    
    #Code taken from here: https://stackoverflow.com/questions/27652543/how-to-use-python-requests-to-fake-a-browser-visit
    #Code taken from here: https://stackoverflow.com/questions/55609049/python-beautifulsoup-selenium-scraper
    
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    results = soup.select('div', class_='s-main-slot s-result-list s-search-results sg-row')
    #                                      s-main-slot s-result-list s-search-results sg-row
    #results = soup.select('div', class_='sg-col-20-of-24 s-result-item s-asin sg-col-0-of-12 sg-col-28-of-32 sg-col-16-of-20 sg-col sg-col-32-of-36 sg-col-12-of-16 sg-col-24-of-28')    
    
    #printme = json.dumps(results) 
  
    # printing result as string 
    #print ("\n", type(printme)) 
    #print ("final string = ", printme) 
    
    
    
    for num in range(50):
        
        
        
        new_product = Product()
        
        products = results[0].select('div[data-index="{}"]'.format(num))
        
        #print(products.prettify())
        
        #if (products[0].select('span', class_='a-size-base-plus a-color-base a-text-normal'))
        names = products[0].select('span', class_='a-size-base-plus a-color-base a-text-normal') #calling all spans
        information = names[0].getText().split('\n')
        
        # print(information)
        # ['', '', '', '', 'Price and other details may vary based on size and color', '', '', '', '']
        
        while '' in information:
            information.remove('')
        
        for info in information:
            try:
                info.encode(encoding='utf-8').decode('ascii')
            except UnicodeDecodeError:
                continue
        
        # print(information)
        # ['Price and other details may vary based on size and color']
        
        count = 0
        
        for info in information:
            count += 1
            #print(info[0]) #I
            # each spot in info is a single character.
            # print('I am in for loop ' + str(count)) # I am in for loop 1
            #if dropped_names.match(info): #
            #if dropped_names.findall(info): # this seems to work
            #if not dropped_names.match(info): # it doesn't pass this spot for any of them it seems
                #print('I am in dropped_names if statement ' + str(count))
                #exit
                #continue
            #elif ratings_line.match(info):
            print(info + ". time through for loop: " + str(count)) # Russet Potato, One Large 1
            if ratings_line.match(info):
                new_product.rating = info
            elif num_reviews_line.match(info):
                new_product.number_of_reviews = info
            elif price_line.match(info):
                info = info.split("$")
                new_product.price = Decimal(info[1])
            elif price_per_line.match(info):
                info = info.split("/")
                info[0] = info[0].replace("(", "")
                info[0] = info[0].replace("$", "")
                info[1] = info[1].replace(")", "")
                info[0] = Decimal(info[0])
                new_product.price_per = info
            elif availability_line.match(info):
                new_product.availability = info
            elif earliest_arrival_line.match(info):
                new_product.earliest_arrival = info
            elif shipping_costs_line.match(info):
                new_product.shipping_cost = info
                # print(info[0])
                # F
                # print(info[1])
                # R                                
                # print(info[2])
                # E
                # in here info is the shipping cost
            #elif not dropped_lines1.match(info):
                #continue
            #elif not dropped_lines11.match(info):
                #print('this is my test: ' + info) # not getting here all the time
                # print('I am new product ' + new_product.name) # Idahoan Buttery Homestyle Mashed Potatoes, Made with Gluten-Free 100% Real Idaho Potatoes, 1.5 oz (Pack of 10)                
            #elif not dropped_lines.findall(info) and product_name.findall(info): # this works but trying to get a little bit more specific
            #elif not dropped_lines.findall(info) and product_name.search(info): # this works but trying to get a little less specific
            #elif not dropped_names.findall(info) and product_name.search(info): # this works but trying to get a little less specific
            elif not dropped_names.findall(info): # this works but trying to get a little less specific
            #elif not dropped_lines.findall(info) # this works
            #elif not info.findall(dropped_lines):
            #elif not dropped_lines.match(info,0,200):
            #elif not dropped_lines.findall(info):
                # print('info ' + str(count) + ' : ' + info) # this prints name
                new_product.name = info
          
        # if not isinstance(new_product.name, NoneType) and not new_product.price == "" and not new_product.price_per == "" and not isinstance(new_product.price_per, NoneType): # this works
        #if not isinstance(new_product.name, NoneType) and not new_product.price == "": # this returned blank name but somehow populated other fields
        if not new_product.name == "" and not new_product.price == "":
        # isinstance(price_per_line.name, NoneType):
        #  and not new_product.name == ""
            new_product.website = "Amazon"
            list_of_products.append(new_product)
        
        # begin josh added
         
        #print(list_of_products)
        #print(information)
        
        #df_bs = pd.DataFrame(list_of_products,columns=['City','Country','Notes'])
        #df_bs.set_index('Country',inplace=True)
        #df_bs.to_csv('beautifulsoup.csv')
                
        #data = {keyword:[keyword,str(results[num]),]}
        
        #with open(data, "w", encoding="utf-8") as f:
            #f.write(html)
        
        # convert dictionary into string 
        # using json.dumps() 
        #result = json.dumps(data)        
        
        
        # result = json.dumps(information) # this one is good
        #result = json.dumps(info) # this prints FREE Shipping on your first order shipped by Amazon
  
        # printing result as string 
        #print ("\n", type(result)) 
        #print ("final string = ", result, "\n") # this one is good
        
        ## data = {keyword:[keyword,str(result),title,ASIN,score,reviews,PRIME,datetime.datetime.today().strftime("%B %d, %Y")]}
        ## print(data)
        
        ## end josh added
        
        
        
    time.sleep(100) #sleep here
    driver.close()
    
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
    'X-Requested-With': 'XMLHttpRequest',} #permissions for bot to access website