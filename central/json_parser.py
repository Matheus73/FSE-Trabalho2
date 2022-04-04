import json
from models import Andar

def read_json_file(path: str) -> dict:
    file = open(path)
    return json.load(file)

def set_gpio_values(andar: Andar, path: str):
    outputs = read_json_file(path)["outputs"]

    for i in outputs:
        if i["tag"] == "Lâmpada da Sala T01":
            andar.set_lampada1_gpio(i["gpio"])
        elif i["tag"] == "Lâmpada da Sala 101":
            andar.set_lampada1_gpio(i["gpio"])

        elif i["tag"] == "Lâmpada da Sala T02":
            andar.set_lampada2_gpio(i["gpio"])
        elif i["tag"] == "Lâmpada da Sala 102":
            andar.set_lampada2_gpio(i["gpio"])

        elif i["tag"] == "Lâmpadas do Corredor Terreo":
            andar.set_corredor_gpio(i["gpio"])
        elif i["tag"] == "Lâmpadas do Corredor":
            andar.set_corredor_gpio(i["gpio"])

        elif i["tag"] == "Ar-Condicionado Terreo":
            andar.set_arcondicionado_gpio(i["gpio"])
        elif i["tag"] == "Ar-Condicionado (1º Andar)":
            andar.set_arcondicionado_gpio(i["gpio"])

        elif i["tag"] == "Aspersor de Água (Incêndio)":
            andar.set_aspersor_gpio(i["gpio"])

        else:
            print("Tag desconhecida")

