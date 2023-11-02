import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(name='wiliot-testers',
                 use_scm_version={
                     'git_describe_command': "git describe --long --tags --match [0-9]*.[0-9]*.[0-9]*",
                     'write_to': "wiliot_testers/version.py",
                     'write_to_template': '__version__ = "{version}"',
                     'root': ".",
                 },
                 setup_requires=['setuptools_scm'],
                 author='Wiliot',
                 author_email='support@wiliot.com',
                 description="A library for interacting with Wiliot's Testers app",
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url='',
                 project_urls={
                     "Bug Tracker": "https://WILIOT-ZENDESK-URL",
                 },
                 license='MIT',
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                 ],
                 packages=setuptools.find_packages(),
                 package_data={"": ["*.*"]},  # add all support files to the installation
                 install_requires=[
                     'setuptools_scm',
                     'pyserial',
                     'yoctopuce',
                     'pandas',
                     'numpy',
                     'pyqtgraph',
                     'PySimpleGUI',
                     'matplotlib',
                     'PyQt5',
                     'pygubu==0.16',
                     'appdirs',
                     'pillow',
                     'wiliot-api>=4.4.3',
                     'wiliot-core>=5.0.4',
                     'wiliot-tools>=4.2.2'
                 ],
                 zip_safe=False,
                 python_requires='>=3.6',
                 include_package_data=True,
                 )
