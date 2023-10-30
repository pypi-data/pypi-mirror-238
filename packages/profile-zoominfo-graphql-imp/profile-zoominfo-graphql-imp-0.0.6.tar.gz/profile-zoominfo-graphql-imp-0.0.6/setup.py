import setuptools

PACKAGE_NAME = "profile-zoominfo-graphql-imp"
package_dir = PACKAGE_NAME.replace("-", "_")

with open('README.md') as f:
    readme = f.read()

setuptools.setup(
    name=PACKAGE_NAME,  # https://pypi.org/project/profile-zoominfo-graphql-imp-local-python-package
    version='0.0.6',
    author="Circles",
    author_email="sahar.g@circ.zone",
    url=f"https://github.com/circles-zone/{PACKAGE_NAME}",
    packages=[package_dir],
    package_dir={package_dir: "profile_zoominfo_graphql_imp/src"},
    package_data={package_dir: ['*.py']},
    long_description=readme,
    long_description_content_type='text/markdown',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "pytest>=7.4.0",
        "python-dotenv>=1.0.0",
        "database-without-orm-local>=0.0.104",
        "logger-local>=0.0.66",
        "profile-local>=0.0.34",
        "zoomus>=1.2.1"
    ]
)
