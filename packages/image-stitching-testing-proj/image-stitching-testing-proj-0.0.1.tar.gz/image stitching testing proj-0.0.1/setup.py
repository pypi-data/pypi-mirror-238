from setuptools import setup, find_packages

setup(
    name='image stitching testing proj',
    version='0.0.1',
    description='PYPI Image Stitching Test Package',
    author='j.Kim.vivity',
    author_email='jinsu.kim@vivity.ai',
    url='',
    install_requires=['opencv-python', 'stitching',],
    packages=find_packages(exclude=[]),
    keywords=['stitching test', 'panorama test'],
    python_requires='>=3.10',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.10',
    ],
)