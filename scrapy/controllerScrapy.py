from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from bs4 import BeautifulSoup

import requests


class ScrapyChrome:
    def __init__(self, url):
        self.chrome_options = Options()
        self.chrome_options.add_argument("window-size=1920x1080")
        self.chrome_options.add_argument("disable-gpu")
        self.chrome_options.add_argument("headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option(
            'useAutomationExtension', False)
        self.chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36")

        self.driver = webdriver.Chrome(
            executable_path=ChromeDriverManager().install(), options=self.chrome_options)
        self.driver.get(url)

    def get_scrapy(self):
        return self.driver

    def script(self, script):
        self.driver.execute_script(script)

    def click(self, elemento):
        elemento.Click()

    def get_screen_shot(self, elemento):
        elemento.location_once_scrolled_into_view
        return elemento.screenshot('gest.png')

    def buscar_xpath(self, elemento):
        return self.driver.find_element(By.XPATH, elemento)

    def buscar_class(self, elemento):
        return self.driver.find_element(By.CLASS_NAME, elemento)


class ScrapySoup:
    def __init__(self, url) -> None:
        self.my_headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
                           "Accept": "text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,image/apng,*/*;q=0.8"}
        self.url = url
        self.html = requests.get(url, headers=self.my_headers).content
        self.soup = BeautifulSoup(self.html, 'html.parser')

    def get_soup(self):
        return self.soup

    def busca(self, tag, atributo, nome,):
        return self.soup.find('{}'.format(tag), attrs={'{}': '{}'.format(atributo, nome)})

    def busca_todos(self, tag, atributo, nome):
        resultado = []

        for i in self.soup.find_all('{}'.format(tag), attrs={'{}': '{}'.format(atributo, nome)}):
            resultado.append(i.text)

        return resultado
