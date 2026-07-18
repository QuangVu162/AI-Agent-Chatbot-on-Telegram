import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from typing import Union, List, Optional, Dict, Any

class ChartDrawer:
    """
    This is a class to draw chart datatc

    The class support to draw following charts:
    - bar chart
    - line chart
    - pie chart
    - column chart
    - stacked bar chart
    - histogram chart
    """

    def __init__(self, figsize: tuple = (10,6), style: str = "darkgrid", palette:str = "husl"):
        """
        the function is to initialize the chart class
        :param figsize: the size of the figure (width, height)
        :param style: the style of the chart (default to darkgrid)
        :param palette: the color palette of the chart (default to husl)
        """
        self.figsize = figsize
        self.style = style
        self.palette = "tab10"

        #Configure the style for seaborn
        sns.set_theme(style = self.style, palette = self.palette)

#Bar chart
    def bar_chart(self
                  ,data: Union[pd.DataFrame, dict]
                  ,x:str = None
                  ,y:str = None
                  ,title:str = "Bar Chart"
                  ,xlabel:str = "X Axis"
                  ,ylabel:str = "Y Axis"
                  ,hue:str = None
                  ,figsize:tuple = None
                  ) -> None:

        """
        Draw the bar chart
        :param data: pd.DataFrame or dict
        :param x: column name for x axis
        :param y: column name for y axis
        :param title: title of the bar chart, default "Bar Chart"
        :param xlabel: name of the x axis, default "X Axis"
        :param ylabel: name of the y axis, default "Y Axis
        :param hue: specify the hue
        :param figsize: size of the figure (width, height)
        :return:
        """

        # Change the dictionary into dataframe if the input data is in dict type
        if isinstance(data, dict):
            data = pd.DataFrame(data)

        # Specify the figsize of the chart
        figsize = figsize or self.figsize
        plt.figure(figsize = figsize)

        #bar chart
        plot = sns.barplot(
            data = data,
            x = x,
            y = y,
            hue = hue,
            palette = self.palette
        )

        # Add data label
        for container in plot.containers:
            plot.bar_label(container, fmt="%.1f", padding=3, fontsize=15, weight='bold')

        #chart information
        plt.title(title, fontsize = 16, weight = 'bold')
        plt.xlabel(xlabel, fontsize = 16)
        plt.ylabel(ylabel, fontsize = 16)
        plt.xticks(rotation = 45, ha = 'right')
        plt.tight_layout()

        plt.show()

#Pie chart
    def pie_chart(self
                  ,data: Union[pd.Series, dict, list]
                  ,labels:List[str] = None
                  ,title:str = "Pie Chart"
                  ,autopct:str = "%1.1f%%"
                  ,startangle:int = 90
                  ,figsize:tuple = None
                  ,explode:List[float] = None
                  ) -> None:

        """
        Draw the pie chart
        :param data: the data in the format of pd.Series, dict, or list
        :param labels: the lable of each category
        :param title: title of the pie chart, default "Pie Chart
        :param autopct: the format of data label
        :param startangle: the start angle, default 90
        :param figsize: figure size of the pie chart (width, height)
        :param explode: pull out one or more slices to emphasize the data
        :return: the pie chart
        """

        if isinstance(data, dict):
            labels = list(data.keys())
            values = list(data.values())

        #figure size of the pie chart
        figsize = figsize or self.figsize
        plt.figure(figsize = figsize)

        #set the color pelette for the pie chart
        colors = sns.color_palette(self.palette, len(data))

        #pie chart
        plt.pie(
            data,
            labels = labels,
            autopct = autopct,
            startangle = startangle,
            colors = colors,
            explode = explode,
            textprops = {'fontsize': 13, 'weight':'bold'}
        )

        plt.title(title, fontsize = 16, fontweight = 'bold')
        plt.axis('equal')
        plt.tight_layout()

        plt.show()

