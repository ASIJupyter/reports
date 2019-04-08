import setuptools

setuptools.setup(
    name="Sentinel-Utilities",
    version="0.1.4",
    author="Sentinel Notebooks Devs",
    author_email="zhzhao@microsoft.com",
    description="Tools for Sentinel Notebooks",
    long_description="Version management, Azure management client operations",
    long_description_content_type="text/plain",
    url="https://github.com/Azure/Azure-Sentinel",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
)
