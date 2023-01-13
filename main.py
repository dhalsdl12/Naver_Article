import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from pytz import timezone
from github_setting import get_github_repo, upload_github_issue


def pageCrawl(drive):
    article_list = drive.find_elements(By.XPATH, "//ul[@class=\"list_news\"]/li")
    for article in article_list:
        try:
            news_info = article.find_element(By.XPATH, "./div/div/a[@class=\"news_tit\"]")
            news_text = article.find_element(By.XPATH, "./div/div/div[@class=\"news_dsc\"]/div/a")
            title = news_info.get_attribute('title')
            link = news_info.get_attribute('href')
            article_title.append(title)
            article_link.append(link)
            article_text.append(news_text.text)
        except:
            print("error")


def extract_book_data():
    upload_contents = ''

    for i in range(len(article_title)):
        url = '\"' + article_link[i] + '\"'
        title = article_title[i]
        text = article_text[i]
        content = f"<a href={url}>" + title + "</a>" + "<br/>"
        content += "<blockquote data-ke-style=\"style2\">" + text + "</blockquote><br/>\n"
        upload_contents += content

    return upload_contents


def execute_drive():
    url = 'https://search.naver.com/search.naver?where=news&query=%EB%A7%A8%EC%B2%B4%EC%8A%A4%ED%84%B0%20%EC%8B%9C%ED%8B%B0&sm=tab_opt&sort=0&photo=0&field=0&pd=4&ds=2023.01.12.10.34&de=2023.01.13.10.34&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3A1d&is_sug_officeid=0'

    chrome_driver = os.path.join('chromedriver')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')

    drive = webdriver.Chrome(chrome_driver, options=chrome_options)
    drive.get(url)
    pageCrawl(drive)


if __name__ == "__main__":
    access_token = os.environ['MY_GITHUB_TOKEN']
    repository_name = "Naver_Article"
    seoul_timezone = timezone('Asia/Seoul')
    today = datetime.now(seoul_timezone)
    today_date = today.strftime("%Y년 %m월 %d일")
    
    article_title = []
    article_link = []
    article_text = []

    execute_drive()

    for i in range(len(article_title)):
        print(article_title[i])
        print(article_link[i])
        print(article_text[i])

    issue_title = f"Naver 맨체스터시티 Article({today_date})"
    upload_contents = extract_book_data()
    repo = get_github_repo(access_token, repository_name)
    upload_github_issue(repo, issue_title, upload_contents)
    print("Upload Github Issue Success!")
