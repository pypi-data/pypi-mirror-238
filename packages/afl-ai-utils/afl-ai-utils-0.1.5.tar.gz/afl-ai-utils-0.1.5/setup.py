import setuptools

with open("README.md", "r") as fh:
    description = fh.read()

setuptools.setup(
    name="afl-ai-utils",
    version="0.1.5",
    author="Abhay Kumar",
    author_email="abhay.kumar@arvindbrands.co.in",
    packages=["afl_ai_utils"],
    description="A sample test package",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/gituser/test-tackage",
    license='MIT',
    python_requires='>=3.8',
    install_requires=["requests", "google-cloud-bigquery", "pandas", "db_dtypes"]
)