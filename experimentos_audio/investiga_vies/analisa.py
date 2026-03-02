import pandas as pd
import matplotlib.pyplot as plt


def plota_estimativas_media(dados, ax=None, color=None, diagonal=False, label=None):

    if ax is None:
        fig, ax = plt.subplots()
        ax.set_xlabel('Verdadeiro')
        ax.set_ylabel('Estimado')

    if color is None:
        color = ax._get_lines.get_next_color()

    ax.scatter(
        dados['# verdadeiro'],
        dados[' estimado'],
        alpha=0.5,
        color=color
    )

    g = dados.groupby('# verdadeiro')[' estimado'].mean()
    ax.plot(
        g.index,
        g.values,
        color=color,
        marker='o',          
        linestyle='-',
        label=label
    )

    # Diagonal (no label)
    if diagonal:
        ax.plot([-90, 90], [-90, 90], 'k')

    return ax


def plota_estimativas_std(dados, ax=None, color=None, label=None):

    if ax is None:
        fig, ax = plt.subplots()
        ax.set_xlabel('Verdadeiro')
        ax.set_ylabel('Desvio')

    if color is None:
        color = ax._get_lines.get_next_color()

    g = dados.groupby('# verdadeiro')[' estimado'].std()
    ax.plot(
        g.index,
        g.values,
        color=color,
        marker='o',          
        linestyle='-',
        label=label
    )

    return ax


if __name__ == '__main__':
    import sys
    import pandas as pd
    cond1 = sys.argv[1]
    cond2 = sys.argv[2]

    suj = pd.read_csv(cond1)
    suj_outro = pd.read_csv(cond2)

    lab1 = cond1.split('/')[0]
    lab2 = cond2.split('/')[0]
    ax = plota_estimativas_media(suj, diagonal=True, label=lab1)
    plota_estimativas_media(suj_outro, ax, label=lab2)
    ax.legend()
    
    ax = plota_estimativas_std(suj, label=lab1)
    plota_estimativas_std(suj_outro, ax, label=lab2)
    ax.legend()

    plt.show()
