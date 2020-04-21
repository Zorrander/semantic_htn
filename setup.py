from setuptools import setup

package_name = 'semantic_htn'

setup(
    name=package_name,
    version='0.0.1',
    packages = [package_name],
    install_requires=[
        'setuptools',
    ],
    zip_safe=True,
    maintainer='alex',
    maintainer_email='alexandre.angleraud@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    download_url='https://github.com/Zorrander/semantic_htn/archive/v0.0.1.tar.gz',
    tests_require=['pytest'],
)
