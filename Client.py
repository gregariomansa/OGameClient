import time

import requests

import NetworkHandler
import SettingsLoader


def matchVariable(inputs, saveFile, networkHandler):
    if inputs == "UserUsername":
        return networkHandler.Username
    if inputs == "UserPassword":
        return networkHandler.Password
    if inputs == "UserServer":
        return networkHandler.Server
    return ""


def invokePacket(packetName, save, networkHandler):
    packet = save.Packets[packetName]
    url = packet["URL"]
    packetBody = 0
    if "querydata" in packet:
        url += packet["querydata"]
        for element in packet["queryreplacements"]:
            url = url.replace(element, matchVariable(packet["queryreplacements"][element], save, networkHandler))
    print("[DEBUG] url is " + url)
    request = requests.Request(packet["Method"], url)
    prepped = request.prepare()
    if "formdata" in packet:
        packetBody = packet["formdata"]
        for element in packet["formreplacements"]:
            packetBody = packetBody.replace(element,
                                            matchVariable(packet["formreplacements"][element], save, networkHandler))
        length = len(packetBody)
        prepped.body = packetBody
        prepped.headers["Content-Length"] = length
        prepped.headers["Content-Type"] = packet["content-type"]
        prepped.headers["Accept"] = packet["accept"]
        prepped.headers["Accept-Encoding"] = packet["encoding"]
        prepped.headers["Connection"] = packet["connection"]
    prepped.headers["Host"] = packet["Host"]
    resp = networkHandler.session.send(prepped, allow_redirects=False)
    try:
        shouldRedirect = resp.headers["Location"] != None
    except:
        shouldRedirect = False
    while shouldRedirect:
        request = requests.Request("Get", resp.headers["Location"])
        print("[LOG] Redirecting to " + resp.headers['Location'] + "...")
        prep = request.prepare()
        resp = networkHandler.session.send(prep)
        try:
            shouldRedirect = resp.headers["Location"] != None
        except:
            shouldRedirect = False
    if str(resp.status_code) != packet["Estimated-Response"]:
        print("[WARNING] Packet " + packetName + " got a failed Response, expected " + packet[
            "Estimated-Response"] + ", got " + str(resp.status_code))
    else:
        print("[LOG]Successfully send packet" + packetName)


clients = []
saveFile = SettingsLoader.Settings("settings.json")

for user in saveFile.logins:
    clients.append(
        NetworkHandler.NetworkHandler(user, saveFile.logins[user]["password"], saveFile.logins[user]["server"],
                                      proxy=saveFile.Proxies, UA=saveFile.UA))

for client in clients:
    client.grabCookies(saveFile.cookieUrls)

invokePacket("PckOffLogin", saveFile, clients[0])

while True:
    time.sleep(5)
    print("Idling...")
