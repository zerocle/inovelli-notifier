import homeassistant.helpers.template as template

clearNotification = {
    "led_effect": 0,
    "led_color": 0,
    "led_level": 0,
    "led_duration": 1,
}
devicesToNotify = []
notifications = {
}

def notifyDevices():
    global notifications
    global devicesToNotify
    global clearNotification
    task.unique("notify_devices")
    while(len(notifications) > 0):
        log.info(f"Current notifications: {notifications.keys()}")
        for key in list(notifications.keys()):
            notificationParams = notifications[key]
            log.info(f"Sending notification: {notificationParams}")
            for device in devicesToNotify:
                service.call("zha", "issue_zigbee_cluster_command",ieee=device, manufacturer=4655, cluster_id=64561, endpoint_id=1, cluster_type="in", command=1,command_type="server", params=notificationParams)
            task.sleep(notificationParams["led_duration"])
    log.info(f"Clearing notifications")
    for device in devicesToNotify:
        service.call("zha", "issue_zigbee_cluster_command",ieee=device, manufacturer=4655, cluster_id=64561, endpoint_id=1, cluster_type="in", command=1,command_type="server", params=clearNotification)

@service
def add_notification(notificationName, led_color, led_effect=1,  led_level=50, notification_duration=10):
    """yaml 
name: Add Notification
description: Add a notification to the list of notifications to send.
fields:
    notificationName:
        description: The name of the notification
        example: "Garage Door Open"
        required: true
        selector:
            text:

    led_color:
        description: The color to use for the notification. Visit https://nathanfiscus.github.io/inovelli-notification-calc/ to calculate the color value.
        example: 0
        default: 0
        required: true
        selector:
            number:
                min: 0
                max: 255
                mode: box
                initial: 0

    led_effect:
        description: The effect to use for the notification.
        example: 1
        required: false
        default: 1
        selector:
            select:
                options:
                    - label: off
                      value: 0
                    - label: clear
                      value: 255
                    - label: solid
                      value: 1
                    - label: slow blink
                      value: 3
                    - label: medium blink
                      value: 15
                    - label: fast blink
                      value: 2
                    - label: pulse
                      value: 4
                    - label: aurora
                      value: 8
                    - label: slow falling
                      value: 9
                    - label: medium falling
                      value: 10
                    - label: fast falling
                      value: 11
                    - label: slow rising
                      value: 12
                    - label: medium rising
                      value: 13
                    - label: fast rising
                      value: 14
                    - label: chase
                      value: 5
                    - label: slow chase
                      value: 16
                    - label: medium chase
                      value: 5
                    - label: fast chase
                      value: 17
                    - label: fast siren
                      value: 18
                    - label: slow siren
                      value: 19
                    - label: open-close
                      value: 6
                    - label: small-big
                      value: 7

    led_level:
        description: The brightness to use for the notification. 0 is off, 100 is full brightness.
        example: 50
        required: false
        default: 50
        selector:
            number:
                min: 0
                max: 100
                mode: box
                initial: 50

    notification_duration:
        description: The time, in seconds, to show the notification before transitioning to the next notification
        example: 10
        required: false
        default: 10
        selector:
            number:
                min: 0
                max: 100
                mode: box
                initial: 10
                unit: seconds

"""
    global notifications
    notifications[notificationName] = {
        "led_effect": led_effect,
        "led_color": led_color,
        "led_level": led_level,
        "led_duration": notification_duration + 1,
    }
    task.create(notifyDevices)

@service
def remove_notification(notificationName):
    """yaml 
name: Remove Notification
description: Remove a notification from the list of notifications.
fields:
    notificationName:
        description: The name of the notification
        example: "Garage Door Open"
        required: true
        selector:
            text:
"""
    global notifications
    if notificationName in notifications:
        del notifications[notificationName]
    task.create(notifyDevices)

@service
def clear_notifications():
    """yaml 
name: Clear Notifications
description: Clear all notifications currently active.
"""
    global notifications
    notifications = {}
    task.create(notifyDevices)



def loadApp(app_name, factory):
    if 'apps' not in pyscript.config:
        log.info("no apps section in pyscript config")
        return
    
    if app_name not in pyscript.config['apps']:
        log.info(f"no {app_name} app in pyscript config")
        return

    for app in pyscript.config['apps'][app_name]:
        log.info(f"loading {app_name} app: {app}")
        factory(app)


@time_trigger('startup')
def notificationManagerStartup():
    loadApp('inovelli_notifier', setupNotificationDevices)

def setupNotificationDevices(config):
    global devicesToNotify
    switches = config.get('switches')
    for device in switches:
        identifiers = template.device_attr(hass=hass, device_or_entity_id=device, attr_name='identifiers')
        if len(identifiers) > 0:
            actualIdentifier = identifiers.pop()[1]
            devicesToNotify.append(actualIdentifier)
        else:
            log.error(f"Device [{device}] has no identifiers, skipping")