from typing import List

from bson import ObjectId
from pymongo import MongoClient
from wikirate4py.models import SourceItem

from wikirate4py.exceptions import NotFoundException

import wikirate4py

client = MongoClient("localhost:27017",
                     username='admin',
                     password='w00d4th3s0u1',
                     authSource='admin')

db = client.get_database("msa_assessed")

api = wikirate4py.API('NzSK5muu3o7oSwDa2PpUVQtt')


def sources_to_list(sources):
    list_of_sources = []
    for s in sources:
        if isinstance(s, SourceItem):
            list_of_sources.append(s.name)
        else:
            list_of_sources.append(s['name'])
    return list_of_sources


def conflict_free(verified_answers_ids, entity):
    conflict_free = True
    for id in verified_answers_ids:
        answer = db.aus_assessed_statements.find_one({'_id': id})
        metric = answer['name'].split('+')
        try:
            a = api.get_answer_by(metric[0], metric[1], entity, metric[3])
            original_sources = sources_to_list(answer['sources'])
            child_sources = sources_to_list(a.sources)

            if answer['value'] == a.value and any(item in child_sources for item in original_sources):
                continue
            else:
                print(answer)
                print(a)
                print()
                conflict_free = False
        except NotFoundException as e:
            continue
    return conflict_free


statements = db.assessed_0523.find({"verified": True, "related_entities": {'$exists': True}})

counter = 0
for statement in statements:
    print('Statement ID: {0}'.format(statement['_id']))
    related_entities = statement['related_entities']
    verified_answers_ids = statement['verified_answers_ids']

    for entity in related_entities:
        print(entity)
        is_conflict_free = conflict_free(verified_answers_ids, entity)
        if is_conflict_free:
            for id in verified_answers_ids:
                answer = db.aus_assessed_statements.find_one({'_id': id})
                metric = answer['name'].split('+')
                try:
                    a = api.get_answer_by(metric[0], metric[1], entity, metric[3])
                    # api.verify_answer(a.id)
                    # if a.metric == 'Business & Human Rights Resource Centre+Modern Slavery Statement':
                    #     api.verify_answer(a.id)
                    #     print(a)
                    #     continue
                    #
                    # source = ''
                    # for s in sources_to_list(answer['sources']):
                    #     source += s + '\n'
                    #
                    # value = ''
                    # if answer['value'].__contains__(', '):
                    #     for v in answer['value'].split(', '):
                    #         value += v + '\n'
                    # else:
                    #     value = answer['value']
                    # try:
                    #     comments = api.get_comments(answer['_id'])
                    # except NotFoundException as ex:
                    #     comments = ''
                    # copied_answer = api.update_research_metric_answer(
                    #     metric_designer=metric[0],
                    #     metric_name=metric[1],
                    #     company=entity,
                    #     value=value,
                    #     year=answer['year'],
                    #     source=source,
                    #     comment=comments + '<hr>' + ' Data copied from <b>' + answer[
                    #         'company'] + ' for ' +
                    #             answer['year'].__str__() + '</b>'
                    # )
                    # print(copied_answer)
                    # api.verify_answer(copied_answer.id)
                except NotFoundException as e:
                    source = ''
                    for s in sources_to_list(answer['sources']):
                        source += s + '\n'

                    value = ''
                    if answer['value'].__contains__(', '):
                        for v in answer['value'].split(', '):
                            value += v + '\n'
                    else:
                        value = answer['value']
                    try:
                        comments = api.get_comments(answer['_id'])
                    except NotFoundException as ex:
                        comments = ''
                    copied_answer = api.update_research_metric_answer(
                        metric_designer=metric[0],
                        metric_name=metric[1],
                        company=entity,
                        value=value,
                        year=answer['year'],
                        source=source,
                        comment=comments + '<hr>' + ' Data copied from <b>' + answer[
                            'company'] + ' for ' +
                                answer['year'].__str__() + '</b>'
                    )
                    print(copied_answer)
                    api.verify_answer(copied_answer.id)

            db.assessed_0523.update_one({'_id': statement['_id']},
                                        {'$pull': {'related_entities': entity},
                                         '$push': {'answers_copied_to_rc': entity}})

print(counter)
