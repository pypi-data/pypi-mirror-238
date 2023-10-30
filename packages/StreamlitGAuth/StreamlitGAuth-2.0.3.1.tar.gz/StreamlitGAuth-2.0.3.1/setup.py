from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="StreamlitGAuth",
    version="2.0.3.1",
    description="st_googleauth is a Python library that provides Streamlit integration for Google Authenticator. It enables single sign-on (SSO) with Google Authenticator for Streamlit applications.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="rahul katoch",
    author_email="rahulkatoch99@gmail.com",
    maintainer="Rahul Katoch",
    maintainer_email="rahulkatoch99@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords="streamlit google-authenticator SSO goole_oauth",
    python_requires=">=3.6",
    license="MIT",
    install_requires=[
        "streamlit",
        # Add any other dependencies your package needs
    ],
)
