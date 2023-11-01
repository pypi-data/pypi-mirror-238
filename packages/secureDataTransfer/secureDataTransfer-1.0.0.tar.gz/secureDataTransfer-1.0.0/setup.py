from setuptools import setup, find_packages

setup(
    name="secureDataTransfer",
    description="The 'Secure Data Transfer'  seamlessly is a robust solution for safeguarding and sharing sensitive information.",
    version="1.0.0",
    author="Marzouq",
    author_email="01marzouq@gmail.com",
    packages=find_packages(),
    install_requires=[
        "pycryptodome>=3.10.1",
        "pyqt5"
    ],
    entry_points={
        "console_scripts": [
            "secure-data-transfer = secureDataTransfer.mainGUI:main"
        ]
    },
)
