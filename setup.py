from setuptools import setup

setup(
    name='cfn-yaml-tags',
    version='0.1.0',
    description='Support parsing of CloudFormation YAML tags',
    py_modules=["cfn_yaml_tags"],
    install_requires=["pyyaml"],
    author='Ben Kehoe',
    author_email='bkehoe@irobot.com',
    project_urls={
        "https://github.com/iRobotCorporation/cfn-yaml-tags",
    },
    license='Apache Software License 2.0',
    classifiers=(
        'Development Status :: 2 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'License :: OSI Approved :: Apache Software License',
    ),
    keywords='aws cloudformation',
)