
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

plt.style.use('fivethirtyeight')

# Read CSV and plot data for visualization
def animate(i):
    data = pd.read_csv('data.csv')
    x = data['TIME']
    y1 = data['BTC_USD_KRAKEN']
    y2 = data['BTC_USD_BITSTAMP']

    plt.cla()

    plt.plot(x, y1, marker = '*', label='BTC_USD_KRAKEN')
    plt.plot(x, y2, marker = 'o', label='BTC_USD_BITSTAMP')

    plt.xlabel('Time')
    plt.ylabel('BTC Price in USD')
    plt.title('Real-time BTC Price in Exchanges')

    plt.legend(loc='upper left')
    plt.tight_layout()


anim = animation.FuncAnimation(plt.gcf(), animate)

plt.tight_layout()
plt.show()