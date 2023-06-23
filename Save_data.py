
import os,numpy as np,pandas as pd, matplotlib.pyplot as plt
from datetime import datetime

def Save_profiles_npy(name,Param):
    PARAM={'actPower':Param.Profile_actP,
                'reactPower':Param.Profile_actQ}
    np.save(name+'.npy', PARAM)

def Save_voltages_npy(name,Param):
    for iscenario in range(len(Param.Vmg)):
        PARAM={'Vmg':Param.Vmg[iscenario]}
        np.save(os.path.join(name,'Vmg'+str(iscenario)+'.npy'), PARAM)


def Plot_bars(name,Param,PFM, SimTime,VOF):
    x = np.arange(len(PFM))

    fig, ax = plt.subplots()
    # Create the bars for SimTime
    ax.barh(x, SimTime, color='blue', label='SimTime')
    # Create the bars for VOF
    ax.barh(x, -np.array(VOF), color='red', label='VOF')

    # Set the y-axis tick positions and labels
    ax.set_yticks(x)
    ax.set_yticklabels(PFM)

    # Set the x-axis label
    ax.set_xlabel('Time                            Value')
    max=np.max([np.max(SimTime),np.max(VOF)])
    max=max*1.1
    max2=max*0.15
    ax.set_xlim([-max,max ])
    ax.axis('off')
    # Write the rounded values in front of the bars
    for i, (time, vof) in enumerate(zip(SimTime, VOF)):
        ax.text(time+max2, i, f'{round(time, 4)}', ha='left', va='center', color='black')
        ax.text(-vof-max2, i, f'{round(vof, 4)}', ha='right', va='center', color='black')
        ax.text(0, i, f'{PFM[i]}', ha='right', va='center', color='black')
    
    ax.text(0, -1, r'$\sum|v_{i,t}-1|\cdot \alpha$                            Time (s)', ha='center', va='center', color='black')
    
    # Show Plot
    plt.savefig(name+'.png', bbox_inches='tight')
    plt.savefig('test.png', bbox_inches='tight')
    a=1
