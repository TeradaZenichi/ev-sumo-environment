import traci

class EVSE:
    def __init__(self):
        # -----------------------------
        # Station identification
        # -----------------------------
        self.ids = []            # List of charging station IDs
        self.count = 0           # Total number of stations

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

        # -----------------------------
        # Charging state
        # -----------------------------
        self.transit = 0         # 0 = not allowed, 1 = allows charging while moving
        self.lane = None
        self.edge = None

        pass

    def update(self):
        # List of available stations
        self.ids = traci.chargingstation.getIDList()
        self.count = len(self.ids)
        return
    
    def status(self, stationId):
        # Vehicles connected to the station
        self.veh = traci.chargingstation.getVehicleIDs(stationId)
        self.veh_count = traci.chargingstation.getVehicleCount(stationId)

        # Charging power
        self.power = traci.chargingstation.getChargingPower(stationId)

        # Station efficiency
        self.eff = traci.chargingstation.getEfficiency(stationId)

        # Charging while moving
        self.transit = traci.chargingstation.getChargeInTransit(stationId)
        return

    def get_edge(self, stationId):
        """
        Returns the edge (road segment) where the charging station is located.
        This edge can be used directly with traci.vehicle.changeTarget().
        """
        self.lane = traci.chargingstation.getLaneID(stationId)
        self.edge = traci.lane.getEdgeID(self.lane)
        return