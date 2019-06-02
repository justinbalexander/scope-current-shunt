#!/usr/bin/env python3
from skidl import *

lib_search_paths[KICAD].append('library/snapEDA')
lib_search_paths[KICAD].append('/usr/share/kicad/library')

# Global nets
v_neg_rail = Net('V-', drive=POWER)
v_pos_rail = Net('V+', drive=POWER)
vdd = Net('VDD', drive=POWER)
gnd = Net('GND', drive=POWER)

## Useful nodes
vo = Net('Vo')

# Templated Parts
BatteryHolder = Part(
    'snapEDA',
    'BH123A',
    footprint='BH123A:BH123A',
    dest=TEMPLATE)
R0603_SMD = Part(
    'Device',
    'R',
    footprint='Resistor_SMD:R_0603_1608Metric',
    dest=TEMPLATE)
R1206_SMD = Part(
    'Device',
    'R',
    footprint='Resistor_SMD:R_1206_3216Metric',
    dest=TEMPLATE)
C0603_SMD = Part(
    'Device',
    'C',
    footprint='Capacitor_SMD:C_0603_1608Metric',
    dest=TEMPLATE)
TwoPinHeader100Mils = Part(
    'Connector',
    'Conn_01x02_Male',
    footprint='Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical',
    dest = TEMPLATE)
TwoTermScrewBlock = Part(
    'Connector',
    'Screw_Terminal_01x02',
    footprint='Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical',
    dest = TEMPLATE)


# Part Instantiations
r_shunt = R1206_SMD(value='1',tolerance='1%',rating='1/4W') # RS-6108
r_output_load = R0603_SMD(value='R2.5K')
r_gain = R0603_SMD(value='2.74K',tolerance='1%') # RS-6124
DUT = TwoTermScrewBlock()
op_amp = Part('snapEDA', 'INA129P', footprint='INA129P:DIP254P762X508-8')
i_sense_out = TwoPinHeader100Mils()
batt_negative_rail = BatteryHolder()
batt_positive_rail = BatteryHolder()
batt_dut = BatteryHolder()

# Part connections
## Voltage rails
batt_negative_rail['-'] += v_neg_rail
batt_negative_rail['+'] += gnd
batt_positive_rail['-'] += gnd
batt_positive_rail['+'] += v_pos_rail
batt_dut['-'] += gnd
batt_dut['+'] += vdd

## Op-amp
op_amp_bypass = C0603_SMD(value='0.1uF', dest=TEMPLATE) * 2
op_amp['RG','RG_2'] += r_gain['1','2']
v_pos_rail & op_amp['V+'] & op_amp_bypass[0] & gnd
v_neg_rail & op_amp['V-'] & op_amp_bypass[1] & gnd
op_amp['REF'] += gnd
vo & op_amp['VO'] & r_output_load & gnd

# DUT
vdd & DUT & op_amp['V+IN'] & r_shunt & op_amp['V-IN'] & gnd

## Measurement points
vo & i_sense_out & gnd
gnd += TwoPinHeader100Mils()['.*'] # extra ground points

ERC()
generate_netlist()
generate_xml()
