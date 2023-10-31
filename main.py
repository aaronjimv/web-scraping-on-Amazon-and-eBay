from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from selenium.webdriver.chrome.service import Service
from connection import *
from products import Products
from threading import Thread

def get_soup(url):
    '''
    Retrieves and returns the BeautifulSoup object of a given URL.

    Parameters:
        url (str): The URL to scrape.

    Returns:
        BeautifulSoup: The BeautifulSoup object containing the parsed HTML content of the URL.
    '''
    options = webdriver.ChromeOptions() 
    options.add_experimental_option('excludeSwitches', ['enable-logging']) 
    service = Service('driver/chromedriver.exe') 
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    sleep(1)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    driver.close()

    return soup

def get_amazon_object(soup):
    '''
    Extracts and returns the selected Amazon product URL and price from the given Amazon search results page.

    Parameters:
        soup (BeautifulSoup): The BeautifulSoup object of the Amazon search results page.

    Returns:
        tuple: A tuple containing the Amazon product URL (str) and price (str).
    '''
    products = soup.find_all('div', {'class':'s-result-item'})
    for i, product in enumerate(products):
        try:
            name = product.find('span', {'class':'a-size-medium a-color-base a-text-normal'}).text
            price = product.find('span', {'class':'a-price'}).text
            print(f'{i+1}. {name}. Precio: {price}')
        except:
            pass
    selected = int(input("\nChooses the Amazon product: "))
    amazon_url = products[selected-1].find('a', {'class':'a-link-normal s-no-outline'}).attrs['href']
    amazon_price = products[selected-1].find('span', {'class':'a-price'}).text
    return amazon_url, amazon_price.split('$').pop().replace(',', '')


def get_ebay_object(soup):
    '''
    Extracts and returns the selected eBay product URL and price from the given eBay search results page.

    Parameters:
        soup (BeautifulSoup): The BeautifulSoup object of the eBay search results page.

    Returns:
        tuple: A tuple containing the eBay product URL (str) and price (str).
    '''
    products = soup.find_all('li', {'class':'s-item s-item__pl-on-bottom'})
    for i, product in enumerate(products):
        try:
            name = product.find('div', {'class':'s-item__title'}).text
            price = product.find('span', {'class':'s-item__price'}).text
            print(f'{i+1}. {name}. Precio: {price}')
        except:
            pass
    selected = int(input("\nChooses the eBay product: "))
    ebay_url = products[selected-1].find('a', {'class':'s-item__link'}).attrs['href']
    ebay_price = products[selected-1].find('span', {'class':'s-item__price'}).text
    return ebay_url, ebay_price[3:]

def check_price():
    '''
    Periodically checks the prices of products in the database on Amazon and eBay.
    Prints price changes and comparisons.
    '''
    while True:
        products = Products(None, None, None, None, None).get_products()
        for product in products:
            try:
                amazon_soup = get_soup("https://www.amazon.com"+product[2])
                ebay_soup = get_soup(product[3])

                new_amazon_price = amazon_soup.find('span', {'class':'a-offscreen'}).text
                new_ebay_price = ebay_soup.find('span', {'class':'ux-textspans ux-textspans--SECONDARY ux-textspans--BOLD'}).text

                print(f'\nProduct {product[1].replace("+", " ")}: ')
                print(f'Amazon: Old price: {str(product[4])} New price: {new_amazon_price.split('$').pop().replace(',', '')}')
                print(f'eBay: Old price: {str(product[5])} New price: {new_ebay_price[4:]}')

                if float(new_amazon_price.split('$').pop().replace(',', '')) < float(product[4]):
                    print(f'The product {product[1].replace("+", " ")} price dropped on Amazon')
                if float(new_ebay_price[4:]) < float(product[5]):
                    print(f'The product {product[1].replace("+", " ")} price dropped on eBay')
                if float(new_amazon_price.split('$').pop().replace(',', '')) < float(new_ebay_price[4:]):
                    print(f'The product {product[1].replace("+", " ")} It has a lower price on Amazon')
                if float(new_ebay_price[4:]) < float(new_amazon_price.split('$').pop().replace(',', '')):
                    print(f'The product {product[1].replace("+", " ")} It has a lower price on eBay')
                
                sleep(3600)
            except:
                print("Cambio en el html de la pagina!!!")

def init():
    '''
    Initializes the web scraping process.
    Asks the user if they want to register a new product, then starts the price monitoring thread.
    '''
    print(" -- Web Scraping -- \n")
    response = input("You want to register a new product? y/n: ")

    if response == "y":
        name = input("Enter the name of the product to search: ").replace(" ", "+")
        amazon_result_url = f'https://www.amazon.com/s?k={name}&__mk_es_US=ÅMÅŽÕÑ&crid=2B6YI9ANUULVP&sprefix=nintendo+switch%2Caps%2C131&ref=nb_sb_noss_2'
        ebay_result_url = f'https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2380057.m570.l1311&_nkw={name}&_sacat=0'

        amazon_soup = get_soup(amazon_result_url)
        amazon_url, amazon_price = get_amazon_object(amazon_soup)
        
        ebay_soup = get_soup(ebay_result_url)
        ebay_url, ebay_price = get_ebay_object(ebay_soup)
        
        products = Products(name, amazon_url, ebay_url, amazon_price, ebay_price)
        print(products.save_products())

    thread = Thread(target=check_price)
    thread.start()

if __name__ == "__main__":
    init()