![banner](docs/images/banner.png)

![R](https://img.shields.io/badge/r-%23276DC3.svg?style=for-the-badge&logo=r&logoColor=white)

# 🎱 SA National Lottery Analysis

The national lottery is so interesting to me. I don't think I'll ever play it, but the data behind it looks interesting!
There are websites that love to show what the draw frequency of the numbers are:
- https://www.lotteryextreme.com/south_africa/lotto-statistics
- https://www.lotteryresults.co.za/tools/lotto/number-analysis

But I'm quite curious about the financial side! How many winners are there? What are they paid? What does the rollover look like over time? Can you see a type of money-in-money-out analysis? Many South Africans play this thing.

This is quite interesting:
- More than 60% of lottery players have household incomes less than R10,000 (See: [IOL](https://www.iol.co.za/news/south-africa/most-lottery-players-in-sa-live-off-less-than-r10k-per-month-38500627))
- Nearly 28% of the people who play the lottery are unemployed. (See: [IOL](https://www.iol.co.za/news/south-africa/most-lottery-players-in-sa-live-off-less-than-r10k-per-month-38500627))
- This showed that seven out of 10 people played the Lottery regularly (See: [NLCSA](https://www.nlcsa.org.za/our-history/))

Anywhoo! I was on the lottery's history page, ready to make a bot:
- https://www.nationallottery.co.za/lotto-history

And then I saw in my "networks tab" what API calls they make to their backend... then I thought "hmm this is quite simple... can I write a Python script that can get all the lotteries in history with this loophole?"

The answer is yes! I got all 975 available lotteries up to 2015/06/03! 🙂

Run the script `get_lottery_data.py` to get the data. It will save it to a CSV file.


---

Made with ❤️ by [Johandielangman](https://github.com/Johandielangman)
