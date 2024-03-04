def UserEntity(item) -> dict:
    return {
        "id":str(item["_id"]),
        "userName":item["userName"],
        "email":item["email"],
        "password":item["password"]
    }



def UsersEntity(entity) -> list:
    return [UserEntity(item) for item in entity]