import requests
from google.oauth2 import service_account
import googleapiclient.discovery
from googleapiclient.http import MediaFileUpload
import base64
import os


class GoogleDrive:
    def __init__(self, service_account_file):
        SCOPES = ('https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/presentations')
        credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes=SCOPES)
        self.slides_service = googleapiclient.discovery.build('slides', 'v1', credentials=credentials)

    def download_image(self, presentation_id, slide_id, filename):
        thumbnail_response = self.slides_service.presentations().pages().getThumbnail(presentationId=presentation_id,
                                                                                      pageObjectId=slide_id).execute()
        thumbnail_url = thumbnail_response.get('contentUrl')

        response = requests.get(thumbnail_url, stream=True)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

    def get_image_base64(self, presentation_id, slide_id):
        thumbnail_response = self.slides_service.presentations().pages().getThumbnail(presentationId=presentation_id,
                                                                                      pageObjectId=slide_id).execute()
        thumbnail_url = thumbnail_response.get('contentUrl')

        response = requests.get(thumbnail_url)
        response.raise_for_status()
        return base64.b64encode(response.content).decode('utf-8')

    def download_all_images(self, presentation_id, slides_obj, folder_name="slides_images"):
        import os
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        total_slides = slides_obj.get_total_slides(presentation_id)
        for i in range(1, total_slides + 1):
            slide_id = slides_obj.get_slide_id(presentation_id, slide_number=i)
            filename = os.path.join(folder_name, f'slide_{i}.png')
            self.download_image(presentation_id, slide_id, filename)

        print(f"所有 {total_slides} 页的幻灯片已保存在 '{folder_name}' 文件夹中。")

    # 其他与Drive相关的操作方法可以在这里添加...

    def upload_file(self, file_path, mime_type='image/jpeg'):
        """上传本地文件到Google Drive并返回其ID。"""

        file_metadata = {
            'name': os.path.basename(file_path)
        }
        media = MediaFileUpload(file_path, mimetype=mime_type)
        file = self.slides_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        return file['id']
