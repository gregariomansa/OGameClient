import json


class Settings():
    settingsFileHandle = 0
    UA = ""
    Proxies = {}
    logins = []
    cookieUrls = []
    Packets = {}
    Requests = {}

    def grabData(self, key, data):
        if key in data:
            return data[key]
        else:
            print("[ERROR]" + key + " not defined! Please fix it!")

    def __init__(self, name):
        try:
            self.settingsFileHandle = open(name, "r")
            data = json.load(self.settingsFileHandle)
            self.Requests = self.grabData("Requests", data)
            self.UA = self.grabData("UA", data)
            self.Packets = self.grabData("Requests", data)
            self.Proxies = self.grabData("Proxies", data)
            self.logins = self.grabData("logins", data)
            self.cookieUrls = self.grabData("cookieUrls", data)
            self.settingsFileHandle.close()
        except Exception as e:
            print(e)
            self.settingsFileHandle = open(name, "w")
            data = {}
            data["UA"] = self.UA
            data["Requests"] = self.Packets
            data["Proxies"] = self.Proxies
            data["logins"] = self.logins
            data["cookieUrls"] = self.cookieUrls
            data["Requests"] = self.Requests
            json.dump(data, self.settingsFileHandle)
            self.settingsFileHandle.close()
