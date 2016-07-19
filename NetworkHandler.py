import requests


class NetworkHandler():
    def __init__(self, user, password, server, proxy={}, UA=""):
        self.proxy = proxy
        self.session = requests.Session()
        self.UA = UA
        self.Username = user
        self.Password = password
        self.Server = server
        print("[LOG] Added user " + user + " with password " + password)
    def applyUserAgent(self, request):
        if self.UA == "":
            return request
        request.headers["User-Agent"] = self.UA
        return request

    def getCookies(self):
        return self.session.cookies

    def grabCookies(self, urls):
        for url in urls:
            req = requests.Request("GET", url)
            prep = req.prepare()
            prep = self.applyUserAgent(prep)
            if self.proxy == {}:
                self.session.send(prep)
            else:
                self.session.send(prep, proxies=self.proxy)