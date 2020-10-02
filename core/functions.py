import json
import requests
import os
import sys
import time
from core.data import *
path_parent = os.path.dirname(os.getcwd()) #pega diretório pai para realizar operações dentro das pastas


def get(option,endpoint = endpoint,tokenAPI = tokenAPI,cryptKey = cryptKey, pg = "1"):
    url = endpoint + "/" + option + "?tokenAPI=" + tokenAPI + "&cryptKey=" + cryptKey + "&pg=" +pg
    if requests.get(url).status_code == 200:
        response = requests.get(url).json()
        #with open("response.txt","w") as file: #para gravar arquivo, evitar puxar muitos calls na API
            #json.dump(response,file)
        return response #json.dumps(response, sort_keys=True, indent=4,ensure_ascii=False)
    else:
        print(requests.get(url).status_code)
        return 0


def getDownloadURL(uuidDoc, option = "documents",endpoint = endpoint,tokenAPI = tokenAPI,cryptKey = cryptKey):
    url = endpoint + "/" + option + "/"+ uuidDoc+ "/download" +"?tokenAPI=" + tokenAPI + "&cryptKey=" + cryptKey
    if requests.post(url).status_code == 200:
        response = requests.post(url,data={	"type": "PDF",	"language": "pt"})
        return response.json()['url']
    else:
        print(requests.post(url).status_code)
        return 0

def createBackupDir(timestamp):
    try:
        os.mkdir(path_parent+"/backup/backup"+timestamp)
    except OSError:
        print("Creation of the backup directory failed")
    else:
        print("Successfully created the backup directory")

def backupProcess():
    downloadFromBackup(backupFile)

def backupFile():
    data = get("documents")
    if data == 0:
        sys.exit("Erro ao executar backup!")
    linhaInfo = data[0].copy() #copia o primeiro elemento com os dados dos documentos
    if linhaInfo["total_pages"] != linhaInfo["current_page"]: #se tiver mais de uma página, roda a call novamente para pegar os dados das prox paginas
        i = linhaInfo["current_page"]
        j = linhaInfo["total_pages"]
        while j != i:
            newData = get("documents", i+1)
            for item in range(1, newData[0]["total_documents"]+1):
                data.update(item)
                i += 1
    timestamp = str(round(time.time()))
    #busca as URLs de download e adiciona no dicionário por documento
    for i in range(1, linhaInfo["total_documents"]+1):
        data[i]["downloadURL"] = getDownloadURL(data[i]["uuidDoc"])
        data[i]["timestamp"] = timestamp
        print(data[i])
    print("URLs de download obtidas com sucesso")

    #gera um arquivo com os dados finalizados para conferência
    with open(path_parent+"/backup/" +"backup"+ timestamp +".txt", "w") as fileBkp:
        json.dump(data, fileBkp)
        print("Arquivo de backup salvo com sucesso")
    return "backup" + timestamp


def downloadFromBackup(filename):
    #fazer o backup direto do arquivo salvo anteriormente. para não fazer o processo novamente.
    with open(path_parent+"/backup/" + filename) as json_file:
        data = json.load(json_file)
    createBackupDir(data[1]["timestamp"])
    for i in range(1,data[0]["total_documents"]+1):
        print(data[i])
        print("Baixando PDFs")
        requestsURL = requests.get(data[i]["downloadURL"])
        with open(path_parent+"/backup/" +"backup"+ data[i]["timestamp"] +"/"+ data[i]["nameDoc"] + "-" + data[i]["statusId"]+".pdf","wb+") as pdf:
            pdf.write(requestsURL.content)