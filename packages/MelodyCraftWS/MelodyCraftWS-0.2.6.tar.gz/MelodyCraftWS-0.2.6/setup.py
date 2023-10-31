from setuptools import setup, find_packages

setup(
    name='MelodyCraftWS',
    version='0.2.6',
    packages=find_packages(),
    install_requires=[
        'Flask==3.0.0',
        'Flask-SocketIO==5.3.6',
        'audiocraft==1.0.0',
        'torch==1.13.1+cu117',
        'torchvision==0.14.1+cu117',
        'torchtext==0.14.1',
        'torchaudio==0.13.1',
        'torchdata==0.5.1',
    ],
    dependency_links=[
        'https://download.pytorch.org/whl/cu117',
    ],
    author='Sergio Sánchez Sánchez',
    author_email='dreamsoftware92@gmail.com',
    description='🎶 Transform text into beautiful melodies and stream real-time WebSockets to clients! 🚀',
    url='https://github.com/sergio11/melodycraftWS',
    keywords=['music', 'text', 'WebSocket', 'melody'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7, <4',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
)

"""
MelodyCraftWS Setup

This setup script configures the installation of the SongCraftWebSocket package. SongCraftWebSocket is a Python package designed for generating melodies from textual content and providing real-time WebSockets notifications to clients. The package integrates Flask and other dependencies to achieve this functionality.

Project Details:
- Name: MelodyCraftWS
- Version: 0.2.6
- Author: Sergio Sánchez Sánchez
- Email: dreamsoftware92@gmail.com
- Description: MelodyCraftWS is a package that enables the generation of music from text input and the communication of progress and results to clients using WebSockets. It is intended for developers and enthusiasts interested in text-to-melody conversion and real-time event streaming.
- Repository: https://github.com/sergio11/melodycraftWS
- Keywords: music, text, WebSocket, melody

Requirements:
- Flask 3.0.0
- Flask-SocketIO 5.3.6
- audiocraft 1.0.0

Development Status: Beta

License: MIT License

Python Version Compatibility: 3.7, 3.8, 3.9, 3.10

For more details, please refer to the project's README.md file.
"""