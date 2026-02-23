import json, os

class Url:
    urls = {}
    counter = None
    app = None

    @staticmethod
    def getId(num):
        chars = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        if num == 0:
            return chars[0]
    
        result = []
        while num > 0:
            result.append(chars[num % 62])
            num //= 62
    
        return ''.join(reversed(result))
    
    @classmethod
    def getUrls(cls, username):
        return [id for id, data in cls.urls.items() 
            if data['owner'] == username]
    
    @classmethod
    def addUrl(cls, url, username):
        id = cls.getId(cls.counter)
        cls.counter += 1

        cls.urls[id] = {
            'url': url,
            'owner': username
        }
        
        cls.updateDatabase()
        
        return id
    
    @classmethod
    def updateDatabase(cls):
        path = cls.dbPath(cls.app)
        with open(path, "w", encoding="utf-8") as f:
                json.dump({"counter": cls.counter, "urls": cls.urls}, f)
    
    @classmethod
    def deleteAllUrls(cls, username):
        idToDelete = [id for id, data in cls.urls.items() 
        if data['owner'] == username]
    
        for id in idToDelete:
            del cls.urls[id]
        
        Url.updateDatabase()
            
    @staticmethod
    def dbPath(app):
        return os.path.join(app.instance_path, "database.json")

    @classmethod
    def loadData(cls, app):
        cls.app = app
        path = cls.dbPath(cls.app)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        try:
            with open(path, "r", encoding="utf-8") as f:
                print("DB loaded successfully")
                database = json.load(f)
                cls.urls = database.get("urls", {})
                cls.counter = database.get("counter", 0)
                
        except FileNotFoundError:
            with open(path, "w", encoding="utf-8") as f:
                json.dump({}, f)
                print("DB created successfully")
