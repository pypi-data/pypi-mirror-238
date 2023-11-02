from setuptools import setup, find_packages

setup(
    name='mfio',
    version='1.2.3',
    description='自用文件读写检索匹配工具',
    url='',
    author='yunhgu',
    author_email='1508777473@qq.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'loguru',
        'xlrd==1.2.0',
        'xlwt',
        'numpy',
        'opencv_python',
        'xmltodict',
        "pyyaml",
        "requests",
        "openpyxl"
    ],
    python_requires='>=3.7'
)
