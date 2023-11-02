from setuptools import setup, find_packages


with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='2023_assignment1_viewscounter',
    version='0.0.5',
    description='Questo assignment si concentra sulla creazione di un\'applicazione che conta e monitora le visualizzazioni degli utenti',
    author='Team CED',
    author_email='damianoficara@gmail.com,c.ricci19@campus.unimib.it,emiliotoli21@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',  
    license='MIT',
    packages=find_packages(exclude=["tests"]),
    zip_safe=False
)
