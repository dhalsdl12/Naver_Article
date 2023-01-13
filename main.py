import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from pytz import timezone
from github import Github


def get_github_repo(access_token, repository_name):
    g = Github(access_token)
    return g.get_user().get_repo(repository_name)


def upload_github_issue(repo, title, body):
    repo.create_issue(title=title, body=body)
    

def pageCrawl():
    article_list = drive.find_elements(By.XPATH, "//ul[@class=\"list_news\"]/li")
    for article in article_list:
        try:
            news_info = article.find_element(By.XPATH, "./div/div/a[@class=\"news_tit\"]")
            title = news_info.get_attribute('title')
            link = news_info.get_attribute('href')
            article_title.append(title)
            article_link.append(link)
        except:
            print("error")


def extract_book_data():
    upload_contents = ''

    for i in range(len(article_title)):
        url = article_link[i]
        title = article_title[i]
        content = f"<a href={url}>" + title + "</a>" + "<br/>\n"
        upload_contents += content

    return upload_contents
    

if __name__ == "__main__":
    url = 'https://search.naver.com/search.naver?where=news&query=%EB%A7%A8%EC%B2%B4%EC%8A%A4%ED%84%B0%20%EC%8B%9C%ED%8B%B0&sm=tab_opt&sort=0&photo=0&field=0&pd=4&ds=2023.01.12.10.34&de=2023.01.13.10.34&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3A1d&is_sug_officeid=0'

    access_token = os.environ['MY_GITHUB_TOKEN']
    repository_name = "Naver_Article"
    seoul_timezone = timezone('Asia/Seoul')
    today = datetime.now(seoul_timezone)
    today_date = today.strftime("%Y년 %m월 %d일")
    
    article_title = []
    article_link = []

    chrome_driver = os.path.join('chromedriver')
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')

    drive = webdriver.Chrome(chrome_driver, options=chrome_options)
    drive.get(url)

    pageCrawl()
    for i in range(len(article_title)):
        print(article_title[i])
        print(article_link[i])

    issue_title = f"Naver 맨체스터시티 Article({today_date})"
    upload_contents = extract_book_data()
    repo = get_github_repo(access_token, repository_name)
    upload_github_issue(repo, issue_title, upload_contents)
    print("Upload Github Issue Success!")
    
    
    drive.close()
