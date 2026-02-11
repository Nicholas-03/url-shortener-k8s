class Url:
    urls = {}
    counter = 0

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
        
        return id
    
    @classmethod
    def deleteAllUrls(cls, username):
        idToDelete = [id for id, data in cls.urls.items() 
                     if data['owner'] == username]
    
        for id in idToDelete:
            del cls.urls[id]
