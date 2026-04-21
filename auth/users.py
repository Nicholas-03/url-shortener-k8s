import json, os

class User:
    users = {}
    app = None

    @classmethod
    def createUser(cls, name, pwd):
        cls.users[name] = pwd
        cls.updateDatabase()
    
    @classmethod
    def updateDatabase(cls):
        path = cls.dbPath(cls.app)
        with open(path, "w", encoding="utf-8") as f:
                json.dump(cls.users, f)
        
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
                cls.users = json.load(f)
                
        except FileNotFoundError:
            with open(path, "w", encoding="utf-8") as f:
                json.dump({}, f)