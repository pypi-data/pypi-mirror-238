from setuptools import find_packages, setup

PACKAGE_NAME = "pi_promptflow_tools"

setup(
    name=PACKAGE_NAME,
    version="2.0.0",
    description="A tool package for the ProcessInsights team to us for custom prompt flow tools.",
    packages=find_packages(),
    entry_points={
        "package_tools": ["copilot_metaprompt_tool = pi_promptflow_tools.tools.utils:list_package_tools"],
    },
    include_package_data=True,   # This line tells setuptools to include files from MANIFEST.in
)