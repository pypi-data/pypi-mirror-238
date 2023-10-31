from pymongo import MongoClient

import wikirate4py
from wikirate4py import Cursor

client = MongoClient("localhost:27017",
                     username='admin',
                     password='w00d4th3s0u1',
                     authSource='admin')

db = client.get_database("msa_project")

api = wikirate4py.API('ThessaloWikiRate')

# cursor = Cursor(api.get_relationship_answers, metric_name='Subsidiary Of', metric_designer='Commons', view='detailed',
#                 per_page=200)
#
# while cursor.has_next():
#     subsidiaries = cursor.next()
#     for s in subsidiaries:
#         json = s.json()
#         json['_id'] = json['id']
#         del json['id']
#         db.platform_subsidiaries.insert_one(json)

subsidiaries = db.platform_subsidiaries.find({'sources': {'$in': ['Source-000139335', 'Source-000127271']}})

for subsidiary in subsidiaries:
    print(subsidiary['_id'])
    api.delete_wikirate_entity(subsidiary['_id'])

client.close()
