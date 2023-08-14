import csv
from collections import Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statistics as stats
import controlchart

from .models import ControlPlotFile


def read_file(data, filename, user, columname):
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(data[columname])
    counted_c = Counter(df['date'].dt.month)
    month_freq = sorted(dict(counted_c, ).items())
    return build_plot(month_freq, filename, user)


def build_plot(month_freq, filename, user):
    months, count_month = list(zip(*month_freq))
    count_month = list(count_month)
    s = controlchart.Spc(count_month, controlchart.CHART_X_MR_X)
    x_labels = [1,2,3,4,5,6,7,8,9,10,11,12]
    b = s.get_chart(title='Control Chart')
    # b.set_xticks(months, x_labels)
    plotadress = f"{filename}_control.png"
    b.get_figure().savefig(f'uploads/{plotadress}')
    p = ControlPlotFile(plot=f'../uploads/{plotadress}', plot_user=user)
    p.save()

    data = {
        "chart": p.plot
    }
    print('Hi from contcalc', data.get('chart'))
    return data


if __name__ == "__main__":
    read_file(df, filename, user)