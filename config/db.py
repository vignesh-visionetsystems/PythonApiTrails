from pymongo import MongoClient 


url = "mongodb://localhost:27017"

con = MongoClient(url)


db_instance = con.get_database("Organization")


