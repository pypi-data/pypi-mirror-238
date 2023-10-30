from setuptools import setup

setup(
    name="example_package_skymap",
    version="0.0.3",
    author="Nguyen Van Trien",
    author_email="trien.nv195934@gmail.com",
    description="A small example package",
    packages=['dist'],
    install_requires=[
        "python-dotenv",
        # Add any other dependencies here
    ],
    keywords=["python", "eofactory", "skymap", "data"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Operating System :: Microsoft :: Windows",
    ],
)