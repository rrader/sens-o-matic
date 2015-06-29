def door_sensor_factory():
    from sensomatic.sensors.reed_switch import reed_switch_sensor
    return reed_switch_sensor


def file_sensor_factory():
    from sensomatic.sensors.test_file import file_content_sensor
    return file_content_sensor['/tmp/tst']


KNOWN_SENSORS = {
    'door': {
        'factory': door_sensor_factory,
        'meta': {
            'values': {
                '0': 'Door is closed',
                '1': 'Door is opened'
            }
        }
    },
    'file': {
        'factory': file_sensor_factory,
        'meta': {
            'values': {
                '0': '0 in the file',
                '1': '1 in the file'
            }
        }
    }
}
