from setuptools import setup, find_packages

setup(name='pymle-diffusion',
      version='0.0.7',
      description='Maximum Likelihood Estimation (MLE) and simulation for SDE',
      long_description='Maximum Likelihood Estimation (MLE) and simulation for '
                       'Stochastic Differential Equations (SDE)',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.7',
          'Topic :: Scientific/Engineering ',
          "Operating System :: OS Independent",
      ],
      keywords='sde mle maximum likelihood difussion estimation simulation',
      url='https://github.com/jkirkby3/pymle',
      author='Justin Lars Kirkby',
      author_email='jkirkby33@gmail.com',
      license='MIT',
      packages=find_packages(),
      python_requires=">=3.7",
     # package_dir={'pymle-diffusion': 'pymle'},
      # package_data={'pymle': ['pymle/data/*.csv']},
      install_requires=[
          'numba',
          'setuptools',
          'numpy',
          'scipy',
          'pandas',
          'seaborn'
      ],
      include_package_data=True,
      # package_data={'pymle': ['data2/*.csv']},
      zip_safe=False)
