import json
import sys

import requests
import spacy
from spacy.pipeline import EntityRuler

skill_list = ['SAP', 'SAS', 'ERP',  'Workday', 'salesforce', 'Esuite', 'COGNOS', 'AWS', 'SPSS',
              'MS Office', 'Microsoft Office', 'Dynamics', 'Microsoft Excel', 'Excel', 'Word', 'PowerPoint', 'Visio', 'Access', 'Outlook', 'SharePoint',
              'Google Sheets', 'Google Analytics', 'Google Data Studio',
              'database', 'SQL', 'Oracle', 'Mongo', 'SSRS', 'Power BI', 'Tableau', 'BI', 'CRM', 'ERP',
              'programming', 'debugging', 'R', 'Python', 'Javascript', 'VBA', 'C#', 'Java',
              'Git', 'Github',
              'prioritization', 'communication', 'presentation', 'collaboration', 'creative',
              'analyze', 'analytics', 'visualization', 'statistical', 'predictive modelling',
              'design', 'project management', 'writing', 'leadership', 'problem solving', 'integrity', 'detail-oriented',
              'data-driven', 'organized', 'passionate',
              'Spanish',
              ]


def get_job_description(job_id):
    url = f'http://tofin-Appli-9CZQN0QUMIV7-2117560493.us-west-2.elb.amazonaws.com/api/v1/jobPosting/{job_id}'
    with requests.get(url, stream=True, allow_redirects=True) as response:
        if response.status_code != 200:
            raise Exception
        job_posting = response.content
        return json.loads(job_posting)['job_description']


if __name__ == '__main__':
    job_id = sys.argv[1]
    jd = get_job_description(job_id)

    print(jd)
    print()

    nlp = spacy.load('en_core_web_md')

    ruler = EntityRuler(nlp, phrase_matcher_attr="LOWER")  # add `overwrite_ents=True` if after ner
    patterns = [{"label": "SKILL", "pattern": skill} for skill in skill_list]
    ruler.add_patterns(patterns)

    nlp.add_pipe(ruler, before='ner')

    with nlp.disable_pipes('tagger', 'parser'):
        doc = nlp(jd)
        for ent in doc.ents:
            print(ent.text, ent.label_)
