from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='falkor',
    version='0.0.2',
    description='Deploys the Falkor Large Language Model',
    author='Collin Paran',  
    long_description=long_description,
    long_description_content_type="text/markdown", 
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "transformers",
        "sentencepiece",
        "bitsandbytes",
        "accelerate",
        "torch",
        "fastapi",
        "uvicorn",
        "joblib",
        "python-multipart",
        "langchain",
        "pydantic"
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
    ],
    license='Apache-2.0', 
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'serve=vectorlite.server:main',
        ],
    },
)
