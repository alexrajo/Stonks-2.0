import tkinter as tk
import stockscraper
import backtester
import manager
#from PIL import ImageTk, Image

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        master.minsize(500, 600)
        self.pack()
        self.backtester = backtester.Backtester()

        self.top_menu = None
        self.windows = {}
        self.current_window = "welcome"
        self.top_buttons = [
            #{"text": "Find stocks", "window_name": "stockfinder"},
            {"text": "Backtest", "window_name": "backtest"},
            #{"text": "Paper trading", "window_name": "papertrade"}
        ]

        self.backtest_inputs = {
            "stock": None,
            "stock_txt": None,
            "strategy": None,
            "start_capital": None
        }
        self.backtest_result_label = None
        self.backtest_result_var = tk.StringVar()

        self.bt_stocks = [
            "EURONEXT/EQNR", "EURONEXT/RECSI", "EURONEXT/NEL", "EURONEXT/KOA", "EURONEXT/SALME", "EURONEXT/AOW",
            "EURONEXT/NHY", "EURONEXT/AKRBP"
        ]
        self.strategies = []
        for s in manager.s:
            self.strategies.append(s)

        self.setup_ui()

    def setup_ui(self):
        # Top menu
        self.top_menu = tk.Frame(self.master)
        self.top_menu.pack(fill="both", ipady=10)

        def create_topbutton(info):
            btn = tk.Button(self.top_menu, bg="white", text=info["text"], command=lambda: self.open_menu(info["window_name"]))
            btn.pack(expand=True, fill="both", side=tk.LEFT)

        for btn_info in self.top_buttons:
            create_topbutton(btn_info)

        # Welcomescreen
        frame = tk.Frame(self.master, bg="#a0d7c7")
        self.windows["welcome"] = frame

        # cnv = tk.Canvas(frame)
        # cnv.pack(expand=True, fill="both")
        # sminem = ImageTk.PhotoImage(Image.open("media/sminem.png"))
        # cnv.create_image(0, 0, image=sminem, anchor=tk.NW)
        frame.pack(expand=True, fill="both")

        # Stockfinder
        frame = tk.Frame(self.master, bg="#d5e9d0")
        listframe = tk.Frame(frame, bg="gray")
        buttonframe = tk.Frame(frame, bg="black")

        listframe.pack(expand=True, fill="both", side=tk.LEFT)
        buttonframe.pack(fill="both", side=tk.RIGHT, ipadx=100)

        def create_stock_frame(info):
            frame = tk.Frame(listframe, bg="white", highlightbackground="black", highlightthickness=1)
            frame.pack(expand=True, fill="x", side="top", ipady=20)

            symbol_label = tk.Label(frame, text=info["symbol"])
            name_label = tk.Label(frame, text=info["name"])

            percent_change = info["percent_change"]
            prc_color = "black"
            if percent_change[0] == "+":
                prc_color = "green"
            elif percent_change[0] == "-":
                prc_color = "red"

            percent_change_label = tk.Label(frame, text=percent_change, fg=prc_color)

            symbol_label.pack(expand=True, fill="both", side="left")
            name_label.pack(expand=True, fill="both", side="left")
            percent_change_label.pack(expand=True, fill="both", side="left")

        stocks = [] # stockscraper.get_stocks("most-active", 20)
        for stock in stocks:
            create_stock_frame(stock)

        self.windows["stockfinder"] = frame

        # Backtesting
        frame = tk.Frame(self.master, bg="#a0d7c7")
        self.windows["backtest"] = frame

        options_container = tk.Frame(frame, bg="black")
        options_container.pack(expand=True, fill="both", anchor="center", padx=100, pady=50)
        title_label = tk.Label(options_container, bg="white", text="Options", font=("Calibri", 30))
        title_label.pack(expand=True, fill="x", ipady=5, anchor="n")

        options_inner_container = tk.Frame(options_container)
        options_inner_container.pack(expand=True, fill="x", anchor="center", padx=20, ipady=50)

        def create_dropdown_menu(title, input_type, options):
            o_title = tk.Label(options_inner_container, text=title, font=("Calibri", 14))
            o_title.pack()
            self.backtest_inputs[input_type] = tk.StringVar()
            self.backtest_inputs[input_type].set(options[0])
            o_input = tk.OptionMenu(options_inner_container, self.backtest_inputs[input_type], *options)
            o_input.pack()


        create_dropdown_menu(title="Stock:", input_type="stock", options=self.bt_stocks)
        ticker_input_txt = tk.Entry(options_inner_container, text="Input ticker")
        ticker_input_txt.pack()
        self.backtest_inputs["stock_txt"] = ticker_input_txt

        create_dropdown_menu(title="Strategy:", input_type="strategy", options=self.strategies)

        o_title = tk.Label(options_inner_container, text="Start capital:", font=("Calibri", 14))
        o_title.pack()
        o_input = tk.Entry(options_inner_container)
        o_input.pack()
        self.backtest_inputs["start_capital"] = o_input

        self.backtest_result_label = tk.Label(options_inner_container, textvariable=self.backtest_result_var, font=("Calibri", 16))
        self.backtest_result_label.pack()

        run_btn = tk.Button(options_container, text="Run backtest", font=("Calibri", 20), command=self.run_backtest)
        run_btn.pack(expand=True, fill="x", anchor="s")

        # Paper trading
        frame = tk.Frame(self.master, bg="#b5a7c7")
        self.windows["papertrade"] = frame

    def open_menu(self, window_name):
        if window_name == self.current_window:
            return

        frame = self.windows[window_name]
        if frame is None:
            return

        if self.current_window is not None:
            old_frame = self.windows[self.current_window]
            if old_frame:
                old_frame.pack_forget()

        frame.pack(expand=True, fill="both")
        self.current_window = window_name

    def run_backtest(self):
        stock = self.backtest_inputs["stock_txt"].get() or self.backtest_inputs["stock"].get()
        strategy = self.backtest_inputs["strategy"].get()
        start_capital = self.backtest_inputs["start_capital"].get() or 0
        start_capital = int(start_capital)

        result = self.backtester.run_test(stock=stock, strategy=strategy, capital=start_capital)
        self.backtest_result_var.set("Porfolio start: {} \n Portfolio end: {} \n Change: {}%".format(result["start"], result["end"], result["percent_change"]))


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry("500x600")
    root.title("Stonks")
    app = Application(master=root)
    app.mainloop()
