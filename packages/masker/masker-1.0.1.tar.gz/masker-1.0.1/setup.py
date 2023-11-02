from setuptools import setup, find_packages

setup(
    name='masker',
    version='1.0.1',
    description='Masking tool',
    author='Aras',
    author_email='arasmutluayy@gmail.com',
    packages=find_packages(),
    install_requires=[
        'SQLAlchemy~=2.0.22',
        'flask~=3.0.0'
    ],
    package_data={
        'config': ['*.cfg'],
    },
    include_package_data=True,
    data_files=[('', ['app.py', 'README.md', 'requirements.txt'])],
    entry_points={
        'console_scripts': [
            'masker=app:main',
        ],
    }
)
