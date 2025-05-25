from setuptools import setup, find_packages

setup(
    name="DiSchema",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'setuptools'
    ],
    description="",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="David León",
    author_email="davidalfonsoleoncarmona@gmail.com",
    url="https://github.com/davidleonstr/DiSchema",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11.3",
)

# I use Python 3.13.1.