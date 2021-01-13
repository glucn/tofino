from datetime import datetime, timedelta

from bs4 import BeautifulSoup


def parse(file_str: str):
    soup = BeautifulSoup(file_str, 'html.parser')

    job_title = soup.find("h1", class_="jobsearch-JobInfoHeader-title").string
    job_description = '\n'.join([x for x in soup.find("div", class_="jobsearch-jobDescriptionText").strings])
    company_name = soup.find("div", class_="jobsearch-InlineCompanyRating").contents[0].string
    location_string = soup.find("div", class_="jobsearch-JobInfoHeader-subtitle").contents[-1].string
    posted = soup.find("div", class_="jobsearch-JobMetadataFooter").stripped_strings

    # print(job_title)
    # print(cleansing(job_description))
    # print(company_name)
    print(location_string)

    # print((job_title, job_description))
    # print([x.string for x in posted])
    # print(repr(posted))

    # for s in posted:
    #     if s.endswith(" days ago"):
    #         if s.replace(" days ago", "") == "30+":
    #             n = 30
    #         else:
    #             n = int(s.replace(" days ago", ""))
    #         dt = datetime.now() - timedelta(days=n)
    #         dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    #         print(dt)



def cleansing(s: str):
    return bytes(s, 'utf-8').decode('utf-8', 'ignore')


if __name__ == '__main__':
    with open('4cbaa21f-693f-4531-bb9b-9f44aea2d749.html', 'r') as file:
        parse(file.read())
