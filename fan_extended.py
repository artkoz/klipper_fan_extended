# Support fans that are controlled by gcode
#
# Initial Copyright (C) 2016-2020  Kevin O'Connor <kevin@koconnor.net>
# Copyright (c) 2023 Artem Kozakov artko@mgslab.com
# This file may be distributed under the terms of the GNU GPLv3 license.
from . import fan

PIN_MIN_TIME = .100


class PrinterFanExtended:
    cmd_SET_FAN_SPEED_help = "Sets the speed of a fan"

    def __init__(self, config):
        self.printer = config.get_printer()
        self.reactor = self.printer.get_reactor()
        self.gcode = self.printer.lookup_object('gcode')
        self.fan = fan.Fan(config, default_shutdown_speed=0.)
        self.fan_name = config.get_name().split()[-1]
        self.min_speed = config.getfloat(
            'min_speed', 0., minval=0., maxval=1.)
        self.max_speed = config.getfloat(
            'max_speed', 1., minval=0., maxval=1.)
        self.cur_speed = 0
        self.min_temp = config.getfloat(
            'min_temp', 0., minval=0, maxval=300)
        self.max_temp = config.getfloat(
            'max_temp', 100., minval=0, maxval=300)

        if self.max_temp < self.min_temp:
            self.max_temp = self.min_temp

        if self.max_speed < self.min_speed:
            self.max_speed = self.min_speed
        self.temp_sensor = config.get("temp_sensor", "")
        self.pheaters = []
        gcode = self.printer.lookup_object("gcode")
        gcode.register_mux_command("SET_FAN_SPEED", "FAN",
                                   self.fan_name,
                                   self.cmd_SET_FAN_SPEED,
                                   desc=self.cmd_SET_FAN_SPEED_help)

        self.printer.register_event_handler("klippy:ready", self.handle_ready)

    def handle_ready(self):
        self.pheaters = self.printer.lookup_object('heaters')
        reactor = self.printer.get_reactor()
        reactor.register_timer(self.callback, reactor.monotonic()+PIN_MIN_TIME)

    def callback(self, eventtime):
        try:
            if self.temp_sensor != '':
                temps = self.printer.lookup_object(self.temp_sensor)
                tstatus = temps.get_status(eventtime)
                cur_temp = tstatus["temperature"]
                self.cur_speed = self.min_speed
                if cur_temp <= self.min_temp:
                    self.cur_speed = self.min_speed
                else:
                    if cur_temp >= self.max_temp:
                        self.cur_speed = self.max_speed
                    else:
                        val_a = self.max_temp - self.min_temp
                        val_b = cur_temp - self.min_temp
                        val_c = val_b / val_a
                        val_d = (self.max_speed - self.min_speed) * val_c
                        need_speed = val_d + self.min_speed
                        self.cur_speed = need_speed
                        self.fan.set_speed_from_command(self.cur_speed)
                if self.cur_speed < self.min_speed:
                    self.cur_speed = self.min_speed
                if self.cur_speed > self.max_speed:
                    self.cur_speed = self.max_speed
                self.fan.set_speed_from_command(self.cur_speed)
        except Exception as e:
            self.gcode.respond_info("except %s" % (str(e)))
        return eventtime + 1.

    def get_status(self, eventtime):
        return self.fan.get_status(eventtime)

    def cmd_SET_FAN_SPEED(self, gcmd):
        speed = gcmd.get_float('SPEED', 0.)
        if speed < self.min_speed:
            speed = self.min_speed
        if speed > self.max_speed:
            speed = self.max_speed
        self.cur_speed = speed
        self.fan.set_speed_from_command(speed)


def load_config_prefix(config):
    return PrinterFanExtended(config)
