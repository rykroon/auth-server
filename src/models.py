import pymongo


class BaseModel:
    collection = None

    def delete(self):
        pass

    def save(self):
        pass


class Client(BaseModel):
    pass


class User(BaseModel):
    pass