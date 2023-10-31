from setuptools import setup, find_packages


setup(
    name='scprotein', 
    version='0.1.0',  
    author='LiWei', 
    description='scprotein is a deep contrastive learning framework for Single-cell Proteomics Embedding.',  
    url='https://github.com/TencentAILabHealthcare/scPROTEIN',
    packages=find_packages(),  
    install_requires=[  
        'torch>=1.10.0',
        'scanpy>=1.8.2',
        'numpy>=1.22.3',
        'pandas>=1.3.5',
        'scipy>=1.8.1',
        'scikit_learn>=1.1.1',
        'torch_geometric>=2.0.4'
    ],
    python_requires=">=3.8",
    author_email = 'nkuweili@mail.nankai.edu.cn',
    license='Apache'
)
