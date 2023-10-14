
import spotpy
from cali_class import spot_setup



spot_setup = spot_setup()


sampler = spotpy.algorithms.mc(spot_setup, dbname='SCEUA_hymod', dbformat='csv', parallel='mpi')

#Select number of maximum repetitions
sampler.sample(20000)

results = spotpy.analyser.load_csv_results('SCEUA_hymod')

import matplotlib.pyplot as plt
fig= plt.figure(1,figsize=(9,5))
plt.plot(results['like1'])
plt.show()
plt.ylabel('RMSE')
plt.xlabel('Iteration')
fig.savefig('SCEUA_objectivefunctiontrace.png',dpi=300)



bestindex,bestobjf = spotpy.analyser.get_minlikeindex(results)

best_model_run = results[bestindex]

fields=[word for word in best_model_run.dtype.names if word.startswith('sim')]
best_simulation = list(best_model_run[fields])

fig= plt.figure(figsize=(16,9))
ax = plt.subplot(1,1,1)
ax.plot(best_simulation,color='black',linestyle='solid', label='Best objf.='+str(bestobjf))
ax.plot(spot_setup.evaluation(),'r.',markersize=3, label='Observation data')
plt.xlabel('Number of Observation Points')
plt.ylabel ('Discharge [l s-1]')
plt.legend(loc='upper right')
fig.savefig('SCEUA_best_modelrun.png',dpi=300)
#c=1
