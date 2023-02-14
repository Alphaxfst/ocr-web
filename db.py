from pymongo import MongoClient

class Mongo():
    """
        Class ini digunakan untuk menghubungkan aplikasi dengan database MongoDB
    """
    def __init__(self):
        self.__connection = "mongodb+srv://admin:IBV5Z7h21uKDYjqW@ocrweb.qwtraxg.mongodb.net/?retryWrites=true&w=majority"
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
        """
            Fungsi ini digunakan untuk melakukan proses insert dokumen ke database MongoDB
            @params:
                resultDict = Dictionary berisi hasil scan OCR
            @return:
                Jika berhasil, return object cursor MongoDB
                Jika gagal, return string info error
        """
        try:
            self.__ocrCollection.insert_one(resultDict)
        except Exception as e:
            return f"Error insert results | {e}"

    def getByUsername(self, username):
        """
            Fungsi ini digunakan untuk mengambil history scan berdasarkan username
            @return:
                Jika berhasil, return object cursor MongoDB
                Jika gagal, return string info error
        """
        try:
            results = self.__ocrCollection.find({'uploaded_by': username})
        except Exception as e:
            return f"Error get documents | {e}"
        return results

    def getUsers(self):
        """
            Fungsi ini digunakan untuk mengambil semua data user
            @return:
                Jika berhasil, return object cursor MongoDB
                Jika gagal, return string info error
        """
        try:
            results = self.__usersCollection.find({})
        except Exception as e:
            return f"Error get users | {e}"
        return results
    
    def getUsersByUsername(self, username):
        """
            Fungsi ini digunakan untuk mengambil info user berdasarkan username (digunakan pada login)
            @return:
                Jika berhasil, return object cursor MongoDB
                Jika gagal, return string info error
        """
        try:
            results = self.__usersCollection.find({'username': username})
        except Exception as e:
            return f"Error get users | {e}"
        return results
    
    def insertUser(self, userDict):
        """
            Fungsi ini digunakan untuk menginput data user (digunakan pada register)
            @return:
                Jika berhasil, return object cursor MongoDB
                Jika gagal, return string info error
        """
        try:
            result = self.__usersCollection.insert_one(userDict)
            print(result)
        except Exception as e:
            return f"Error insert user | {e}"

    def removeOCR(self):
        self.__ocrCollection.drop()
