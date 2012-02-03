from setuptools import setup, find_packages

setup(
    name="django-cache-toolbox-modified",
    packages=find_packages(),
    version="0.1.1",
    author="Matt Long",
    license="BSD",
    author_email="matt@mattlong.org",
    url="http://pypi.python.org/pypi/django-cache-toolbox-modified/",
    description="Non-magical object caching for Django. Based on django-cache-toolbox by Playfire.com",
    long_description="cache_toolbox is intended to be a lightweight series of independent tools to leverage caching within Django projects. A modified version of django-cache-toolbox by Playfire.com. Their project page is http://code.playfire.com/django-cache-toolbox",
    install_requires=['django>=1.3.0'],
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Operating System :: Unix',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
