from setuptools import setup, find_packages

readme = """
# SigmaHTTP - modern, async and easy async HTTP framework, written in Python.

### ⚠️ Warning!
> The SigmaHTTP framework has not been released yet.
> <br>Stay tuned to the news to find out when the release will be made.
> <br>**Then run `pip install --upgrade sigmahttp`**
> <br>
> <br>Discord server: https://discord.gg/BKHcUMVhqe
"""

setup(
    name="sigmahttp",
    version="0.0.1",
    description="SigmaHTTP - modern, async and easy async HTTP framework, written in Python.",
    long_description=readme,
    author="True Sigma",
    author_email="sigmahttp@gmail.com",
    url="https://github.com/sigmahttp/sigmahttp",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
        "Framework :: AsyncIO",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
    keywords="http https http-server http_server httpserver http-library http_library httplibrary",
    install_requires=[],
    long_description_content_type="text/markdown",
)
