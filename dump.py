from uiautomator import Device
import json
config = json.loads(open('config.json', 'r').read())

d = Device(config['device'])
d.dump('dump.xml')