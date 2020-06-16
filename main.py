import mplcursors
import pandas
import numpy as np
import matplotlib.pyplot as plt

from covid_stats import CovidStats


def draw(df: pandas.DataFrame):
    # These are the colors that will be used in the plot
    color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c',
                      '#98df8a', '#d62728', '#ff9896', '#9467bd', '#c5b0d5',
                      '#8c564b', '#c49c94', '#e377c2', '#f7b6d2', '#7f7f7f',
                      '#c7c7c7']

    fig, ax = plt.subplots(1, 1, figsize=(12, 14))

    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)

    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()

    fig.subplots_adjust(left=.06, right=.94, bottom=.07, top=.94)

    x_range = [i for i in range(df.date.size)]

    ax.xaxis.set_major_formatter(plt.FuncFormatter('{:.0f}'.format))
    ax.yaxis.set_major_formatter(plt.FuncFormatter('{:.3g}'.format))

    plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

    plt.tick_params(axis='both', which='both', bottom='off', top='off',
                    labelbottom='on', left='off', right='off', labelleft='on')

    plt.xlabel("date")
    plt.ylabel("new cases")
    plt.xticks(x_range, df.date.tolist(), rotation=90, fontsize=10)
    plt.yticks(np.arange(start=0, step=50, stop=500), fontsize=10)
    for rank, column in enumerate(df.columns[1:]):
        line = plt.plot(x_range, df[column].tolist(), lw=2.5,
                        color=color_sequence[rank], label=column)
        mplcursors.cursor(line)
    fig.suptitle('COVID-19 in Poland by region', fontsize=18, ha='center')

    plt.legend()
    plt.show()


POPULATION = {
              'dolnośląskie': 2_901_225,
              'kujawsko-pomorskie': 2_077_775,
              'lubelskie': 2_117_619,
              'lubuskie': 1_014_548,
              'łódzkie': 2_466_322,
              'małopolskie': 3_400_577,
              'mazowieckie': 5_403_412,
              'opolskie': 986_506,
              'podkarpackie': 2_129_015,
              'podlaskie': 1_181_533,
              'pomorskie': 2_333_523,
              'śląskie': 4_533_565,
              'świętokrzyskie': 1_241_546,
              'warmińsko-mazurskie': 1_428_983,
              'wielkopolskie': 3_493_969,
              'zachodniopomorskie': 1_701_030,
              }
# Population for 1 Jan 2019
# Data from: https://pl.wikipedia.org/wiki/Ludno%C5%9B%C4%87_Polski#Ludno%C5%9B%C4%87_wed%C5%82ug_wojew%C3%B3dztw


def normalize(df):
    df2 = df.copy()
    for name, population in POPULATION.items():
        df2[name] = df[name] * 1e5 / population

    return df2


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Plot CoViD-19 trajectories of polish voivodenships.')
    parser.add_argument('--normalize', dest='normalize', action='store_const',
                        const=normalize, default=lambda x: x,
                        help='normalize data by population size [100 000]')
    args = parser.parse_args()

    covid = CovidStats()
    df = covid.get_data()
    draw(args.normalize(df))
