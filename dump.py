from uiautomator import Device
import yaml
config = yaml.load(open('config.yml', 'r').read())

d = Device(config['device'])
d.dump('dump.xml')