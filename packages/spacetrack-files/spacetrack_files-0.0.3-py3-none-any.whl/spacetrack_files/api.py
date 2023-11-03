from datetime import datetime
import requests
import json
from tqdm import tqdm

URI_BASE = "https://www.space-track.org"
class SpaceTrackUris:
    LOGIN = URI_BASE + "/ajaxauth/login"

    class PublicFiles:
        DIRS                    = URI_BASE + "/publicfiles/query/class/dirs"
        LOAD_PUBLIC_DATA        = URI_BASE + "/publicfiles/query/class/loadpublicdata"
        FILES                   = URI_BASE + "/publicfiles/query/class/files"

        def DOWNLOAD(filename: str): 
            return URI_BASE + f"/publicfiles/query/class/download?name={filename}"

from dataclasses import dataclass
import json
from dataclasses import dataclass
import json

units = {"Bytes": 1, "KB": 2**10, "MB": 2**20, "GB": 2**30}
def parse_size(size):
    number, unit = [string.strip() for string in size.split()]
    return int(float(number)*units[unit])

@dataclass
class FileMeta:
    type: str
    date: datetime
    size: str
    size_bytes: int
    link: str
    name: str

    def from_json(data):
        type = data['type']
        date = data['date']
        size = data['size']
        size_bytes = parse_size(data['size'])
        link = data['link']
        name = data['name']
        
        file_meta = FileMeta(type, date, size, size_bytes, link, name)
        return file_meta

class SpaceTrackApi:
    session: requests.Session

    def __init__(self, login, password) -> None:
        self.session = requests.Session()
        response = self.session.post(SpaceTrackUris.LOGIN, data={'identity': login, 'password': password})
        assert response.status_code == 200

    def _execute_request(self, uri):
        response = self.session.get(uri)
        if response.status_code != 200:
            print(f'WARNING: got {response.status_code} status code')
        if response.content == 0:
            print(f'WARNING: no content')
        return response
        pass

    def getDirsWithFiles(self) -> list[str]:
        response = self._execute_request(SpaceTrackUris.PublicFiles.FILES)
        files_list = json.loads(response.content)
        return files_list
    
    def getFilesMetaList(self) -> list[FileMeta]:
        response = self._execute_request(SpaceTrackUris.PublicFiles.LOAD_PUBLIC_DATA)
        files_meta_json = json.loads(response.content)
        file_meta = list(map(FileMeta.from_json, files_meta_json))
        return file_meta
    
    def getDirsList(self) -> list[str]:
        response = self._execute_request(SpaceTrackUris.PublicFiles.DIRS)
        dirs_list = json.loads(response.content)
        return dirs_list
    
    def downloadFile(self, filename, save_path):
        download_uri = SpaceTrackUris.PublicFiles.DOWNLOAD(filename)
        print(f'Attempting download: {download_uri}')
        download = self.session.get(download_uri, stream=True)
        assert download.status_code == 200

        content_length = int(download.headers['Content-Length'])
        chunk_size = 8192  # Размер чанка
        total_chunks = (content_length + chunk_size - 1) // chunk_size
        
        with open(save_path, 'wb') as file:
            for chunk in tqdm(download.iter_content(chunk_size), total=total_chunks):
                if chunk:
                    file.write(chunk)
