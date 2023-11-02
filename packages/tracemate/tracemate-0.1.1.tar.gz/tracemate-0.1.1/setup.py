from setuptools import setup, find_packages

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name='tracemate',
    version='0.1.1',
    author='Alex Figueroa',
    author_email='alexfigueroa.solutions@gmail.com',
    description='🔍 Tracemate: A comprehensive tracing and logging toolkit for Python CLI applications.',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    license='MIT',
    url='https://github.com/alexfigueroa-solutions/tracemate',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    install_requires=requirements,
    scripts=[
        # If you have any scripts to run, add them here
        # 'bin/myscript',
    ],
    include_package_data=True,
    package_data={
    },
)
