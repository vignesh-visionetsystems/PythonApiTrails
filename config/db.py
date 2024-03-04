from pymongo import MongoClient 


# url = "mongodb://localhost:27017"
url = "mongodb+srv://vvigneshvenkatesh:InDlPDnaGlwefxyE@clusterfirst.egbpl0f.mongodb.net/?retryWrites=true&w=majority&appName=ClusterFirst"


con = MongoClient(url)


db_instance = con.get_database("Organization")


