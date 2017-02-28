from os.path import join, dirname

from setuptools import setup, find_packages

setup(
    name='reporting-lib',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    requires=['python (>= 2.5)', 'django (>= 1.3)', 'django'],
    description='blabla',
    long_description=open(join(dirname(__file__), 'README.rst')).read(),
    author='KN',
    author_email='kovnata95@mail.ru',
    url='https://github.com/HeyTricky/django-error-reporting',
    download_url='https://github.com/HeyTricky/django-error-reporting',
    # license='MIT License',
    keywords='django',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ],
)
