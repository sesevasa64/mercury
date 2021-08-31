from setuptools import setup, find_packages


with open("qsilver/README.md") as f:
    long_description = f.read()

setup(
    name='qsilver',
    version='0.2',
    license='MIT',
    author="Vsevolod Vlasov",
    author_email='sesevasa64@gmail.com',
    packages=find_packages(),
    url='https://github.com/sesevasa64/qsilver',
    keywords=["async", "concurrent"],
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True
)
