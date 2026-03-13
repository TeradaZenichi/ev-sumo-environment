import numpy as np
import traci
from pathlib import Path
import csv

class EV:
    def __init__(self, id:str,type:str,dest:str):
        # -----------------------------
        # Vehicle identification
        # -----------------------------
        self.id = id                                                                # Unique vehicle ID
        self.type = type                                                            # Vehicle type

        # -----------------------------
        # Add the vehicle
        # -----------------------------
        self._addveh(dest)

        # -----------------------------
        # Energy state
        # -----------------------------
        self.energy = 0.0                                                           # Current battery charge (kWh)
        self.energy_loaded = 0.0                                                    # Total energy charged over time (kWh)
        self.energy_regen = 0.0                                                     # Total regenerated energy (kWh)
        self.capacity = 0.0                                                         # Total battery capacity (kWh)
        self.soc = 0.0                                                              # State of charge (%)

        # -----------------------------
        # Location and route
        # -----------------------------
        self.edge = None                                                            # Current edge
        self.dest = None                                                            # Current intermediate destination
        self.final_dest = None                                                      # Final trip destination
        self.penultimate_dest = None                                                # penultimate final trip destination

        # -----------------------------
        # Motion
        # -----------------------------
        self.speed = 0.0                                                            # Current speed (m/s)
        self.consumption = 0.0                                                      # Instantaneous electric consumption (kWh/s)
        self.speedKm = 0.0                                                          # Current speed (km/h)

        # -----------------------------
        # Stop state (bitmask)
        # -----------------------------
        self.stop_state = 0                                                         # Current stop state (bitmask)

        # -----------------------------
        # Distances
        # -----------------------------
        self.dist_to_dest  = np.inf                                                 # Distance to current destination (m)
        self.dist_to_final = np.inf                                                 # Distance to final destination (m)
        self.total_dist    = np.inf                                                 # Total distance traveled (m)


        # -----------------------------
        # Initial initialization
        # -----------------------------  
        self.update_energy()
        self.update_route()
        self.update_finalroute()
        self.update_motion()
        self.update_distances()
        pass

    def _addveh(self,dest):                                                         # dest vector = [destination_edge, route_id]

        self.create_route(dest)

        traci.vehicle.add(
                vehID=self.id,
                routeID=dest[1],
                typeID=self.type,
                depart=traci.simulation.getTime()
            )

        return

    def update_energy(self):
        self.energy = round(float(traci.vehicle.getParameter(self.id, "device.battery.chargeLevel")) / 1000, 2)
        self.energy_loaded = round(float(traci.vehicle.getParameter(self.id, "device.battery.energyCharged")) / 1000, 2)
        #self.energy_regen = round(float(traci.vehicle.getParameter(self.id, "device.battery.energyRegenerated")) / 1000, 2)
        self.capacity = round(float(traci.vehicle.getParameter(self.id, "device.battery.capacity")) / 1000, 2)
        self.soc = round(100 * self.energy / self.capacity, 2) 

    def update_route(self):
        route_id = traci.vehicle.getRouteID(self.id)
        edges = traci.route.getEdges(route_id)
        self.edge = traci.vehicle.getRoadID(self.id)
        self.dest = edges[-1]

    def update_finalroute(self):
        route_id = traci.vehicle.getRouteID(self.id)
        edges = traci.route.getEdges(route_id)
        if len(edges) >=2 :
            self.final_dest = edges[-1]
            self.penultimate_dest = edges[-2]
        else :
            self.final_dest = edges[-1]
            self.penultimate_dest = self.final_dest           
    
    def update_motion(self):
        self.speed = round(traci.vehicle.getSpeed(self.id), 2)
        self.consumption = round(traci.vehicle.getElectricityConsumption(self.id) / 1000, 2)
        self.speedKm = round(self.speed * 3.6, 2)

    def stop(self):
        state = int(traci.vehicle.getStopState(self.id))
        self.stop_state = state

        states = []

        if state & 1:
            states.append("stopped")
        if state & 2:
            states.append("parking")
        if state & 4:
            states.append("triggered")
        if state & 8:
            states.append("container triggered")
        if state & 16:
            states.append("bus stop")
        if state & 32:
            states.append("container stop")
        if state & 64:
            states.append("charging station")
        if state & 128:
            states.append("parking area")

        return states if states else ["moving"]

    def update_distances(self):
        self.dist_to_dest = round(
            traci.vehicle.getDrivingDistance(
                self.id,
                self.dest,
                traci.lane.getLength(f"{self.dest}_0")
            ),
            2
        )

        self.dist_to_final = round(
            traci.vehicle.getDrivingDistance(
                self.id,
                self.final_dest,
                traci.lane.getLength(f"{self.final_dest}_0")
            ),
            2
        )

        self.total_dist = round(traci.vehicle.getDistance(self.id), 2)
        return
    
    def color(self):     
        if self.soc <= 10:
            color = (139, 0, 0, 255)        # Vermelho Escuro (Crítico extremo)
        elif self.soc <= 20:
            color = (255, 0, 0, 255)        # Vermelho
        elif self.soc <= 30:
            color = (255, 69, 0, 255)       # Laranja avermelhado
        elif self.soc <= 40:
            color = (255, 140, 0, 255)      # Laranja escuro
        elif self.soc <= 50:
            color = (255, 165, 0, 255)      # Laranja
        elif self.soc <= 60:
            color = (255, 215, 0, 255)      # Amarelo dourado
        elif self.soc <= 70:
            color = (255, 255, 0, 255)      # Amarelo
        elif self.soc <= 80:
            color = (173, 255, 47, 255)     # Verde amarelado
        elif self.soc <= 90:
            color = (127, 255, 0, 255)      # Verde claro
        else:
            color = (0, 255, 0, 255)        # Verde (bateria cheia)
        
        traci.vehicle.setColor(self.id, color)
        
    def recharge_substation(self,dest):                                              # dest vector = [station edge, station id]
        traci.vehicle.changeTarget(self.id, dest[0])
        traci.vehicle.setChargingStationStop(self.id, dest[1], duration=300,flags=1)
        self.update_route() 
        return 
    
    def stopParking(self,dest):                                                      # dest vector = [parking edge, parking_id]
        traci.vehicle.changeTarget(self.id, dest[0])
        traci.vehicle.setParkingAreaStop(self.id, dest[1], duration=300)
        self.update_route()
        return
    
    def skip_stop(self):
        traci.vehicle.resume(self.id)
        return
    
    def returnfinaldest(self):                                             
        traci.vehicle.changeTarget(self.id, self.final_dest)
        self.update_finalroute()
        return

    def newroute(self,dest):                                                         # destination vector = [destination id]
        
        current_route = traci.vehicle.getRoute(self.id)

        route = traci.simulation.findRoute(self.final_dest, dest[0], vType=self.type)
        
        if self.penultimate_dest != self.final_dest:
            new_route = [current_route[-2]] + [current_route[-1]] + list(route.edges)[1:]
        else : 
            new_route = [current_route[-1]] + list(route.edges)[1:]

        traci.vehicle.setRoute(self.id, new_route)

        self.update_route()
        self.update_finalroute()
        return 
    
    def newroute_finaldest(self,dest): # destination vector = [destination id]. 
        '''Use this function when you want to create a new route for a long streets and the final street is the conditional.'''
        route = traci.simulation.findRoute(self.edge, dest[0], vType=self.type)

        if route.edges:
            traci.vehicle.setRoute(self.id, route.edges)

        self.update_route()
        self.update_finalroute()
        return

    def newdestin(self,dest):                                                       # destination vector = [destination id]                                          
        traci.vehicle.changeTarget(self.id, dest[0])
        self.update_route()
        self.update_finalroute()
        return 


    def create_route(self,dest):                                                     # destination vector = [destination id, route id,edge initial]
        route = traci.simulation.findRoute(dest[2], dest[0], vType=self.type)
        traci.route.add(dest[1], route.edges)
        return 
    

    
    def step(self, action, dest):
        if self.id in traci.vehicle.getIDList():
            self.update_route()
            self.color()
        else:
            return
        
        if action == "Continue":
            return
        
        elif action == "Recharge":
            self.recharge_substation(dest)
            return
        
        elif action == "Park":
            self.stopParking(dest)
            return
        
        elif action == "Return to final destination":
            self.returnfinaldest()
            return
        
        elif action == "Skip stop":
            self.skip_stop()
            return
        
        elif action == "Find new destination":
            self.newdestin(dest)
            return
        
        elif action == "Find new route":
            self.newroute(dest)
            return
        elif action == "Find new route from the final edge":
            self.newroute_finaldest(dest)
            return
    
    def register(self,TIME):

        self.update_route()
        self.update_energy()
        self.update_motion()
        self.update_distances()

        base_dir = Path(__file__).resolve().parent.parent  # volta para a raiz do projeto
        pasta_results = base_dir / "sumo" / "results"
        pasta_results.mkdir(parents=True, exist_ok=True)  # garante que a pasta existe
        arquivo_csv = pasta_results / f"{self.id}.csv"

        with open(arquivo_csv, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                self.id,
                self.speedKm,
                self.edge,
                self.total_dist,
                self.dest,
                self.dist_to_dest,
                self.type,
                self.soc,
                TIME       
            ])
