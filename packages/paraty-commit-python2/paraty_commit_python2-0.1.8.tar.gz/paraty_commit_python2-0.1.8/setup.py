
from setuptools import setup
from setuptools.command.install import install

class custom_install_code(install):
    def run(self):
        install.run(self)

setup(
    name='paraty_commit_python2',
    version='0.1.8',
    description='Una biblioteca personalizada',
    author='José Luis Villada',
    author_email='jlvillada@paratytech.com',
    cmdclass={
        'install': custom_install_code
      },
    packages=['paraty_commit_python2'],
    install_requires=['colorama', 'pylint==1.9.5'],
    # package_data={'paraty_commit_jlvillada': ['*', '.pre-commit-config.yaml']}
    include_package_data=True,
    python_requires='>=2.7, <3',
    entry_points={
        'console_scripts': [
            'paraty_commit = paraty_commit_python2.precommit:main',
        ],
    },
)