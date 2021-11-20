from tkinter import messagebox
from bs4 import BeautifulSoup
import requests
import urllib
import urllib.parse
import time
import helper


class eGela:
    _login = 0
    _cookiea = "MoodleSessionegela=ftvembt2rmeabfurj204s0qf50629403"
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
            elif goiburua == "Location":
                location = erantzuna.headers[goiburua]
        # self._cookiea = cookiea
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
                     'Cookie': self._cookiea}
        erantzuna = requests.request(metodoa, uria, headers=goiburuak, allow_redirects=False)
        print(metodoa + " " + uria)
        kodea = erantzuna.status_code
        deskribapena = erantzuna.reason
        print(str(kodea) + " " + deskribapena)
        for goiburua in erantzuna.headers:
            print(goiburua + ": " + erantzuna.headers[goiburua])
            if goiburua == "Set-Cookie":
                cookiea = erantzuna.headers[goiburua].split(";")[0]
            elif goiburua == "Location":
                location = erantzuna.headers[goiburua]
        edukia = erantzuna.content
        print("Edukia: ")
        print(edukia)
        # self._cookiea=cookiea

        progress = 66
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)

        print("\n##### 3. ESKAERA #####")
        metodoa = 'POST'
        print("Metodoa: ")
        print(metodoa)
        uria = location
        goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded',
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
        print(self._cookiea)

        progress = 100
        progress_var.set(progress)
        progress_bar.update()
        time.sleep(0.1)
        popup.destroy()

        if 'Location' in erantzuna.headers:
            uria = erantzuna.headers['Location']
            metodoa = 'POST'
            print("Metodoa: ")
            print(metodoa)
            # uria = location
            goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded',
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
            print(self._cookiea)

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
            print("\n")
            print("Login incorrect!")

    def get_pdf_refs(self):
        popup, progress_var, progress_bar = helper.progress("get_pdf_refs", "Downloading PDF list...")
        progress = 0
        progress_var.set(progress)
        progress_bar.update()

        print("\n##### 4. ESKAERA (Ikasgairen eGelako orrialde nagusia) #####")
        metodoa = 'POST'
        data = ""
        section = 1
        pdf = []
        status = 0
        pdf_kop = 0
        kop = 1
        print("Metodoa: ")
        print(metodoa)
        print(self._cookiea)
        while status != 404 and pdf_kop != kop:
            goiburuak = {'Host': 'egela.ehu.eus', 'Content-Type': 'application/x-www-form-urlencoded',
                         'Content-Length': str(len(data)), 'Cookie': self._cookiea}
            uria = "https://egela.ehu.eus/course/view.php?id=48048#section-" + str(section)
            # uria = "https://egela.ehu.eus/course/view.php?id=48048"
            # uria = "https://egela.ehu.eus/course/view.php?id=48048"
            print(uria)
            erantzuna = requests.request(metodoa, uria, data=data, headers=goiburuak, allow_redirects=False)
            edukia = erantzuna.content
            status = erantzuna.status_code
            print(status)

            if erantzuna.status_code == 200:
                print("Asignaturas")
                soup = BeautifulSoup(erantzuna.content, "html.parser")
                pdf_results = soup.find_all("div", {"class": "activityinstance"})
                # pdf_results = soup.find_all('a', {'class': 'aalink'})
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
                    pdf_kop = pdf_kop + 1
                    if pdf.__contains__(uria):
                        print("PDF hau " + uria + " aurkituta dago jada!")
                    else:
                        headers = {'Host': 'egela.ehu.eus', 'Cookie': self._cookiea}
                        erantzuna = requests.get(uria, headers=headers, allow_redirects=False)
                        status = erantzuna.status_code
                        print(status)
                        if status == 303:
                            pdf_uria = erantzuna.headers['Location']
                            erantzuna = requests.get(pdf_uria, headers=headers, allow_redirects=False)
                            print(metodoa + " " + uria)
                            kodea = erantzuna.status_code
                            deskribapena = erantzuna.reason
                            print(str(kodea) + " " + deskribapena)
                            pdf_link = pdf_uria.split("mod_resource/content/")[1].split("/")[1].replace("%20", "_")
                            pdf_izena = pdf_link.split('/')[-1]
                            self._refs.append({'link': pdf_uria, 'pdf_name': pdf_izena})

                        elif 'resource' in uria:
                            print(metodoa + " " + uria)
                            kodea = erantzuna.status_code
                            deskribapena = erantzuna.reason
                            print(str(kodea) + " " + deskribapena)
                            pdf_link = pdf_uria.split("mod_resource/content/")[1].split("/")[1].replace("%20", "_")
                            pdf_izena = pdf_link.split('/')[-1]
                            self._refs.append({'link': pdf_uria, 'pdf_name': pdf_izena})
                        else:
                            print(metodoa + " " + uria)
                            kodea = erantzuna.status_code
                            deskribapena = erantzuna.reason
                            print(str(kodea) + " " + deskribapena)
                            edukia = erantzuna.content
                            # print(edukia)
                            status = erantzuna.status_code
                            soup2 = BeautifulSoup(edukia, 'html.parser')
                            div_pdf_elements = soup2.find_all('div', {'class': 'resourceworkaround'})
                            # print(div_pdf)
                            for div in div_pdf_elements:
                                if "href" in str(div):
                                    pdf_link = div["href"]
                            # pdf_link = div_pdf.a['href']
                            pdf_izena = pdf_link.split('/')[-1]
                            self._refs.append({'link': pdf_link, 'pdf_name': pdf_izena})

                        pdf.append(uria)

                progress += 1.5
                progress_var.set(progress)
                progress_bar.update()
                time.sleep(0.1)

            section = section + 1

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
