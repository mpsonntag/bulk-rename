try:
    from setuptools import setup
except ImportError as ex:
    from distutils.core import setup

packages = [
    'bren'
]

with open('README.rst') as f:
    description_text = f.read()

install_req = ["pyyaml"]

tests_req = ["pytest"]

setup(
    name='bulkrename',
    version='1.0.0',
    description='bulk file rename',
    author='Michael Sonntag',
    packages=packages,
    test_suite='test',
    install_requires=install_req,
    tests_require=tests_req,
    include_package_data=True,
    long_description=description_text,
    license="BSD"
)
