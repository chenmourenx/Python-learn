import requests
from bs4 import BeautifulSoup


def get_trending_repos(language='Any', date_range='daily'):
    if language == 'Any':
        url = f'https://github.com/trending?since={date_range}'
    else:
        url = f'https://github.com/trending?since={date_range}&spoken_language_code={language}'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        repos = []
        for repo in soup.find_all('article', {'class': 'Box-row'}):
            # 判断描述是否为空
            description = repo.find('p', {'class': 'col-9 color-fg-muted my-1 pr-4'})
            if description:
                description = description.text.strip()
            else:
                description = ""
            repo_info = {
                'name': repo.find('h1').text.strip(),
                'url': repo.find('h1').find('a').get('href'),
                'description': description,
                'stars': int(
                    repo.find('a', {'class': 'Link--muted d-inline-block mr-3'}).text.strip().replace(',', ''))
            }
            repos.append(repo_info)
        return repos
    else:
        print(f'Failed to get trending repos, status code: {response.status_code}')
        return []


def save_repos_info(repos, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        for repo in repos:
            f.write(f'Name: {repo["name"]}\n')
            f.write(f'URL: https://github.com{repo["url"]}\n')
            f.write(f'Description: {repo["description"]}\n')
            f.write(f'Stars: {repo["stars"]}\n\n')


if __name__ == '__main__':
    language = input('Enter the language:zh,en (default: Any): ') or 'Any'
    date_range = input('Enter the date range:daily,weekly,monthly(default: today): ') or 'today'
    repos = get_trending_repos(language, date_range)
    save_repos_info(repos, 'trending_repos.txt')
