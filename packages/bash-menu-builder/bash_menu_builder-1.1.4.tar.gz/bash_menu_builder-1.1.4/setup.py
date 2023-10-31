from setuptools import setup


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='bash_menu_builder',
    version='1.1.4',
    author='Oleksii.Popov',
    author_email='popovaleksey1991@gmail.com',
    description='Bash Menu Builder',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/OleksiiPopovDev/Bash-Menu-Builder',
    packages=['bash_menu_builder'],
    install_requires=['pynput==1.7.6'],
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='bash menu vizual python',
    project_urls={
        'Documentation': 'https://github.com/OleksiiPopovDev/Bash-Menu-Builder'
    },
    python_requires='>=3.9'
)
