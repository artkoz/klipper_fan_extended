# klipper_fan_extended

Modified fan_generic, Print cooling fan.
[fan_extended my_fan_extended]

#all parameters from original [fan] section https://www.klipper3d.org/Config_Reference.html?h=fans#fans

#linear regulation of fan speed, if additional parameters provided:
#min_speed:
#the minimum speed will be set after the printer is in ready state. default = 0, from  0 to max_speed
#max_speed:
#maximum allowed speed. default 1.
#min_temp:
#minimal temperature, temp_sensor <= min_temp, speed = min_spped
#max_temp:
#maximum temperature, temp_sensor >= max_temp, speed = max_spped
#linear adjustment within min_temp...max_temp, speed proportionally between min_speed and max_speed
#temp_sensor: temperature_sensor host_sbc
#the value of the sensor that is taken for adjustment
#specified as the full name of the object.
#for example, if you need to adjust using the host temperature
#[temperature_sensor host_sbc]
#sensor_type: temperature_host
#
#
#

