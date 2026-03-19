from datetime import datetime, timedelta
from parking import PARKING
import gymnasium as gym
from sumo import Sumo
from evse import EVSE
import numpy as np
from ev import EV
import random
import traci



class SingleEV(gym.Env):
    def __init__(self, config, vehicle, start):
        super().__init__()
        self.simulation = Sumo(config, vehicle)   # cria objeto da classe Sumo

        # esse caso vai ser só um EV e colocar as rotas iniciais e finais da primeira parte no json
        car = vehicle[list(vehicle.keys())[0]]
        car = EV(list(vehicle.keys())[0], car["type"], [car["initial_edge"],car["routeid"], car["final_edge"]])
        self.done = False
        
    
    def step(self, action):
        reward = 0
        
        # step do ev
        traci.simulationStep()

        # mexer na rota se for necessário
        self.ev.step()


        # atualizar o 
        if traci.simulation.getTime() == self.simulation.max_time:
            self.done = True

        return # state, reward, terminated, truncated, info

    def get_obs(self):
        obs = []
        # observaçõe do ambiente (horário etc)

        # observações do EV
        pass


    def reset(self):
        # termo aleatório de inicialização

        pass

    def close(self):

        pass