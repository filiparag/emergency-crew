#! /bin/env python3

import numpy as np
from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import load
import csv
import gmaps

def prosecni_cluster(_centroidi, _sve_nezgode):

    sve_nezgode_cluster = []
    for tacka in _sve_nezgode:
        rastojanja = []
        for centroid in _centroidi:
            rastojanja.append(np.linalg.norm(tacka-centroid))
        sve_nezgode_cluster.append(rastojanja.index(min(rastojanja)))

    return sve_nezgode_cluster

def varijansa_i_max_puta(_centroidi, _sve_nezgode, _sve_nezgode_cluster):

    varijanse = []
    duzine = []
    najdalje = []
    for cent in range(len(_centroidi)):
        duzine_puta = []
        najdalje.append(0)
        for nezgoda in range(len(_sve_nezgode)):
            if _sve_nezgode_cluster[nezgoda] == cent:
                duzine_puta.append(np.linalg.norm(_centroidi[cent] - _sve_nezgode[nezgoda]))
                if max(duzine_puta) == np.linalg.norm(_centroidi[cent] - _sve_nezgode[nezgoda]):
                    najdalje[cent] = _sve_nezgode[nezgoda]
        varijanse.append(np.var(duzine_puta))
        duzine.append(max(duzine_puta))

    gmapscalc = []
    for ind in range(len(najdalje)):
        gmapscalc.append(gmaps.trajanje_voznje(_centroidi[ind], najdalje[ind]))

    return varijanse, duzine, gmapscalc

podaci = load.load()

for key in podaci:
    
    data = np.array(podaci[key]['xy'])
    kmeans = KMeans(n_clusters=load.sluzbe, random_state=10).fit(data)
    podaci[key]['centroids'] = kmeans.cluster_centers_
    podaci[key]['cluster'] = kmeans.labels_


# policija_centroid = np.mean(np.array([
#         podaci['mat']['centroids'],
#         podaci['park']['centroids'],
#         podaci['jedVoz']['centroids']
#     ]), axis=0)

# print(policija_centroid)

# hitna_centroid = np.mean(np.array([
#         podaci['pov']['centroids'],
#         podaci['pog']['centroids'],
#         podaci['pes']['centroids'],
#         podaci['dvaVoz']['centroids']
#     ]), axis=0)

policija_centroid_sve = [
    *podaci['mat']['centroids'],
    *podaci['park']['centroids'],
    *podaci['jedVoz']['centroids']
    ]

hitna_centroid_sve = [
    *podaci['pov']['centroids'],
    *podaci['pog']['centroids'],
    *podaci['pes']['centroids'],
    *podaci['dvaVoz']['centroids']
]


kmeans_policija = KMeans(n_clusters=load.sluzbe, random_state=10).fit(policija_centroid_sve)
kmeans_hitna = KMeans(n_clusters=load.sluzbe, random_state=10).fit(policija_centroid_sve)

policija_centroid = kmeans_policija.cluster_centers_
hitna_centroid = kmeans_hitna.cluster_centers_

# print(policija_centroid)


# exit()

sve_nezgode = []
for key in podaci:
    sve_nezgode += podaci[key]['xy']

sve_nezgode_cluster_policija = prosecni_cluster(policija_centroid, sve_nezgode)
sve_nezgode_cluster_hitna = prosecni_cluster(hitna_centroid, sve_nezgode)


xp = [point[0] for point in sve_nezgode]
yp = [point[1] for point in sve_nezgode]

xcp = [point[0] for point in policija_centroid]
ycp = [point[1] for point in policija_centroid]

xch = [point[0] for point in hitna_centroid]
ych = [point[1] for point in hitna_centroid]

plt.figure(1)
plt.scatter(yp, xp)

plt.figure(6)
plt.scatter(yp, xp, c=sve_nezgode_cluster_policija)
plt.scatter(ycp, xcp, marker='x', c='r')

plt.figure(7)
plt.scatter(yp, xp, c=sve_nezgode_cluster_hitna)
plt.scatter(ycp, xch, marker='+', c='r')

# hitna_varijansa_duzine_puta = []
# for cent in range(len(hitna_centroid)):
#     hitna_duzine_puta = []
#     for nezgoda in range(len(sve_nezgode)):
#         if sve_nezgode_cluster_hitna[nezgoda] == cent:
#             hitna_duzine_puta.append(np.linalg.norm(hitna_centroid[cent] - sve_nezgode[nezgoda]))
#     hitna_varijansa_duzine_puta.append(np.var(hitna_duzine_puta))

hitna_varijansa, hitna_max_duzina, hitna_gmaps_trajanja = varijansa_i_max_puta(hitna_centroid, sve_nezgode, sve_nezgode_cluster_hitna)
policija_varijansa, policija_max_duzina, policija_gmaps_trajanja = varijansa_i_max_puta(policija_centroid, sve_nezgode, sve_nezgode_cluster_hitna)

print('#########################')
print('Hitna pomoc:')
print('Varijansa', hitna_varijansa)
print('Max euklidska duzina puta', hitna_max_duzina)
print('Google Maps vreme i putanja', hitna_gmaps_trajanja)

print('#########################')
print('Policija')
print('Varijansa', policija_varijansa)
print('Max euklidska duzina puta', policija_max_duzina)
print('Google Maps vreme i putanja', policija_gmaps_trajanja)

# print(hitna_varijansa, hitna_max_duzina)
# print(policija_varijansa, policija_max_duzina)

# hitna_sve = []
# for ind in range(len(sve_nezgode)):
#     hitna_sve.append([sve_nezgode[ind][0], sve_nezgode[ind][1], sve_nezgode_cluster_hitna[ind]])

# with open("hitna.csv", "w") as f:
#     writer = csv.writer(f)
#     writer.writerows(hitna_sve)


# policija_sve = []
# for ind in range(len(sve_nezgode)):
#     policija_sve.append([sve_nezgode[ind][0], sve_nezgode[ind][1], sve_nezgode_cluster_policija[ind]])

# with open("policija.csv", "w") as f:
#     writer = csv.writer(f)
#     writer.writerows(policija_sve)

# print(hitna_sve)

plt.show()