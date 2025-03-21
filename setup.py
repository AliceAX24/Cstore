from setuptools import setup, find_packages

setup(
    name="cstore",
    version="0.1.0",
    packages=find_packages(),
)

import cstore
def test_load_credentials():
    assert callable(cstore.load_credentials)

def test_create_account():
    assert callable(cstore.create_account)