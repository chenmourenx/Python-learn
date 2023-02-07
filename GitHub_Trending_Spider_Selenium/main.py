from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time


def get_trending_repos(language='Any', date_range='Today'):
    options = Options()
    options.add_argument('--headless')
    service = Service(executable_path='C:\Program Files\Google\Chrome\Application\chromedriver.exe')
    driver = webdriver.Chrome(service=service)
    driver.get(f'https://github.com/trending?since={date_range}&spoken_language_code={language}')
    time.sleep(3)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    repos = []
    for repo in soup.select('.Box-row'):
        repo_name = repo.select('.h3 a')[0].get('href').strip()
        repo_url = repo_name
        repo_description = repo.select('.col-9')[0].text.strip()
        # 判断所用语言是否为空
        star_elements = repo.select('.repo-language-color + span')
        if star_elements:
            star_element = star_elements[0].text.strip()
            repo_language = star_element
        else:
            repo_language = ''
        # repo_language = repo.select('.repo-language-color + span')[0].text.strip()
        repo_stars = repo.select('.Link--muted')[0].text.strip()
        # repo_stars = repo.select('a')[0].get_text(strip=True)
        repos.append({
            'repo_name': repo_name,
            'repo_url': repo_url,
            'repo_description': repo_description,
            'repo_language': repo_language,
            'repo_stars': repo_stars,
        })
    driver.quit()
    return repos


def save_repos_to_file(repos, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for repo in repos:
            f.write(f'Name: {repo["repo_name"]}\n')
            f.write(f'URL: https://github.com{repo["repo_url"]}\n')
            f.write(f'Description: {repo["repo_description"]}\n')
            f.write(f'Language: {repo["repo_language"]}\n')
            f.write(f'Stars: {repo["repo_stars"]}\n\n')


if __name__ == '__main__':
    repos = get_trending_repos()
    save_repos_to_file(repos, 'trending_repos.txt')
