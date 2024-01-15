from playwright.sync_api import sync_playwright
import time
from bs4 import BeautifulSoup
import csv

keywords = [
    "python",
    "django",
    "javascript",
]


def job_scrapper(keyword):
    p = sync_playwright().start()

    browser = p.chromium.launch(headless=False)
    # headless=True 일 때는 브라우저를 실행하지만 볼 수는 없음.

    page = browser.new_page()

    page.goto(f"https://www.wanted.co.kr/search?query={keyword}&tab=position")

    # time.sleep(3)
    # page.click("button.Aside_searchButton__Xhqq3")
    # time.sleep(3)
    # page.get_by_placeholder("검색어를 입력해 주세요.").fill("python")
    # time.sleep(3)
    # page.keyboard.down("Enter")
    # time.sleep(3)
    # page.click("a#search_tab_position")

    for x in range(5):
        time.sleep(2)
        page.keyboard.down("End")

    content = page.content()

    p.stop()

    soup = BeautifulSoup(content, "html.parser")

    jobs = soup.find_all(
        "div", class_="JobCard_container__FqChn JobCard_container--variant-card__znjV9"
    )

    jobs_db = []

    for job in jobs:
        link = f"https://www.wanted.co.kr/{job.find('a')['href']}"
        title = job.find("strong", class_="JobCard_title__ddkwM").text
        company_name = job.find("span", class_="JobCard_companyName__vZMqJ").text
        location = job.find("span", class_="JobCard_location__2EOr5").text
        reward = job.find("span", class_="JobCard_reward__sdyHn").text
        job = {
            "title": title,
            "company_name": company_name,
            "location": location,
            "reward": reward,
            "link": link,
        }
        jobs_db.append(job)

    file = open(f"{keyword}_jobs.csv", "w")
    writer = csv.writer(file)
    writer.writerow(
        [
            "Title",
            "Company",
            "Location",
            "Reward",
            "Link",
        ]
    )

    for job in jobs_db:
        writer.writerow(job.values())
        # .values 는 list = [a='1', b='2', c='3'] 의 list = [1,2,3] 이런식으로 key의 value 만 찾게해줌


for keyword in keywords:
    job_scrapper(keyword)
