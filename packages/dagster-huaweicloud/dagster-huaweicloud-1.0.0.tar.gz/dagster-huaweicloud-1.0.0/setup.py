from setuptools import setup

MAIN_REQUIREMENTS = [
    "pydantic==1.10.11",
    "esdk-obs-python",
    "dagster"
]

setup(
    name="dagster-huaweicloud",
    description="Package for Huaweicloud-specific Dagster framework solid and resource components",
    license="OSI Approved :: Apache Software License",
    author="HuaweiCloud",
    author_email="",
    keywords="dagster",
    url="https://gitee.com/HuaweiCloudDeveloper/huaweicloud-dagster-components-python",
    version="1.0.0",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.9",
    install_requires=MAIN_REQUIREMENTS,
    classifiers=[],
)
