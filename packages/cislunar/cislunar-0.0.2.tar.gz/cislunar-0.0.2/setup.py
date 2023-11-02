from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='cislunar',
    version='0.0.2',
    description='Cislunar Utility Toolkit',
    author='Erin Lee Ryan',  
    long_description=long_description,
    long_description_content_type="text/markdown", 
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "fastapi",
        "uvicorn",
        "joblib",
        "python-multipart",
        "pydantic"
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6'
)
