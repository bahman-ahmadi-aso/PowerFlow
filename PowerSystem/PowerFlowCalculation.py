
import numpy as np
import time 
def PowerFlowCalculation(Param):

    ## the power flow outs
    if Param.PowerFlowMethod == 'Laurent':
        ########################   Laurent   ############################
        from PowerSystem.run_pf_Laurent import run_pf_Laurent
        nb = Param.System_Data_Nodes.shape[0]
        Vmg = []
        for iSA in range(len(Param.P_profiles)):
            ViSA=[]
            for iT in range(Param.nTime):
                V_0 = np.ones((nb - 1)) + 1j * np.zeros((nb - 1))  # Flat start
                k = 0
                K = 5  # Max iterations
                tol = 100
                epsilon = 1 * 10 ** (-6)
                PP=np.array(Param.P_profiles[iSA][iT])
                QQ=np.array(Param.Q_profiles[iSA][iT])
                while (k <= K) & (tol >= epsilon):
                    V = run_pf_Laurent(Param.System_Data_Nodes,PP,QQ, Param.Sbase, Param.Yds, Param.Ydd, V_0)
                    tol = max(abs(abs(V) - abs(V_0)))
                    V_0 = V  # Voltage at load buses
                    k += 1
                ViSA.append(abs(V_0))
                Ss = np.conj(Param.Yss + Param.Ysd * V_0)  # Power at substation
            Vmg.append(ViSA)
    elif Param.PowerFlowMethod in ('bfsw',"fbs","nr",'fdxb','gs','dc'):
        import pandapower as pp
        Vmg = []
        for iSA in range(len(Param.Profile_actP)):
            ViSA=[]
            for iT in range(Param.nTime):
                Param.network.load.p_mw=np.array(Param.P_profiles[iSA][iT])/1000
                Param.network.load.q_mvar=np.array(Param.Q_profiles[iSA][iT])/1000

                pp.runpp(Param.network,algorithm=Param.PowerFlowMethod,init="flat")
                ViSA.append(np.array(Param.network.res_bus.vm_pu))
            Vmg.append(ViSA)
    elif Param.PowerFlowMethod=='Alliander':
        from power_grid_model import LoadGenType
        from power_grid_model import PowerGridModel, CalculationMethod, CalculationType
        from power_grid_model import initialize_array
        Vmg = []
        for iSA in range(len(Param.P_profiles)):
            load_profile = initialize_array("update", "sym_load", (Param.nTime, Param.nLoad))  
            load_profile["id"] = [Param.sysData["sym_load"]["id"]]

            load_profile["p_specified"] = np.multiply(Param.P_profiles[iSA],1000)
            load_profile["q_specified"] = np.multiply(Param.Q_profiles[iSA],1000)

            time_series_mutation = {"sym_load": load_profile}

            output_data = Param.network.calculate_power_flow(
                update_data=time_series_mutation,
                threading=0,
                symmetric=True,
                error_tolerance=1e-8,
                max_iterations=20,
                calculation_method=CalculationMethod.newton_raphson)

            Vmg.append(np.array([[output_data['node'][iT][ibus][2] for ibus in range(Param.nLoad)] for iT in range(Param.nTime)]))

    elif Param.PowerFlowMethod in ('tensor', 'hp' , 'sequential' ,'hp-tensor'):
        if len(Param.P_profiles)*Param.nTime>960000:
            claster=1000
            uotient, remainder = divmod(len(Param.P_profiles),claster)
            print(uotient, remainder)
            Vmg=[]
            for i in range(1,uotient+1):
                print(i)
                solutions = Param.network.run_pf(active_power=np.array(Param.P_profiles[-1+(i*claster-(claster-1)):i*claster-1]),
                        reactive_power=np.array(Param.Q_profiles[-1+(i*claster-(claster-1)):i*claster-1]),algorithm=Param.PowerFlowMethod)
                Vmg.append(abs(solutions["v"]))
            if remainder>0:
                print('last')
                solutions = Param.network.run_pf(active_power=np.array(Param.P_profiles[-1+(uotient*claster-(claster-1)):len(Param.P_profiles)]),
                        reactive_power=np.array(Param.Q_profiles[-1+(uotient*claster-(claster-1)):len(Param.P_profiles)]),algorithm=Param.PowerFlowMethod)
                Vmg.append(abs(solutions["v"]))
        else:
            solutions = Param.network.run_pf(active_power=np.array(Param.P_profiles),
                        reactive_power=np.array(Param.Q_profiles),algorithm=Param.PowerFlowMethod)
            Vmg=abs(solutions["v"])
    else:
        print('PowerFlowMethod is not defined')
        Vmg=0
    

    Param.Vmg=Vmg
    return Param

