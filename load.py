#! /bin/env python3

import matplotlib.pyplot as plt
import csv

def row_data(row, point_list):

    point_list['x'].append(float(row[2].replace(',', '.')))
    point_list['y'].append(float(row[3].replace(',', '.')))
    point_list['xy'].append([float(row[3].replace(',', '.')), float(row[2].replace(',', '.'))])

    return point_list

def load():

    podaci = {
        'mat': {
            'x': [],
            'y': [],
            'xy': [],
            'centroids': None,
            'cluster': None
        },
        'pov': {
            'x': [],
            'y': [],
            'xy': [],
            'centroids': None,
            'cluster': None
        },
        'pog': {
            'x': [],
            'y': [],
            'xy': [],
            'centroids': None,
            'cluster': None
        },
        'park': {
            'x': [],
            'y': [],
            'xy': [],
            'centroids': None,
            'cluster': None
        },
        'pes': {
            'x': [],
            'y': [],
            'xy': [],
            'centroids': None,
            'cluster': None
        },
        'jedVoz': {
            'x': [],
            'y': [],
            'xy': [],
            'centroids': None,
            'cluster': None
        },
        'dvaVoz': {
            'x': [],
            'y': [],
            'xy': [],
            'centroids': None,
            'cluster': None
        }
    }

    with open("data.csv", "r") as f:
        reader = csv.reader(f)
        index = 0
        for row in reader:
            if index > 4000:
                break
            index += 1
            
            if row[4] == 'mat':
                podaci['mat'] = row_data(row, podaci['mat'])
            if row[4] == 'pov':
                podaci['pov'] = row_data(row, podaci['pov'])
            if row[4] == 'pog':
                podaci['pog'] = row_data(row, podaci['pog'])

            if row[5] == 'park':
                podaci['park'] = row_data(row, podaci['park'])
            if row[5] == 'pes':
                podaci['pes'] = row_data(row, podaci['pes'])
            if row[5] == 'jedVoz':
                podaci['jedVoz'] = row_data(row, podaci['jedVoz'])
            if row[5] == 'dvaVoz':
                podaci['dvaVoz'] = row_data(row, podaci['dvaVoz'])

    return podaci

# print(load())