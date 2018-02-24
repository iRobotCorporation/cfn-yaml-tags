from setuptools import setup

def find_version(name):
    import os.path, codecs, re
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, name), 'r') as fp:
        version_file = fp.read()
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='cfn-yaml-tags',
    version=find_version('cfn_yaml_tags.py'),
    description='Support parsing of CloudFormation YAML tags',
    py_modules=["cfn_yaml_tags"],
    install_requires=["pyyaml"],
    author='Ben Kehoe',
    author_email='bkehoe@irobot.com',
    project_urls={
        "Source code": "https://github.com/iRobotCorporation/cfn-yaml-tags",
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