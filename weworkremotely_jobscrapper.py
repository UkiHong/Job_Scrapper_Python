import requests
from bs4 import BeautifulSoup

all_jobs = []


def scrape_page(url):
    print(f"Scrapping {url}...")
    response = requests.get(url)

    soup = BeautifulSoup(
        response.content,
        "html.parser",
    )

    jobs = soup.find("section", class_="jobs").find_all("li")[1:-1]
    # [1:-1] -> 리스트의 첫번째와 마지막을 제외한 리스트만 보여줌, -1 을 사용한 이유는 리스트안의 값이 몇개 인지 모르기 때문

    for job in jobs:
        title = job.find("span", class_="title").text
        # .text 는 해당 값의 text 만 extract
        company, position, region = job.find_all("span", class_="company")
        # python syntex: find_all의 span 에서 company 를 가진 게 총 3개 이기때문에 company, position, region 3개 값을 정해서 꼭 넣어줘야 함. value 가 2개면 작동 x

        url = job.find("div", class_="tooltip").next_sibling["href"]
        # "div"의 "tooltip"에서 .next_sibling 이라는 method로 첫번째가 아닌 다음 "href" attribute를 찾음
        # ["href"] 는 .text 와 비슷하게 "href"라는 attribute를 extract

        job_data = {
            "title": title,
            "company": company.text,
            "position": position.text,
            "region": region.text,
            "url": f"https://weworkremotely.com/{url}",
        }
        # job_data dictionary

        all_jobs.append(job_data)


def get_pages(url):
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    return len(soup.find("div", class_="pagination").find_all("span", class_="page"))
    # len() 리스트의 길이를 알려줌


total_pages = get_pages("https://weworkremotely.com/remote-full-time-jobs?page=1")


for x in range(total_pages):
    # range()는 for loops 를 몇번 실행시킬 지 지정해줌
    url = f"https://weworkremotely.com/remote-full-time-jobs?page={x+1}"
    print("request page", x + 1)
    # 해당 웹사이트가 page=1 부터 시작하므로 x+1
    scrape_page(url)

print(len(all_jobs))
