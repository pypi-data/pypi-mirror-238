# 封装这个类
import os
import random

from tybase.google_tool.drive import GoogleDrive
from tybase.google_tool.slides import GoogleSlides
from loguru import logger


class SlidesProcessor:
    '''
    from tybase.google_tool.processor import SlidesProcessor

    '''

    def __init__(self, service_account_file):
        self.slides = GoogleSlides(service_account_file)
        self.drive = GoogleDrive(service_account_file)

    def process_template(self, presentation_id, template_indexes, replacements, output_filename):
        # 复制模板页面
        new_slide_id_list = self.slides.duplicate_slide(presentation_id, template_indexes)
        logger.info("复制页面完成!")

        # 进行文本替换
        self.slides.replace_placeholders(presentation_id, replacements, slide_id=new_slide_id_list[0])
        logger.info("文本替换完成!")

        # 下载图片
        self.drive.download_image(presentation_id, new_slide_id_list[0], output_filename)
        logger.info("图片下载完成!")

        # 删除复制的页面
        self.slides.delete_slide(presentation_id, new_slide_id_list[0])
        logger.info("页面删除完成!")

    def process_random_template(self, presentation_id, template_indexes, replacements_list, output_folder,
                                filename_template=None):
        # 确保输出文件夹存在
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # 如果没有提供文件名模板，则使用默认模板
        if filename_template is None:
            filename_template = "slide_thumbnail_{idx}.jpg"

        for idx, replacements in enumerate(replacements_list):
            # 随机选择一个模板
            random_template_index = random.choice(template_indexes)

            # 复制模板页面
            new_slide_id_list = self.slides.duplicate_slide(presentation_id, [random_template_index])
            logger.info(f"复制页面 {random_template_index} 完成!")

            # 进行文本替换
            self.slides.replace_placeholders(presentation_id, replacements, slide_id=new_slide_id_list[0])
            logger.info("文本替换完成!")

            # 下载图片
            output_filename = os.path.join(output_folder, filename_template.format(idx=idx))
            self.drive.download_image(presentation_id, new_slide_id_list[0], output_filename)
            logger.info(f"图片 {output_filename} 下载完成!")

            # 删除复制的页面
            self.slides.delete_slide(presentation_id, new_slide_id_list[0])
            logger.info("页面删除完成!")


if __name__ == '__main__':
    SERVICE_ACCOUNT_FILE = 'credentials.json'
    presentation_id = 'xxxx'
    processor = SlidesProcessor(SERVICE_ACCOUNT_FILE)

    replacements_list = [
        {
            '{{ title }}': '提供情绪价值1',
            '{{ content }}': '的10种方法1!'
        },
        {
            '{{ title }}': '提供情绪价值2',
            '{{ content }}': '的10种方法2!'
        },
        # ... [其他替换字典]
    ]
    #
    processor.process_random_template(presentation_id, [1, 2], replacements_list, 'output_folder',
                                      "my_custom_name_{idx}.jpg")
