import pandas as pd
import matplotlib.pyplot as plt

def plot_allocation(weights, tickers, show_plot=True):
    # Create DataFrame
    df = pd.DataFrame({
        'Ticker': tickers,
        'Allocation (%)': weights * 100
    })
    df['Allocation (%)'] = df['Allocation (%)'].round(2)

    # Data for pie chart — only > 0%
    df_pie = df[df['Allocation (%)'] > 0]

    # Create figure & axes
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    # Pie chart
    explode = [0.03] * len(df_pie)
    ax1.pie(
        df_pie['Allocation (%)'],
        labels=df_pie['Ticker'],
        autopct='%1.1f%%',
        startangle=90,
        colors=plt.cm.Set3.colors,
        wedgeprops={'edgecolor': 'white'},
        explode=explode
    )
    ax1.set_title("Optimal Portfolio Allocation", fontsize=14, fontweight='bold')

    # Table
    ax2.axis('off')
    table = ax2.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc='center',
        loc='center'
    )
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1, 1.2)
    ax2.set_title("Allocation Table", fontsize=14, fontweight='bold')

    plt.tight_layout()


    if show_plot:
        plt.show(block=True)

    return fig 
