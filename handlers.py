import requests as req

def getExample():
    r = req.get("https://www.example.com")
    print(r)
    print(r.text[0:300])
