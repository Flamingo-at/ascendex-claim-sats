import queue
import cloudscraper

from loguru import logger


def info(scraper: cloudscraper.CloudScraper, headers: dict):
    with scraper.get('https://ascendex.com/api/task/v3/reward/info', headers=headers) as response:
        return(int(response.json()['data']['balance']))


def worker(q: queue.Queue):
    while True:
        try:
            accounts = q.get()
            authorization, cookie = accounts.split(":")

            headers = {'authorization': authorization,
                       'cookie': f'authtoken={cookie}'}

            scraper = cloudscraper.create_scraper()

            balance_start = info(scraper, headers)

            logger.info("Take daily bonus")
            scraper.post('https://ascendex.com/api/task/v3/mining/dailyBonus',
                      json={"timeZone": "Africa/Cairo"}, headers=headers)

            balance_finish = info(scraper, headers)
            logger.info(f"Balance: {balance_finish}")

            if balance_start == balance_finish:
                raise Exception()
        except:
            with open('error.txt', 'a', encoding='utf-8') as f:
                f.write(f'{accounts}\n')
            logger.error("Error\n")
        else:
            with open('successfully.txt', 'a', encoding='utf-8') as f:
                f.write(f'{accounts}\n')
            logger.success("Successfully\n")


def main():
    accounts = open("accounts.txt", "r+").read().strip().split("\n")
    q = queue.Queue()
    for account in list(accounts):
        q.put_nowait(account)
    worker(q)


if __name__ == '__main__':
    print("Bot Ascendex Claim SATs @flamingoat\n")
    main()