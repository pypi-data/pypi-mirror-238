from distutils.core import setup

setup(
    name='anek_service',
    version='0.0.2',
    description='GRPC client for anek_service',
    author='ci',
    author_email='p.a.anokhin@gmail.com',
    packages=['anek_service'],
    package_data={
      'anek_service': ['*.pyi', 'py.typed'],
    },
    include_package_data=True,
)
