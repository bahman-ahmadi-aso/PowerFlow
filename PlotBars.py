import sys,os,time,numpy as np,pandas as pd,matplotlib.pyplot as plt

PFM=['NR','FBS','FDM','LPF','APNR','TPF'] 
SimTime=[696.496,1004.146,806.412,657.355,4.059,3.117]

VOF=[6.9475,6.9475,6.9475,6.9475,6.9902,6.9475]



x = np.arange(len(PFM))

fig, ax = plt.subplots()
# Create the bars for SimTime
ax.barh(x, SimTime, color='cornflowerblue',  edgecolor='blue', label='SimTime')

# Set the y-axis tick positions and labels
ax.set_yticks(x)
ax.set_yticklabels(PFM)

max=np.max([np.max(SimTime)])
max=max*1.1
max2=max*0.15
ax.set_xlim([-max,max ])
ax.axis('off')
# Write the rounded values in front of the bars
for i, (time, vof) in enumerate(zip(SimTime, VOF)):
    ax.text(time+max2, i, f'{round(time, 4)}', ha='left', va='center', color='black')
    ax.text(0, i, f'{PFM[i]}', ha='right', va='center', color='black')

ax.text(0, -1, r'                              Time (s)', ha='center', va='center', color='black')

# Show Plot
plt.savefig('test1.png', bbox_inches='tight')



fig, ax = plt.subplots()
# Create the bars for SimTime
# Create the bars for VOF
ax.barh(x, -np.array(VOF), color='mediumaquamarine',  edgecolor='green', label='VOF')

# Set the y-axis tick positions and labels
ax.set_yticks(x)
ax.set_yticklabels(PFM)

max=np.max([np.max(VOF)])
max=max*1.1
max2=max*0.15
ax.set_xlim([-max,max ])
ax.axis('off')
# Write the rounded values in front of the bars
for i, (time, vof) in enumerate(zip(SimTime, VOF)):
    ax.text(-vof-max2, i, f'{round(vof, 4)}', ha='right', va='center', color='black')
    ax.text(3, i, f'{PFM[i]}', ha='right', va='center', color='black')

ax.text(0, -1, r'$\sum|v_{i,t}-1|\cdot \alpha$                                    ', ha='center', va='center', color='black')

# Show Plot
plt.savefig('test2.png', bbox_inches='tight')


a=1




