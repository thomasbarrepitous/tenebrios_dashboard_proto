import json

authentication_file = "auth.json"

with open(authentication_file) as auth_file:
    auth_json = json.loads(auth_file.read())
    auth = (auth_json["username"], auth_json["password"])
