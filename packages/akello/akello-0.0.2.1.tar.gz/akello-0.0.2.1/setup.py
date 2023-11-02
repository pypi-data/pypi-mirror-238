from setuptools import setup, find_packages

VERSION = '0.0.2.1'
DESCRIPTION = 'FastAPI server akello.io'
LONG_DESCRIPTION = 'FastAPI server for running Measurement Based Care (MBC) programs'

setup(
    name="akello",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    include_package_data=True,
    test_suite="akello",
    package_data={'akello': ['*.yaml']},
    author="Vijay Selvaraj",
    author_email="vijay@akellohealth.com",
    license="Apache License 2.0",
    packages=find_packages(),
    tests_require=['PyYAML', 'responses'],
    install_requires=['PyYAML', 'requests', 'responses'],
    keywords='healthcare, chatgpt, screening',
    classifiers= [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        "Programming Language :: Python :: 3",
    ]
)