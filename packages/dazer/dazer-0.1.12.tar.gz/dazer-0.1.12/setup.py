from setuptools import setup

setup(
    name='dazer',
    version='0.1.12',
    author='Maiykol',
    author_email='michael.hartung@uni-hamburg.de',
    packages=['dazer'],
    scripts=[],
    url='http://pypi.python.org/pypi/dazer/',
    license='LICENSE',
    description='DAtaset siZe Effect estimatoR',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        "pandas==2.1.1",
        "scikit-learn==1.3.1"
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        # 'License :: OSI Approved :: BSD License',  
        # 'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3.11',
    ],
)