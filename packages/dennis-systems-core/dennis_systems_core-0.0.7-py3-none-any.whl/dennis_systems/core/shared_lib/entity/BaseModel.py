
class BaseModel:
    __id: int
    __delete: bool

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id

