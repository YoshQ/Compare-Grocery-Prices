from bs4 import BeautifulSoup
from selenium import webdriver
from Amazon_Products_Scraper import scrape_Amazon_search_results, product1
from PickNSave_Products_Scraper import scrape_PickNSave_search_results
from FestivalFoods_Products_Scraper import scrape_FestivalFoods_search_results
from Product import *
from difflib import SequenceMatcher
import time

search_for_these = []
# product1 = ("Potatoes", 5,"lb")
#product1 = "Potatoes" #was using this one

search_for_these.append(product1) 

unique_item = True
absolute_cheapest = True
cheapest_per_count = True

for product in search_for_these:
    
    list_of_names = []
    price_checker = {}
    list_of_products = []
    shorter_item = ""
    final_list = []
    count = 0
    
#    scrape_Amazon_search_results(list_of_products, product)
#   scrape_PickNSave_search_results(list_of_products, product[0])
    scrape_FestivalFoods_search_results(list_of_products, product[0])
    
    for x in list_of_products:
        
        count += 1 #this works
        
        #Product.printProduct
        print("Product " + str(count) + ":")
        #print("The following is the printProduct method")
        Product.printProduct(x)        
        print(" ")