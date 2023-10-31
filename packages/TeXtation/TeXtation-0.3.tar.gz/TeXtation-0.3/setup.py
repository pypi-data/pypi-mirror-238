from setuptools import setup, find_packages

setup(
    name='TeXtation',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'aiohttp==3.8.6',
        'aiosignal==1.3.1',
        'async-timeout==4.0.3',
        'attrs==23.1.0',
        'certifi==2023.7.22',
        'charset-normalizer==3.3.1',
        'colorama==0.4.6',
        'customtkinter==5.2.1',
        'darkdetect==0.8.0',
        'frozenlist==1.4.0',
        'idna==3.4',
        'multidict==6.0.4',
        'openai==0.28.1',
        'packaging==23.2',
        'python-dotenv==1.0.0',
        'requests==2.31.0',
        'tk==0.1.0',
        'tqdm==4.66.1',
        'urllib3==2.0.7',
        'yarl==1.9.2'
    ],
    author='Adel Moussa',
    author_email='moussaadel97@gmail.com',
    description='This is a package for converting text prompts to ready to use latex',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/adeoo/TeXtation',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Text Processing :: Markup :: LaTeX',
        'Topic :: Utilities'
    ],
    license='MIT',
    keywords='latex, text, conversion, tkinter, GUI',
    python_requires='>=3.7',
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'textation=TeXtation.main:main',
        ],
    },
)
