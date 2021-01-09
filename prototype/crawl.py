import requests


def _process_message(url):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Content-Type': 'text/html',
    }

    with requests.get(url, stream=True, allow_redirects=True, headers=headers) as response:
        if response.status_code != 200:
            print(f'Getting URL "{url}" resulted in status code {response.status_code}')
            raise Exception

        print(f'Original URL {url}, final URL {response.url}')

        print(response.url)
        print(response.content)


if __name__ == '__main__':
    _process_message('https://ca.indeed.com/rc/clk?jk=68c29bf549e90565&fccid=354f4c12e3c6bd5a&vjs=3')
