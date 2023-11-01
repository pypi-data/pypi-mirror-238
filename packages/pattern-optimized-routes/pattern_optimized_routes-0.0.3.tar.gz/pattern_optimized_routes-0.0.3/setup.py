from setuptools import setup, find_packages
import os

abs_path = os.path.abspath(os.path.dirname(__file__))

setup(
    name='pattern_optimized_routes',
    version='0.0.3',
    license='MIT',
    description = 'Package to simulate the MultilevelERU (Expected Road Usage) model and the literature baselines results on a road network with a traffic demand.',
    long_description = open(os.path.join(abs_path, 'README.rst')).read(),
    author="Ludovico Lemma",
    author_email='lwdovico@protonmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/lwdovico/pattern-optimized-routes',
    keywords='Utils',
    install_requires=[
          'routing_lib',
      ],

)