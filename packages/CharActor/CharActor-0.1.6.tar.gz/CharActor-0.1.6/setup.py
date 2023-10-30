from setuptools import setup, find_packages

setup(
    name='CharActor',
    version='0.1.6',
    description='A module for creating and managing rpg characters.',
    author='James Evans',
    author_email='joesaysahoy@gmail.com',
    url='https://github.com/primal-coder/CharActor',
    packages=find_packages(),
    install_requires=['dicepy', 'getch', 'pyglet', 'pymunk'],
    python_requires='>=3.8',
    keywords='rpg character dnd d&d dungeons and dragons dungeons & dragons player character actor charactor',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Games/Entertainment :: Role-Playing',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8'
        ],
    include_package_data=True,
    package_data={'CharActor': ['_charactor/dicts/*.json']}
)