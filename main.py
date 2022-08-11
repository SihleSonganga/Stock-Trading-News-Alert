import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
stock_api_key = "LGIFGHSQUDMJADT7"
news_api_key = "092623db77c14609a1629069986f0116"
frequency = "Time_Series_Daily"
TWILIO_SID = "AC7599ea7a6b3b85f69f6ee703e8899e1a"
TWILIO_AUTH_TOKEN = "61ec012dc9324641d790ba7ef36bf0b1"

stock_parameters = {
    "function": frequency,
    "symbol": STOCK_NAME,
    "apikey": stock_api_key
}

news_parameters = {
    "apikey": news_api_key,
    "q": "tesla"
}

# gets yesterday's closing stock price
response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
response.raise_for_status()

data = response.json()["Time Series (Daily)"]
stock_data_list = [value for (key, value) in data.items()]
yesterday_data = stock_data_list[0]
yesterday_closing_price = float(stock_data_list[0]["4. close"])


# day before yesterday closing stock price
day_before_yesterday_closing_price = float(stock_data_list[2]["4. close"])


# find positive difference between yesterday stock price and day before yesterday
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
difference = float(abs(difference))

# workout percentage increase
difference_percentage = float(difference / yesterday_closing_price) * 100



# get news articles
if difference_percentage > 1:
    news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    articles = news_response.json()["articles"]
    three_articles = articles[:3]
    print(three_articles)


formatted_articles = [f"Headline: {article['title']}, \nBrief: {article['description']}" for article in three_articles]


# send each article as separate message via twilio
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

for article in formatted_articles:
    message = client.messages.create(
        body=article,
        from_="+13344876456",
        to="+27731142432"
    )

#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

