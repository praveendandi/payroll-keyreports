from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in payroll_key_reports/__init__.py
from payroll_key_reports import __version__ as version

setup(
	name="payroll_key_reports",
	version=version,
	description="Payroll Key Reports",
	author="caratRED Technologies LLP",
	author_email="info@caratred.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
