from setuptools import setup

setup(
    name='texttv',
    version='1.0.0',    
    description='A terminal texttv client',
    url='https://github.com/erikstenlund/texttv',
    author='Erik Stenlund',
    author_email='erikstenlund@protonmail.com',
    license='MIT',
    install_requires=['readchar'],
    packages=["texttv"],
    entry_points={
        "console_scripts": [
            "texttv = texttv:cli"
        ]
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
    ],
)
