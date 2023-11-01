from pathlib import Path
from setuptools import find_packages, setup

setup(
    name="retroapi",
    version="0.2.0",
    description="retroapi for retrosynthesis routes and exploring reaction conditions",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    url="https://github.com/bruceunx/retrosynthesis",
    author="Bruceunx",
    author_email="bruceunx@gmail.com",
    license="MIT License",
    project_urls={"Source": "https://github.com/bruceunx/retrosynthesis"},
    classifiers=[
        'Intended Audience :: Science/Research',
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
    python_requires=">=3.8,<3.12",
    install_requires=["requests", "aiohttp"],
    packages=find_packages(),
    include_package_data=True
)
