from setuptools import setup, Extension
from Cython.Build import cythonize
from sys import platform
import os


def readme():
    with open("README.md") as f:
        return f.read()


boost_include_dir = None
include_dirs = []
extra_compile_args = []
extra_link_args = []

if platform == "win32":
    extra_compile_args = ["/std:c++17", "/O2"]
    boost_include_dir = os.environ.get("BOOST_ROOT")
elif platform == "linux":
    extra_compile_args = ["-std=c++17", "-O3"]
    extra_link_args = ["-Wl,-O3"]
elif platform == "darwin":  # macOS
    extra_compile_args = ["-std=c++17", "-O3"]
    extra_link_args = ["-Wl,-dead_strip"]

if boost_include_dir:
    include_dirs.append(boost_include_dir)
setup(
    name="nazo_ip2asn",
    ext_modules=cythonize(
        Extension(
            name="",
            sources=["nazo_ip2asn/ip2asn.pyx"],
            language="c++",
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args,
        ),
        compiler_directives={
            "language_level": 3,
            "boundscheck": False,
            "wraparound": False,
            "binding": True,
            "cdivision": True,
        },
    ),
    include_dirs=include_dirs,
    author="bymoye",
    author_email="s3moye@gmail.com",
    version="0.0.3",
    description="A ip2asn tools for python.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    license="MIT",
    package_data={
        "": [
            "nazo_ip2asn/ip2asn.pyi",
            "nazo_ip2asn/ip2asn.pyx",
        ]
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Cython",
        "Programming Language :: C++",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    packages=["nazo_ip2asn"],
)
