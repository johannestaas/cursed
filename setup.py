import os
from setuptools import setup

#  cursed
#  Simplified curses


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="cursed",
    version="0.2.1",
    description="Simplified curses",
    author="Johan Nestaas",
    author_email="johannestaas@gmail.com",
    license="GPLv3+",
    keywords="",
    url="https://www.bitbucket.org/johannestaas/cursed",
    packages=['cursed'],
    package_dir={'cursed': 'cursed'},
    long_description=read('README.rst'),
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable',
        # 'Development Status :: 6 - Mature',
        # 'Development Status :: 7 - Inactive',
        'License :: OSI Approved :: GNU General Public License v3 or later '
        '(GPLv3+)',
        'Environment :: Console',
        'Environment :: X11 Applications :: Qt',
        'Environment :: MacOS X',
        'Environment :: Win32 (MS Windows)',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
    ],
    install_requires=[
        'gevent', 'six',
    ],
    entry_points={
        # 'console_scripts': [
        #     'cursed=cursed:main',
        # ],
    },
    # package_data={
    # 'cursed': ['catalog/*.edb'],
    # },
    # include_package_data=True,
)
