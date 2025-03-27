from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="portman-testing",
    version="0.1.0",
    author="Portman Team",
    author_email="ivo.kinnunen@siili.com",
    description="A testing package for Portman Agent project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/herratomsiili/portman_agent",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "psycopg2-binary>=2.9.0",
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=21.5b2",
            "flake8>=3.9.0",
        ],
    },
)
