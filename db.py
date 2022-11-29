from pymongo import MongoClient

class Mongo():
    def __init__(self):
        self.__connection = "mongodb://localhost:27017/"
        self.__creds = MongoClient(self.__connection)
        self.__document = self.__creds.db_ocr
        self.__ocrCollection = self.__document.ocr
        self.__usersCollection = self.__document.users
    
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

    def getByUsername(self, username):
        try:
            results = self.__ocrCollection.find({'uploaded_by': username})
        except Exception as e:
            return f"Error get documents | {e}"
        return results

    def getUsers(self):
        try:
            results = self.__usersCollection.find({})
        except Exception as e:
            return f"Error get users | {e}"
        return results
    
    def getUsersByUsername(self, username):
        try:
            results = self.__usersCollection.find({'username': username})
        except Exception as e:
            return f"Error get users | {e}"
        return results
    
    def insertUser(self, userDict):
        try:
            result = self.__usersCollection.insert_one(userDict)
            print(result)
        except Exception as e:
            return f"Error insert user | {e}"

    def removeOCR(self):
        self.__ocrCollection.drop()
