import time

import wikirate4py
from pymongo import MongoClient

client = MongoClient("localhost:27017",
                     username='admin',
                     password='w00d4th3s0u1',
                     authSource='admin')

db = client.get_database("fti_project")

api = wikirate4py.API('rMrVM3sSrtsiX23fKfsM5Qtt')

metrics = db.pc_answers_2023.distinct("metric")

for metric in metrics:
    print(metric)
    fields = metric.split("+")
    answers = api.get_answers(fields[1], fields[0], published="false")
    print(answers)

# for answer in answers:
#     # sources = set(answer['wikirate_sources'])
#     # source = ''
#     # for s in sources:
#     #     source += s + "\n"
#     #
#     # value = ''
#     # if len(answer['value']) > 1:
#     #     for v in answer['value']:
#     #         value += v + "\n"
#     # else:
#     #     value = answer['value'][0]
#
#     metric_name = answer['metric'].split('+')[1]
#     metric_designer = answer['metric'].split('+')[0]
#     # comment = ''
#     # if answer.get('comment') is not None:
#     #     comment = answer['comment']
#
#     for wid in answer['wikirate_id']:
#         start_time = time.time()
#         try:
#             # if 'import_status_' + str(wid) in answer:
#             #     continue
#             print(answer['year'])
#             print(metric_name)
#             print(wid)
#             metric = api.get_answer_by(metric_designer=metric_designer,
#                                        metric_name=metric_name,
#                                        company=wid,
#                                        year=answer['year'])
#             a = api.update_research_metric_answer_by_id(id=metric.id,
#                                                         unpublished="0")
#             end_time = time.time()
#             exec_time = end_time - start_time
#             print("Exec Time: " + exec_time.__str__())
#             print(a)
#             db.answers_2023.update_one({'_id': answer['_id']}, {'$set': {'import_status_' + str(wid): 'imported'}})
#         except Exception as e:
#             print(e.__str__())
#
# client.close()
