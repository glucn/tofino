import json
import sys

import requests
import spacy
from spacy.pipeline import EntityRuler


skill_list = ['SQL', 'SAP', 'SAS', 'Python', 'ERP', 'BI', 'MS Office', 'Microsoft Office', 'Dynamics', 'Excel', 'Word',
              'PowerPoint', 'Workday',
              'Tableau', 'Java', 'Mongo', 'AWS', 'VBA', 'Oracle', 'SPSS', 'Javascript', 'Visio', 'Access', 'Git',
              'Github', 'R', 'salesforce', 'Esuite', 'COGNOS',
              'prioritization', 'communication', 'presentation',
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
