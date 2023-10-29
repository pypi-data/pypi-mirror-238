from setuptools import setup, find_packages

VERSION = '0.2.4'
DESCRIPTION = 'A Python tool for video-based traffic analytiscs'
LONG_DESCRIPTION = ''

setup(
    name="dnt",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Zhenyu Wang",
    author_email="wonstran@hotmail.com",
    license='MIT',
    packages=find_packages(include=("*.yaml")),
    keywords=('traffic', 'vehicle', 'trajectory', 'safety'),
    url = 'https://its.cutr.usf.edu/dnt/',
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    install_requires = [
        'numpy',
        'pandas',
        'matplotlib',
        'torch',
        'torchvision',
        'torchaudio',
        'ultralytics',
        'easydict',
        'filterpy',
        'matplotlib',
        'numpy_indexed',
        'opencv-python',
        'opencv-contrib-python',
        'pandas',
        'geopandas',
        'shapely',
        'scipy',
        'scikit-learn',
        'scikit-image',
        'tqdm',
        'vidgear',
    ],
    python_requires='>=3.9',
    include_package_data=True,
)