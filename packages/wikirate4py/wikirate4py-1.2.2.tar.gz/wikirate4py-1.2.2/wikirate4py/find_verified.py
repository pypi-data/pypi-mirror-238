import math

import pandas as pd
from pymongo.errors import DuplicateKeyError

import wikirate4py
from pymongo import MongoClient

from wikirate4py import Cursor

client = MongoClient("localhost:27017",
                     username='admin',
                     password='w00d4th3s0u1',
                     authSource='admin')

db = client.get_database("msa_assessed")

api = wikirate4py.API('ThessaloWikiRate')

df = pd.read_excel("C:\\Users\\vasgat\\Downloads\\TEST MSA research copy to subsidiaries(1).xlsx",
                   sheet_name='CompanyYears', engine='openpyxl')

api = wikirate4py.API('ThessaloWikiRate')

for index, row in df.iterrows():
    company = row['Company name']
    year = row['Year']
    id = row['Company ID']
    c = None
    if math.isnan(id):
        try:
            c = api.get_company(company)
            id = c.id
        except Exception as e:
            print("Nan: " + company)
    print(id)

    if not math.isnan(id):
        if c is None:
            c = api.get_company(int(id))
        assessment = db.uk_assessed_0523.find_one({'company': c.name, 'year': year})
        if assessment is not None:
            db.uk_assessed_0523.update_one({'_id': assessment['_id']}, {'$set': {'wikirate_id': int(id)}})
