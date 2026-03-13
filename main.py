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

    Key = 0
    for id in vehicles:
        ev = EV(id, vehicles[id]["type"], ['E103',"ROTA DA POLICIA",'E165'])
        evs.append(ev)
    
    simulation.setup_results_and_headers()
    
    edges = traci.edge.getIDList()

    ruas = set()

    for edge in edges:
        if not edge.startswith(":"):  # ignora edges internas
            ruas.add(edge.split("_")[0])

    while traci.simulation.getTime() < simulation.max_time:
        ev.step("Continue",[])
        ev.register(traci.simulation.getTime())

        if ev.soc <50 and not("charging station" in ev.stop()):
            ev.step("Recharge", [chargers.edge,chargers.id])

        if ev.soc == 80 :
            ev.step("Park", [park.edge,park.id])

        if "parking" in ev.stop() or "charging station" in ev.stop():
            ev.step("Return to final destination", [])

            if "parking" in ev.stop() and "charging station" not in ev.stop() :
                Key +=1
                print(Key)
                if Key == 10 :
                    ev.step("Skip stop",[]) 

            
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