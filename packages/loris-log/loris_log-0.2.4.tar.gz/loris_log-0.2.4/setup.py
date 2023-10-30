import os
from setuptools import setup, find_packages

BUILD_ID = os.environ.get("BUILD_BUILDID", "0")

setup(
    name="loris_log",
    version="0.2.4",
    # Author details
    author='Kah Seng, Sze Ling, Stanley',
    author_email='lim0709@gmail.com, sltang@handalindah.com.my, stanly@handalindah.com.my',
    packages=['loris_log']    
)