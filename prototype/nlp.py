import json

import requests
import spacy
from spacy.matcher.phrasematcher import PhraseMatcher
from spacy.tokens.doc import Doc
from spacy.tokens.span import Span

nlp = spacy.load('en_core_web_md')

job_id = 'd399a130-57d1-4535-aa59-27adfbbe3b36'
url = f'http://52.41.240.242/api/v1/jobPosting/{job_id}'

jd = ''

with requests.get(url, stream=True, allow_redirects=True) as response:
    if response.status_code != 200:
        raise Exception
    job_posting = response.content
    jd = json.loads(job_posting)['job_description']

print(jd)

skill_list = ['SQL', 'SAP', 'SAS', 'Python', 'ERP', 'BI', 'Microsoft Office', 'Dynamics', 'Excel',
              'Tableau', 'Java', 'Mongo', 'AWS', 'VBA', 'Oracle', 'SPSS', 'Javascript', 'Visio', 'Access', 'Git',
              'Github', 'R', 'Salesforce', 'prioritization']
patterns = list(nlp.pipe(skill_list))
matcher = PhraseMatcher(nlp.vocab)
matcher.add('SKILL', None, *patterns)


def match_skill(doc: Doc):
    matches = matcher(doc)
    for _, start, end in matches:
        # Generate Span representing the entity & set label
        entity = Span(doc, start, end, label='SKILL')
        # Overwrite doc.ents and add entity – be careful not to replace!
        doc.ents = list(doc.ents) + [entity]

    return doc


nlp.add_pipe(match_skill)

with nlp.disable_pipes('tagger', 'parser', 'ner'):
    doc = nlp(jd)
    for ent in doc.ents:
        print(ent.text, ent.label_)
