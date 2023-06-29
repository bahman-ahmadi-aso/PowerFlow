
"""
@author: Bahman Ahmadi -- b.ahmadi@utwente.nl


note: you need the following libraries to run the code
using Alliander power flow methods >> power_grid_model
Other power flow methods >> pandapower
"""
#########################
import sys,os,time,numpy as np,pandas as pd
sys.path.append(os.path.join(os.getcwd(),"data"))
sys.path.append(os.path.join(os.getcwd(),"PowerSystem"))
Directory_name=os.getcwd()
from PowerSystem.Parameters import Parameters 
from PowerSystem.PowerFlowCalculation import PowerFlowCalculation as PFC
import data.ReadData as RD
Param=Parameters()


Config_scenario=['config1','config2']

for sc in Config_scenario:
	##chose the power flow method
	Param.PowerFlowMethod='Laurent' # 'Alliander',   'Laurent' ,       "bfsw","nr",'fdxb','gs','dc'
	
	Param.Directory_name=Directory_name
	##chose the grid
	Param.TestSystem='Nodes_33_'+sc
	Param.TestSystemLines='Lines_33_'+sc
	## add the base power and voltage of the system
	if Param.TestSystem=='Nodes_33_'+sc:
		Param.Sbase = 1000  # kVA
		Param.Vbase = 12.66  # kV
	elif Param.TestSystem=='Nodes_34':
		Param.Sbase = 1000  # kVA
		Param.Vbase = 12.66  # kV
	elif Param.TestSystem=='Nodes_150':
		Param.Sbase = 400  # kVA
		Param.Vbase = 20  # kV  maybe 20 kV
	elif Param.TestSystem=='Nodes_141':
		Param.Sbase = 10000  # kVA
		Param.Vbase = 12.5  # kV  maybe 20 kV
	else:
		print('Test system (S_base and V_base) is not defined!')

	## creating a network based on the power flow method
	if Param.PowerFlowMethod=='Laurent':
		Param.profile_info=1
		from PowerSystem.create_net_data import makeYbus_laurent
		System_Data_Nodes = pd.read_csv(os.path.join(Directory_name,'data/grid_data/'+Param.TestSystem+'.csv'))
		Param.System_Data_Nodes=System_Data_Nodes
		System_Data_Lines = pd.read_csv(os.path.join(Directory_name,'data/grid_data/'+Param.TestSystemLines+'.csv'))
		Yss, Ysd, Yds, Ydd = makeYbus_laurent(System_Data_Lines, System_Data_Nodes, Param.Sbase, Param.Vbase)  # Calculates the Ybus submatrices
		Param.Yss=Yss
		Param.Ysd=Ysd
		Param.Yds=Yds
		Param.Ydd=Ydd
	elif Param.PowerFlowMethod in ("bfsw","nr",'fdxb','gs','dc'):  #'nr' for Newton-Raphson, 'fdxb' for Fast Decoupled with BX bus splitting, 'gs' for Gauss-Seidel, 'dc' for DC power flow, and 'fbs' for Backward/Forward Sweep
		import pandapower as pp
		from PowerSystem.create_net_data import create_pandapower_net
		Param.profile_info=0
		System_Data_Nodes = pd.read_csv(os.path.join(Directory_name,'data/grid_data/'+Param.TestSystem+'.csv'))
		System_Data_Lines = pd.read_csv(os.path.join(Directory_name,'data/grid_data/'+Param.TestSystemLines+'.csv'))
		Param.network=create_pandapower_net(System_Data_Lines, System_Data_Nodes,Param.Vbase)	
	elif Param.PowerFlowMethod=='Alliander':
		Param.profile_info=0
		from PowerSystem.create_net_data import create_Alliander_net
		System_Data_Nodes = pd.read_csv(os.path.join(Directory_name,'data/grid_data/'+Param.TestSystem+'.csv'))
		System_Data_Lines = pd.read_csv(os.path.join(Directory_name,'data/grid_data/'+Param.TestSystemLines+'.csv'))
		Param.network,Param.sysData=create_Alliander_net(System_Data_Lines, System_Data_Nodes,Param.Vbase)	
	else:
		print('The power flow method is not defined!')
		print('Choose one of the following methods: "Laurent", "Alliander", "tensor", "hp" , "sequential" , "hp-tensor", "bfsw","nr","fdxb","gs","dc"')

	###############################
	#preparing data series for the power flow
	Param.TimeSeriesScenario=['sc1','sc2']
	for iTimeSeries in Param.TimeSeriesScenario:
		#based on scaled load curves choose the number of time steps or modify ReadData.py in Data folder to read the load curves
		Param.day=range(1)#,362)    #the length of the time series for each scenario is 96 time series data per day(scenario)# change it based on your scenario
		Param=RD.read_act_react_DATA(Param,iTimeSeries)  #read the time series data
		Param.P_profiles.append(Param.P_profile)
		Param.Q_profiles.append(Param.Q_profile)
	###############################


	###############################
	folder_name=os.path.join( 'Results',Param.TestSystem+'_'+Param.PowerFlowMethod )
	try:
		os.mkdir(os.path.join(Directory_name,folder_name))
	except:
		pass


	## calculating the power flow(s)
	tic = time.time()
	Param = PFC(Param)
	toc=time.time()-tic
	print('Elapsed time for the power flow: ',toc)

	## saving the results
	for i in range(len(Param.Vmg)):
		np.savetxt(os.path.join(Directory_name,folder_name,"Vmg"+str(i)+".csv"), Param.Vmg[i], delimiter=",")
	import Save_data as SD
	SD.Save_voltages_npy(os.path.join(Directory_name,folder_name),Param)

	## reseting the parameters
	Param=Parameters()

checkpoint=1
