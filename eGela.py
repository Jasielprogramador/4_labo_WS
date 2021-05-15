from tkinter import messagebox
import requests
import urllib
import urllib.parse #https://stackoverflow.com/questions/28906859/module-has-no-attribute-urlencode
from bs4 import BeautifulSoup
import time
import helper


class eGela:
    _login = 0
    _cookie = ""
    _refs = []
    _root = None

    def __init__(self, root):
        self._root = root

    def check_credentials(self, username, password, event=None):
        popup, progress_var, progress_bar = helper.progress("check_credentials", "Logging into eGela...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        print("##### 1. ESKAERA #####")
        metodo = 'GET'
        goiburuak = {'Host': 'egela.ehu.eus'}
        edukia = ''
        uria = "http://egela.ehu.eus/login/index.php"

        erantzuna = requests.request(metodo, uria, headers=goiburuak, data=edukia, allow_redirects=False)

        codigo = erantzuna.status_code
        descripcion = erantzuna.reason
        print(str(codigo) + " " + descripcion)

        cookiea = ""
        location = ""

        if 'Location' in erantzuna.headers:
            location = erantzuna.headers['Location']
        if 'Set-Cookie' in erantzuna.headers:
            cookiea = erantzuna.headers['Set-Cookie'].split(",")[0]

        self._cookie = cookiea

        progress = 33
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)

        print("\n##### 2. ESKAERA #####")
        host = "egela.ehu.eus"
        metodo = 'POST'
        goiburuak = {'Host': host, 'Cookie': cookiea,
                     'Content-Type': 'application/x-www-form-urlencoded',
                     'Content-Length': '0'}
        edukia = {'username': username, 'password': password}
        edukia_encoded = urllib.parse.urlencode(edukia)
        goiburuak['Content-Length'] = str(len(edukia_encoded))
        erantzuna = requests.request(metodo, location, headers=goiburuak, data=edukia_encoded, allow_redirects=False)



        print("metodoa: " + metodo)
        print("uria: " + location)
        print("edukia: " + edukia_encoded)

        codigo = erantzuna.status_code
        descripcion = erantzuna.reason
        print(str(codigo) + " " + descripcion)

        if 'Location' in erantzuna.headers:
            location = erantzuna.headers['Location']
        if 'Set-Cookie' in erantzuna.headers:
            cookiea = erantzuna.headers['Set-Cookie'].split(",")[0]

        progress = 66
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)

        print("\n##### 3. ESKAERA #####")

        metodo = 'GET'
        goiburuak = {'Host': host, 'Cookie': cookiea}
        edukia = ''
        erantzuna = requests.request(metodo, location, headers=goiburuak, data=edukia, allow_redirects=False)

        print("HIRUGARREN ESKAERA")
        print("metodoa: " + metodo)
        print("uria: " + location)
        print("edukia: " + edukia)

        codigo = erantzuna.status_code
        descripcion = erantzuna.reason
        print(str(codigo) + " " + descripcion)

        progress = 100
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)
        popup.destroy()

        erantzuna.headers['Location'] = 'https://egela.ehu.eus/course/view.php?id=29145'
        if erantzuna.headers.__contains__('Location'):
            headers = {'Host': 'egela.ehu.eus', 'Cookie': self._cookie}
            erantzuna.headers['Location'] = 'https://egela.ehu.eus/course/view.php?id=42336'
            requests.request('GET', erantzuna.headers['Location'], headers=headers, allow_redirects=False)
            self._login = 1
            self._root.destroy()
        else:
            print("Alert Message", "Login incorrect!")



    def get_pdf_refs(self):
        popup, progress_var, progress_bar = helper.progress("get_pdf_refs", "Downloading PDF list...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        print("\n##### 4. ESKAERA (Ikasgairen eGelako orrialde nagusia) #####")

        host = "egela.ehu.eus"
        metodo = 'GET'
        uria = "https://egela.ehu.eus/course/view.php?id=42336"
        goiburuak = {'Host': host, 'Cookie': self._cookie}
        edukia = ''
        erantzuna = requests.request(metodo, uria, headers=goiburuak, data=edukia, allow_redirects=False)

        print("LAUGARREN ESKAERA")

        print("metodoa: " + metodo)
        print("uria: " + uria)
        print("edukia: " + edukia)

        codigo = erantzuna.status_code
        descripcion = erantzuna.reason
        print(str(codigo) + " " + descripcion)

        print("\n##### HTML-aren azterketa... #####")

        soup = BeautifulSoup(erantzuna.content, 'html.parser')
        a_links = soup.find_all("a", {'class': 'ehu-visible'})

        for each in a_links:
            if each['src'].find("/pdf") != -1:
                print("\n##### PDF-a bat aurkitu da! #####")
                pdf_link = each.parent['href']
                uria = pdf_link
                headers = {'Host': 'egela.ehu.eus', 'Cookie': self._cookie}
                erantzuna = requests.get(uria, headers=headers, allow_redirects=False)
                kodea = erantzuna.status_code
                deskribapena = erantzuna.reason
                print(str(kodea) + " " + deskribapena)
                edukia = erantzuna.content

                soup2 = BeautifulSoup(edukia, 'html.parser')
                div_pdf = soup2.find('div', {'class': 'resourceworkaround'})
                pdf_link = div_pdf.a['href']
                pdf_izena = pdf_link.split('/')[-1]
                self._refs.append({'link': pdf_link, 'pdf_name': pdf_izena})

            progress += 1.5
            progress_var.set(progress)
            progress_bar.update()
            time.sleep(0.1)

        popup.destroy()
        return self._refs

    def get_pdf(self, selection):
        print("##### PDF-a deskargatzen... #####")
        metodoa = 'GET'
        uria = self._refs[selection]['link']
        print(uria)
        headers = {'Host': 'egela.ehu.eus','Cookie': self._cookie}
        erantzuna = requests.get(uria, metodoa, headers=headers, allow_redirects=False)
        pdf_file = erantzuna.content
        pdf_name = self._refs[selection]['pdf_name']

        return pdf_name, pdf_file


