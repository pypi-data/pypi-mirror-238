from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='djamal',
    version='0.1',
    author='Ehigie (Pystar) Aito',
    author_email='aitoehigie@gmail.com',
    description=' A Django extension to deploy web apps anywhere, from bare metal to cloud VMs.',
    long_description=" A Django extension to deploy web apps anywhere, from bare metal to cloud VMs.",
    long_description_content_type='text/markdown',
    url='https://github.com/aitoehigie/djamal', 
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'djamal=djamal.management.commands.djamal:Command',
        ],
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.6',
)
