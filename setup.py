from setuptools import setup, find_packages
setup(
    name='tfs',
    version='0.0.1',
    description='File Processing Library.',
    url='https://github.com/twj2417/filesystem',
    author='Weijie Tao',
    author_email='twj2417@gmail.com',
    license='MIT',
    namespace_packages=['tfs'],
    packages=find_packages('src/python'),
    package_dir={'': 'src/python'},
    install_requires=[
        'click',
        'rx',
    ],
    scripts=[],
    zip_safe=False
)
