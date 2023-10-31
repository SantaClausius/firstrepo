# -*- coding: utf-8 -*-
"""
Created on Thu May  4 11:17:18 2023

@author: ahuerta
"""

# -*- coding: utf-8 -*-
"""
Created on Wed May  3 08:31:59 2023

@author: ahuerta
"""
# MODULES
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import trapz
import os

# PARAMETERS

TOF_path=str('C:\\Users\\staff\\Desktop\\TOF\\20230508\\')
# dataset
file_name=TOF_path+'shot112.csv'

# Length of TOF(in m)
L=1.9

# Light speed (in m/s)
c=3e8

# proton mass (in MeV/c2)
mp=938


ToF_light = L/c

rest_mass_energy = mp *1.**2 # mp is given in MeV/c**

# FUNCTIONS
def find_nearest(array,value):
    idx = (np.abs(array-value)).argmin()
    #return array[idx]
    return idx

# Store coordinates
coords = []
def onclick(event): 
    #global ix, iy
    ix, iy = event.xdata, event.ydata

    # print 'x = %d, y = %d'%(
    #     ix, iy)

    # assign global variable to access outside of function
    global coords
    coords.append((ix, iy))

    # Disconnect after 2 clicks
    if len(coords) == 3:
        fig.canvas.mpl_disconnect(cid)
        plt.close()
    return

# PROGRAMME

# parse measurement

file=open(file_name,'r')
csv_reader=csv.reader(file,delimiter=',')
counter=0

for row in csv_reader:
    counter+=1
    if row!=[] and row[0]=='Record Length':
            n_data=int(float(row[1]))
#            print(n_data)
    if row!=[] and row[0]=='Horizontal Delay':
            delay=float(row[1])
    if row==['TIME','CH3']:
        break
    
contents = np.loadtxt(file_name,skiprows=counter,delimiter=",")
    
x = contents[:,0]
y = contents[:,1]

#Zoom of area of interest
t_delay=find_nearest(x,delay)
t_zoom=0.00000075 #s
t_zoom1=find_nearest(x,delay+0.5*t_zoom)
t_zoom2=find_nearest(x,delay-1*t_zoom)

#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.plot(x[0:t_zoom2],y[0:t_zoom2])

noise=np.mean(abs(y[0:t_zoom2]))
print(noise)

new_time=x[t_zoom2:t_zoom1]
new_y=y[t_zoom2:t_zoom1]

for i in range(0,len(new_time)):
    if abs(new_y[i])>abs(noise)*10:
        new_t0=new_time[i]
        break

t0=t_zoom2+i-5
t1=t0+150
t2=t_zoom1

#print(i)
#print(len(new_time))

   
fig = plt.figure()
ax = fig.add_subplot(111)
#ax.plot(x[t_zoom2+i-5:t_zoom1],y[t_zoom2-5+i:t_zoom1])
ax.plot(x[t1:t2],y[t1:t2])
plt.show()

#earliest_ions_after_protons_Sa2021 = x[t1] * (np.sqrt(2.)-1.)
drift_time_eiap=x[t1]-x[t0]+ToF_light+(x[t1]-x[t0]+ToF_light)* (np.sqrt(2.)-1.)
T_eiap =1./np.sqrt(1. - (L/c/drift_time_eiap)**2) - 1. 
kinetic_energy_eiap = rest_mass_energy * T_eiap

# physical meaning of measurement: kinetic energy to rest mass energy
delta_t_light_to_projectiles = x[t1:t2] - x[t0]


ToF_light = L/c


drift_time = delta_t_light_to_projectiles + ToF_light


T =1./np.sqrt(1. - (L/c/drift_time)**2) - 1. 

# interpretation of measurement: kinetic energy
   
rest_mass_energy = mp *1.**2 # mp is given in MeV/c**
kinetic_energy = rest_mass_energy * T



plt.semilogy(kinetic_energy,-(y[t1:t2]-y[t0]))
plt.axvline(x = kinetic_energy_eiap, color = 'orange', label = 'axvline - full height')

plt.show()

# Integrate the spectrum
cumulative_counts= trapz(-y[t1:t2],x[t1:t2])

print(cumulative_counts)
'''
while True:
    counter +=1
    line=file.readline()
    print(line, type(line))
    print(counter)
    if counter==21:
        break
'''    
