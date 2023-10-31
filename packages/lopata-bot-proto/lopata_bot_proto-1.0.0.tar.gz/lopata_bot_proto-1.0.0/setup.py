from distutils.core import setup

setup(
    name='lopata_bot_proto',
    version='1.0.0',
    description='GRPC client for lopata_bot_proto',
    author='ci',
    author_email='p.a.anokhin@gmail.com',
    packages=['lopata_bot_proto'],
    package_data={
      'lopata_bot_proto': ['*.pyi', 'py.typed'],
    },
    include_package_data=True,
)
