from setuptools import find_packages, setup

setup(
    name="pf_package_template",
    version="0.0.9",
    description="This is the prompt flow package template",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["my_tool = pf_package_template.__init__:main"],
        "package_tools": ["my_tools = pf_package_template.tools.utils:list_package_tools"],
    },
    include_package_data=True,   # This line tells setuptools to include files from MANIFEST.in
    long_description_content_type='text/markdown',
)