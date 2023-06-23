import os,numpy as np,pandas as pd, matplotlib.pyplot as plt
from datetime import datetime
def read_act_react_DATA(Param,scenario):
    for iiday in Param.day:
        ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
        start = '2022-01-01 00:00:00'
        end = '2022-12-31 23:59:00'
        dt = pd.date_range(start=start, end=end)
        dtd = datetime.strptime(str(dt[iiday-1]), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
        #load system data
        ##
        df = pd.read_csv(os.path.join(Param.Directory_name,"data/time_series/P_"+scenario+".csv"))
        df['date_time'] = pd.to_datetime(df['date_time'], format="%d/%m/%Y %H:%M")
        date_filter = df['date_time'].dt.date == pd.to_datetime(dtd).date()
        filtered_df = df[date_filter]
        active_power_time_series = filtered_df.iloc[:,1:].values#  1: neglect the first data (column) in csv file
        ##
        df = pd.read_csv(os.path.join(Param.Directory_name,"data/time_series/Q_"+scenario+".csv"))
        df['date_time'] = pd.to_datetime(df['date_time'], format="%d/%m/%Y %H:%M")
        date_filter = df['date_time'].dt.date == pd.to_datetime(dtd).date()
        filtered_df = df[date_filter]
        reactive_power_time_series =filtered_df.iloc[:,1:].values# 

        LoadData = pd.read_csv(os.path.join(Param.Directory_name,"data/grid_data/"+Param.TestSystem+".csv"),index_col=0,parse_dates=True)
        maxP=LoadData["PD"].values
        maxQ=LoadData["QD"].values
        SameLoadCurve="yes"
        Base_load_data="no"
        if SameLoadCurve=="yes":
            ap=np.array([[active_power_time_series[t][0] for n in range(len(maxP))] for t in range(len(active_power_time_series))])
            aq=np.array([[reactive_power_time_series[t][0] for n in range(len(maxP))] for t in range(len(active_power_time_series))])
            P_profiles1=maxP*ap
            Q_profiles1=maxQ*aq
            if Base_load_data=="yes":
                scale=np.array([active_power_time_series[t][0] for t in range(len(active_power_time_series))])
                scale=scale/np.max(scale)
                scaleAll1='yes'
                if scaleAll1=='yes':
                    scale=np.add(np.multiply(scale,0),1)
                ap=np.array([[scale[t] for n in range(len(maxP))] for t in range(len(active_power_time_series))])
                aq=np.array([[scale[t] for n in range(len(maxP))] for t in range(len(active_power_time_series))])
                P_profiles1=maxP*ap
                Q_profiles1=maxQ*aq
        else:
            P_profiles1=maxP*active_power_time_series
            Q_profiles1=maxQ*reactive_power_time_series



        Param.P_profile=P_profiles1[:,Param.profile_info:]
        Param.Q_profile=Q_profiles1[:,Param.profile_info:]
        Param.nTime=len(Param.P_profile)
        Param.nLoad=len(Param.P_profile[0])

        
        
    return Param




