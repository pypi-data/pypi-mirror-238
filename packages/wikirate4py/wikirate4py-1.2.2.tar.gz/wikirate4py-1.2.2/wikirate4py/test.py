import wikirate4py

api = wikirate4py.API('ThessaloWikiRate')

answers = api.get_answers(metric_name='Address',
                          metric_designer='Commons',
                          view='detailed')

print(answers[0].sources[0].original_source)