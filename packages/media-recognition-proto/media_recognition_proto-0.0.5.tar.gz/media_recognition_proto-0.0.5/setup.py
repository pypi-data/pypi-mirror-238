from distutils.core import setup

setup(
    name='media_recognition_proto',
    version='0.0.5',
    description='GRPC client for media_recognition_proto',
    author='ci',
    author_email='p.a.anokhin@gmail.com',
    packages=['media_recognition_proto'],
    package_data={
      'media_recognition_proto': ['*.pyi', 'py.typed'],
    },
    include_package_data=True,
)
