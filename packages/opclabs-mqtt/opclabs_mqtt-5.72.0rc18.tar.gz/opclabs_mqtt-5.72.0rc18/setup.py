version='5.72.0-pre0018'
from setuptools import setup

# Read the contents of the README file.
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
      author='CODE Consulting and Development, s.r.o.',
      author_email='sales09@opclabs.com',
      description='MQTT communication package based on System.Net.Mqtt library by Xamarin (Microsoft).',
      include_package_data=True,
      install_requires=['opclabs_quickopc'],
      keywords='QuickOPC, OPC, UA, PubSub, MQTT',
      #license=
      #license_file=
      license_files=['opclabs_mqtt\\OpcLabs.Mqtt\\*.htm', 'opclabs_mqtt\\OpcLabs.Mqtt\\*.html', 'opclabs_mqtt\\OpcLabs.Mqtt\\*.txt'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      name='opclabs_mqtt',
      packages=['opclabs_mqtt'],
      zip_safe=False,
      url='https://kb.opclabs.com/OpcLabs.Mqtt_communication_package?python',
      version=version,
)
