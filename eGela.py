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

        cookiea = ""
        popup, progress_var, progress_bar = helper.progress("check_credentials", "Logging into eGela...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        print("##### 1. ESKAERA #####")
        metodo = "POST"
        edukia = {'username': username.get(), 'password': password.get()}
        goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded',
                     'Content-Length': str(len(edukia))}
        uria = "http://egela.ehu.eus/login/index.php"

        edukia_encoded = urllib.parse.urlencode(edukia)
        goiburuak['Content-Length'] = str(len(edukia_encoded))

        erantzuna = requests.request(metodo, uria, headers=goiburuak, data=edukia_encoded, allow_redirects=False)

        codigo = erantzuna.status_code
        descripcion = erantzuna.reason
        print(str(codigo) + " " + descripcion)

        if 'Location' in erantzuna.headers:
            uria = erantzuna.headers['Location']
        if 'Set-Cookie' in erantzuna.headers:
            cookiea = erantzuna.headers['Set-Cookie'].split(",")[0]

        progress = 33
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)

        print("\n##### 2. ESKAERA #####")
        host = "egela.ehu.eus"
        metodo = 'POST'
        goiburuak = {'Host': host, 'Cookie': cookiea,
                     'Content-Type': 'application/x-www-form-urlencoded',
                     'Content-Length': str(len(edukia))}
        edukia_encoded = urllib.parse.urlencode(edukia)
        goiburuak['Content-Length'] = str(len(edukia_encoded))
        erantzuna = requests.request(metodo, uria, headers=goiburuak, data=edukia_encoded, allow_redirects=False)



        print("metodoa: " + metodo)
        print("uria: " + uria)
        print("edukia: " + edukia_encoded)

        codigo = erantzuna.status_code
        descripcion = erantzuna.reason
        print(str(codigo) + " " + descripcion)

        if 'Location' in erantzuna.headers:
            uria= erantzuna.headers['Location']
        if 'Set-Cookie' in erantzuna.headers:
            cookiea = erantzuna.headers['Set-Cookie'].split(",")[0]

        progress = 66
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)

        print("\n##### 3. ESKAERA #####")

        metodo = 'GET'
        goiburuak = {'Host': 'egela.ehu.eus', "Cookie": cookiea}
        erantzuna = requests.request(metodo, uria, headers=goiburuak, allow_redirects=False)

        print("HIRUGARREN ESKAERA")
        print("metodoa: " + metodo)
        print("uria: " + uria)
        #print("edukia: " + edukia_encoded)

        if 'Location' in erantzuna.headers:
            uria = erantzuna.headers['Location']
        if 'Set-Cookie' in erantzuna.headers:
            cookiea = erantzuna.headers['Set-Cookie'].split(",")[0]

        erantzuna = requests.request(metodo, uria, headers=goiburuak, allow_redirects=False)

        codigo = erantzuna.status_code
        descripcion = erantzuna.reason
        print(str(codigo) + " " + descripcion)

        progress = 100
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)
        popup.destroy()



        COMPROBACION_DE_LOG_IN = erantzuna.status_code == 200

        if COMPROBACION_DE_LOG_IN:
            self._login = 1
            print(self._login)
            self._cookie = cookiea
            #print(self._cookiea)
            self._root.destroy()
        else:
            messagebox.showinfo("Alert Message", "Login incorrect!")



    def get_pdf_refs(self):
        popup, progress_var, progress_bar = helper.progress("get_pdf_refs", "Downloading PDF list...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        print("\n##### 4. ESKAERA (Ikasgairen eGelako orrialde nagusia) #####")

        metodo = 'POST'
        datuak = ""
        goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded',
                     'Content-Length': str(len(datuak)), "Cookie": self._cookie}
        uria = "https://egela.ehu.eus/course/view.php?id=42336&section=1"
        erantzuna = requests.request(metodo, uria, headers=goiburuak, allow_redirects=False)

        print("LAUGARREN ESKAERA")

        print("metodoa: " + metodo)
        print("uria: " + uria)

        codigo = erantzuna.status_code
        descripcion = erantzuna.reason
        print(str(codigo) + " " + descripcion)

        if (erantzuna.status_code == 200):
            print("Web Sistemak")
            soup = BeautifulSoup(erantzuna.content, "html.parser")
            pdf_results = soup.find_all("div", {"class": "activityinstance"})
            kop = str(pdf_results).count("pdf")

        print("PDF kopurua " + str(kop))
        # print("PDF kopurua " + str(len(self._refs)))
        progress_step = float(100.0 / kop)
        # progress_step = float(100.0 / len(self._refs))
        print("\n##### HTML-aren azterketa... #####")

        for pdf in pdf_results:
            if pdf.find("img", {
                "src": "https://egela.ehu.eus/theme/image.php/fordson/core/1619589309/f/pdf"}):  # egelako elementuetatik, pdf bezala agertzen direnak bilatu
                # ACTUALIZAR BARRA DE PROGRESO
                # POR CADA PDF ANIADIDO EN self._refs
                progress += progress_step
                progress_var.set(progress)
                progress_bar.update()
                time.sleep(0.1)

                uri = pdf.find("a")["href"] + "&redirect=1"
                metodo = 'POST'
                datuak = ""
                goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded',
                             'Content-Length': str(len(datuak)), "Cookie": self._cookie}
                erantzuna = requests.request(metodo, uri, data=datuak, headers=goiburuak,
                                             allow_redirects=False)

                pdf_uri = erantzuna.headers['Location']
                pdf_link = pdf_uri.split("mod_resource/content/")[1].split("/")[1].replace("%20", "_")
                self._refs.append({"pdf_name": pdf_link, "pdf_link": pdf_uri})

        for elem in self._refs:
            print(elem)
        popup.destroy()
        return self._refs

    def get_pdf(self, selection):
        print("##### PDF-a deskargatzen... #####")
        pdf_name = self._refs[selection]['pdf_name']
        pdf_link = self._refs[selection]['pdf_link']


        cook = self._cookie
        goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded',
                     'Content-Length': '0', "Cookie": cook}
        erantzuna = requests.request('GET', pdf_link, headers=goiburuak, allow_redirects=False)

        pdf_file = erantzuna.content
        print(pdf_name + " downloaded !")

        return pdf_name, pdf_file


