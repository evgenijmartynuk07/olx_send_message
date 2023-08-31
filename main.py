import json
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


BASE_URL = "https://www.olx.ua/"

chrome_options = Options()
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.9999.999 Safari/537.36")
chrome_options.add_argument("accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7")
chrome_options.add_argument("accept-encoding=gzip, deflate, br")
chrome_options.add_argument("accept-language=uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Firefox(options=chrome_options)


def new_session(link) -> None:

    driver.get(link)
    with open("cookies.json", "r") as file:
        cookies = json.load(file)

    for raw in cookies:
        driver.add_cookie({"name": raw["name"], "value": raw["value"]})

    driver.refresh()


def write_to_file(messages_list: list) -> None:
    with open("message.txt", "w") as file:
        for message in messages_list:
            file.write(message + "\n")


def find_message_links(links: list) -> None:
    message_text = "Доброго дня"
    to_file = []

    for link in links:
        new_session(link)
        time.sleep(2)
        wait = WebDriverWait(driver, 10)
        message_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-cy='ad-contact-message-button']")))
        time.sleep(2)
        message_button.click()

        time.sleep(3)
        textarea_element = driver.find_element(By.NAME, "message.text")
        textarea_element.send_keys(message_text)

        time.sleep(2)
        h4_element = driver.find_element(By.CLASS_NAME, "css-1lcz6o7.er34gjf0")
        to_file.append(f"{h4_element.text}: {message_text}")

        time.sleep(2)
        svg_element = driver.find_element(By.CSS_SELECTOR, "svg.css-15wjrqi")
        svg_element.click()
        svg_element.click()

    write_to_file(to_file)


def find_links_on_home_page() -> None:
    page = requests.get(BASE_URL).content
    soup = BeautifulSoup(page, "html.parser")

    links = [
        link.select_one("a")["href"] for link in soup.select(".wrap.tleft.rel.fleft")[:10]
    ]

    find_message_links(links)


if __name__ == "__main__":
    find_links_on_home_page()
