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

    def analisa(cond, ax1=None, ax2=None):
        suj = pd.read_csv(cond)
        lab = cond.split('/')[-1]
        diag = True if ax1 is None else False

        ax1 = plota_estimativas_media(suj, ax1, diagonal=diag, label=lab)
        ax1.legend()

        ax2 = plota_estimativas_std(suj, ax2, label=lab)
        ax2.legend()

        return ax1, ax2

    ax1, ax2 = analisa(sys.argv[1])

    for cond in sys.argv[2:]:
        analisa(cond, ax1, ax2)

    plt.show()
