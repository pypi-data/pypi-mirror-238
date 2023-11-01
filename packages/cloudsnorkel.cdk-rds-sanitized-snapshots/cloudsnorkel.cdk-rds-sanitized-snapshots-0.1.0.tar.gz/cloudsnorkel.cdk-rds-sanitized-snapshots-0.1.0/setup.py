import json
import setuptools

kwargs = json.loads(
    """
{
    "name": "cloudsnorkel.cdk-rds-sanitized-snapshots",
    "version": "0.1.0",
    "description": "CDK construct to periodically take snapshots of RDS databases, sanitize them, and share with selected accounts.",
    "license": "Apache-2.0",
    "url": "https://github.com/CloudSnorkel/cdk-rds-sanitized-snapshots.git",
    "long_description_content_type": "text/markdown",
    "author": "Amir Szekely<amir@cloudsnorkel.com>",
    "bdist_wheel": {
        "universal": true
    },
    "project_urls": {
        "Source": "https://github.com/CloudSnorkel/cdk-rds-sanitized-snapshots.git"
    },
    "package_dir": {
        "": "src"
    },
    "packages": [
        "cloudsnorkel.cdk_rds_sanitized_snapshots",
        "cloudsnorkel.cdk_rds_sanitized_snapshots._jsii"
    ],
    "package_data": {
        "cloudsnorkel.cdk_rds_sanitized_snapshots._jsii": [
            "cdk-rds-sanitized-snapshots@0.1.0.jsii.tgz"
        ],
        "cloudsnorkel.cdk_rds_sanitized_snapshots": [
            "py.typed"
        ]
    },
    "python_requires": "~=3.7",
    "install_requires": [
        "aws-cdk-lib>=2.85.0, <3.0.0",
        "constructs>=10.0.5, <11.0.0",
        "jsii>=1.91.0, <2.0.0",
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
