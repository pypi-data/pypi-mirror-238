# from setuptools import setup
# setup()
import os
from setuptools import setup, find_packages

def load_doc_file(readme_file_path: str) -> str:
    doc_str = ""
    with open(readme_file_path, "r", encoding="utf-8") as fh:
        doc_str = fh.read()
    return doc_str

def load_version(readme_file_path: str) -> str:
    ver_str = ""
    with open(readme_file_path, "r", encoding="utf-8") as fh:
        ver_str = fh.read()
    _, version = ver_str.split("=")
    version = version.replace('"', "").replace(" ", "")
    return version

def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths

package_data_files = []
package_data_files += package_files('nanosurf/app')
package_data_files += package_files('nanosurf/doc')
package_data_files += package_files('nanosurf_internal/app')
package_data_files += package_files('nanosurf_internal/doc')
package_data_files += package_files('nanosurf/lib/frameworks/qt_app')

long_description_file = load_doc_file('nanosurf/doc/README.md')

setup(
    name='nanosurf',
    version=load_version('nanosurf/_version.py'),
    author='Nanosurf AG',
    author_email='scripting@nanosurf.com',
    description='Python API for Nanosurf controllers and Nanosurf style application framework',
    long_description=long_description_file,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(
        include=['*'],
    ),
    package_data={'': package_data_files},
    include_package_data = False,
    zip_safe=False,
    install_requires=[
        "pywin32>=306;platform_system=='Windows'", 
        'lupa>=2.0;platform_system=="Windows"',
        'matplotlib', 'numpy', 'scipy', 'notebook', 
        'pyside6', 'pyqtgraph>=0.13.3', 
        'h5py>=3.8',
        'psutil', 'debugpy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        "License :: OSI Approved :: MIT License"
    ],
    entry_points={
        'console_scripts': [
            'nanosurf_help = nanosurf:help',
        ],
        'pyinstaller40': [
            'hook-dirs = nanosurf:get_py_installer_hook_dirs'
        ]
    },
    python_requires='>=3.9'
)

