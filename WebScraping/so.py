import requests
from bs4 import BeautifulSoup as bs

url=f'https://stackoverflow.com/jobs?q=python&sort=i'
def get_last_page():

    html=requests.get(url)
    soup=bs(html.text,'html.parser')
    pages=soup.find('div',class_='s-pagination').find_all('a')
    last_page=pages[-2].get_text(strip=True)
    return int(last_page)

def extract_job(html):
    title=html.find('div',class_='grid').find('h2').find('a')['title']
    company,location=html.find('h3',class_='fc-black-700').find_all('span',recursive=False)
    company=company.get_text(strip=True)
    location=location.get_text(strip=True)
    return {'title':title,'company':company,'location':location}

def extract_jobs(last_page):
    jobs=[]
    for page in range(last_page):
        html=requests.get(f"{url}&pg={page+1}")
        soup=bs(html.text,'html.parser')
        results=soup.find('div',class_='-job')
        for result in results:
            job=extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs():
    last_page=get_last_page()
    jobs=extract_jobs(last_page)
    return jobs