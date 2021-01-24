import json
import logging

import spacy as spacy
from spacy.pipeline import EntityRuler

from app.handlers.base_handler import BaseHandler

nlp = spacy.load('en_core_web_sm')

skill_list = ['SAP', 'SAS', 'ERP',  'Workday', 'salesforce', 'Esuite', 'COGNOS', 'AWS', 'SPSS',
              'MS Office', 'Microsoft Office', 'Dynamics', 'Microsoft Excel', 'Excel', 'Word', 'PowerPoint', 'Visio', 'Access', 'Outlook', 'SharePoint',
              'Google Sheets', 'Google Analytics', 'Google Data Studio',
              'database', 'SQL', 'Oracle', 'Mongo', 'SSRS', 'Power BI', 'Tableau', 'BI', 'CRM', 'ERP',
              'programming', 'debugging', 'R', 'Python', 'Javascript', 'VBA', 'C#', 'Java',
              'Git', 'Github',
              ]

ruler = EntityRuler(nlp, phrase_matcher_attr="LOWER")  # add `overwrite_ents=True` if after ner
patterns = [{"label": "SKILL", "pattern": skill} for skill in skill_list]
ruler.add_patterns(patterns)
nlp.add_pipe(ruler, before='ner')


class ResumeAssistantHandler(BaseHandler):
    """
    API handler for ResumeAssistant
    """

    JSON_HEADER = {'Content-Type': 'application/json'}

    @classmethod
    def analyze(cls, job_posting: str):
        logging.info(f'ResumeAssistantHandler-analyze is called with [{job_posting}]')
        result = []
        with nlp.disable_pipes('tagger', 'parser'):
            doc = nlp(job_posting)
            for ent in doc.ents:
                if ent.label_ == 'SKILL':
                    result.append(
                        {
                            'text': ent.text,
                            'label': ent.label_,
                            'start': ent.start,
                            'end': ent.end
                        }
                    )
        return json.dumps(result), 200, cls.JSON_HEADER

