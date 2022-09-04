from setuptools import setup, find_packages
setup(
    name='yamlconf',
    version='0.0.1',
    description='Reading settings written in yaml',
    author='keika',
    author_email='keika076@gmail.com',
    license='MIT',
    classifiers=[
        'Topic :: Utilities'
    ],
    keywords='キーワード',
    install_requires=[
        'PyYAML==6.0',
        'pytest==7.1.3'
    ],
    py_modules=[
        'yamlconf/config',
        'yamlconf/const',
        'yamlconf/utils',
    ]
)