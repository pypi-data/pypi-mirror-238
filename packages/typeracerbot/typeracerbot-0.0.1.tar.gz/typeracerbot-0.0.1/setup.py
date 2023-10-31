from setuptools import find_packages, setup

with open("typeracerbot/README.md", "r") as f:
    long_description = f.read()

setup(
    name="typeracerbot",
    version="0.0.1",
    description="A script that automatically types on typeracer",
    #package_dir={"": "app"},
    packages=find_packages(include=['typeracerbot']),
    package_data={'': ['letters']},
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    author="prerobnem",
    author_email="prerobnem@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Operating System :: MacOS",
    ],
    install_requires=["pyautogui >= 0.9.54","opencv-python >= 4.8.1.78","numpy >= 1.26.1","imutils >= 0.5.4"],
    extras_require={
        "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.11",
)