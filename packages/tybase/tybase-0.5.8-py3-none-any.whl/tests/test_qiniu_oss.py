from qiniu import Auth, put_file
from urllib.parse import quote


class QiniuTools:
    def __init__(self, access_key, secret_key, bucket_name):
        self.q = Auth(access_key, secret_key)
        self.bucket_name = bucket_name

    def upload_file(self, cloud_file_path, loc_target_path):
        # 生成上传Token
        token = self.q.upload_token(self.bucket_name, cloud_file_path)
        # 调用上传方法
        ret, info = put_file(token, cloud_file_path, loc_target_path)
        if ret:
            # 这里简单返回文件名作为成功上传的标志，实际应用中你可以根据需要修改
            return cloud_file_path
        else:
            raise Exception("Upload to Qiniu failed!")


def upload_file_to_qiniu(cloud_file_path: str, loc_target_path: str):
    # 这些参数可以从环境变量或者配置文件中读取，以增加安全性
    access_key = 'CuEf0CRuGsO5Vu6wQ3b-3dwyJeaVXVN5blOyoOJQ'
    secret_key = 'jHY3PiaGmGepPr-pwKsBRVPTGu7ZCWFfGFBnzfUD'
    bucket_name = 'tyushow'

    # 实例化七牛云的对象
    qn = QiniuTools(access_key, secret_key, bucket_name)
    res_path = qn.upload_file(cloud_file_path, loc_target_path)
    res_path = quote(res_path,safe='')
    # 上传文件到七牛云，并获取返回的路径
    return res_path


# 使用示例
cloud_file_name = 'apitest/222.jpg'  # 文件在云存储上的名称
local_file_path = '1694486238447.jpg'  # 本地文件路径
uploaded_path = upload_file_to_qiniu(cloud_file_name, local_file_path)
print(f"File uploaded to Qiniu at: {uploaded_path}")

