from evse import EVSE
from ev import EV
from parking import PARKING
from sumo import Sumo
import traci
import json



"""Load config at config/config.json"""
with open(r'config/config.json', 'r') as config_file:
    config = json.load(config_file)

with open('config/vehicles.json', "r", encoding="utf-8") as f:
    vehicles = json.load(f)


def main():

    simulation = Sumo(config)   # cria objeto da classe Sumo
    chargers = EVSE()  # cria objeto da classe EVSE
    evs = []
    for id in vehicles:
        ev = EV(id, vehicles[id]["type"], ['E103',"ROTA DA POLICIA",'E165'])
        evs.append(ev)
    
    

    #simulation.setup_results_and_headers()
    
    while traci.simulation.getTime() != simulation.max_time:
 
        traci.simulationStep()





if __name__ == "__main__":
    main()






'''

    def recharge_substation(self,temp):

        charging_stations = traci.chargingstation.getIDList()
        
        station_id = random.choice(charging_stations)
        lane_id = traci.chargingstation.getLaneID(station_id)
        edge_id = lane_id.split("_")[0]

        traci.vehicle.changeTarget(self.id, edge_id)
        traci.vehicle.setChargingStationStop(self.id, station_id, duration=temp,flags=1)  
        return 
    
    def stopParking(self,temp):

        all_parkings = traci.parkingarea.getIDList()

        parkingID = random.choice(all_parkings)
        lane_id = traci.parkingarea.getLaneID(parkingID)
        edge_id = lane_id.split("_")[0]

        traci.vehicle.changeTarget(self.id, edge_id)
        traci.vehicle.setParkingAreaStop(self.id, parkingID, duration=temp)

        return
    
      
    def newroute(self):

        edges = []
        route_id = f"route_{self.id}"

        # Achar edges válidas
        for edge in traci.edge.getIDList():
            if edge.startswith(":"):  # ignore internal edges
                continue
            if traci.edge.getLaneNumber(edge) == 0:
                continue

            for i in range(traci.edge.getLaneNumber(edge)):
                lane_id = f"{edge}_{i}"
                allowed = traci.lane.getAllowed(lane_id)

                if not allowed:
                    if self.type not in self.configer["RESTRICTED_TYPES"]:
                        edges.append(edge)
                        break
                else:
                    if self.type in allowed:
                        edges.append(edge)
                        break

        for travel in range(10):

            to_edge = random.choice(edges)

            while to_edge == self.edge:
                to_edge = random.choice(edges)

            route = traci.simulation.findRoute(self.edge, to_edge, vType=self.type)

            if not route.edges:
                continue

            # Adiciona rota se ainda não existir
            if route_id not in traci.route.getIDList():
                traci.route.add(route_id, route.edges)

            
            traci.vehicle.setRouteID(self.id, route_id)

            return 

        return 

'''