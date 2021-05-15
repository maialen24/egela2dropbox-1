from tkinter import messagebox
from bs4 import BeautifulSoup
import requests
import urllib
import urllib.parse
import time
import helper


class eGela:
    _login = 0
    _cookiea = ""
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
        metodoa = 'POST'
        print("Metodoa: ")
        print(metodoa)
        uria = "https://egela.ehu.eus/login/index.php"
        print("Uria: ")
        print(uria)
        headers = {'Host': 'egela.ehu.eus',
                   'Content-Type': 'application/x-www-form-urlencoded', }
        data = {'username': username.get(),
                'password': password.get()}
        data_encoded = urllib.parse.urlencode(data)
        headers['Content-Length'] = str(len(data_encoded))
        erantzuna = requests.request(metodoa, uria, headers=headers, data=data_encoded, allow_redirects=False)
        print(metodoa + " " + uria)
        kodea = erantzuna.status_code
        deskribapena = erantzuna.reason
        print(str(kodea) + " " + deskribapena)
        cookiea = ""
        location = ""
        for goiburua in erantzuna.headers:
            print(goiburua + ": " + erantzuna.headers[goiburua])
            if goiburua == "Set-Cookie":
                cookiea = erantzuna.headers[goiburua].split(";")[0]
                print("Cookie: ")
                print(cookiea)
            elif goiburua == "Location":
                location = erantzuna.headers[goiburua]
                print("Location: ")
                print(location)
        self._cookiea = cookiea
        edukia = erantzuna.content
        print("Edukia: ")
        print(edukia)
        progress = 33
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(1)

        print("\n##### 2. ESKAERA #####")

        metodoa = 'GET'
        print("Metodoa: ")
        print(metodoa)
        uria = location
        goiburuak = {'Host': uria.split('/')[2],
                     'Cookie': cookiea}
        erantzuna = requests.request(metodoa, uria, headers=goiburuak, allow_redirects=False)
        print(metodoa + " " + uria)
        kodea = erantzuna.status_code
        deskribapena = erantzuna.reason
        print(str(kodea) + " " + deskribapena)
        for goiburua in erantzuna.headers:
            print(goiburua + ": " + erantzuna.headers[goiburua])
            if goiburua == "Set-Cookie":
                cookiea = erantzuna.headers[goiburua].split(";")[0]
                print("Cookie: ")
                print(cookiea)
            elif goiburua == "Location":
                location = erantzuna.headers[goiburua]
                print("Location: ")
                print(location)
        edukia = erantzuna.content
        print("Edukia: ")
        print(edukia)

        progress = 66
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)

        print("\n##### 3. ESKAERA #####")
        metodoa = 'POST'
        print("Metodoa: ")
        print(metodoa)
        print(location)
        uria = location
        goiburuak = {'Host': 'egela.ehu.eus',  'Content-Type': 'application/x-www-form-urlencoded',
                     'Content-Length': str(len(data)), 'Cookie': self._cookiea}
        data_encoded = urllib.parse.urlencode(data)
        goiburuak['Content-Length'] = str(len(data_encoded))
        erantzuna = requests.request(metodoa, uria, data=data_encoded, headers=goiburuak, allow_redirects=False)
        print(metodoa + " " + uria)
        kodea = erantzuna.status_code
        deskribapena = erantzuna.reason
        print(str(kodea) + " " + deskribapena)
        for goiburua in erantzuna.headers:
            print(goiburua + ": " + erantzuna.headers[goiburua])
        edukia = erantzuna.content
        print("Edukia: ")
        print(edukia)

        progress = 100
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)
        popup.destroy()

        if erantzuna.status_code == 200:
            self._login = 1
            self._root.destroy()
        else:
            messagebox.showinfo("Alert Message", "Login incorrect!")
            print("Login incorrect!")

    def get_pdf_refs(self):
        popup, progress_var, progress_bar = helper.progress("get_pdf_refs", "Downloading PDF list...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        print("\n##### 4. ESKAERA (Ikasgairen eGelako orrialde nagusia) #####")
        metodoa = 'POST'
        data = ""
        print("Metodoa: ")
        print(metodoa)
        goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded',
                     'Content-Length': str(len(data)), 'Cookie': self._cookiea}
        uria = "https://egela.ehu.eus/course/view.php?id=42336&section=1"
        erantzuna = requests.request(metodoa, uria, data=data, headers=goiburuak, allow_redirects=False)
        edukia = erantzuna.content

        if erantzuna.status_code == 200:
            print("Web Sistemak")
            soup = BeautifulSoup(erantzuna.content, "html.parser")
            pdf_results = soup.find_all("div", {"class": "activityinstance"})
            kop = str(pdf_results).count("pdf")
            print("PDF kop: " + str(kop))

        print("\n##### HTML-aren azterketa... #####")
        soup = BeautifulSoup(edukia, 'html.parser')
        item_results = soup.find_all('img', {'class': 'iconlarge activityicon'})
        for each in item_results:

            if each['src'].find("/pdf") != -1:
                print("\n##### PDF-a bat aurkitu da! #####")
                pdf_link = each.parent['href']

                uria = pdf_link
                headers = {'Host': 'egela.ehu.eus',
                           'Cookie': self._cookiea}
                erantzuna = requests.get(uria, headers=headers, allow_redirects=False)
                print(metodoa + " " + uria)
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
        print("Metodoa: ")
        print(metodoa)
        uria = self._refs[selection]['link']
        print("Uria: ")
        print(uria)
        headers = {'Host': 'egela.ehu.eus',
                   'Cookie': self._cookiea}
        erantzuna = requests.get(uria, headers=headers, allow_redirects=False)
        pdf_file = erantzuna.content
        pdf_name = self._refs[selection]['pdf_name']
        print("PDF Izena: ")
        print(pdf_name)

        return pdf_name, pdf_file
