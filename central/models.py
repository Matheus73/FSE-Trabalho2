class Andar:
    def __init__(self):
        self.nome = ''
        self.lampada1 = False
        self.lampada1_gpio = False
        self.lampada2 = False
        self.lampada2_gpio = False
        self.corredor = False
        self.corredor_gpio = False
        self.arcondicionado = False
        self.arcondicionado_gpio = False
        self.aspersor = False
        self.aspersor_gpio = False
        self.temperatura = 0
        self.umidade = 0
        self.porta = False
        self.janela1 = False
        self.janela2 = False
        self.fumaca = False
        self.alarme = False
        self.ocupacao = 0

    def set_name(self,value):
        self.nome = value

    def get_janela2(self):
        return self.janela2

    def get_alarme(self):
        return self.alarme

    def get_janela1(self):
        return self.janela1

    def get_porta(self):
        return self.porta

    def get_name(self):
        return self.nome

    def get_arcondicionado(self):
        return self.arcondicionado

    def get_aspersor(self):
        return self.aspersor

    def get_ocupacao(self):
        return self.ocupacao

    def get_fumaca(self):
        return self.fumaca

    def get_lampada1(self):
        return self.lampada1

    def get_lampada2(self):
        return self.lampada2

    def get_corredor(self):
        return self.corredor

    def get_temperature(self):
        return self.temperatura

    def set_temperature(self,value):
        self.temperatura = value

    def get_moisture(self):
        return self.umidade

    def set_moisture(self,value):
        self.umidade = value

    def set_umidade(self,value):
        self.umidade = value

    def set_ocupacao(self,value):
        self.ocupacao += value

    def get_all(self) -> dict:
        data = {
                "nome": self.nome,
                "lampada1": self.lampada1,
                "lampada2": self.lampada2,
                "corredor": self.corredor,
                "arcondicionado": self.arcondicionado,
                "aspersor": self.aspersor,
                "temperatura": self.temperatura,
                "umidade": self.umidade,
                "porta": self.porta,
                "janela1": self.janela1,
                "janela2": self.janela2,
                "fumaca": self.fumaca,
                "ocupacao": self.ocupacao,
                }
        return data

    def set_lampada1(self):
        self.lampada1 = not self.lampada1

    def set_lampada1_gpio(self, value):
        self.lampada1_gpio = value

    def set_lampada2_gpio(self, value):
        self.lampada2_gpio = value

    def set_corredor_gpio(self, value):
        self.corredor_gpio = value

    def set_arcondicionado_gpio(self, value):
        self.arcondicionado_gpio = value

    def set_aspersor_gpio(self, value):
        self.aspersor_gpio = value

    def get_lampada1_gpio(self):
        return self.lampada1_gpio

    def get_lampada2_gpio(self):
        return self.lampada2_gpio

    def get_corredor_gpio(self):
        return self.corredor_gpio

    def get_arcondicionado_gpio(self):
        return self.arcondicionado_gpio

    def get_aspersor_gpio(self):
        return self.aspersor_gpio

    def set_alarme(self):
        self.alarme = not self.alarme

    def set_lampada2(self):
        self.lampada2 = not self.lampada2

    def set_corredor(self):
        self.corredor = not self.corredor
        
    def set_arcondicionado(self):
        self.arcondicionado = not self.arcondicionado
        
    def set_aspersor(self):
        self.aspersor = not self.aspersor

    def set_porta(self):
        self.porta = not self.porta

    def set_janela1(self):
        self.janela1 = not self.janela1

    def set_janela2(self):
        self.janela2 = not self.janela2

    def set_fumaca(self):
        self.fumaca = not self.fumaca
