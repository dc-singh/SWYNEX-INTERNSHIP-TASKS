from src.utility.utils import load_json, save_file



def one_user(id: int):
    data = load_json()
    for user in data:
        if user["id"] == id:
            return user
    return None

def delete_user(id: int):
    data = load_json()

    for index, user in enumerate(data):
        if user["id"] == id:
            del data[index]
            save_file(data)
            return {"message": "data deleted Successfully"}

    return {"message": "user not found"}