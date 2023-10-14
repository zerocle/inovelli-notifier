# Inovelli Notifier

Inovelli Notifier is a [Pyscript](https://github.com/custom-components/pyscript) for [Home Assistant](https://www.home-assistant.io/) that allows you to queue notifications for [Inovelli's 2 in 1 Blue](https://inovelli.com/) switches. Multiple distinct notifications can be added and removed using a name identifier. Each notification can have a distinct color/effect/brightness/duration. Notifications can also be cleared one at a time by name, or clear all notifications at once. Switches that you want included in the notification group should be indicated within the configuration.yaml file.

## Configuration

Place `novelli_notifier.py` in the `~/config/pyscript` folder within your Home Assistant installation

In the `configuration.yaml` add the following configuration:

```yaml
pyscript:
  apps:
    inovelli_notifier:
      - switches:
          button.my_inovelli_switch_identify:
          button.my_other_inovelli_switch_identify:
          button.my_third_inovelli_switch_identify:
```

## Calling the Script

### Adding Notifications

Notifications can be added using the `add_notification` service.

```yaml
service: pyscript.add_notification
data:
  notificationName: foobar
  led_color: 26
  led_effect: "4"
  led_level: 50
  notification_duration: 10
```

### Removing Notifications

Notifications can be removed using the `remove_notification` service.

```yaml
service: pyscript.remove_notification
data:
  notificationName: foobar
```

### Clear Notifications

All notifications can be cleared using the `clear_notifications` service.

```yaml
service: pyscript.clear_notifications
data: {}
```

## Automation Example

```yaml
alias: Front door open
description: ""
trigger:
  - platform: state
    entity_id:
      - binary_sensor.lumi_lumi_sensor_magnet_aq2_opening
    to: "on"
condition: []
action:
  - service: pyscript.add_notification
    data:
      notificationName: frontDoorOpen
      led_color: 80
      led_effect: 4
      led_level: 50
mode: single
```
