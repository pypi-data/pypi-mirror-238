from setuptools import setup, find_packages

setup(
    name='rpa_suite',
    version='0.1',
    packages=find_packages(),
    description='Conjunto de ferramentas para uso basico e generico, voltados para facilitar o dia a dia de desenvolvimento RPA com python.',
    long_description=open('README.md').read(),
    author='Camilo Costa de Carvalho',
    author_email='camilo.costa1993@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='basic-tools, email-tools, email-validation, file-tools, simple-functions',
    install_requires=['loguru'],
)
