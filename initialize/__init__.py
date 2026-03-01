import traci
from sumolib import checkBinary
import json
from pathlib import Path

class INITIALIZE:

    """Load config at config/config.json"""
    with open(r'initialize/config.json', 'r') as initialize_file:
        config = json.load(initialize_file)
    
    def __init__(self):
        self.Max_Time = 0
        self.veh = []
        pass

    def upveh(self):
        list_vehicles = [f"veh_{i}" for i in range(config["vehicles_number"])]