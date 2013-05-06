from setuptools import setup, find_packages

version = '0.1.0'

LONG_DESCRIPTION = """
"""

setup(
    name='django-survey',
    version=version,
    description="survey",
    long_description=LONG_DESCRIPTION,
    install_requires=[
        ],
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    keywords='vote,survey,django',
    author='yuanxunxun',
    author_email='yuanxunxun@insigma.com.cn',
    url='http://iot-hg.insigma.com.cn/yuanxunxun/vote/',
    license='BSD',
    packages=find_packages(),
    package_data = {
        'survey': [
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
