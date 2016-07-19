import json


class Settings():
    settingsFileHandle = 0
    UA = ""
    Proxies = {}
    logins = {}

    def __init__(self, name):
        try:
            self.settingsFileHandle = open(name, "r")
            data = json.load(self.settingsFileHandle)
            if "UA" in data:
                self.UA = data["UA"]
            else:
                print("[ERROR]User Agent not defined! Please fix it!")
            if "Proxies" in data:
                self.Proxies = data["Proxies"]
            else:
                print("[ERROR]Proxies not defined! Please fix it!")
            if "logins" in data:
                self.logins = data["logins"]
            else:
                print("[ERROR]User Agent not defined! Please fix it!")
            self.settingsFileHandle.close()
        except:
            self.settingsFileHandle = open(name, "w")
            data = {}
            data["UA"] = self.UA
            data["Proxies"] = self.Proxies
            data["logins"] = self.logins
            json.dump(data, self.settingsFileHandle)
            self.settingsFileHandle.close()
