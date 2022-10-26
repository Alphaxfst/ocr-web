from pymongo import MongoClient

class Mongo():
    def __init__(self):
        self.__connection = "mongodb://localhost:27017/"
        self.__creds = MongoClient(self.__connection)
        self.__document = self.__creds.db_ocr
        self.__collection = self.__document.ocr
    
    def loadDocument(self):
        return self.__document
    
    def loadCollection(self):
        return self.__collection

    def insertOCRResult(self, resultDict):
        try:
            self.__collection.insert_one(resultDict)
        except Exception as e:
            f"Error | {e}"

    def get(self):
        try:
            results = self.__collection.find({})
        except Exception as e:
            return f"Error | {e}"
        return results
