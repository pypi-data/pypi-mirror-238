# Liusch (LiU Schedule)
This is a simple module for polybar which shows the next course scheduled at LIU. It supports the merging of several schedules to allow for high customizability.

![Polybar](https://i.imgur.com/fqsRZhV.png)

## Installation
```bash
pip install liusch
```
## Polybar settings
```ini 
[module/liusch]
type = custom/script
exec = liusch
interval = 900
```

## Usage
### Adding a Schedule
```bash
liusch -a example_name https://cloud.timeedit.net/liu/web/schema/ri667QQQY63Zn3Q5861309Z7y6Z06.ics
```

### Adding a Whitelisted Course
Some entries in TimeEdit has several course codes. To tell the module which of these should be shown the wanted code can be whitelisted.
```bash
liusch -aw TDDD23
```

Please view the help page for the full documentation
```bash
liusch -h
```
