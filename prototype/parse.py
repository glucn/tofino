# from datetime import datetime, timedelta

from bs4 import BeautifulSoup


def parse(file_str: str):
    soup = BeautifulSoup(file_str, 'html.parser')

    title_h1 = soup.find("h1", class_="jobsearch-JobInfoHeader-title")
    if title_h1:
        job_title = title_h1.string
    else:
        job_title = ''

    jd_div = soup.find("div", class_="jobsearch-jobDescriptionText")
    if jd_div:
        job_description = '\n'.join([x for x in jd_div.strings])
    else:
        job_description = ''

    company_div = soup.find("div", class_="jobsearch-InlineCompanyRating")
    if company_div and company_div.contents:
        company_name = company_div.contents[0].string
    else:
        company_name = ''

    subtitle_div = soup.find("div", class_="jobsearch-JobInfoHeader-subtitle")
    if subtitle_div and subtitle_div.contents:
        location_string = subtitle_div.contents[-1].string
    else:
        location_string = ''

    footer_div = soup.find("div", class_="jobsearch-JobMetadataFooter")
    if footer_div:
        posted = footer_div.stripped_strings
    else:
        posted = ''

    print(job_title)
    print(cleansing(job_description))
    print(company_name)
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
    with open('58ede61f-bd31-4607-bd53-3f48849487f9.html', 'r') as file:
        parse(file.read())
