# from datetime import datetime, timedelta

from bs4 import BeautifulSoup


def parse(file_str: str):
    soup = BeautifulSoup(file_str, 'html.parser')

    if title := soup.find("h1", class_="jobsearch-JobInfoHeader-title"):
        job_title = title.string
    else:
        job_title = ''

    if jd := soup.find("div", class_="jobsearch-jobDescriptionText"):
        job_description = '\n'.join([x for x in jd.strings])
    else:
        job_description = ''

    if (company := soup.find("div", class_="jobsearch-InlineCompanyRating")) and company.contents:
        company_name = company.contents[0].string
    else:
        company_name = ''

    if subtitle := soup.find("div", class_="jobsearch-JobInfoHeader-subtitle"):
        location_string = subtitle.contents[-1].string
    else:
        location_string = ''

    if footer := soup.find("div", class_="jobsearch-JobMetadataFooter"):
        posted = footer.stripped_strings
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
