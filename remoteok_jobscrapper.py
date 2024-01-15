import requests
from bs4 import BeautifulSoup

keywords = ["python", "javascript", "java"]
all_jobs = []


def search_jobs(keywords):
    response = requests.get(
        f"https://remoteok.com/remote-{keyword}-jobs",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        },
    )
    soup = BeautifulSoup(response.content, "html.parser")
    jobs = soup.find_all("tr", class_="job")

    for job in jobs:
        company = job.find("td", class_="company")
        url = job.find("a", class_="preventLink")["href"]

        job_data = {
            "company": company.find("h3").text.replace("\n", ""),
            "title": company.find("h2").text.replace("\n", ""),
            "location": company.find("div", class_="location").text,
            "link": f"https://remoteok.com/{url}",
        }
        all_jobs.append(job_data)


for keyword in keywords:
    search_jobs(keyword)


print(all_jobs)
print(len(all_jobs))
