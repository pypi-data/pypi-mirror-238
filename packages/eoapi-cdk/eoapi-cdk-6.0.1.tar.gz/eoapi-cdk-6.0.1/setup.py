import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "eoapi-cdk",
    "version": "6.0.1",
    "description": "A set of constructs deploying pgSTAC with CDK",
    "license": "ISC",
    "url": "https://github.com/developmentseed/eoapi-cdk.git",
    "long_description_content_type": "text/markdown",
    "author": "Anthony Lukach<anthony@developmentseed.org>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/developmentseed/eoapi-cdk.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "eoapi_cdk",
        "eoapi_cdk._jsii"
    ],
    "package_data": {
        "eoapi_cdk._jsii": [
            "eoapi-cdk@6.0.1.jsii.tgz"
        ],
        "eoapi_cdk": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.99.1, <3.0.0",
        "aws-cdk.aws-apigatewayv2-integrations-alpha>=2.47.0.a0, <3.0.0",
        "aws-cdk.aws-lambda-python-alpha>=2.47.0.a0, <3.0.0",
        "constructs>=10.1.113, <11.0.0",
        "jsii>=1.69.0, <2.0.0",
        "publication>=0.0.3",
        "typeguard~=2.13.3"
    ],
    "classifiers": [
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Typing :: Typed",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
