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

    def schedule_to_df(self):
        """
        change schedule list into pd.DataFrame, each row consisted of start, end, job
        """
        pass

    def draw_gantt_chart(self):
        pass