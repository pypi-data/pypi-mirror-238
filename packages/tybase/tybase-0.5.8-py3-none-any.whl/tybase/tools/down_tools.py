import os
import requests
import hashlib
import mimetypes
from PIL import Image


class FileDownloader:
    """
    from tybase.tools.down_tools import FileDownloader
    FileDownloader: 一个用于下载文件的类。

    属性:
    save_dir (str): 文件下载的默认保存目录。

    方法:
    - download_file(url): 根据URL下载单个文件。
    - download_files(urls): 根据URL列表下载多个文件。
    - download_file_into_directory(url, directory, target_filename): 下载文件并保存到指定目录并使用指定文件名。

    使用示例:
        downloader = FileDownloader(save_dir="./downloads/audio")
        path = downloader.download_file(single_url)
        directory_path = downloader.download_files(urls)

    完整例子
    # 使用示例
    downloader = FileDownloader(save_dir="./downloads/audio")

    # # 单个文件下载
    single_url = "https://www.baidu.com/output_audio.mp3"
    path = downloader.download_file(single_url)
    print(f"文件已保存至: {path}")

    # 多文件下载
    urls = [
        "https://www.baidu.com/1691052671.png",
        "https://www.baidu.com/1691054539.png",
    ]
    directory_path = downloader.download_files(urls)
    print(f"所有文件已保存至目录: {directory_path}")
    """

    def __init__(self, save_dir='./downloads'):
        """
        初始化FileDownloader类。

        参数:
        - save_dir (str): 文件下载的保存目录。默认为'./downloads'。
        """
        self.save_dir = save_dir
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    @staticmethod
    def calculate_md5_for_string(input_string):
        """
        根据提供的字符串计算MD5值。

        参数:
        - input_string (str): 需要计算MD5的字符串。

        返回:
        str: 计算出的MD5值。
        """
        md5 = hashlib.md5()
        md5.update(input_string.encode('utf-8'))
        return md5.hexdigest()

    def download_file(self, url):
        url_md5 = self.calculate_md5_for_string(url)

        response = requests.get(url, stream=True)
        response.raise_for_status()

        content_type = response.headers.get('Content-Type', '')
        if "image" in content_type:
            file_extension = ".jpg"
        else:
            guessed_extension = mimetypes.guess_extension(content_type, strict=False)
            file_extension = guessed_extension if guessed_extension else os.path.splitext(url.split('?')[0])[-1]

        final_file_name = f"{url_md5}{file_extension}"
        final_file_path = os.path.join(self.save_dir, final_file_name)
        temp_file_path = final_file_path + ".tmp"

        os.makedirs(os.path.dirname(final_file_path), exist_ok=True)

        # If it's an image and we want to force save as .jpg
        if file_extension == ".jpg":
            image = Image.open(response.raw)
            image.save(temp_file_path, 'JPEG')
        else:
            with open(temp_file_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)

        os.rename(temp_file_path, final_file_path)

        return final_file_path

    def download_files(self, urls):
        """
        根据URL列表下载多个文件。

        参数:
        - urls (List[str]): 文件的URL地址列表。

        返回:
        List[str]: 下载文件的完整路径列表。
        """
        concatenated_urls = ''.join(urls)
        urls_md5 = self.calculate_md5_for_string(concatenated_urls)
        specific_save_dir = os.path.join(self.save_dir, urls_md5)

        # 检查该目录是否已存在，如果存在则表示这批文件已经被下载过
        if not os.path.exists(specific_save_dir):
            os.makedirs(specific_save_dir)

        file_paths = []  # 初始化一个列表来保存下载文件的完整路径

        # 为每个URL下载文件并命名
        for index, url in enumerate(urls, start=1):
            file_extension = os.path.splitext(url.split('?')[0])[-1]
            target_filename = f"{index:02}{file_extension}"
            file_path = self.download_file_into_directory(url, specific_save_dir, target_filename)
            file_paths.append(file_path)  # 将下载的文件的完整路径添加到列表中

        return {
            "directory": specific_save_dir,
            "file_paths": file_paths
        }

    def download_file_into_directory(self, url, directory, target_filename):
        """
        下载文件并保存到指定目录并使用指定文件名。

        参数:
        - url (str): 文件的URL地址。
        - directory (str): 指定的保存目录。
        - target_filename (str): 目标文件名。

        返回:
        str: 下载文件的保存路径。
        """
        final_file_path = os.path.join(directory, target_filename)

        # 检查文件是否已经存在
        if os.path.exists(final_file_path):
            return final_file_path

        # 如果文件不存在，则下载
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(final_file_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return final_file_path
