from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(
    name             = 'sabalt',
    version          = '0.1',
    description      = 'Toolkit for bass lines transcription',
    long_description = readme()
    url              = 'http://github.com/lvanderlaat/sabalt',
    author           = 'Leonardo van der Laat',
    author_email     = 'lvmzxc@gmail.com',
    packages         = ['sabalt'],
    install_requires = [
        'ipython'
    ]
    zip_safe     = False
    scripts=[
        'bin/sabalt-pre-process',
        'bin/sabalt-pitches',
        'bin/sabalt-score'
    ],
)
