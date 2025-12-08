import pandas as pd
import matplotlib.pyplot as plt

dados = pd.read_csv('sandro_01ago2024_proc/estimativas_dicoico_sandro_01ago2024_proc.csv')

# Substituir "ITD0ILD0" por "ambos0"
dados[' estimulo'] = dados[' estimulo'].str.replace('ITD0ILD0', 'ambos0')

condicoes = [
    ['ITD0fastonset', 'ILD0fastonset', 'ambos0fastonset', "ORIGfastonset"],
    ['ITD0slowonset', 'ILD0slowonset', 'ambos0slowonset', "ORIGslowonset"]
]

fig, axs = plt.subplots(2, 4, figsize=(15, 10))

for i in range(2):
    for j in range(4):
        cond = condicoes[i][j]
        estimulosFiltrados = dados[dados[' estimulo'].str.contains(cond)]
        
        axs[i, j].scatter(estimulosFiltrados['# verdadeiro'], estimulosFiltrados[' estimado'])
        axs[i, j].set_ylim(-90, 90)
        axs[i, j].set_title(f'Condição: {cond}')
        axs[i, j].set_xlabel('Ângulo Verdadeiro')
        axs[i, j].set_ylabel('Ângulo Estimado')
        axs[i, j].grid(True)

# Ajustar o layout para não sobrepor os elementos
plt.tight_layout()
plt.show()
