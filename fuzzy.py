import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt 

# 1. Definir as variáveis fuzzy
# Definindo o universo de discurso
temperatura = ctrl.Antecedent(np.arange(0, 101, 1), 'temperatura')  # Temperatura em °C (0 a 100)
fluxo_agua = ctrl.Antecedent(np.arange(0, 101, 1), 'fluxo_agua')    # Fluxo de água em L/min (0 a 100)
abertura_valvula = ctrl.Consequent(np.arange(0, 101, 1), 'abertura_valvula')  # Abertura da válvula em % (0 a 100)

# 2. Definir as funções de pertinência para cada variável
# Funções de pertinência para temperatura
temperatura['baixa'] = fuzz.trapmf(temperatura.universe, [0, 0, 20, 40])
temperatura['media'] = fuzz.trapmf(temperatura.universe, [30, 40, 60, 70])
temperatura['alta'] = fuzz.trapmf(temperatura.universe, [60, 80, 100, 100])

# Funções de pertinência para fluxo de água
fluxo_agua['baixo'] = fuzz.trapmf(fluxo_agua.universe, [0, 0, 20, 40])
fluxo_agua['medio'] = fuzz.trapmf(fluxo_agua.universe, [30, 40, 60, 70])
fluxo_agua['alto'] = fuzz.trapmf(fluxo_agua.universe, [60, 80, 100, 100])

# Funções de pertinência para abertura da válvula
abertura_valvula['pequena'] = fuzz.trapmf(abertura_valvula.universe, [0, 0, 20, 40])
abertura_valvula['moderada'] = fuzz.trapmf(abertura_valvula.universe, [30, 40, 60, 70])
abertura_valvula['grande'] = fuzz.trapmf(abertura_valvula.universe, [60, 80, 100, 100])

# 3. Definir as regras fuzzy

regra1 = ctrl.Rule(temperatura['baixa'] & fluxo_agua['alto'], abertura_valvula['grande'])
regra2 = ctrl.Rule(temperatura['baixa'] & fluxo_agua['medio'], abertura_valvula['moderada'])
regra3 = ctrl.Rule(temperatura['media'] & fluxo_agua['alto'], abertura_valvula['moderada'])
regra4 = ctrl.Rule(temperatura['media'] & fluxo_agua['baixo'], abertura_valvula['pequena'])
regra5 = ctrl.Rule(temperatura['alta'] & fluxo_agua['baixo'], abertura_valvula['pequena'])
regra6 = ctrl.Rule(temperatura['alta'] & fluxo_agua['alto'], abertura_valvula['moderada'])

# 4. Criar o sistema de controle fuzzy

sistema_controle = ctrl.ControlSystem([regra1, regra2, regra3, regra4, regra5, regra6])
simulador = ctrl.ControlSystemSimulation(sistema_controle)

# 5. Fuzzificação e inferência: Definindo os valores de entrada e calculando a saída
# Vamos fuzzificar para uma temperatura de 45°C e um fluxo de água de 80 L/min
simulador.input['temperatura'] = 45
simulador.input['fluxo_agua'] = 80

# Computando o valor de saída
simulador.compute()

# Exibindo o resultado da abertura da válvula
abertura = simulador.output['abertura_valvula']
if abertura <= 40:
    categoria = "pequena"
elif 40 < abertura <= 70:
    categoria = "moderada"
else:
    categoria = "grande"

print(f"Abertura da válvula: {simulador.output['abertura_valvula']:.2f}% - {categoria}")

# 6. Plotagem das funções de pertinência
# Plotar as funções de pertinência para a variável temperatura
temperatura.view()
plt.title("Função de Pertinência - Temperatura")
plt.xlabel("Temperatura (°C)")
plt.ylabel("Grau de Pertinência")

# Plotar as funções de pertinência para a variável fluxo de água
fluxo_agua.view()
plt.title("Função de Pertinência - Fluxo de Água")
plt.xlabel("Fluxo de Água (L/min)")
plt.ylabel("Grau de Pertinência")

# Plotar as funções de pertinência para a variável abertura da válvula
abertura_valvula.view()
plt.title("Função de Pertinência - Abertura da Válvula")
plt.xlabel("Abertura da Válvula (%)")
plt.ylabel("Grau de Pertinência")

# Exibir as funções de pertinência para a saída calculada
abertura_valvula.view(sim=simulador)
plt.title("Função de Pertinência - Abertura da Válvula (Simulação)")
plt.xlabel("Abertura da Válvula (%)")
plt.ylabel("Grau de Pertinência")

plt.show()