#Line Chart
    def line_chart(self
                   ,data: Union[pd.DataFrame, dict]
                   ,x:str = None
                   ,y:str = None
                   ,title:str = "Line Chart"
                   ,xlabel:str = "X Axis"
                   ,ylabel:str = "Y Axis"
                   ,hue:str = None
                   ,figsize:tuple = None
                   ,markers:bool = False
                   ,ci:int = 95) -> None:

        """
        Line Chart
        :param data: The data in the format of pd.DataFrame, dict
        :param x: name of column for x axis
        :param y: name of column for y axis
        :param title: Title of the line chart, default "Line Chart"
        :param xlabel: lable of x axis, default "X Axis"
        :param ylabel: lable of y axis, default "Y Axis
        :param hue: hue
        :param figsize: figure size of the line chart
        :param markers: allow the line chart to have markers
        :param ci: confidence interval
        :return:
        """

        #Check if the data type is dictionary, need to change it into pd.DataFrame
        if isinstance(data, dict):
            data = pd.DataFrame(data)

        figsize = figsize or self.figsize
        plt.figure(figsize = figsize)

        sns.lineplot(
            data = data,
            x = x,
            y = y,
            hue = hue,
            palette = self.palette,
            markers = markers,
            ci = ci)

        plt.title(title, fontsize = 16, fontweight = 'bold')
        plt.xlabel(xlabel, fontsize = 16)
        plt.ylabel(ylabel, fontsize = 16)
        plt.xticks(rotation = 45, ha = 'right')
        plt.grid(True, alpha = 0.3)
        plt.tight_layout()

        plt.show()



#Column chart
    def column_chart(self,
                     data: Union[pd.DataFrame, dict],
                     x:str = None,
                     y:str = None,
                     title:str = "Column Chart",
                     xlabel:str = None,
                     ylabel:str = None,
                     hue:str = None,
                     figsize:tuple = None,
                     ) -> None:

        """
        Column Chart
        :param data: data in the format of pd.DataFrame, dict
        :param x: column name for x axis
        :param y: column name for y axis
        :param title: title of the column chart, default "Column Chart
        :param xlabel: lable of x axis, default "X Axis"
        :param ylabel: label of y axis, default "Y Axis"
        :param hue: hue
        :param figsize: figure size of the column chart (width, height)
        :return:
        """

        if isinstance(data, dict):
            data = pd.DataFrame(data)

        figsize = figsize or self.figsize
        plt.figure(figsize = figsize)

        sns.barplot(
            data = data,
            x = x,
            y = y,
            hue = hue,
            palette = self.palette)

        plt.title(title, fontsize = 16, fontweight = 'bold')
        plt.xlabel(xlabel, fontsize = 16)
        plt.ylabel(ylabel, fontsize = 16)
        plt.xticks(rotation = 45, ha = 'right')
        plt.tight_layout()

        plt.show()


