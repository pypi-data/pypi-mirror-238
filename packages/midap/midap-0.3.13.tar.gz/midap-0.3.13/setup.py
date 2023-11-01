from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name="midap",
    version="0.3.13",
    description='A package for cell segmentation and tracking.',
    author='Oschmann  Franziska, Fluri Janis',
    author_email='franziska.oschmann@id.ethz.ch, janis.fluri@id.ethz.ch',
    python_requires='>=3.9, <4',
    download_url = 'https://github.com/Microbial-Systems-Ecology/midap/archive/refs/tags/0.3.13.tar.gz',
    keywords='Segmentation, Tracking, Biology',
    install_requires=required,
    packages=find_packages(include=["midap.*"]),
    project_urls={'Midap': 'https://gitlab.ethz.ch/oschmanf/ackermann-bacteria-segmentation/'},
    entry_points={
        'console_scripts': [
            'midap = midap.main:run_module',
            'correct_segmentation = midap.apps.correct_segmentation:main',
            'midap_download = midap.apps.download_files:main',
        ],
    },
)
