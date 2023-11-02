from setuptools import setup

setup(
    name='unipay_sdk',
    version='0.1',
    description='SDK for UniPay.com payment gateway',
    url='https://github.com/BeyondUnderstanding/unipay-sdk',
    install_requires=['requests', 'pydantic'],
    packages=['src.unipay_sdk']
)
