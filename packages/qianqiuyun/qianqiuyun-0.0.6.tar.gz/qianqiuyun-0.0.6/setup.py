import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="qianqiuyun",
    version="0.0.6",
    author="qianqiusoft",
    author_email="develop@qianqiusoft.com",
    description="qianqiuyun sdk",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://git.qianqiusoft.com/library/qianqiuyun-sdk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pymysql',
        'nats-py',
        'influxdb',
        'influxdb-client',
        'DBUtils',
        'cryptography'
    ],
    python_requires='>=3',
)