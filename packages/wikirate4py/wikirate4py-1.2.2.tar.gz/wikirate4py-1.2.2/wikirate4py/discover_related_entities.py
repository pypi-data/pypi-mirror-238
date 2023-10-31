import wikirate4py
from pymongo import MongoClient

from wikirate4py import Cursor

client = MongoClient("localhost:27017",
                     username='admin',
                     password='w00d4th3s0u1',
                     authSource='admin')

db = client.get_database("msa_assessed")

api = wikirate4py.API('ThessaloWikiRate')

statements = db.assessed_0523.find({'verified': True, 'related_entities': {'$exists': False}})

for statement in statements:
    s = db.aus_assessed_statements.find_one({'wikirate_id': statement['wikirate_id'],
                                            'year': statement['year'],
                                            'metric': 'Business & Human Rights Resource Centre+Modern Slavery Statement'})

    if s is not None and len(s['sources']) == 1:
        answers = api.get_answers_by_id(s['sources'][0]['id'], metric_name='Modern Slavery Statement',
                                        year=statement['year'])
        if len(answers) > 1:
            print(s['sources'][0]['name'])
            print(statement['company'])
            for answer in answers:
                print(answer.company)
            print()
    elif s is not None and len(s['sources']) > 1:
        for source in s['sources']:
            answers = api.get_answers_by_id(source['id'], metric_name='Modern Slavery Statement')
            if len(answers) > 1:
                print(source['name'])
                print(statement['company'])
                for answer in answers:
                    print(answer.company)
                print()

client.close()
