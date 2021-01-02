from datetime import datetime, timedelta

from bs4 import BeautifulSoup


def parse(file_str: str):
    soup = BeautifulSoup(file_str, 'html.parser')

    job_title = soup.find("h1", class_="jobsearch-JobInfoHeader-title").string
    job_description = '\n'.join([x for x in soup.find("div", class_="jobsearch-jobDescriptionText").strings])
    company_name = soup.find("div", class_="jobsearch-InlineCompanyRating").contents[0].string
    location_string = soup.find("div", class_="jobsearch-InlineCompanyRating").contents[-1].string
    posted = soup.find("div", class_="jobsearch-JobMetadataFooter").stripped_strings

    # print(job_title)
    # print(cleansing(job_description))
    # print(company_name)
    # print(location_string)

    # print((job_title, job_description))
    # print([x.string for x in posted])
    # print(repr(posted))
    for s in posted:
        if s.endswith(" days ago"):
            if s.replace(" days ago", "") == "30+":
                n = 30
            else:
                n = int(s.replace(" days ago", ""))
            dt = datetime.now() - timedelta(days=n)
            dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
            print(dt)



def cleansing(s: str):
    return bytes(s, 'utf-8').decode('utf-8', 'ignore')


if __name__ == '__main__':
    with open('507f360c-2c9d-4691-b6d3-8946182f0a6c.html', 'r') as file:
    # with open('4273ee89-ee10-4c5c-a727-937fd549b74c.html', 'r') as file:
        parse(file.read())
