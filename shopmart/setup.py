from setuptools import setup, find_packages

setup(
    name="shopmart",
    version="0.1.0",
    packages=find_packages(),
    python_requires='>=3.11,<3.12',  # enforce Python version
    install_requires=[
        "Django==3.2.25",
        "mysqlclient==2.1.1",
        "Pillow==8.4.0",
        "django-jazzmin==2.6.1",
        "asgiref==3.4.1",
        "certifi==2025.4.26",
        "charset-normalizer==2.0.12",
        "idna==3.10",
        "gunicorn==20.1.0",
    ],
)
