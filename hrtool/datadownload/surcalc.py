import math
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

from .models import PlotFile

plt.switch_backend(
    'agg')  # https://stackoverflow.com/questions/52839758/matplotlib-and-runtimeerror-main-thread-is-not-in-main-loop


def dataStructure(data, filename, user):
    # print(data)
    df = data

    filename = filename
    user = user
    x = datetime.today()
    df['StartDay'] = pd.to_datetime(df['StartDay'])
    df['LastDay'] = pd.to_datetime(df['LastDay'])
    df['Event'] = 1
    df.loc[df['LastDay'].isna(), 'Event'] = 0
    df.loc[df['LastDay'].isna(), 'LastDay'] = x
    df['WorkTimeM'] = (df['LastDay'] - df['StartDay']).astype('timedelta64[ns]').dt.days / (365.25 / 12)
    pd.to_numeric(df['WorkTimeM'])  # convert everything to float values
    if len(df.columns) == 4:
        print("KaplanMeier")
        return KaplanMeier(df, filename, user)
    elif len(df.columns) == 5:
        print("LogRank")
        return LogRank(df, filename, user)
    elif len(df.columns) > 5:
        pass
        print("Sorry you add to many parameters if you want to make such research please contact us")
    else:
        print("some mistake")
    print("Hi from dataStructure")


def KaplanMeier(df, filename, user):
    df = df
    kmf = KaplanMeierFitter()
    kmf.fit(durations=df['WorkTimeM'], event_observed=df['Event'], label='Median Survival Time')
    a = [kmf.median_survival_time_]
    px = 1 / plt.rcParams['figure.dpi']
    kmf.plot(color="#2E9FDF", figsize=(854 * px, 480 * px), ci_show=False)
    chartname = f"uploads/{filename}"
    plt.grid(alpha=0.3)  # сетка и ее прозрачность
    plt.xlabel('Months')
    plt.ylabel('Survival')
    plt.title('Employee Median Survival Time')
    plt.legend()
    plt.ylim(0, 1)
    plt.xlim(0, max(df['WorkTimeM']))
    plt.axhline(y=0.5, xmin=0, xmax=a[0] / max(df['WorkTimeM']), color="#E7B800", ls="dotted", lw=1)
    plt.axvline(x=a, ymin=0, ymax=0.5, color="#E7B800", ls="dotted", lw=1)
    y = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    plt.yticks(y)  # размер градации шкалы
    plt.savefig(chartname, dpi=150)
    plt.close()
    # plotadress = '/'.join(chartname.split('\\')[-2:])
    plotadress = f"uploads/{filename}.png"
    # print(user.pk)
    Hazard3m = (1 - kmf.survival_function_at_times(3.0).iloc[0]) * 100
    Hazard6m = (1 - kmf.survival_function_at_times(6.0).iloc[0]) * 100
    Hazard12m = (1 - kmf.survival_function_at_times(12.0).iloc[0]) * 100
    if a[0] == np.inf:
        AvarageSurvival = 'Data non reach median survival time'
    else:
        AvarageSurvival = math.ceil(a[0])
    p = PlotFile()
    p.plot = f'../{plotadress}'
    p.plot_user = user
    p.plot_hazard3m = Hazard3m
    p.plot_hazard6m = Hazard6m
    p.plot_hazard12m = Hazard12m
    p.plot_avr_surv = AvarageSurvival
    p.plot_name = 'KMF'
    p.save()
    print('Hi after plot save')
    data = {
        "Name": "KMF",
        "Hazard3m": "{:.1f}".format(Hazard3m),
        "Hazard6m": "{:.1f}".format(Hazard6m),
        "Hazard12m": "{:.1f}".format(Hazard12m),
        "AvarageSurvival": AvarageSurvival,
        "chart": p.plot
        # "75Survival": kmf.percentile(p="0.25"),
        # "25Survival": kmf.percentile(p="0.75")
    }

    return data

    # возвращаем какой процент сотрудников увольняется в первіе 3,6,12 месяцев работы
    # print(1-kmf.survival_function_at_times(3.0).iloc[0])#коммулятивній риск увольнения в первіе 3 месяца
    # print(1 - kmf.survival_function_at_times(6.0))#коммулятивній риск увольнения в первіе 6 месяца
    # print(1 - kmf.survival_function_at_times(12.0))#коммулятивній риск увольнения в первіе 12 месяца
    # возвращаем процентили дожития сотрудников
    # print(kmf.percentile(p="0.5"))#средняя продолжительность жизни сотрудника в компании
    # print(kmf.percentile(p="0.25"))#3 квартиль продолжительность жизни сотрудника в компании
    # print(kmf.percentile(p="0.75"))#1 квартиль продолжительность жизни сотрудника в компании


