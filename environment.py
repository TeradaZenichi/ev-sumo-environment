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
    def __init__(self, config, vehicles, start):
        super().__init__()
        self.simulation = Sumo(config,vehicles)   # cria objeto da classe Sumo
        self.chargers = EVSE("Charge_ParkD")  # cria objeto da classe EVSE
        self.park = PARKING("ParkAreaC")

    
    def step(self, action):
        # step do ev


        # mexer na rota se for necessário


        # atualizar o 
        pass


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