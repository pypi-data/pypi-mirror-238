from setuptools import setup, find_packages

setup(
    name='yt2text',
    version='1.0.2',
    packages=find_packages(),
    install_requires=[
        'numpy','ffmpeg','whisper','ffmpeg'
    ],
    author='Atahan Uz',
    author_email='atahanuz23@gmail.com',
    description="Extract text from a YouTube video in a single command, using OpenAi's Whisper speech recognition model",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/atahanuz/yt2text',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
