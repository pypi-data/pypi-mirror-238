from pymongo import MongoClient

ids = ["05154287", "02726164", "05706720", "02416242", "LP017842", "02934539", "00489775", "OC399502", "03618935",
       "SL003675", "09830002", "01438185", "02218202", "07751965", "03179216", "06140457", "00171830", "00445790",
       "SC361324", "02579110", "03116851", "03619151", "02338675", "00326199", "03248664", "00582065", "SC497543",
       "06879309", "00212802", "CS001511", "00372106", "01105991"]

client = MongoClient("localhost:27017",
                     username='admin',
                     password='w00d4th3s0u1',
                     authSource='admin')

db = client.get_database("wikirate")

for id in ids:
       company = db.companies_0223.find_one({'open_corporates':id})
       if company is not None:
              print(id+';'+company.get('_id').__str__())
