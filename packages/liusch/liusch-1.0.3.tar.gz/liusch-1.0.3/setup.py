from setuptools import setup

setup(
    name="liusch",
    version="1.0.3",
    packages=["liusch"],
    entry_points={
        "console_scripts": [
            "liusch = liusch.main:main"
        ]
    },
    install_requires=[
        "requests",
    ],
)

