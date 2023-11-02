from setuptools import find_packages, setup

from tools import common
from tools.debug_logger import DebugLogger

common.init()
DebugLogger.line(f'==== {"version": <11}: v{common.cmn_version}')

# @formatter:off
setup(
    description='Pytest module with Verification Protocol, Verification Report and Trace Matrix',
    keywords=['verification', 'pytest'],
    install_requires=[
        'docx',
        'jsmin',
        'pytest',
        'pytest-check',
        'python-docx',
        'reportlab',
    ],
    classifiers=[
        # Choose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing :: Acceptance',
        'Programming Language :: Python :: 3.9',
        common.cmn_classifier_license,
    ],

    # common attributes from here on
    name=common.cmn_mod_name,
    include_package_data=True,
    packages=find_packages(include=f'{common.cmn_mod_dir_name}*', ),
    version=common.cmn_version,
    license=common.cmn_license,
    long_description=common.cmn_long_desc,
    long_description_content_type=common.cmn_long_desc_type,
    author=common.cmn_author,
    author_email=common.cmn_email,
    url=common.cmn_homepage_url,
    download_url=common.cmn_download_url,
)
# @formatter:on

DebugLogger.ok('GenBuildInfo completed successfully')
