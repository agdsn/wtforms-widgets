from setuptools import setup, find_packages

setup(
    name="wtforms-widgets",
    author="The Pycroft Authors",
    description="Decorator driven wtforms extension with Bootstrap 3 support for Flask",
    long_description=__doc__,
    version="1.0.2",
    url="http://github.com/agdsn/wtforms-widgets/",
    packages=find_packages(exclude=["tests", "tests.*"]),
    include_package_data=True,
    zip_safe=False,
    python_requires=">= 3.4",
    install_requires=[
        'Flask-WTF',
        'MarkupSafe',
        'WTForms',
        "WTForms-SQLAlchemy"
    ],
    license="Apache Software License",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
