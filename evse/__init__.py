import traci

class EVSE:
    def __init__(self):
        # -----------------------------
        # Identificação das estações
        # -----------------------------
        self.ids = []               # Lista de IDs das estações de carregamento
        self.count = 0              # Número total de estações

        # -----------------------------
        # Veículos em carregamento
        # -----------------------------
        self.veh = []               # IDs dos veículos atualmente carregando
        self.veh_count = 0       # Número de veículos parados na estação

        # -----------------------------
        # Potência e eficiência
        # -----------------------------
        self.power = 0.0            # Potência atual de carregamento (W)
        self.eff = 0.0              # Eficiência da estação (%)

        # -----------------------------
        # Estado de carregamento
        self.transit = 0  # 0 = não permite, 1 = permite carregar em movimento

        pass

    def update(self):
        # Lista de estações disponíveis
        self.ids = traci.chargingstation.getIDList()
        self.count = len(self.ids)
        return
    
    def status(self, stationId):
        # Veículos conectados à estação
        self.veh = traci.chargingstation.getVehicleIDs(stationId)
        self.veh_count = traci.chargingstation.getVehicleCount(stationId)

        # Potência de carregamento
        self.power = traci.chargingstation.getChargingPower(stationId)

        # Eficiência da estação
        self.eff = traci.chargingstation.getEfficiency(stationId)

        self.transit = traci.chargingstation.getChargeInTransit(stationId)
        return
    


    