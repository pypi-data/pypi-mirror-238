from setuptools import setup, find_packages
with open("README.md", "r", encoding='utf8') as f:
    long_description = f.read()
setup(
    name="halring",
    version="2.2.7",
    # url="http://artifactory.test.com:8081/artifactory",
    url='https://www.python.org',
    license="MIT Licence",
    author="peixiaodong",
    # author_email="pxd7th@vip.qq.com",
    packages=find_packages(exclude=["_unittest"]),
    platform="any",
    description="python常用底层库封装",
    python_requires='>=3.6.0',
    long_description=long_description,                      # 包的详细介绍(一般通过加载README.md)
    long_description_content_type="text/markdown",
    install_requires=[
        'twine==3.8.0',
        'loguru==0.6.0',
        'rsa==4.9',
        # 'pycrypto==2.6.1',
        'artifactory==0.1.17',
        'jira==3.2.0',
        'requests',
        'atlassian-python-api==3.32.2',
        'jieba==0.42.1',
        'xlrd==2.0.1',
        'openpyxl==2.5.6',
        # 'jenkins==1.0.2',
        'python-jenkins==1.7.0',
        'paramiko==3.0.0',
        'PyMySQL==1.0.2',
        'chardet==5.0.0',
        'pymssql',
        'pika==1.3.1',
        'pandas==1.1.5',
        'urllib3==1.26.0',
        'redis==4.3.5',
        'python-docx==0.8.10',
        'pypandoc==1.11',
        'pdfkit==1.0.0',
        'psycopg2-binary',
        'psycopg2==2.7.7',
    ],
    classifiers=[                                           # 关于包的其他元数据(metadata)
        "Programming Language :: Python :: 3",              # 该软件包仅与Python3兼容
        "License :: OSI Approved :: MIT License",           # 根据MIT许可证开源
        "Operating System :: OS Independent",               # 与操作系统无关
    ]

)
