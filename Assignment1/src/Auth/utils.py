import time, json
import base64
import hashlib, hmac

SECRET_KEY = "mySecretKey"

def createToken(username):
    header = {
        "typ": "JWT",
        "alg": "HS256"
    }
    headerJson = json.dumps(header, separators=(',', ':')) # removes white spaces
    encodedHeader = base64.b64encode(headerJson.encode('utf-8')).decode('utf-8')

    payload = {
        "username": username,
        "exp": int(time.time()) + 3600 # in seconds
    }
    payloadJson = json.dumps(payload, separators=(',', ':')) # removes white spaces
    encodedPayload = base64.b64encode(payloadJson.encode('utf-8')).decode('utf-8')

    message = f"{encodedHeader}.{encodedPayload}"
    
    signature = hmac.new(
        SECRET_KEY.encode('utf-8'),
        message.encode('utf-8'),
        hashlib.sha256
    ).digest()
    encodedSignature = base64.b64encode(signature).decode('utf-8')
    
    return f"{encodedHeader}.{encodedPayload}.{encodedSignature}"

def validateToken(token):
    try:
        # Split the JWT into its three parts
        parts = token.split('.')
        if len(parts) != 3:
            print("Wrong length")
            return None
        
        encodedHeader, encodedPayload, encodedSignature = parts
        
        # Recreate the signature
        message = f"{encodedHeader}.{encodedPayload}"
        expectedSignature = hmac.new(
            SECRET_KEY.encode('utf-8'),
            message.encode('utf-8'),
            hashlib.sha256
        ).digest()
        expectedSignature_b64 = base64.b64encode(expectedSignature).decode('utf-8')
        
        # Compare signatures
        if encodedSignature != expectedSignature_b64:
            print("Wrong signature")
            return None
        
        # Decode and parse the payload
        payloadJson = base64.b64decode(encodedPayload).decode('utf-8')
        payload = json.loads(payloadJson)
        
        # Check if token is expired
        if payload['exp'] < int(time.time()):
            print("Token expired")
            return None
        
        # Return the username
        return payload['username']
        
    except Exception:
        return None