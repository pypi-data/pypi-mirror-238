import wikirate4py

api = wikirate4py.API('ThessaloWikiRate')

answers = api.get_relationship_answers(metric_name='Supplier of',
                                            metric_designer='Commons',
                                            country='United Kingdom')