from setuptools import setup

long_description = open("README.md", "r", encoding="utf-8").read()
setup(
    name="proxiestor",
    version="1.7",
    description="Automate Tor Ip Rotation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sptty-chan/proxiestor",
    license="MIT",
    author="Sptty Chan",
    author_email="sptty_chan@ccmail.uk",
    packages=["proxiestor"],
    package_dir={"proxiestor": "src/proxiestor"},
    package_data={"proxiestor": ["./*.cpp"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    entry_points={"console_scripts": ["proxies-build = proxiestor:build"]},
    python_requires=">=3",
    install_requires=[
        "stem==1.8.0",
        "psutil==5.9.6",
        "cython==0.29.33",
    ],
)
