
from spotpy.parameter import Uniform
from spotpy.objectivefunctions import rmse
from spotpy.examples.hymod_python.hymod import hymod
import numpy as np
from califun import califun
import os
import random


class spot_setup(object):
    #K_layer1,K_layer2,K_layer3,porosity1,porosity2,porosity3,coeff1,coeff2,coeff3

    K_layer1 = Uniform(low=-0.5923 , high=-0.1432)
    K_layer2 = Uniform(low=1.581 , high=1.878)
    K_layer3 = Uniform(low=0.8965 , high=1.288)
    porosity1 = Uniform(low=0.336 , high=0.3955)
    porosity2 = Uniform(low=0.2354 , high=0.2676)
    porosity3 = Uniform(low=0.0883 , high=0.12463)
    
    rate = Uniform(low=-3.367 , high=-2.959)
    ani = Uniform(low=0.852 , high=1.101)
    ani2 = Uniform(low=0.02097 , high=0.1976)
    #FID = random.randint(0, 10000000000)
    #fake1 =spotpy.parameter.Uniform(low=0.1 , high=10, optguess=0.5592)
    #fake2 =spotpy.parameter.Uniform(low=0.1 , high=10, optguess=0.5592)

    def __init__(self, obj_func=None):
        #Just a way to keep this example flexible and applicable to various examples
        self.obj_func = obj_func
        #Transform [mm/day] into [l s-1], where 1.783 is the catchment area
        self.Factor = 1.783 * 1000 * 1000 / (60 * 60 * 24)
        #Load Observation data from file
        self.PET,self.Precip   = [], []
        self.date,self.trueObs = [], []
        #Find Path to Hymod on users system
        self.owd = os.path.dirname(os.path.realpath(__file__))
        Streamflow = np.loadtxt("./TLnewtest2sfb2/TLstreamflow_11_15.txt")
        self.trueObs = Streamflow/15.55
        self.weight = np.zeros(Streamflow[:365].shape) + 1
        self.weight[Streamflow[:365]>1] = 1.0
        self.index = ~np.isnan(Streamflow[:365])



    def simulation(self,x):
        #Here the model is actualy startet with one paramter combination
        #data = hymod(self.Precip, self.PET, x[0], x[1], x[2], x[3], x[4])

        sim = califun(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8])
        sim = sim
        #The first year of simulation data is ignored (warm-up)
        return sim[:365]

    def evaluation(self):
        return self.trueObs[:365]

    def objectivefunction(self,simulation,evaluation, params=None):
        #SPOTPY expects to get one or multiple values back,
        #that define the performance of the model run
        if not self.obj_func:
            # This is used if not overwritten by user
            like = np.sqrt(np.mean((((simulation[self.index])-(evaluation[self.index]))*self.weight[self.index])**2))
            #like = np.mean((simulation-evaluation)**2)/np.mean((evaluation-np.mean(evaluation))**2)
        else:
            #Way to ensure flexible spot setup class
            like = self.obj_func(evaluation,simulation)
        return like
