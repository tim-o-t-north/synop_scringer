# -*- coding: iso-8859-1 -*-
import csv
import urllib2
import os
import string


# function returning sign of temperature
def fn_sign(code_number, style_neg="-", style_pos="+"):
    if (code_number == 1):
        sign_of_temperature = style_neg
    elif (code_number == 0):
        sign_of_temperature = style_pos
    return sign_of_temperature


# function returning the temperature as somthing human readable
def fn_temperature(code_number):
    temperature = float(code_number[2:5]) / 10
    sign_of_temp = float(code_number[1:2])
    return fn_sign(sign_of_temp) + str(temperature)


# function taking pressure in 4 digit 1 dp form
# and returning full pressure
def fn_readable_pressure(pressure):
    if pressure[0] == '0':
        pressure = '1' + pressure
        pressure = float(pressure) / 10
        return pressure
    elif pressure[0] == '9':
        pressure = float(pressure) / 10
        return pressure


# function returning pressure tendency string
# float_out is intended to be a boolean, if set false
# output will be a string representing tendency
# /\ /- / 
def fn_pressure_tendency(tendency, float_out=True):
    change = tendency[2:5]
    trend = tendency[1:2]
    if float(trend) < 5:
        change = float(change) * -0.1
    else:
        change = float(change) * 0.1
    return change


# Liquid precip coding information
def fn_liquid_precip(RRRt):
    volume = RRRt[1:5]
    return float(volume) / 10
    duration = RRRt[5:6]
    #if duration == "5":
    #    return volume
    #else:
    #    return "no one hour precip available"


# vis decode function
# deals with frankly baffling synop vis code_number
def fn_vis_decode(vis):
    if vis > 90:
       ship_vis = True
    else:
        ship_vis = False
    
    if vis < 56:
        vis = vis / 10
    elif vis < 80:
        vis = vis - 50
    elif vis < 89:
        vis = ((vis-80) * 5) + 30
    elif vis == 89:
        vis = 'greater than 70 km' 
    elif vis ==90:
        vis = 'less than 0.05 km'
    elif vis == 91:
        vis = 0.05
    elif vis == 92:
        vis = 0.2
    elif vis == 93:
        vis = 0.5
    elif vis == 94:
        vis = 1
    elif vis == 95:
        vis = 2
    elif vis == 96:
        vis = 4
    elif vis == 97:
        vis = 10
    elif vis == 98:
        vis = 20
    elif vis == 99:
        vis = "greater than 50 km"
    else :
        vis = 'error: visibility code uninterpretable'
    output = {'visiblity': vis, 'vis from ship': ship_vis }
    return output

# second part1  decoder function
def fn_part1b_decode(data):
    output = {}
    data = string.split(data, " ")
    for item in data:
        output[item] = item
    output['spiltpartb'] = data
    
    return output


# first part1  decoder function
def fn_part1a_decode(data):
    output = {}
    output['wmo number'] =  data[11:16]
    #not currently working, and I don't know why
    vis_code = int(data[20:22])
    #output['vis as code'] = vis_code
    output.update(fn_vis_decode(vis_code))
    #output['visibility'] = (fn_vis_decode(vis_code))
    output['wind speed'] =  (data[26:29])
    output['wind direction'] = (data[24:26] + '0')
    return output

# main synop decoder
def synop_decoder(data):
    output = {}
    data = string.split(data, " 333 ")[0]
    output['part1'] = data
    output['part1a'] = data[0:29]
    output['part1b'] = data[28:]
    
    return output


    


# version commented - using test data to avoid annoying @g1m3t (hem hem)
# url = "http://www.ogimet.com/cgi-bin/getsynop?block=3414&begin=201602010000&end=201602011200"
# response = urllib2.urlopen(url)
response = open("sample_synop.html").readlines()

messages = csv.reader(response)

for message in messages:
    print message
    synop_full_message={}
    synop_full_message["synop"] = message[-1]
    synop_full_message['year'] = message [1]
    synop_full_message['month'] = message [2]
    synop_full_message['day'] = message[3]
    synop_full_message['hour'] = message [4]
    synop_full_message.update(synop_decoder(synop_full_message["synop"]))
    synop_full_message.update(fn_part1a_decode(synop_full_message["part1a"]))
    synop_full_message.update(fn_part1b_decode(synop_full_message["part1b"]))


    print "--==-- Final Output  --==--"
    print synop_full_message
    print "--==--    The End------------------------------------"
    #fn_synop_decoder(synop_part1a,synop_part1b, True)

