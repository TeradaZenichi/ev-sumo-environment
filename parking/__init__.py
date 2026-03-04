import traci

class PARKING:
    def __init__(self):
        # -----------------------------
        # Identificação dos parkings
        # -----------------------------
        self.ids = []            # IDs das áreas de estacionamento
        self.count = 0           # Número total de parkings

        # -----------------------------
        # Veículos no estacionamento
        # -----------------------------
        self.veh = []            # IDs dos veículos estacionados
        self.veh_count = 0       # Número de veículos no parking

        pass

    def update(self):
        # Lista de estacionamentos disponíveis
        self.ids = traci.parkingarea.getIDList()
        self.count = len(self.ids)
        return

    def status(self, parkingId):
        # Veículos estacionados na área
        self.veh = traci.parkingarea.getVehicleIDs(parkingId)

        # Número total de veículos no estacionamento
        self.veh_count = traci.parkingarea.getVehicleCount(parkingId)
        return