import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cdk-skill-management",
    "version": "1.0.13",
    "description": "CDK constructs to manage Alexa Skills",
    "license": "MIT",
    "url": "https://github.com/t0bst4r/cdk-skill-management.git",
    "long_description_content_type": "text/markdown",
    "author": "t0bst4r<82281152+t0bst4r@users.noreply.github.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/t0bst4r/cdk-skill-management.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cdk_skill_management",
        "cdk_skill_management._jsii"
    ],
    "package_data": {
        "cdk_skill_management._jsii": [
            "cdk-skill-management@1.0.13.jsii.tgz"
        ],
        "cdk_skill_management": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.101.0, <3.0.0",
        "constructs>=10.0.0, <11.0.0",
        "jsii>=1.90.0, <2.0.0",
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
        "Programming Language :: Python :: 3.11",
        "Typing :: Typed",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved"
    ],
    "scripts": []
}
"""
)

with open("README.md", encoding="utf8") as fp:
    kwargs["long_description"] = fp.read()


setuptools.setup(**kwargs)
