import pymongo



uri = "mongodb://localhost:27017"

client = pymongo.MongoClient(uri)

myDb = client['Organisation']


employee = myDb.employee


record ={
    "first_name":"vignesh",
    "last_name":"Venkatesh",
    "email":"venkatesh.vignesh@gmail.com"
}


employee.insert_one(record)
 

# message = "Hello World"
# print(message)


