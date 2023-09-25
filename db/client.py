from pymongo import MongoClient

# bdd local
# db_client = MongoClient().local

# bdd remota
url = "mongodb://mongo:NZj9hBPMHkhF7D92QNl8@containers-us-west-143.railway.app:6428"
db_client = MongoClient(url).test


