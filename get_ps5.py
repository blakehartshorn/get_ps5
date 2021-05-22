#!/usr/bin/python3

import sys, threading, requests, time, os
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

display = Display(visible=0, size=(1920, 1080))
display.start()

firefoxOptions = Options()
firefoxOptions.add_argument("-headless")

stores = {
    'Amazon': False,
    'BestBuy': False,
    'Gamestop': False,
    'PlaystationDirect': False,
    'Target': False,
    'Walmart': False,
}

def check_store(store):

    if store == "Amazon":
        amazon = webdriver.Firefox(options=firefoxOptions, service_log_path=os.path.devnull)

        try:
            amazon.get("https://smile.amazon.com/gp/product/B08FC5L3RG")
            element = amazon.find_element_by_id("availability")
            availability = element.text
        except:
            availability = "nope"

        amazon.quit()

        if "Currently unavailable." not in availability:
            stores['Amazon'] = "https://smile.amazon.com/gp/product/B08FC5L3RG"

    elif store == "BestBuy":
        bestbuy = webdriver.Firefox(options=firefoxOptions, service_log_path=os.path.devnull)

        try:
            bestbuy.get("https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149")
            element = bestbuy.find_element_by_class_name("fulfillment-add-to-cart-button")
            availability = element.text
        except:
            availability = "nope"
        bestbuy.quit()

        if "Sold Out" not in availability:
            stores['BestBuy'] = "https://www.bestbuy.com/site/sony-playstation-5-console/6426149.p?skuId=6426149"

    elif store == "Gamestop":
        gamestop = webdriver.Firefox(options=firefoxOptions, service_log_path=os.path.devnull)

        try:
            gamestop.get("https://www.gamestop.com/video-games/playstation-5/consoles/products/playstation-5/11108140.html")
            time.sleep(10)
            element = gamestop.find_element_by_class_name("add-to-cart")
            availability = element.text
        except:
            availability = "nope"
        gamestop.quit()

        if "NOT AVAILABLE" not in availability:
            stores['Gamestop'] = "https://www.gamestop.com/video-games/playstation-5/consoles/products/playstation-5/11108140.html"

    elif store == "PlaystationDirect":
        try:
            r = requests.get("https://direct.playstation.com/en-us/hardware/ps5",timeout=60)
            availability = r.text
        except:
            availability = "none"
        if '                     <div class="out-stock-wrpr js-out-stock-wrpr hide"> <p class="sony-text-body-1">Out of Stock</p> </div>' not in availability:
            stores['PlaystationDirect'] = "https://direct.playstation.com/en-us/hardware/ps5"

    elif store == "Target":
        target = webdriver.Firefox(options=firefoxOptions, service_log_path=os.path.devnull)

        try:
            target.get("https://www.target.com/p/playstation-5-console/-/A-81114595")
            elements = target.find_elements_by_tag_name("div")
            for element in elements:
                try:
                    if "Sold out" in element.text:
                        target.close()
                        return
                    else:
                        continue
                except:
                    continue
        except:
            pass
        target.quit()
        stores['Target'] = "https://www.target.com/p/playstation-5-console/-/A-81114595"

    elif store == "Walmart":
        walmart = webdriver.Firefox(options=firefoxOptions, service_log_path=os.path.devnull)

        try:
            walmart.get("https://www.walmart.com/ip/Sony-PlayStation-5-Video-Game-Console/363472942")
            element = walmart.find_element_by_class_name("display-block-xs")
            availability = element.text
        except:
            availability = "nope"
        walmart.quit()

        if "Out of stock" not in availability:
            stores['Walmart'] = "https://www.walmart.com/ip/Sony-PlayStation-5-Video-Game-Console/363472942"

threads = list()
for store in stores:
    x = threading.Thread(target=check_store, args=(store,))
    threads.append(x)
    x.start()

for index, thread in enumerate(threads):
    thread.join()

display.stop()
critical = False
for store in stores:
    if stores[store]:
        print(f"Check {store}: {stores[store]}")
        critical = True

if critical:
    sys.exit(2)
else:
    print("PS5 out of stock everywhere.")
    sys.exit(0)
