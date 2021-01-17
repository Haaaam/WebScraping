import requests
from bs4 import BeautifulSoup as bs

LIMIT=50
url=f"https://www.indeed.com/jobs?q=python&limit={LIMIT}"
def get_last_page():
    html = requests.get(url)
    soup = bs(html.text, 'html.parser')
    # html 가져오기
    pagination = soup.find('div', {'class': 'pagination'})
    # 페이지 번호 찾기
    links = pagination.find_all('a')
    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page

def extract_job(html):
    title = html.find('h2', class_='title').find('a')['title']
    company = html.find('span', class_='company')
    company_anchor = company.find('a')
    if company_anchor is not None:
        company = str(company_anchor.string)
    else:
        company = str(company.string)
    company=company.strip()
    location=html.find('span',class_='location accessible-contrast-color-location').text
    job_id=html['data-jk']
    return {'title':title,
            'company':company,
            'location':location,
            'link':f'https://www.indeed.com/viewjob?jk={job_id}'}


#직업 공고 title 가져오기
def extract_jobs(last_pages):

    jobs=[]
    for page in range(last_pages):
        print(f"Scraping page{page}")
        result=requests.get(f"{url}&start={page*LIMIT}")
        soup=bs(result.text,'html.parser')
        results=soup.find_all('div',class_='jobsearch-SerpJobCard')
        for result in results:
            job=extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs():
    last_page=get_last_page()
    jobs=extract_jobs(2)
    return jobs