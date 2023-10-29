from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='game_utilities_py',
    version='1.0.0',
    license='MIT License',
    author='George Júnior',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='ctt.georgejr@gmail.com',
    keywords='game utilities',
    description=u'Game Utilities',
    packages=['game_utilities_py'],
    install_requires=['opencv-python','requests','numpy','PyAutoGUI','keyboard','colorama'],)
