from setuptools import setup, find_packages
setup(
  name = 'pallet_loading_env',         
  packages = find_packages(),   
  version = '0.1',      
  license='MIT',        
  description = 'An environment based on the OpenAI gym API tha can be used for the 3D-BPP',  
  author = 'Hendrik Jon Schmidt',                   
  author_email = 'hendrikjonschmidt@gmail.com',      
  url = 'https://github.com/hndrjs/pallet_loading_env',   
  download_url = 'https://github.com/hndrkjs/pallet_loading_env/archive/refs/tags/v_01.tar.gz',    
  keywords = ['Weight Constraints', 'Stability-Check', '3D-BPP', 'Deep Reinforcement Learning'],   
  install_requires=[           
          'numpy',
          'pybullet',
          'gym'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Science/Research',      
    'Topic :: Scientific/Engineering :: Artificial Intelligence',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',      
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
