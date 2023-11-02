version='5.72.0-pre0018'
from setuptools import setup

# Read the contents of the README file.
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
      author='CODE Consulting and Development, s.r.o.',
      author_email='sales09@opclabs.com',
      description='QuickOPC Client and Subscriber Toolkit for OPC UA and OPC Classic.',
      include_package_data=True,
      install_requires=['pythonnet'],
      keywords='OPC, OPC-UA',
      #license=
      #license_file=
      license_files=['opclabs_quickopc\\OpcLabs.QuickOpc\\*.htm', 'opclabs_quickopc\\OpcLabs.QuickOpc\\*.html', 'opclabs_quickopc\\OpcLabs.QuickOpc\\*.txt'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      name='opclabs_quickopc',
      packages=['opclabs_quickopc'],
      zip_safe=False,
      url='https://www.opclabs.com/products/quickopc?python',
      version=version,
)
