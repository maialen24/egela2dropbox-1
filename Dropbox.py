import requests
import urllib
import urllib.parse
import webbrowser
from socket import AF_INET, socket, SOCK_STREAM
import json
import helper

# Los he sacado de la app mia (WEBSISTEMAK2021) de Dropbox
app_key = 'jzqijn4fw2c6813'
app_secret = 'vodl11sr1r7nxme'

server_addr = "localhost"

# En este caso vamos a utilizar el puerto 8090, la misma que la app de Dropbox
server_port = 8090

redirect_uri = "http://" + server_addr + ":" + str(server_port)


class Dropbox:
    _access_token = ""
    _path = "/"
    _files = []
    _root = None
    _msg_listbox = None

    def __init__(self, root):
        self._root = root

    def local_server(self):
        # 8090. portuan entzuten dagoen zerbitzaria sortu
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind((server_addr, server_port))
        server_socket.listen(1)
        print("\tLocal server listening on port " + str(server_port))

        # nabitzailetik 302 eskaera jaso
        client_connection, client_address = server_socket.accept()
        eskaera = client_connection.recv(1024)
        print("\tRequest from the browser received at local server:")
        print("Eskaera: ")
        print(eskaera)

        # eskaeran "auth_code"-a bilatu
        lehenengo_lerroa = eskaera.decode("utf8").split('\n')[0]
        aux_auth_code = lehenengo_lerroa.split(' ')[1]
        auth_code = aux_auth_code[7:].split('&')[0]
        print("\tauth_code: " + auth_code)

        # erabiltzaileari erantzun bat bueltatu
        http_response = "HTTP/1.1 200 OK\r\n\r\n" \
                        "<html>" \
                        "<head><title>Proba</title></head>" \
                        "<body>The authentication flow has completed. Close this window.</body>" \
                        "</html>"
        client_connection.sendall(http_response.encode(encoding="utf8"))
        client_connection.close()
        server_socket.close()
        return auth_code

    def do_oauth(self):
        uri = "https://www.dropbox.com/oauth2/authorize"
        parametroak = {'response_type': 'code', 'client_id': app_key, 'redirect_uri': redirect_uri}
        parametroak_encoded = urllib.parse.urlencode(parametroak)
        webbrowser.open(uri + '?' + parametroak_encoded)
        print("/oauth2/authorize")
        auth_code = self.local_server()
        print("auth_code: " + auth_code)
        uri = "https://api.dropboxapi.com/oauth2/token"
        goiburuak = {'Host': 'api.dropboxapi.com', 'Content-Type': 'application/x-www-form-urlencoded'}
        datuak = {'code': auth_code, 'client_id': app_key, 'client_secret': app_secret, 'redirect_uri': redirect_uri,
                  'grant_type': 'authorization_code'}
        erantzuna = requests.post(uri, headers=goiburuak, data=datuak, allow_redirects=False)
        status = erantzuna.status_code
        edukia = erantzuna.text
        edukia_json = json.loads(edukia)
        access_token = edukia_json['access_token']
        print("Status: ")
        print(str(status))
        print("Edukia: ")
        print(edukia)
        print("access_token: ")
        print(access_token)

        self._access_token = access_token
        self._root.destroy()

    def list_folder(self, msg_listbox):
        print("/list_folder")
        uri = "https://api.dropboxapi.com/2/files/list_folder"
        if self._path == '/':
            path = ""
        else:
            path = self._path
        datuak = {'path': path, "recursive": False, "include_media_info": False, "include_deleted": False,
                  "include_has_explicit_shared_members": False, "include_mounted_folders": True,
                  "include_non_downloadable_files": True}
        datuak_encoded = json.dumps(datuak)
        goiburuak = {'Host': 'api.dropboxapi.com', 'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/json'}
        erantzuna = requests.post(uri, headers=goiburuak, data=datuak_encoded, allow_redirects=False)
        status = erantzuna.status_code
        edukia = erantzuna.text
        print("Status: ")
        print(str(status))
        print("Edukia: ")
        print(edukia)
        edukia_json_dict = json.loads(edukia)

        self._files = helper.update_listbox2(msg_listbox, self._path, edukia_json_dict)

    def transfer_file(self, file_path, file_data):
        print("/upload" + file_path)
        uri = "https://content.dropboxapi.com/2/files/upload"
        datuak = {'path': file_path, 'mode': 'add', 'autorename': True, 'mute': False, 'strict_conflict': False}
        datuak_json = json.dumps(datuak)
        goiburuak = {'Host': 'content.dropboxapi.com', 'Authorization': 'Bearer ' + self._access_token,
                     'Dropbox-API-Arg': datuak_json, 'Content-Type': 'application/octet-stream'}
        erantzuna = requests.post(uri, headers=goiburuak, data=file_data, allow_redirects=False)
        status = erantzuna.status_code
        print("Status: ")
        print(str(status))

    def delete_file(self, file_path):
        print("/delete_file " + file_path)
        uri = 'https://api.dropboxapi.com/2/files/delete'
        datuak = {'path': file_path}
        datuak_json = json.dumps(datuak)
        goiburuak = {'Host': 'api.dropboxapi.com', 'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/json'}
        erantzuna = requests.post(uri, headers=goiburuak, data=datuak_json, allow_redirects=False)
        status = erantzuna.status_code
        print("Status: ")
        print(str(status))

    def create_folder(self, path):
        print("/create_folder " + str(path))
        uri = 'https://api.dropboxapi.com/2/files/create_folder'
        datuak = {'path': path, 'autorename': False}
        datuak_json = json.dumps(datuak)
        goiburuak = {'Host': 'api.dropboxapi.com', 'Authorization': 'Bearer ' + self._access_token,
                     'Content-Type': 'application/json'}
        erantzuna = requests.post(uri, headers=goiburuak, data=datuak_json, allow_redirects=False)
        status = erantzuna.status_code
        print("Status: ")
        print(str(status))
