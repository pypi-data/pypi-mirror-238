version='5.72.0-pre0018'
from setuptools import setup

# Read the contents of the README file.
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
      author='CODE Consulting and Development, s.r.o.',
      author_email='sales09@opclabs.com',
      description='Ethernet and capture file communication package.',
      include_package_data=True,
      install_requires=['opclabs_quickopc'],
      keywords='QuickOPC, OPC, UA, PubSub, Ethernet, UDP, capture',
      #license=
      #license_file=
      license_files=['opclabs_pcap\\OpcLabs.Pcap\\*.htm', 'opclabs_pcap\\OpcLabs.Pcap\\*.html', 'opclabs_pcap\\OpcLabs.Pcap\\*.txt'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      name='opclabs_pcap',
      packages=['opclabs_pcap'],
      zip_safe=False,
      url='https://kb.opclabs.com/OpcLabs.Pcap_communication_package?python',
      version=version,
)
