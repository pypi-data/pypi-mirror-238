# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
# from setuptools.command.install import install
#
# class custom_install_code(install):
#     def run(self):
#         install.run(self)

setup(
    name='paraty_commit_python2',
    version='0.1.23',
    description='Una biblioteca personalizada',
    author='José Luis Villada',
    author_email='jlvillada@paratytech.com',
    # cmdclass={'install': custom_install_code},
    # packages=['paraty_commit_python2'],
    packages=find_packages(),
    install_requires=['colorama', 'pylint==1.9.5'],
    # package_data={'paraty_commit_jlvillada': ['*', '.pre-commit-config.yaml']}
    include_package_data=True,
    python_requires='>=2.7, <3',
    entry_points={'console_scripts': ['paraty_commit = paraty_commit_python2.precommit:main',],},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',  # Indica que es compatible solo con Python 2
    ],
)