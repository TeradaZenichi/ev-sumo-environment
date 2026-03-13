import traci

class EVSE:
    def __init__(self,id:str):
        # -----------------------------
        # Station identification
        # -----------------------------
        self.id = id            # List of charging station IDs
        
        # =========================================================
        # Localização na rede
        # =========================================================
        self.lane = traci.chargingstation.getLaneID(self.id)                # Lane onde a estação está localizada
        self.edge = traci.lane.getEdgeID(self.lane)                         # Edge correspondente
        self.startPos = traci.chargingstation.getStartPos(self.id)          # Início da estação na lane (metros)
        self.endPos =traci.chargingstation.getEndPos(self.id)               # Fim da estação na lane (metros)
        
        
        # -----------------------------
        # Vehicles charging
        # -----------------------------
        self.veh = []            # IDs of vehicles currently charging
        self.veh_count = 0       # Number of vehicles stopped at the station

        # -----------------------------
        # Power and efficiency
        # -----------------------------
        self.power = 0.0         # Current charging power (W)
        self.eff = 0.0           # Station efficiency (%)

        # =========================================================
        # Parâmetros operacionais
        # =========================================================
        self.delay = 0.0            # Delay antes do carregamento iniciar
        self.transit = 0            # 0 = not allowed, 1 = allows charging while moving
        


        pass
    
    def status(self):
        # Vehicles connected to the station
        self.veh = traci.chargingstation.getVehicleIDs(self.id)
        self.veh_count = traci.chargingstation.getVehicleCount(self.id)

        # Charging power
        self.power = traci.chargingstation.getChargingPower(self.id)

        # Station efficiency
        self.eff = traci.chargingstation.getEfficiency(self.id)
        
        # Delay para iniciar o carregamento
        self.delay = traci.chargingstation.getChargeDelay(self.id)

        # Charging while moving
        self.transit = traci.chargingstation.getChargeInTransit(self.id)
        return
