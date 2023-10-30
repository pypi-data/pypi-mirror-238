from setuptools import setup, find_packages

setup(
    name='tybase',
    version='0.5.7',
    include_package_data=True,
    description='修复了文件下载的通用功能',
    long_description=open('README.md', 'r', encoding='utf-8').read(),
    long_description_content_type='text/markdown',  # 版本描述
    author='Tuya',
    author_email='353335447@qq.com',
    url='https://github.com/yourusername/your_package',
    packages=find_packages(),
    install_requires=[
        'setuptools',
        "opencv-python",
        'Pillow',
        "redis",
        "celery",
        "loguru",
        "openpyxl",
        'requests',
        "python-dotenv",
        "retrying",
        "pymysql",
        "mysql-connector-python",
        "sqlalchemy",
        "pandas",
        "langchain",
        "openai",
        'python-dotenv',
        "oss2",
        "google-auth",
        "google-auth-oauthlib",
        "google-auth-httplib2",
        "google-api-python-client"

        # List your package dependencies here
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.10',
    ],
)
