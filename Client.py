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
        print("[Debug] Body is " + prepped.body)
        print(prepped.headers)
    prepped.headers["Host"] = packet["Host"]
    resp = networkHandler.session.send(prepped)
    if str(resp.status_code) != packet["Estimated-Response"]:
        print("[WARNING] Packet " + packetName + " got a failed Response, expected " + packet[
            "Estimated-Response"] + " got " + str(resp.status_code))
        print(resp.history[0].headers)
    else:
        print("[LOG]Successfully send packet" + packetName + " and received response with history")


clients = []
saveFile = SettingsLoader.Settings("settings.json")

for user in saveFile.logins:
    clients.append(
        NetworkHandler.NetworkHandler(user, saveFile.logins[user]["password"], saveFile.logins[user]["server"],
                                      proxy=saveFile.Proxies, UA=saveFile.UA))

for client in clients:
    client.grabCookies(saveFile.cookieUrls)

invokePacket("PckOffLogin", saveFile, clients[0])
