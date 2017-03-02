from distutils.core import setup

setup(
    name='flask-finder',
    version='0.0.1',
    packages=['finder', 'finder.ext'],
    url='none',
    license='GPL3.0',
    author='yu.zhang',
    author_email='geasyheart@163.com',
    description='微服务注册与发现-finder',
    install_requires=[
        'Flask==0.12',
        'redis==2.10.5',
        'requests==2.13.0',
    ]
)
