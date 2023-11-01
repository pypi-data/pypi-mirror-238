from setuptools import setup, find_packages

setup(
    name="composo",
    version="0.1.4",
    description="Composo Python Package",
    author="Luke Markham",
    author_email="luke@composo.ai",
    packages=find_packages(),
    package_data={
        'composo': ['pyarmor_runtime_000000/*'],
    },
    install_requires=[
        "requests>=2.25.1",
        "colorama>=0.4.4",
    ],
    python_requires=">=3.8",
)
