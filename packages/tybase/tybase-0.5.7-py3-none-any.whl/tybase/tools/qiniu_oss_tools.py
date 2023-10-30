from qiniu import Auth, put_file

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