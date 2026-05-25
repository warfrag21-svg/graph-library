# setup.py
from setuptools import setup, find_packages

setup(
    name="graph-library",
    version="1.0.0",
    description="Библиотека для построения и визуализации графов",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/warfragking21-svg/graph-library",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Основные зависимости (если есть)
        # "matplotlib>=3.5.0",  # раскомментировать если нужна визуализация
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
        "viz": [
            "matplotlib>=3.5.0",
        ],
    },
)