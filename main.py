from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

form_url = "https://docs.google.com/forms/d/e/1FAIpQLScyJlmHNyGG6VlNs4OEufDFYosum4TISxEMz0XLG-0vz8f3bQ/viewform?usp=sf_link"
zillow_url = "https://appbrewery.github.io/Zillow-Clone/"


response = requests.get(zillow_url)
soup = BeautifulSoup(response.content, "html.parser")
longaddress = soup.find_all("a", class_="StyledPropertyCardDataArea-anchor")
all_address = [address.text.strip().split(",") for address in longaddress]
address = ["".join(address[1:]).strip() for address in all_address]
price_data = soup.find_all("span", class_="PropertyCardWrapper__StyledPriceLine")
prices = [price.text.split("+")[0] for price in price_data]
price = [price.split("/")[0] for price in prices]
link_data = soup.find_all("a", class_="StyledPropertyCardDataArea-anchor")
link = [link["href"] for link in link_data]
data_len = len(link_data)


option = webdriver.ChromeOptions()
option.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=option)

counter = 0
while data_len > 0:
    driver.get("https://docs.google.com/forms/d/1yaLcYuEjcKJdOp1Kxt3KjkRzwUSb_EsFg4abqaSdZy0/edit")
    time.sleep(2)
    form_address = driver.find_element(By.XPATH,
                                       '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    form_price = driver.find_element(By.XPATH,
                                     '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    form_link = driver.find_element(By.XPATH,
                                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    data_len -= 1
    form_address.send_keys(address[counter])
    form_price.send_keys(price[counter])
    form_link.send_keys(link[counter])
    submit_button.click()
    time.sleep(1)
    counter += 1

print("Transmission completed.")
driver.close()
