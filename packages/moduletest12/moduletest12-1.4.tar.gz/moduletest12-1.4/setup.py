from os.path import dirname, join
# from pip.req import parse_requirements

from setuptools import (
    find_packages,
    setup,
)

requirements="""requests>=2.18.4
six>=1.11.0"""


# def parse_requirements(filename):
#     """ load requirements from a pip requirements file """
#     lineiter = (line.strip() for line in open(filename))
#     return [line for line in lineiter if line and not line.startswith("#")]
def parse_requirements():
    return requirements.split("\n")

setup(
    name='moduletest12',  # 模块名称
    version='1.4',
    description='A mini spider framework, like Scrapy',  # 描述
    packages=find_packages(exclude=[]),
    author='davezj127',
    author_email='davezj127@gmail.com',
    license='Apache License v2',
    package_data={'': ['*.*']},
    # url='#',
    install_requires=parse_requirements(),  # 所需的运行环境
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix',
    ],
    python_requires='>=3.6',

)

