from setuptools import setup

setup(
    name='django-spruce',
    version='5.3.4',
    packages=['spruce_ui'],
    include_package_data=True,
    install_requires=[
        'Django',
        'requests',
        'django-import-export',
    ],
    author='江绿岸',
    author_email='jlarjjszx@tom.com',
    zip_safe=False,
)
