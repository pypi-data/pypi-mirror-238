version='5.72.0-pre0018'
from setuptools import setup

# Read the contents of the README file.
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
      author='CODE Consulting and Development, s.r.o.',
      author_email='sales09@opclabs.com',
      description='MQTT communication package based on MQTTnet and MQTTnet.Extensions.ManagedClient libraries by Christian Kratky.',
      include_package_data=True,
      install_requires=['opclabs_quickopc'],
      keywords='QuickOPC, OPC, UA, PubSub, MQTT',
      #license=
      #license_file=
      license_files=['opclabs_mqttnet\\OpcLabs.MqttNet\\*.htm', 'opclabs_mqttnet\\OpcLabs.MqttNet\\*.html', 'opclabs_mqttnet\\OpcLabs.MqttNet\\*.txt'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      name='opclabs_mqttnet',
      packages=['opclabs_mqttnet'],
      zip_safe=False,
      url='https://kb.opclabs.com/OpcLabs.MqttNet_communication_package?python',
      version=version,
)
