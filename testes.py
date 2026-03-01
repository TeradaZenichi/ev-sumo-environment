class cachorro:
    def __init__(self,nome,raça,idade):
        self.nome = nome
        self.raça=raça
        self.idade=idade
        pass

    def esportes(self) :
        if self.raça == "pitbul":
            return "corrida"
        elif self.raça == "pintcher":
            return "futebol de cachorro"
        elif self.raça =="buldog":
            return "natação"
        else:
            return "atletismo" 
        
    def maquina_do_tempo(self):
        self.idade = self.idade*20

dog = cachorro("rex","buldog",2)
a=1