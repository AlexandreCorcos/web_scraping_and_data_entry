from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

URL_ZILLOW = "https://appbrewery.github.io/Zillow-Clone/"
URL_DRIVE = "https://docs.google.com/forms/d/e/1FAIpQLSfEhztyUq3UoSrDzWFkQpjkLxukHkStrnJdyrEj-ag2n-Ua1Q/viewform"

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

response = requests.get(URL_ZILLOW, headers=header)
zillow_page = response.text

soup = BeautifulSoup(zillow_page, "html.parser")


# ADDRESS SCRAPING
all_address = soup.find_all("address", {"data-test": "property-card-addr"})
address_list = [address.getText(strip=True) for address in all_address]
print(address_list)

# PRICE SCRAPING
all_prices = soup.find_all("span", {"data-test": "property-card-price"})
price = [price.getText(strip=True) for price in all_prices]
price_list = []

for i in price:
    new_price = i.strip("+/mo+ 1bd")
    price_list.append(new_price)
print(price_list)

# LINK SCRAPING
all_links_elements = soup.select(".StyledPropertyCardDataWrapper a")
links_list = [link["href"] for link in all_links_elements]
print(links_list)


# SELENIUM

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

for x in range(len(address_list)):

    driver.get(URL_DRIVE)
    time.sleep(1)
    address_question = driver.find_element(By.XPATH, value="//*[@id='mG61Hd']/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input")
    address_question.send_keys(address_list[x])

    price_question = driver.find_element(By.XPATH, value="//*[@id='mG61Hd']/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input")
    price_question.send_keys(price_list[x])

    link_question = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_question.send_keys(links_list[x])
    time.sleep(0.2)
    submit_button = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span')
    submit_button.click()
    print(f"{x} in total of {len(address_list) - 1}")