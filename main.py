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
    contador = 0

    for id in vehicles:
        ev = EV(id, vehicles[id]["type"], ['E103',"ROTA DA POLICIA",'E165'])
        evs.append(ev)
    
    simulation.setup_results_and_headers()
    
    chargers.update()
    W = random.choice(chargers.ids)
    chargers.get_edge(W)

    edges = traci.edge.getIDList()

    ruas = set()

    for edge in edges:
        if not edge.startswith(":"):  # ignora edges internas
            ruas.add(edge.split("_")[0])

    while traci.simulation.getTime() < simulation.max_time:

        # if not ev.edge.startswith(":"):
        #         rua = ev.edge.split("_")[0]
        ev.step("Continue",[])
        ev.register(traci.simulation.getTime())

        if ev.soc < 20 and not(ev.going_to_charge):
            ev.step("Recharge", [chargers.edge,w])
        elif ev.penultimate_dest == ev.edge:
            contador+=1
            w= random.choice([x for x in ruas if x != ev.final_dest])
            route_id = f"route_{ev.id}_{contador}"
            ev.step("Find new route", [w,route_id])


        traci.simulationStep()

if __name__ == "__main__":
    main()