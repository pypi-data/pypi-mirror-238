from setuptools import setup

setup(
    name="fastapi_init",
    version="0.1.12",
    description="A simple Python library",
    author="Le Dinh Manh",
    author_email="manhld@rabiloo.com",
    packages=["fastapi_init"],
    install_requires=["requests", "GitPython"],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": ["fastapi_init=fastapi_init.main:main"],
    },
)
