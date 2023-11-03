"""
CSDN主页：https://blog.csdn.net/as604049322
"""

import setuptools

with open("README.md", "r", encoding="u8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="UpdateChromeDriver",
    version="0.0.2",
    author="小小明",
    author_email="604049322@qq.com",
    description="针对115以上版本的谷歌游览器自动升级selenium驱动。",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPLv3",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    package_data={},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        'requests', 'tqdm', "selenium > 4.0.0"
    ],
    platforms='any',
    zip_safe=True,
    python_requires=">=3.6"
)
