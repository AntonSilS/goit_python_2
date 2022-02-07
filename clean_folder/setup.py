from setuptools import setup, find_packages


setup(
    name="clean-folder",
    version="0.0.1",
    author="Silchenko Anton",
    author_email="example@example.com",
    description="This packet sorts you files by extesions in specifed directory",
    url="https://github.com/AntonSilS/goit_python_2",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    packages=find_packages(),
    entry_points={'console_scripts': ['clean-folder = clean_folder.clean:main']} 
)    
