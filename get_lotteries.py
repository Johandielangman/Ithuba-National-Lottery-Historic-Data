#! /c/Python311/python
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~
#      /\_/\
#     ( o.o )
#      > ^ <
#
# Author: Johan Hanekom
# Date: November 2024
#
# ~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~^~


from datetime import datetime
import concurrent.futures
import pandas as pd
import requests
import json
import os
from typing import (
    Dict,
    List
)

# Some constants

GET_LOTTERY_DATA_LINK: str = "https://www.nationallottery.co.za/index.php?task=results.redirectPageURL&Itemid=265"
OUTPUT_DIR: str = os.path.join(os.path.dirname(__file__), "data", "raw")
NUM_WORKERS: int = 15


def get_lotto_data(
    draw_number: str
) -> Dict:
    payload: Dict[str, str] = {
        'drawNumber': draw_number,
        'gameName': 'LOTTO',
        'isAjax': 'true'
    }

    response: requests.Response = requests.request(
        "POST",
        GET_LOTTERY_DATA_LINK,
        data=payload
    )
    return response.json()


class LotteryHistory:
    """A simple class used to fetch all the historic lotteries. The main data point of interest is the draw number"""
    base_url: str = "https://www.nationallottery.co.za/index.php?task=results.getHistoricalData&Itemid=265"
    limit: int = 10_000  # make sure I miss nothing!

    def __init__(
        self,
        start_date: datetime,
        end_date: datetime,
        game_name: str = 'LOTTO',
    ) -> None:
        """Constructor for the LotteryHistory class

        Args:
            start_date (datetime): The start date of the lottery
            end_date (datetime): The end date of the lottery
            game_name (str, optional): The name of the game. Defaults to 'LOTTO'.
        """
        self.start_date = start_date
        self.end_date = end_date
        self.game_name = game_name

    def get_lotteries(self) -> Dict:
        """Fetches all the historic lotteries

        Returns:
            Dict: The historic lotteries
        """

        payload: Dict[str, str] = {
            'gameName': self.game_name,
            'startDate': self.start_date.strftime('%d/%m/%Y'),
            'endDate': self.end_date.strftime('%d/%m/%Y'),
            'offset': '0',
            'limit': str(self.limit),
            'isAjax': 'true',
            'isAjax': 'true'
        }

        response: requests.Response = requests.request(
            "POST",
            self.base_url,
            data=payload
        )

        return response.json()


if __name__ == "__main__":
    print("Fetching the historic lotteries")
    start_date: datetime = datetime(2000, 1, 1)
    end_date: datetime = datetime.now()

    lottery_history: LotteryHistory = LotteryHistory(start_date, end_date)
    lotteries: Dict = lottery_history.get_lotteries()
    # print(lotteries)
    print(f"Fetched {len(lotteries)} historic lotteries")

    draw_numbers: List[str] = [lottery['drawNumber'] for lottery in lotteries['data']]

    all_lottery_data: List[Dict] = []
    semi_clean_lottery_data: List[Dict] = []
    failed_draw_numbers: List[str] = []
    n_total: int = len(draw_numbers)
    n_success: int = 0
    n_failed: int = 0

    with concurrent.futures.ThreadPoolExecutor(max_workers=NUM_WORKERS) as executor:
        future_to_draw_number: Dict[concurrent.futures.Future, str] = {
            executor.submit(get_lotto_data, draw_number): draw_number
            for draw_number in draw_numbers
        }
        for future in concurrent.futures.as_completed(future_to_draw_number):
            draw_number: str = future_to_draw_number[future]
            try:
                data: Dict = future.result()
                all_lottery_data.append(data)
                semi_clean_lottery_data.append(data.get('data', {}).get('drawDetails', {}))
            except Exception as exc:
                print(f"Draw number {draw_number} generated an exception: {exc}")
                failed_draw_numbers.append(draw_number)
                n_failed += 1
            else:
                n_success += 1
            finally:
                print(f"Processed {n_success + n_failed}/{n_total} draw numbers")

    print("-" * 50)
    print(f"Successfully fetched {n_success} lotteries")
    print(f"Failed to fetch {n_failed} lotteries")
    print("-" * 50)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if all_lottery_data:
        with open(os.path.join(OUTPUT_DIR, "lotteries.json"), "w") as f:
            json.dump(all_lottery_data, f)

    if semi_clean_lottery_data:
        df: pd.DataFrame = pd.DataFrame(semi_clean_lottery_data)
        df.to_csv(
            os.path.join(OUTPUT_DIR, "lotteries.csv"),
            index=False
        )

    if failed_draw_numbers:
        with open(os.path.join(OUTPUT_DIR, "failed_draw_numbers.json"), "w") as f:
            json.dump(failed_draw_numbers, f)
