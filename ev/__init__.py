import numpy as np
import traci

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
        self.charge = 0.0         # Carga atual da bateria (Wh)
        self.energy_loaded = 0.0  # Energia total carregada ao longo do tempo (Wh)
        self.energy_regen = 0.0   # Energia total regenerada (Wh)
        self.capacity = 0.0       # Capacidade total da bateria (Wh)
        self.energy_level = 0.0   # Estado de carga (%)

        # -----------------------------
        # Localização e rota
        # -----------------------------
        self.edge = None          # Edge atual
        self.dest = None          # Destino intermediário atual
        self.final_dest = None    # Destino final da viagem

        # -----------------------------
        # Movimento
        # -----------------------------
        self.speed = 0.0          # Velocidade atual (m/s)
        self.power = 0.0          # Consumo elétrico instantâneo (Wh/s)

        # -----------------------------
        # Estado de parada (bitmask)
        # -----------------------------
        # 1   = parado
        # 2   = estacionando
        # 4   = acionado
        # 8   = contêiner acionado
        # 16  = no ponto de ônibus
        # 32  = no ponto de contêiner
        # 64  = na estação de carregamento
        # 128 = na área de estacionamento
        self.stop_state = 0       # Estado atual de parada (bitmask)

        # -----------------------------
        # Distâncias
        # -----------------------------
        self.dist_to_dest = np.inf    # Distância até o destino atual (m)
        self.dist_to_final = np.inf   # Distância até o destino final (m)
        self.total_dist = np.inf      # Distância total percorrida (m)
        pass

    def identify(self, id):
        self.id = id
        self.type = traci.vehicle.getTypeID(self.id)
        return
    
    def update_energy(self):
        self.charge = float(traci.vehicle.getParameter(self.id, "device.battery.chargeLevel"))
        self.energy_loaded = float(traci.vehicle.getParameter(self.id, "device.battery.energyCharged"))
        self.energy_regen = float(traci.vehicle.getParameter(self.id, "device.battery.energyRegenerated"))
        self.capacity = float(traci.vehicle.getParameter(self.id, "device.battery.capacity"))
        self.energy_level = 100 * self.charge / self.capacity

    def update_route(self, final_dest):
        route_id = traci.vehicle.getRouteID(self.id)
        edges = traci.route.getEdges(route_id)

        self.edge = traci.vehicle.getRoadID(self.id)
        self.dest = edges[-1]
        self.final_dest = final_dest
    
    def update_motion(self):
        self.speed = traci.vehicle.getSpeed(self.id)
        self.power = traci.vehicle.getElectricityConsumption(self.id)
    
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
        self.dist_to_dest = traci.vehicle.getDrivingDistance(
            self.id,
            self.dest,
            traci.lane.getLength(f"{self.dest}_0")
        )

        self.dist_to_final = traci.vehicle.getDrivingDistance(
            self.id,
            self.final_dest,
            traci.lane.getLength(f"{self.final_dest}_0")
        )

        self.total_dist = traci.vehicle.getDistance(self.id)
        return