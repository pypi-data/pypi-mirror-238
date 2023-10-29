import setuptools

setuptools.setup(
    name="discohooker",
    version="1.0.6",
    author="MaxPython110331",
    author_email="max.gamil110331@gmail.com",
    description="A easy PyPI to send Discord Webhook!",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://replit.com/@MAX110331/discohooker",                                         
    packages=["discohooker"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests", "datetime", "pytz"],
    python_requires=">=3.6"
)