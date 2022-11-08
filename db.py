from pymongo import MongoClient

class Mongo():
    def __init__(self):
        self.__connection = "mongodb://localhost:27017/"
        self.__creds = MongoClient(self.__connection)
        self.__document = self.__creds.db_ocr
        self.__ocrCollection = self.__document.ocr
        self.__usersCollection = self.__document.ocr
    
    def loadDocument(self):
        return self.__document
    
    def loadOCRCollection(self):
        return self.__ocrCollection

    def loadUsersCollection(self):
        return self.__usersCollection

    def insertOCRResult(self, resultDict):
        try:
            self.__ocrCollection.insert_one(resultDict)
        except Exception as e:
            return f"Error insert results | {e}"

    def get(self):
        try:
            results = self.__ocrCollection.find({})
        except Exception as e:
            return f"Error get documents | {e}"
        return results

    def getUsers(self):
        try:
            results = self.__usersCollection.find({})
        except Exception as e:
            return f"Error get users | {e}"
        return results
    
    def insertUser(self, userDict):
        try:
            self.__usersCollection.insert_one(userDict)
        except Exception as e:
            return f"Error insert user | {e}"
