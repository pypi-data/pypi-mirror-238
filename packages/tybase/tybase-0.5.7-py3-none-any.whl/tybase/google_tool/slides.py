from google.oauth2 import service_account
import googleapiclient.discovery


class GoogleSlides:
    def __init__(self, service_account_file):
        SCOPES = ('https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/presentations')
        credentials = service_account.Credentials.from_service_account_file(service_account_file, scopes=SCOPES)
        self.slides_service = googleapiclient.discovery.build('slides', 'v1', credentials=credentials)

    def get_slide_id(self, presentation_id, slide_number=1):
        presentation = self.slides_service.presentations().get(presentationId=presentation_id).execute()
        slides = presentation.get('slides')
        return slides[slide_number - 1]['objectId']

    # 获取幻灯片的所有页数
    def get_total_slides(self, presentation_id):
        presentation = self.slides_service.presentations().get(presentationId=presentation_id).execute()
        return len(presentation.get('slides'))

    def duplicate_slide(self, presentation_id, slide_numbers=[1]):
        """复制指定的幻灯片页面并返回新页面的ID列表。"""
        new_slide_ids = []
        for slide_number in slide_numbers:
            slide_id = self.get_slide_id(presentation_id, slide_number)
            requests = [{
                'duplicateObject': {
                    'objectId': slide_id
                }
            }]
            response = self.slides_service.presentations().batchUpdate(body={'requests': requests},
                                                                       presentationId=presentation_id).execute()
            new_slide_ids.append(response['replies'][0]['duplicateObject']['objectId'])
        return new_slide_ids

    def delete_slide(self, presentation_id, slide_id):
        """删除指定的幻灯片页面。"""
        requests = [{
            'deleteObject': {
                'objectId': slide_id
            }
        }]
        self.slides_service.presentations().batchUpdate(body={'requests': requests},
                                                        presentationId=presentation_id).execute()

    def replace_placeholders(self, presentation_id, replacements, slide_id=None):
        requests = []
        for placeholder, replacement in replacements.items():
            request = {
                'replaceAllText': {
                    'containsText': {'text': placeholder},
                    'replaceText': replacement
                }
            }
            if slide_id:
                request['replaceAllText']['pageObjectIds'] = [slide_id]
            requests.append(request)
        self.slides_service.presentations().batchUpdate(body={'requests': requests},
                                                        presentationId=presentation_id).execute()

    def replace_image_placeholder(self, presentation_id, placeholder_image_id, new_image_url, slide_id=None):
        # 获取指定的幻灯片或默认的第一张幻灯片
        presentation = self.slides_service.presentations().get(presentationId=presentation_id).execute()
        slides = presentation.get('slides')
        target_slide = None
        if slide_id:
            for slide in slides:
                if slide['objectId'] == slide_id:
                    target_slide = slide
                    break
        else:
            target_slide = slides[0]

        if not target_slide:
            raise ValueError(f"Slide with ID '{slide_id}' not found!")

        # 在指定的幻灯片中查找占位符图片
        target_image = None
        for image in target_slide['pageElements']:
            if 'image' in image and image['objectId'] == placeholder_image_id:
                target_image = image
                break

        if not target_image:
            raise ValueError(f"Placeholder image with ID '{placeholder_image_id}' not found in the specified slide!")

        # position = target_image['size']
        size = target_image['size']

        # 创建替换图片的请求
        requests = [{
            'createImage': {
                'url': new_image_url,
                'objectId': 'new_image_' + target_image['objectId'],
                'elementProperties': {
                    'pageObjectId': target_slide['objectId'],
                    'size': size,
                    'transform': target_image['transform']
                }
            }
        }, {
            'deleteObject': {
                'objectId': target_image['objectId']
            }
        }]

        self.slides_service.presentations().batchUpdate(body={'requests': requests},
                                                        presentationId=presentation_id).execute()


if __name__ == '__main__':
    SERVICE_ACCOUNT_FILE = 'credentials.json'
    presentation_id = 'xxxxxx'  # 图片替换
    slides = GoogleSlides(SERVICE_ACCOUNT_FILE)

    # 替换占位符为图片
    image_url = "http://usfile.xxxxx.com/uploads/android/user/1694260015549.jpg"

    # 根据图片id替换占位符, 用谷歌的脚本来获取 g27d022e8b4a_1_0, slide_id 可以通过 get_slide_id 方法获取
    slides.replace_image_placeholder(presentation_id, "g27d022e8b4a_1_0", image_url, slide_id=None)