#Stacked bar chart
    def stacked_bar_chart(self,
                          data: Union[pd.DatFrame, dict],
                          title:str = "Stacked Bar Chart",
                          xlabel:str = None,
                          ylabel:str = None,
                          figsize:tuple = None,
                          horizontal:bool = False
                          ) -> None:

        """
        Stacked bar chart
        :param data: data in the format of pd.DataFrame, dict. Each column represents each category in the stacked bar chart,
                    and first column contains the information for x axis
        :param title: title of the stacked bar chart, default "Stacked Bar Chart
        :param xlable: label of x axis, default "X Axis"
        :param ylable: label of y axis, default "Y Axis"
        :param figsize: figure size of the stacked bar chart
        :param horizontal: If True, horizontal, if False, vertical. Default False
        :return:
        """

        if isinstance(data, dict):
            data = pd.DataFrame(data)

        figsize = figsize or self.figsize
        plt.figure(figsize = figsize)

        #create the color palette based on the number of column in the dataframe
        colors = sns.color_palette(self.palette, len(data.columns))

        if horizontal:
            data.plot(kind = 'barh', stacked = True, ax = plt.gca(), color = colors)
        else:
            data.plot(kind = 'bar', stacked = True, ax = plt.gca(), color = colors)

        plt.title(title, fontsize=16, fontweight='bold')
        plt.xlabel(xlabel, fontsize=12)
        plt.ylabel(ylabel, fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()

        plt.show()


    #Histogram chart
    def histogram (self,
                   data: Union[pd.Series, np.array, List],
                   title:str = 'Histogram Chart',
                   xlabel:str = 'Value',
                   ylabel:str = 'Frequency',
                   bins: int = 30,
                   figsize:tuple = None,
                   kde:bool = True,
                   stat:str = 'count'
                   ) -> None:

        """
        Histogram Chart
        :param data: the data for drawing histogram chart
        :param title: Title of the chart
        :param xlabel: label of x axis, default "Value"
        :param ylabel: label of y axis, default "Frequency"
        :param bins: the number of bins (bins represents the distance between two points in the histogram)
        :param figsize: figure size of the histogram chart
        :param kde: kernel density estimation
        :param stat: demonstrated statistic figure: count, frequency, density, probability
        :return:
        """

        figsize = figsize or self.figsize
        plt.figure(figsize = figsize)

        sns.histplot(data = data,
                     bins = bins,
                     kde = kde,
                     stat = stat,
                     color = sns.color_palette(self.palette)[0])

        plt.title(title, fontsize = 16, fontweight = 'bold')
        plt.xlabel(xlabel, fontsize = 16)
        plt.ylabel(ylabel, fontsize = 16)
        plt.grid(True, alpha = 0.3, axis = 'y')
        plt.tight_layout()

        plt.show()

    # Scatter plot
    def scatter_plot(self,
                     data: Union[pd.DataFrame, dict],
                     x:str,
                     y:str,
                     hue:str = None,
                     size:str = None,
                     figsize:tuple = None,
                     title:str = 'Scatter Plot Chart',
                     xlabel:str = "X Axis",
                     ylabel:str = "Y Axis",
                     legend_loc:str = "best",
                     legend_bbox:tuple = None,
                     legend_title:str = None
                     ) -> None:

        """
        Draw a scatter plot
        :param data: data in the format of pd.DataFrame or dict
        :param x: column name for x axis
        :param y: column name for y axis
        :param hue: grouping variable that produces points with different colors
        :param size: grouping variable that produces points with different sizes
        :param title: title of the scatter chart, default "Scatter Plot"
        :param xlabel: name of the x axis, default "X Axis"
        :param ylabel: name of the y axis, default "Y Axis"
        :param figsize: size of the figure (width, height)
        :param legend_loc: location of the legend (e.g., 'upper right', 'best')
        :param legend_bbox: bbox_to_anchor for the legend to place it outside, e.g., (1.05, 1)
        :param legend_title: custom title for the legend
        :return: None
        """

        if isinstance(data, dict):
            data = pd.DataFrame(data)

        figsize = figsize or self.figsize
        plt.figure(figsize = figsize)

        #Draw the scatter plot
        sns.scatterplot(data = data,
                        x=x,
                        y=y,
                        hue=hue,
                        size=size,
                        palette=self.palette if hue else None
                        )

        # Set chart information
        plt.title(title, fontsize = 16, weight = 'bold')
        plt.xlabel(xlabel, fontsize = 16)
        plt.ylabel(ylabel, fontsize = 16)

        # Customize the legend if hue or size is provided
        if hue or size:
            legend_title = legend_title or (hue if hue else size)
            plt.legend(title = legend_title, loc = legend_loc, bbox_to_anchor = legend_bbox)

        plt.grid(True, alpha = 0.3)
        plt.tight_layout()

        plt.show()




    # Check the default setting of the class
    def get_figure_info(self) -> Dict[str, Any]:
        return {
            "figure": self.figsize,
            "style": self.style,
            'palette': self.palette
        }


