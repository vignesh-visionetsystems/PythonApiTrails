def RoleEntity(item) -> dict:
    return {
        "roleId":str(item["_id"]),
        "roleName":item["roleName"]
    }



def RolesEntity(entity) -> list:
    return [RoleEntity(item) for item in entity]