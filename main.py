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
    chargers = EVSE()  # cria objeto da classe EVSE
    park = PARKING()
    evs = []

    for id in vehicles:
        ev = EV(id, vehicles[id]["type"], ['E103',"ROTA DA POLICIA",'E165'])
        evs.append(ev)
    
    simulation.setup_results_and_headers()
    
    chargers.update()
    W = random.choice(chargers.ids)
    chargers.get_station_edge(W)


    park.update()
    L = random.choice(park.ids)
    park.get_parking_edge(L)

    edges = traci.edge.getIDList()

    ruas = set()

    for edge in edges:
        if not edge.startswith(":"):  # ignora edges internas
            ruas.add(edge.split("_")[0])

    while traci.simulation.getTime() < simulation.max_time:
        ev.step("Continue",[])
        ev.register(traci.simulation.getTime())

        if ev.soc <50 and not("charging station" in ev.stop()):
            ev.step("Recharge", [chargers.edge,W])

        if ev.soc == 80 : 
            ev.step("Park", [park.edge,L])
        
        if "parking" in ev.stop() or "charging station" in ev.stop():
            ev.step("Return to final destination", [])

        if config["destin flag"] == "True":
            if ev.penultimate_dest == ev.edge:
                w= random.choice([x for x in ruas if x != ev.final_dest])
                ev.step("Find new route", [w])
        else : 
            if ev.final_dest == ev.edge:  
                w= random.choice([x for x in ruas if x != ev.final_dest])
                ev.step("Find new route from the final edge", [w])

        traci.simulationStep()

if __name__ == "__main__":
    main()