import matplotlib.pyplot as plt
import seaborn as sns

class LiveChart:
    def __init__(self, subject, title, style="darkgrid", size=(8, 5), num_axs=1, gridspec=None):
        self.subject = subject
        self.title = title
        self.num_axs = num_axs
        self.is_open = True

        # to run GUI event loop
        plt.ion()

        # Set the Seaborn style
        sns.set(style=style)

        # Set Face Colors
        # sns.set(rc={'axes.facecolor':sns.color_palette("Greys_r")[0], 'figure.facecolor':sns.color_palette("Greys_r")[0]})

        # here we are creating sub plots
        self.fig, self.axs = plt.subplots(num_axs, figsize=size, gridspec_kw=gridspec)
        if num_axs == 1:
            self.axs = [self.axs]

        # delete me when closed
        self.fig.canvas.mpl_connect('close_event', self.close)


    def plot_graph(self):
        raise NotImplementedError()
    
    def update(self):
        for i in range(self.num_axs):
            self.axs[i].clear()
    
        # plot graph
        self.plot_graph()

        # rotating the x-axis tick labels at 30degree 
        # towards right
        plt.xticks(rotation=30, ha='right')

        # adjust subplot to fit frame
        plt.tight_layout()
        
        # drawing updated values
        self.fig.canvas.draw()

        # This will run the GUI event
        # loop until all UI events
        # currently waiting have been processed
        self.fig.canvas.flush_events()

    def close(self, event):
        print(f"Closed a Chart: {self.title}")
        self.is_open = False


class ComparisonChart(LiveChart):
    def __init__(self, market, tickers, kind='Adj Close'):
        ohlcv = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
        if not kind in ohlcv:
            raise ValueError()
        self.kind = kind
        self.tickers = tickers
        title = f"Line Chart ({kind})"
        super().__init__(market, title)

    def plot_graph(self):
        # setting title
        self.axs[0].set_title(self.title, fontsize=20)

        # setting x-axis label and y-axis label
        self.axs[0].set_xlabel('Price (USD)')
        self.axs[0].set_ylabel('Datetime')

        # plot graph for each ticker
        for ticker in self.tickers:
            data = self.subject.get_ohlcv_series(ticker, self.kind)
            self.axs[0].plot(data.index, data, label=ticker)
            self.axs[0].legend(loc='upper left', fancybox=True, framealpha=0.5)


class CandleChart(LiveChart):
    def __init__(self, market, ticker):
        self.ticker = ticker
        title = f"Candle Chart ({ticker}, {market.frequency})"
        super().__init__(market, title, size=(8, 6), num_axs=2, gridspec={'height_ratios':[4,1]})

    def plot_graph(self):
        # setting title
        self.axs[0].set_title(self.title, fontsize=20)

        # setting x-axis label and y-axis label
        self.axs[0].set_ylabel('Price (USD)')
        self.axs[0].get_xaxis().set_visible(False)
        self.axs[1].set_xlabel('Datetime')
        self.axs[1].set_ylabel('Volume')
        self.axs[1].get_yaxis().set_visible(False)
        data = self.subject.get_ohlcv_dataframe(self.ticker)

        # plot candle
        up = data[data['Adj Close'] >= data.Open]
        down = data[data['Adj Close'] < data.Open]

        col1 = 'green'
        col2 = 'red'

        width = .85
        width2 = .065

        # plotting up prices of the stock
        self.axs[0].bar(up.index, up['Adj Close']-up.Open, width, bottom=up.Open, color=col1, linewidth=0)
        self.axs[0].bar(up.index, up.High-up['Adj Close'], width2, bottom=up['Adj Close'], color=col1, linewidth=0)
        self.axs[0].bar(up.index, up.Low-up.Open, width2, bottom=up.Open, color=col1, linewidth=0)
        
        # plotting down prices of the stock
        self.axs[0].bar(down.index, down['Adj Close']-down.Open, width, bottom=down.Open, color=col2, linewidth=0)
        self.axs[0].bar(down.index, down.High-down.Open, width2, bottom=down.Open, color=col2, linewidth=0)
        self.axs[0].bar(down.index, down.Low-down['Adj Close'], width2, bottom=down['Adj Close'], color=col2, linewidth=0)

        # plot volume bar
        volume_data = self.subject.get_ohlcv_series(self.ticker, 'Volume')

        self.axs[1].bar(volume_data.index, volume_data)
        
        
    



        

