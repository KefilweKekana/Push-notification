from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

setup(
	name="push_notifications",
	version="0.0.1",
	description="Firebase Push Notifications for ERPNext",
	author="OctaNode",
	author_email="kefilwe@octanode.co.za",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
