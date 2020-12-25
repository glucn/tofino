from urllib.parse import urlparse, urlunparse

from bs4 import BeautifulSoup


def remove_queries(url):
    uu = urlparse(url)
    return urlunparse(uu._replace(query=''))


def indeed_parse_url(url: str):
    uu = list(urlparse(url))
    uu[0] = 'https'  # scheme
    uu[1] = 'ca.indeed.com'  # netloc, the link in the search results page are all relative
    return urlunparse(uu)


def parse_search_results(html_path):
    html_file = open(html_path, "r", encoding='utf-8')
    soup = BeautifulSoup(html_file.read(), 'html.parser')
    # result = [remove_queries(x['href']) for x in soup.find_all('a', class_='result-card__full-card-link')]
    result = [indeed_parse_url(x['href']) for x in soup.find_all('a', class_='jobtitle turnstileLink')]
    print(result)
    print(len(result))


def parse_single_posting(html_path):
    html_file = open(html_path, "r", encoding='utf-8')
    soup = BeautifulSoup(html_file.read(), 'html.parser')
    job_title = soup.find("h1", class_="topcard__title").string
    job_description = [x for x in soup.find("div", class_="show-more-less-html__markup").strings]

    return job_title, job_description


if __name__ == '__main__':

    parse_search_results("indeed_search_result.html")
    # print(parse_single_posting("single_posting.html"))
