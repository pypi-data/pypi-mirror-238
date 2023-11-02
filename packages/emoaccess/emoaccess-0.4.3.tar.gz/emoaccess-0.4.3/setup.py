from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / 'README.md').read_text(encoding='utf-8')  # noqa

# get version
exec(open('emoaccess/version.py').read())


setup(
    name='emoaccess',
    version=__version__,  # noqa
    description='data access package for emobject',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/enable-medicine/rnd-subgroup/libraries/emo-access',
    author="Ethan A. G. Baker",
    author_email='ethan.baker@enablemedicine.com',
    packages=find_packages(),
    python_requires='>=3.7, <4',

    install_requires=[
        "numpy",
        "pandas",
        "zstandard",
        "python-dotenv",
        "snowflake-connector-python",
        "sqlalchemy<=1.4.46",
        "boto3",
    ],
    extras_require={
        'dev': [
            'flake8',
            'pytest',
        ],
    },
)
