import traci

class PARKING:
    def __init__(self, id: str):
        # -----------------------------
        # Parking identification
        # -----------------------------
        self.id = id            # ID of the parking area

        # -----------------------------
        # Vehicles in the parking
        # -----------------------------
        self.veh = []           # IDs of parked vehicles
        self.veh_count = 0      # Number of vehicles in the parking

        # -----------------------------
        # Location in the network
        # -----------------------------
        self.lane = traci.parkingarea.getLaneID(self.id)   # lane where the parking is located
        self.edge = traci.lane.getEdgeID(self.lane)        # corresponding edge

    def status(self):
        """
        Updates the dynamic state of the parking area.
        Should be called every simulation step.
        """

        # Vehicles parked in the area
        self.veh = traci.parkingarea.getVehicleIDs(self.id)

        # Total number of vehicles in the parking
        self.veh_count = traci.parkingarea.getVehicleCount(self.id)
