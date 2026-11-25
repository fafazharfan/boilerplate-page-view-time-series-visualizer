import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv', parse_dates=['date'], index_col='date')

# Clean data
df = df[
    (df['value'] >= df['value'].quantile(0.025)) &
    (df['value'] <= df['value'].quantile(0.975))
]

def draw_line_plot():
    # Draw line plot
    fig, ax = plt.subplots(figsize=(16,6))
    ax = sns.lineplot(data=df, x='date', y='value', ax=ax)
    ax.set(xlabel='Date', ylabel='Page Views')
    ax.set_title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy().reset_index()
    df_bar['year'] = df_bar.date.dt.year
    df_bar['month'] = df_bar.date.dt.month_name()
    months = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
    df_bar = df_bar.groupby(['year', 'month'])['value'].mean().unstack()
    df_bar = df_bar[months]

    df_long = df_bar.reset_index().melt(
        id_vars = 'year',
        var_name = 'month',
        value_name = 'value'
    )

    # Draw bar plot
    fig, ax = plt.subplots(figsize=(14, 6))
    df_bar.plot(kind='bar', ax=ax)
    ax.set(xlabel='Years', ylabel='Average Page Views')
    plt.legend(title='Months')

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    sns.boxplot(ax=ax1, data=df_box, x=df_box['year'], y=df_box['value'])
    ax1.set(xlabel='Year', ylabel='Page Views', title='Year-wise Box Plot (Trend)')

    sns.boxplot(ax=ax2, data=df_box, x=df_box['month'], y=df_box['value'],
                order=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                       'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
                )
    ax2.set(xlabel='Month', ylabel='Page Views', title='Month-wise Box Plot (Seasonality)')

    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig