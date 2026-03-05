import numpy as np
import traci
import random
import json

class EV:
    def __init__(self, id=None):
        # -----------------------------
        # Identificação do veículo
        # -----------------------------
        self.id = id              # ID único do veículo
        self.type = None          # Tipo do veículo ("electric" ou "electric bus")

        # -----------------------------
        # Estado energético
        # -----------------------------
        self.energy = 0.0         # Carga atual da bateria (KWh)
        self.energy_loaded = 0.0  # Energia total carregada ao longo do tempo (kWh)
        self.energy_regen = 0.0   # Energia total regenerada (kWh)
        self.capacity = 0.0       # Capacidade total da bateria (kWh)
        self.soc = 0.0            # Estado de carga (%)

        # -----------------------------
        # Localização e rota
        # -----------------------------
        self.edge = None          # Edge atual
        self.dest = None          # Destino intermediário atual
        self.final_dest = None    # Destino final da viagem

        # -----------------------------
        # Movimento
        # -----------------------------
        self.speed = 0.0                # Velocidade atual (m/s)
        self.consumption = 0.0          # Consumo elétrico instantâneo (KWh/s)
        self.speedKm = 0.0              # Velocidade atual (Km/h)

        # -----------------------------
        # Estado de parada (bitmask)
        # -----------------------------
        self.stop_state = 0       # Estado atual de parada (bitmask)

        # -----------------------------
        # Distâncias
        # -----------------------------
        self.dist_to_dest = np.inf    # Distância até o destino atual (m)
        self.dist_to_final = np.inf   # Distância até o destino final (m)
        self.total_dist = np.inf      # Distância total percorrida (m)


        # Carrega config
        with open('config/config.json', 'r') as config_file:
            self.configer = json.load(config_file)

        pass

    def identify(self, id):
        self.id = id
        self.type = traci.vehicle.getTypeID(self.id)
        return
    
    def update_energy(self):
        self.energy = round(float(traci.vehicle.getParameter(self.id, "device.battery.chargeLevel")) / 1000, 2)
        self.energy_loaded = round(float(traci.vehicle.getParameter(self.id, "device.battery.energyCharged")) / 1000, 2)
        self.energy_regen = round(float(traci.vehicle.getParameter(self.id, "device.battery.energyRegenerated")) / 1000, 2)
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
        self.final_dest = edges[-1]
    
    def update_motion(self):
        self.speed = round(traci.vehicle.getSpeed(self.id), 2)
        self.consumption = round(traci.vehicle.getElectricityConsumption(self.id) / 1000, 2)
        self.speedKm = round(self.speed * 3.6, 2)

    def stop(self):
        state = int(traci.vehicle.getStopState(self.id))
        self.stop_state = state

        estados = []

        if state & 1:
            estados.append("parado")
        if state & 2:
            estados.append("estacionando")
        if state & 4:
            estados.append("acionado")
        if state & 8:
            estados.append("container acionado")
        if state & 16:
            estados.append("ponto de ônibus")
        if state & 32:
            estados.append("ponto de contêiner")
        if state & 64:
            estados.append("estação de carregamento")
        if state & 128:
            estados.append("estacionamento")

        return estados if estados else ["em movimento"]

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
    
    def recharge_substation(self,destin): # vetor = [edge da estação, id da estação]
        traci.vehicle.changeTarget(self.id, destin[0])
        traci.vehicle.setChargingStationStop(self.id, destin[1], duration=300,flags=1) 
        self.update_route() 
        return 
    
    def stopParking(self,destin): # vetor = [id do estacionamento, id do estacionamento]
        traci.vehicle.changeTarget(self.id, destin[0])
        traci.vehicle.setParkingAreaStop(self.id, destin[1], duration=300)
        self.update_route()
        return
    
    def returnfinaldestin(self):
        traci.vehicle.changeTarget(self.id, self.final_dest)
        self.update_route()
        return

    def newroute(self,destin): #vetor = [id do destino,id da rota]
        route = traci.simulation.findRoute(self.edge, destin[0], vType=self.type)
        traci.route.add(destin[1], route.edges)
        traci.vehicle.setRouteID(self.id, destin[1])
        self.update_route()
        self.update_finalroute()
        return 
    
    def step(self,action,destin) :
        if action == "Seguir" :
            self.update_route()
            return
        
        elif action == "Carregar":
            self.recharge_substation(destin)
            return
        
        elif action == "Estacionar":
            self.stopParking(destin)
            return
        
        elif action == "Voltar ao destino final": 
            self.returnfinaldestin()
            return
        
        elif action == "Achar novo destino":
            self.newroute(destin)
            return

