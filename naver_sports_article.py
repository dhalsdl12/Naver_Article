import os
from selenium import webdriver
from selenium.webdriver.common.by import By


def pageCrawl():
    article_list = drive.find_elements(By.XPATH, "//ul[@class=\"list_news\"]/li")
    for article in article_list:
        try:
            news_info = article.find_element(By.XPATH, "./div/div/a[@class=\"news_tit\"]")
            title = news_info.get_attribute('title')
            link = news_info.get_attribute('href')
            article_title.append(title)
            article_link.append(link)
            file.write(title + '\n' + link + '\n\n')
        except:
            print("error")



url = 'https://search.naver.com/search.naver?where=news&query=%EB%A7%A8%EC%B2%B4%EC%8A%A4%ED%84%B0%20%EC%8B%9C%ED%8B%B0&sm=tab_opt&sort=0&photo=0&field=0&pd=4&ds=2023.01.12.10.34&de=2023.01.13.10.34&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3A1d&is_sug_officeid=0'

article_title = []
article_link = []
file = open("article.txt", "w", encoding="utf-8")

chrome_driver = os.path.join('chromedriver')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--disable-gpu')
drive = webdriver.Chrome(chrome_driver, options=chrome_options)

# drive = webdriver.Chrome('C:\\Users\\dhals\\Downloads\\chromedriver.exe')
drive.get(url)

pageCrawl()
for i in range(len(article_title)):
    print(article_title[i])
    print(article_link[i])

drive.close()
file.close()
print('finish')
