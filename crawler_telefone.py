import re
import threading

import requests
from bs4 import BeautifulSoup


DOMINIO = "https://django-anuncios.solyd.com.br"
URL_AUTOMOVEIS = "https://django-anuncios.solyd.com.br/automoveis/"

LINKS = []
TELEFONES = []


def requisicao(url):
    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            return resposta.text
        else:
            print("Erro de requisição da url")
    except Exception as error:
        print("Erro de requisição da url")
        print(error)
        

def parsing(resposta_html):
    try:
        soup = BeautifulSoup(resposta_html, 'html.parser')
        return soup
    except Exception as error:
        print("Erro de parsing")
        print(error)



def encontrar_links(soup):
    try:
        cards_pai = soup.find("div", class_ = "ui three doubling link cards")
        cards = cards_pai.find_all("a")
    except:
        print("Erro ao encontrar link")
    links=[]
    for card in cards:
        link = card["href"]
        links.append(link)
    return links

    
def encontrar_telefones(soup):
    try:
        descricao = soup.find_all("div", class_="sixteen wide column")[2].p.getText().strip()
    except Exception as error:
        print("Erro ao acessar descrição")
        return None
        
    regex = re.findall(r"\(?0?([1-9]{2})[ \-\.\)]{0,2}(9[ \-\.]?\d{4})[ \-\.]?(\d{4})", descricao)
    if regex:
        return regex



def descobrir_telefones():
    while True:
        try:
            link_anuncio = LINKS.pop(0)
            
        except:
            break
        resposta_anuncio = requisicao(DOMINIO + link_anuncio)
        if resposta_anuncio:
            soup_anuncio = parsing(resposta_anuncio)
            if soup_anuncio:
                telefones = encontrar_telefones(soup_anuncio)
                if telefones:
                   for telefone in telefones:
                       print("Telefone encontrado:", telefone)
                       TELEFONES.append(telefone)
                       salvar_telefone(telefone) 
    

def salvar_telefone(telefone):
    string_telefone = "{}{}{}\n".format(telefone[0], telefone[1], telefone[2])
    try:
        with open("telefones.csv", "a") as file:
            file.write(string_telefone)
    except Exception as error:
        print("Erro ao salvar arquivo")
        print(error)
        
        
if __name__ == "__main__":
    resposta_busca = requisicao(URL_AUTOMOVEIS)
    if resposta_busca:
        soup_busca = parsing(resposta_busca)
        if soup_busca:
            LINKS = encontrar_links(soup_busca)
            
            THREADS = []
            for i in range(15):
                thread = threading.Thread(target=descobrir_telefones)
                THREADS.append(thread)
            
            for thread in THREADS:
                thread.start()
            
            for thread in THREADS:
                thread.join()  
                
                   