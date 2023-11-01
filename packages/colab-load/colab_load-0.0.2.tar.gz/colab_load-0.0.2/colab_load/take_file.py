import requests
import re
import threading
from fake_useragent import UserAgent

class FileNameT(threading.Thread):

    def __init__(self, url: str):
        super().__init__()
        self.ua = UserAgent()
        self.url = url
        self.file_name = None

    def run(self):
        self.file_name = self.get_file_name()

    def get_file_name(self) -> str:
        headers = {
            'authority': 'content.googleapis.com',
            'accept': '*/*',
            'accept-language': 'ru,en;q=0.9',
            'referer': 'https://content.googleapis.com/static/proxy.html?usegapi=1&jsh=m%3B%2F_%2Fscs%2Fabc-static%2F_%2Fjs%2Fk%3Dgapi.gapi.en.CzrNRWo3AFk.O%2Fd%3D1%2Frs%3DAHpOoo8xPbrtpW2bPUIcgU2adGqIEpV82Q%2Fm%3D__features__',
            'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': f'{self.ua.random}',
            'x-clientdetails': 'appVersion=5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F116.0.5845.888%20Safari%2F537.36&platform=Win32&userAgent=Mozilla%2F5.0%20(Windows%20NT%2010.0%3B%20Win64%3B%20x64)%20AppleWebKit%2F537.36%20(KHTML%2C%20like%20Gecko)%20Chrome%2F116.0.5845.888%20Safari%2F537.36',
            'x-goog-encode-response-if-executable': 'base64',
            'x-javascript-user-agent': 'google-api-javascript-client/1.1.0',
            'x-origin': 'https://colab.research.google.com',
            'x-referer': 'https://colab.research.google.com',
            'x-requested-with': 'XMLHttpRequest',
        }

        params = {
            'fields': 'resourceKey,alternateLink,capabilities/canReadRevisions,createdDate,downloadUrl,fileSize,headRevisionId,id,labels,mimeType,originalFilename,owners,parents,properties,shared,teamDriveId,title,userPermission',
            'supportsTeamDrives': 'true',
            'key': 'AIzaSyB10s2vWUTwP0pj20wZoxmpZIt3rRodYeg',
        }

        response = requests.get(
            f'https://content.googleapis.com/drive/v2beta/files/{self.url.split("/")[-1].split("?")[0]}',
            headers=headers,
            params=params,
        )

        try:
            r_j = response.json()['title']
            return re.compile(r'[^\w"]+').sub("_", r_j).replace('"', "_")
        except:
            return ""