from evse import EVSE
from ev import EV
from parking import PARKING
from sumo import Sumo
import traci
import json
import random
from datetime import datetime, timedelta

"""Load config at config/config.json"""
with open(r'config/config.json', 'r') as config_file:
    config = json.load(config_file)

with open('config/vehicles.json', "r", encoding="utf-8") as f:
    vehicles = json.load(f)

def main():

    simulation = Sumo(config,vehicles)   # cria objeto da classe Sumo
    chargers = EVSE("Charge_ParkD")  # cria objeto da classe EVSE
    park = PARKING("ParkAreaC")
    evs = []
    comprimento = simulation.refdist

    for id in vehicles:
        ev = EV(id, vehicles[id]["type"], ['E103',"ROTA DA POLICIA",'E165'],comprimento)
        evs.append(ev)
    
    simulation.setup_results_and_headers()
    
    while traci.simulation.getTime() < simulation.max_time:
        ev.up.general_up()
        ev.step([1,0,0,0,0,0,0,0],[])

        if ev.edge == ev.penultimate_dest : 
            w= random.choice([x for x in simulation.streets if x != ev.final_dest])
            ev.step([0,0,1,0,0,0,0,0],[w])
            ev.up.all_up()
        
        
        traci.simulationStep()


if __name__ == "__main__":
    main()