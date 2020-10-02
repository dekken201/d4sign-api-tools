from core.data import *
import requests, json


def test(endpoint,option,tokenAPI,cryptKey):
    url = endpoint+"/"+option+"?tokenAPI="+tokenAPI+"&cryptKey="+cryptKey

    print(url)
    #print(requests.get(url, headers= {"Content-Type": "application/json"},))
    if (requests.get(url).status_code) == 200:
        print("OK")
    response = requests.get(url).json()
    print(json.dumps(response, sort_keys=True, indent=4))

option="safes"
test(endpoint,option,tokenAPI,cryptKey)


def backupTeste():
    # data = get("documents")
    # if data == 0:
    # sys.exit("Erro ao executar backup!")
    with open('response.txt') as json_file:
        data = json.load(json_file)
        linhaInfo = data[0].copy()

        if linhaInfo["total_pages"] != linhaInfo["current_page"]:
            i = linhaInfo["current_page"]
            j = linhaInfo["total_pages"]
            while j != i:
                newData = get("documents", i + 1)
                for item in range(1, newData[0]["total_documents"] + 1):
                    data.update(item)
                    i += 1

            for i in range(1, linhaInfo["total_documents"] + 1):
                data[i]["downloadURL"] = getDownloadURL(data[i]["uuidDoc"])
                print(data[i])

        # se tiver mais de uma pagina na linha info, lembrar
        # with open(path_parent+"/backup/" +"backup.txt","w") as fileBkp:
        # json.dump(data,fileBkp)


