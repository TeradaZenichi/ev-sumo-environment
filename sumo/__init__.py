import traci
from sumolib import checkBinary
from pathlib import Path
import csv
import subprocess
import sys
import os


class Sumo:

    def __init__(self, config,vehicles):
        
        self.sumoBinary = checkBinary('sumo-gui')
        self.max_time = 0
         
        self.config = config
        self.veh = list(vehicles.keys())
        
        self.uptime()
        self.generate_activity_trips()
        self.apply_fleet_conversion()
        self.startSim()
        pass

    def upveh(self,ID):
        self.veh = ID
        return
    
    def uptime(self):
        self.max_time = self.config["Max_time"]
        return self.max_time
    
    def setup_results_and_headers(self):

        list_vehicles = self.veh

        base_dir = Path(__file__).resolve().parent
        pasta_results = base_dir / "results"
        
        if not pasta_results.exists():
            pasta_results.mkdir(parents=True, exist_ok=True)
        else:
            for item in pasta_results.iterdir():

                if item.is_file():
                    item.unlink()

        cabecalho = [
            "== ID ==",
            "== Velocity (Kh/h) ==",
            "== Atual route ==",
            "== Distance traveled(m) ==",
            "== Destination ==",
            "== Distance from destination(m) ==",
            "== TYPE ==",
            "== Batery level(%) ==",
            "== timestamp =="
        ]

        for veiculo_id in list_vehicles:
            arquivo_csv = pasta_results / f"{veiculo_id}.csv"
            
            with open(arquivo_csv, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(cabecalho)

    def generate_activity_trips(self):
        # O activitygen costuma estar no mesmo diretório do sumo
        # Se 'activitygen' não estiver no PATH, use o caminho completo
        activitygen_bin = "activitygen" 

        cmd = [
            activitygen_bin,
            "--net-file", self.config["net-file"],
            "--stat-file",  self.config["stat"], 
            "--output-file", self.config["route-files"],
            "--random", 
            "--seed", "42"
        ]
        
        try:
            print(f"Executando: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            print("✓ Rotas baseadas em atividades geradas com sucesso!")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar activitygen: {e}")
        except FileNotFoundError:
            print("Erro: O executável 'activitygen' não foi encontrado no PATH.")

    def apply_fleet_conversion(self):
        """
        Executa o script de conversão de frota (mista/elétrica) 
        utilizando o caminho definido no dicionário config.
        """
        # 1. Recupera o caminho do dicionário config

        script_path = self.config["convert-fleet"]

        # 2. Monta o comando usando o executável do Python atual
        # Isso garante que bibliotecas como 'random' e 'os' funcionem corretamente
        cmd = [sys.executable, script_path]

        try:
            # Verifica se o ficheiro existe antes de tentar rodar
            if not os.path.exists(script_path):
                print(f"Erro: O script de conversão não foi encontrado em: {script_path}")
                return

            print(f"Executando conversão de frota: {' '.join(cmd)}")
            
            # Executa o script. O 'capture_output=True' permite ler o que o script imprimiu (os contadores)
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            
            # Imprime o resumo (quantos carros/ônibus foram convertidos) que o script gerou
            print(result.stdout)
            print("✓ Frota convertida para mista com sucesso!")

        except subprocess.CalledProcessError as e:
            print(f"Erro ao executar o script de conversão: {e}")
            if e.stderr:
                print(f"Detalhes do erro: {e.stderr}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")

    #Starts the simulation
    def startSim(self):
        traci.start(
            [
                self.sumoBinary,
                '--net-file', self.config["net-file"],
                '--route-files', self.config["route-mista"],
                '--additional-files', self.config["additional-files"],
                '--step-length', self.config["step"], 
                '--delay', self.config["delay"],
                '--statistic-output', self.config["statistic-output"],
                '--duration-log.statistics', 'true',
                '--tripinfo-output', self.config["tripinfo-output"],
                '--gui-settings-file', self.config["gui-settings-file"],
                '--start',      
                '--quit-on-end' 
            ]
        )
    

    