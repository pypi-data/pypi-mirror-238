import time
import csv
from datetime import datetime

import wikirate4py
from wikirate4py import Cursor

api = wikirate4py.API('ThessaloWikiRate')


companies = []
# companies = api.get_content('~12641428+company')
#
# print(companies)
# print(len(companies))
#
metrics = []

cursor = Cursor(api.get_metrics_of, identifier=12641428, per_page=200)
while cursor.has_next():
    m_set = cursor.next()
    for metric in m_set:
        metrics.append(metric.id)
    break

print(metrics)
print(len(metrics))

company_groups = ['MSA_Renewable_Energy']
for company_group in company_groups:
    rows = []
    answers = []
    for metric in metrics:
        print(metric)
        cursor = Cursor(api.get_answers_by_id, identifier=metric, per_page=100, company_group=company_group,
                        view="detailed")

        while cursor.has_next():
            answers.extend(cursor.next())

    header = ["Answer Page", "Metric", "Company", "Year", "Value", "Source Page"]
    now = datetime.utcnow()
    date_time = now.strftime("%Y-%m-%d %H:%M:%S")

    for answer in answers:
        if company_group == '' and answer.company in companies:
            sources = ""
            for source in answer.sources:
                sources += 'https://wikirate.org/' + source + ", "
            if len(sources) > 0:
                sources = sources[:-2]
            row = [answer.url.replace('\.json', ''), answer.metric, answer.company, answer.year, answer.value,
                   sources]
            rows.append(row)
        elif company_group != '':
            sources = ""
            for source in answer.sources:
                sources += 'https://wikirate.org/' + source + ", "
            if len(sources) > 0:
                sources = sources[:-2]
            row = [answer.url.replace('\.json', ''), answer.metric, answer.company, answer.year, answer.value,
                   sources]
            rows.append(row)
    with open(
            "D:\\Wikirate_MSA_Beyond_Compliance_Dashboard_Dataset_{0}.csv".format(
                'full' if company_group == '' else company_group), 'w',
            encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "# https://wikirate.org/MSA_Beyond_Compliance_Dashboard?filter[company_group]={0}".format(
                company_group)])
        writer.writerow(["# Creative Commons Attribution-ShareAlike 4.0 International License"])
        writer.writerow(["# Last updated at: {0} UTC".format(date_time)])
        writer.writerow(["# "])
        writer.writerow(header)
        # write the data
        writer.writerows(rows)

    f.close()
