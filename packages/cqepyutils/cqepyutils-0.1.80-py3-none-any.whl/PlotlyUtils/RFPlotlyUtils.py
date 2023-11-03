import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from robot.api.deco import keyword
from robot.api import logger
import matplotlib.pyplot as plt
import seaborn as sns


@keyword('Visualize Data')
def visualize_data(*dataframes, x_col: str, y_col: str,
                   plot_type: str = 'bar', titles: list = None, plot_name: str = 'Trace') -> None:
    """
    Visualizes query results as a plot and displays them as a DataFrame.

    Args:
        *dataframes (pd.DataFrame): Variable number of Pandas DataFrames.
        x_col (str): The name of the column to use for the x-axis of the plot.
        y_col (str): The name of the column to use for the y-axis of the plot.
        plot_type (str, optional): The type of plot to use. Default is 'bar', but can be 'line', 'scatter', etc.
        titles (list, optional): A list of titles for each table. Default is None.
        plot_name (str, optional): The name of the trace in the plot. Default is 'Trace'.

    Examples:
        | *Keyword*          | *Arguments*                                                               |
        | `Visualize Data`   | dataframe=x, dataframe2=y, x_col=column_name_1, y_col=column_name_2, plot_type='bar', titles=['Table 1', 'Table 2'], plot_name='Trace' |
        | `Visualize Data`   | dataframe=x, dataframe2=y, x_col=column_name_3, y_col=column_name_4, plot_type='scatter', titles=['Table A', 'Table B'], plot_name='Data' |
        | `Visualize Data`   | dataframe=x, dataframe2=y, x_col=column_name_5, y_col=column_name_6, plot_type='line', titles=['Table X', 'Table Y'], plot_name='Line Data' |
    """

    num_dataframes = len(dataframes)

    if titles is None or len(titles) != num_dataframes:
        titles = ['Table {}'.format(i + 1) for i in range(num_dataframes)]

    logger.info(f'Step - 1: Starting data visualization for {num_dataframes} dataframes.')

    if num_dataframes == 1:
        # If only one dataframe is provided, display it in the center
        fig = go.Figure(data=[go.Table(
            header=dict(values=[col.replace('_', ' ').capitalize() for col in dataframes[0].columns],  # Modify headers
                        fill_color='rgb(30, 53, 76)',
                        font=dict(color='white')),
            cells=dict(values=dataframes[0].T.applymap(lambda x: f'<b>{x}</b>').values.tolist(),  # Center-align values
                       fill_color=[[['#f2f2e8', '#ffffff'][i % 2] for i in range(len(dataframes[0]))]],
                       font=dict(color='black'))
        )])
        fig.update_layout(title=titles[0])
    else:
        # If multiple dataframes are provided, create subplots in a grid layout
        num_rows = (num_dataframes + 1) // 2
        fig = make_subplots(rows=num_rows, cols=2, specs=[[{'type': 'domain'}, {'type': 'domain'}]] * num_rows)

        for i, (dataframe, title) in enumerate(zip(dataframes, titles)):
            row = (i // 2) + 1
            col = (i % 2) + 1

            table = go.Table(
                header=dict(values=[col.replace('_', ' ').capitalize() for col in dataframe.columns],  # Modify headers
                            fill_color='rgb(30, 53, 76)',
                            font=dict(color='white')),
                cells=dict(values=dataframe.T.applymap(lambda x: f'<b>{x}</b>').values.tolist(),  # Center-align values
                           fill_color=[[['#f2f2e8', '#ffffff'][i % 2] for i in range(len(dataframe))]],
                           font=dict(color='black'))
            )

            fig.add_trace(table, row=row, col=col)
            fig.update_xaxes(title_text=title, row=row, col=col)  # Update x-axis title
            fig.update_yaxes(title_text='', row=row, col=col)  # Remove y-axis title

    # Update layout
    fig.update_layout(
        height=500 * ((num_dataframes + 1) // 2) if num_dataframes > 1 else 500,
        margin=dict(t=50, l=50, r=50),
    )
    fig.show()
    logger.info(f'Step - 2: Data visualization complete for {num_dataframes} dataframes.')


@keyword('Visualize Combined Data')
def visualize_data_combined(dataframe1: pd.DataFrame, dataframe2: pd.DataFrame, x_col1: str, y_col1: str, x_col2: str, y_col2: str) -> None:
    """
    Visualizes query results as a plot and displays them as a DataFrame.

    Args:
        dataframe1 (pd.DataFrame): First Pandas DataFrame.
        dataframe2 (pd.DataFrame): Second Pandas DataFrame.
        x_col1 (str): The name of the column to use for the x-axis of the first Seaborn plot.
        y_col1 (str): The name of the column to use for the y-axis of the first Seaborn plot.
        x_col2 (str): The name of the column to use for the x-axis of the second Seaborn plot.
        y_col2 (str): The name of the column to use for the y-axis of the second Seaborn plot.

    Examples:
        | *Keyword*                | *Arguments*                                                                   |
        | `Visualize Combined Data` | dataframe1=x, dataframe2=y, x_col1=column_name_1, y_col1=column_name_2, x_col2=column_name_3, y_col2=column_name_4 |
    """

    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{'type': 'xy'}, {'type': 'xy'}],
               [{'type': 'table', 'colspan': 2}, None]],
        subplot_titles=('Seaborn Chart 1', 'Seaborn Chart 2', 'Dataframe 1', 'Dataframe 2')
    )

    # Generate Seaborn plots and add them to the first row
    plt.figure(figsize=(8, 6))
    sns.barplot(x=x_col1, y=y_col1, data=dataframe1)
    ax1 = plt.gca()
    ax1.get_xaxis().set_visible(False)
    ax1.get_yaxis().set_visible(False)
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers'), row=1, col=1)  # Placeholder for Seaborn chart
    plt.close()

    plt.figure(figsize=(8, 6))
    sns.barplot(x=x_col2, y=y_col2, data=dataframe2)
    ax2 = plt.gca()
    ax2.get_xaxis().set_visible(False)
    ax2.get_yaxis().set_visible(False)
    fig.add_trace(go.Scatter(x=[None], y=[None], mode='markers'), row=1, col=2)  # Placeholder for Seaborn chart
    plt.close()

    # Convert data frames to Plotly tables and add them to the second row
    table_trace1 = go.Table(
        header=dict(values=list(dataframe1.columns), fill_color='rgb(30, 53, 76)', font=dict(color='white')),
        cells=dict(values=dataframe1.T.applymap(lambda x: f'<b>{x}</b>').values.tolist(),
                   fill_color=[[['#f2f2e8', '#ffffff'][i % 2] for i in range(len(dataframe1))]],
                   font=dict(color='black'))
    )

    table_trace2 = go.Table(
        header=dict(values=list(dataframe2.columns), fill_color='rgb(30, 53, 76)', font=dict(color='white')),
        cells=dict(values=dataframe2.T.applymap(lambda x: f'<b>{x}</b>').values.tolist(),
                   fill_color=[[['#f2f2e8', '#ffffff'][i % 2] for i in range(len(dataframe2))]],
                   font=dict(color='black'))
    )

    fig.add_trace(table_trace1, row=2, col=1)
    fig.add_trace(table_trace2, row=2, col=2)

    # Update layout
    fig.update_layout(
        height=800,
        title_text="Combined Data Visualization",
        showlegend=False
    )

    # Show the figure
    fig.show()
