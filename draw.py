"""
https://stackoverflow.com/questions/69667513/how-to-plot-timeline-in-a-single-bar
this link can be helpful to draw gantt chart

basically plotly can be helpful in order to draw gantt chart

only pandas library shall be used

returned Schedule class can be turned into pandas dataframe with dictionary of start, finish, task
and then used in plotly

requirements.txt will be needed for pandas and plotly
"""
import pandas as pd
import plotly.express as pex

from utils import *


class ChartDrawer:
    """
    draw gantt chart
    it converts schedule into pandas dataframe
    then draw gantt chart based on it
    """
    def __init__(self, schedule: Schedule):
        self.schedule = schedule.schedule
        self.data = None  # pd.DataFrame
        self.schedule_to_df()

    def schedule_to_df(self):
        """
        change schedule list into pd.DataFrame, each row consisted of start, end, job
        """
        prev_time = 0
        to_draw = []
        for record in self.schedule:
            pid, end = record
            if pid == 'None':
                prev_time = end
                continue
            else:
                to_draw.append(dict(PID=pid, Start=prev_time, End=end, Stack=1))
                prev_time = end
        self.data = pd.DataFrame(to_draw)
        self.data['delta'] = self.data['End'] - self.data['Start']

    def draw_gantt_chart(self, height):
        gantt = pex.timeline(self.data, x_start='Start', x_end='End', color='PID',
                             y=['']*self.data.shape[0], height=height, text='PID')

        gantt.layout.xaxis.type = 'linear'
        gantt.update_yaxes(visible=False, showticklabels=False)
        for d in gantt.data:
            filt = self.data['PID'] == d.name
            d.x = self.data[filt]['delta'].tolist()
        gantt.update_traces(textposition='auto')
        return gantt