from setuptools import setup, find_packages


setup(
    name="tirmapp",
    version="0.0.1",
    author="Daniel Diego Horcajuelo",
    author_email="dadiego91@gmail.com",
    packages=find_packages(),
    scripts=[
        "manage.py",
        "scripts/delete-migrations.sh",
        "scripts/start-db.sh",
        "scripts/stop-db.sh",
    ],
)