def LogRank(df, filename, user):
    print("Hi from LogRank")
    df = df
    print(df)

    kmf_b = KaplanMeierFitter()
    kmf_nb = KaplanMeierFitter()
    # print('KMstart')
    factors = list(set(df['Factor'].to_numpy()))

    b = df[df['Factor'] == factors[1]]
    nb = df[df['Factor'] == factors[0]]
    print(b)
    kmf_b.fit(durations=b['WorkTimeM'], event_observed=b['Event'], label=f'{factors[1]} Median Survival Time')
    kmf_nb.fit(durations=nb['WorkTimeM'], event_observed=nb['Event'], label=f'{factors[0]} Median Survival Time')
    print('knBNB')

    ba = [kmf_b.median_survival_time_]
    nba = [kmf_nb.median_survival_time_]

    print(ba, nba)

    # print(kmf_b.hazard_)
    px = 1 / plt.rcParams['figure.dpi']
    kmf_b.plot(color="#0057b8", figsize=(854 * px, 480 * px), ci_show=False)  # цвет линии и размер графика
    kmf_nb.plot(color="#ffd800", ci_show=False)
    chartname = f"media/{filename}"

    plt.grid(alpha=0.3)  # сетка и ее прозрачность
    plt.xlabel('Months')
    plt.ylabel('Survival')
    plt.title('Employee Median Survival Time')
    plt.ylim(0, 1)
    plt.xlim(0, max(df['WorkTimeM']))
    plt.axhline(y=0.5, xmin=0, xmax=ba[0] / max(df['WorkTimeM']), color="red", ls="--",
                lw=0.4)  # горизонтальная линия и параметры
    plt.axhline(y=0.5, xmin=0, xmax=nba[0] / max(df['WorkTimeM']), color="red", ls="--",
                lw=0.4)  # вертикальная линия и параметры
    plt.axvline(x=ba, ymin=0, ymax=0.5, color="red", ls="--", lw=0.4)
    plt.axvline(x=nba, ymin=0, ymax=0.5, color="red", ls="--", lw=0.4)
    y = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    plt.yticks(y)  # размер градации шкалы
    plt.savefig(chartname, dpi=150)
    plt.close()

    # plotadress = '/'.join(chartname.split('\\')[-2:])
    plotadress = f"uploads/{filename}.png"
    print(user.pk)
    p = PlotFile(plot=f'../{plotadress}', plot_user=user)
    p.save()
    # logrank_test:
    # Define variables :
    T = b['WorkTimeM']
    E = b['Event']
    T1 = nb['WorkTimeM']
    E1 = nb['Event']

    results = logrank_test(T, T1, event_observed_A=E, event_observed_B=E1)
    if results.p_value < 0.05:
        pvaluetext = 'p.value is less 0.05 that mean there are significant statistical difference between tenure of this groups'
    else:
        pvaluetext = 'p.value is larger 0.05 that mean that there are significant statistical difference between tenure of this groups'

    Hazardb3m = (1 - kmf_b.survival_function_at_times(3.0).iloc[0]) * 100
    Hazardb6m = (1 - kmf_b.survival_function_at_times(6.0).iloc[0]) * 100
    Hazardb12m = (1 - kmf_b.survival_function_at_times(12.0).iloc[0]) * 100

    Hazardnb3m = (1 - kmf_nb.survival_function_at_times(3.0).iloc[0]) * 100
    Hazardnb6m = (1 - kmf_nb.survival_function_at_times(6.0).iloc[0]) * 100
    Hazardnb12m = (1 - kmf_nb.survival_function_at_times(12.0).iloc[0]) * 100

    data = {
        'Name': "Long-Rank",
        "Pvalue": results.p_value,
        "pvaluetext": pvaluetext,
        "GroupbName": factors[1],
        "Hazardb3m": "{:.1f}".format(Hazardb3m),
        "Hazardb6m": "{:.1f}".format(Hazardb6m),
        "Hazardb12m": "{:.1f}".format(Hazardb12m),
        "AvarageSurvivalb": "{:.0f}".format(ba[0]),
        # "75Survivalb": kmf_b.percentile(p="0.25"),
        # "25Survivalb": kmf_b.percentile(p="0.75"),
        "GroupbnName": factors[0],
        "Hazardnb3m": "{:.1f}".format(Hazardnb3m),
        "Hazardnb6m": "{:.1f}".format(Hazardnb6m),
        "Hazardnb12m": "{:.1f}".format(Hazardnb12m),
        "AvarageSurvivalnb": "{:.0f}".format(nba[0]),
        # "75Survivalnb": kmf_nb.percentile(p="0.25"),
        # "25Survivalnb": kmf_nb.percentile(p="0.75")
        "chart": p.plot
    }

    return data


if __name__ == "__main__":
    dataStructure(df, filename, user)
