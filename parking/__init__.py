import traci

class PARKING:
    def __init__(self):
        # -----------------------------
        # Parking identification
        # -----------------------------
        self.ids = []            # IDs of parking areas
        self.count = 0           # Total number of parkings

        # -----------------------------
        # Vehicles in the parking
        # -----------------------------
        self.veh = []            # IDs of parked vehicles
        self.veh_count = 0       # Number of vehicles in the parking

        # -----------------------------
        # Charging state
        # -----------------------------
        self.lane = None
        self.edge = None
        pass

    def update(self):
        # List of available parking areas
        self.ids = traci.parkingarea.getIDList()
        self.count = len(self.ids)
        return

    def status(self, parkingId):
        # Vehicles parked in the area
        self.veh = traci.parkingarea.getVehicleIDs(parkingId)

        # Total number of vehicles in the parking
        self.veh_count = traci.parkingarea.getVehicleCount(parkingId)
        return
    
    def get_parking_edge(self, parkingId):
        """
        Returns the edge (road segment) where the parking area is located.
        This edge can be used with traci.vehicle.changeTarget().
        """
        self.lane = traci.parkingarea.getLaneID(parkingId)
        self.edge = traci.lane.getEdgeID(self.lane)
        return 