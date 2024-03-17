from tkinter import messagebox
import requests
from tkinter import *


STOCK_NAMES = ["AMZN", "AAPL", "TSLA"]
COMPANY_NAMES = ["Amazon.com Inc", "Apple Inc", "Tesla Inc"]
STOCK_MARKETS = ["NASDAQ", "NASDAQ", "NASDAQ"]
ASSET_TYPES = ["Stock", "Stock", "Stock"]
IPO_DATES = ["1997-05-15", "1980-12-12", "2010-06-29"]

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "your-api-key"
NEWS_API_KEY = "your-api-key"

BG = "#EEE2DE"
BG2 = "#B6BBC4"
SC = "#2541B2"
CC = "#1768AC"

window = Tk()
window.title("Stock Trading News")
window.geometry("900x730")
window.config(padx=25, pady=25, bg=BG)

textbox_stock = Entry(bg=BG, width=80)
textbox_stock.insert(0, "Please enter a stock name.")
textbox_stock.grid(column=0, row=0, columnspan=2)


def get_stock():
    input = textbox_stock.get().upper()
    if input in STOCK_NAMES:
        stock_params = {
            "function": "TIME_SERIES_DAILY",
            "symbol": input,
            "apikey": STOCK_API_KEY,
        }

        response = requests.get(STOCK_ENDPOINT, params=stock_params)
        # print(response)
        response.raise_for_status()
        data = response.json()["Time Series (Daily)"]
        # print(data)
        data_list = [value for (key, value) in data.items()]
        time_list = [key for (key, value) in data.items()]
        yesterday_time = time_list[0]
        # print(yesterday_time)
        a_day_before_time = time_list[1]
        yesterday_data = data_list[0]
        # print(yesterday_data)
        yesterday_closing_price = yesterday_data["4. close"]
        # print(yesterday_closing_price)

        # Get the day before yesterday's closing stock price
        day_before_yesterday_data = data_list[1]
        day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
        # print(day_before_yesterday_closing_price)

        difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
        # print(difference)

        # Work out the percentage difference in price between closing price yesterday
        # and closing price the day before yesterday.
        diff_percent = (difference / float(yesterday_closing_price)) * 100
        # print(diff_percent)

        i = STOCK_NAMES.index(input)
        company = COMPANY_NAMES[i]
        stock_market = STOCK_MARKETS[i]
        ipo_date = IPO_DATES[i]
        asset_type = ASSET_TYPES[i]

        stock_label.config(text=f"___________\n\n{textbox_stock.get().upper()}\n___________")
        company_label.config(text=f"Company: {company}")
        market_label.config(text=f"Stock Market: {stock_market}")
        asset_label.config(text=f"Asset Type: {asset_type}")
        ipo_label.config(text=f"Ipo Date: {ipo_date}")
        stock_yesterday.config(text=f"Time: {yesterday_time} Price: {yesterday_closing_price}")
        stock_a_day_before.config(text=f"Time: {a_day_before_time} Price: {day_before_yesterday_closing_price}")
        difference_label.config(text=f"%{diff_percent:.2f}")
        if difference > 0:
            canvas.itemconfig(image_diff, image=up_image)
        else:
            canvas.itemconfig(image_diff, image=down_image)

        get_news(diff_percent, company)

    else:
        messagebox.showinfo(title="Warning", message="Please enter a valid stock name.")


def get_news(percent, company):
    if abs(percent) >= 0:
        news_params = {
            "apiKey": NEWS_API_KEY,
            "qInTitle": company,
        }

        news_response = requests.get(NEWS_ENDPOINT, params=news_params)
        articles = news_response.json()["articles"]

        # Use Python slice operator to create a list that contains the first 3 articles.
        three_articles = articles[:3]
        for article in three_articles:
            if article == "":
                formatted_articles = [f"{textbox_stock.get().upper()} \nHeadline: This not any news about this stock."]
            else:
                formatted_articles = [(f"{textbox_stock.get().upper()}: \nHeadline: {article['title']}. "
                                       f"\n\nBrief: {article['description']}") for article in three_articles]
            news_information.config(text=f"\n{formatted_articles[0]}", wraplength=300)


# ***************************************UI SETUP *************************************** #

button_enter = Button(text="Enter", width=15, font=("Times", "10", "bold italic"),
                      fg="black", bg=BG, command=get_stock)
button_enter.grid(column=4, row=0)

stock_label = Label(text="___________\n\nSTOCK\n___________", font=("Times", "30", "bold italic"), fg=SC, bg=BG)
stock_label.config(padx=20, pady=20)
stock_label.grid(column=1, row=1, rowspan=2)

company_label = Label(text="Company: _________________________", font=("Times", "10", "bold italic"), fg=CC,
                      bg=BG, wraplength=300)
company_label.config(padx=20, pady=20)
company_label.grid(column=0, row=4, columnspan=3)

market_label = Label(text="Stock Market: ________________________", font=("Times", "10", "bold italic"), fg=CC, bg=BG)
market_label.grid(column=0, row=5, columnspan=2)

asset_label = Label(text="Asset Type: __________________________", font=("Times", "10", "bold italic"), fg=CC, bg=BG)
asset_label.config(padx=20, pady=20)
asset_label.grid(column=0, row=6, columnspan=2)

ipo_label = Label(text="Ipo Date: ____________________________", font=("Times", "10", "bold italic"), fg=CC, bg=BG)
ipo_label.config(padx=10, pady=10)
ipo_label.grid(column=0, row=7, columnspan=2)

stock_yesterday = Label(text="Time: 0000-00-00 Price: 0$", font=("Times", "12", "bold italic"), fg="Black", bg=BG)
stock_yesterday.grid(column=2, row=3, columnspan=3)

stock_a_day_before = Label(text="Time: 0000-00-00 Price: 0$", font=("Times", "12", "bold italic"), fg="Black", bg=BG)
stock_a_day_before.grid(column=2, row=4, columnspan=3)

difference_label = Label(text="%0", font=("Times", "20", "bold italic"), fg="Black", bg=BG)
difference_label.grid(column=3, row=2)

canvas = Canvas(width=114, height=140, bg=BG, highlightthickness=0)
start = PhotoImage(file="images/start.png")
up_image = PhotoImage(file="images/up.png")
down_image = PhotoImage(file="images/down.png")
image_diff = canvas.create_image(57, 70, image=start)
canvas.grid(column=4, row=2)

news_title = Label(text="\n\nNEWS", font=("Times", "15", "bold italic"), fg=BG2, bg=BG)
news_title.grid(column=1, row=8, columnspan=4)

news_information = Label(text="\n\n____________________________________________________________________",
                         font=("Times", "9", "italic"), fg="Black", bg=BG)
news_information.grid(column=1, row=9, columnspan=4)

window.mainloop()
