import pickle
import os


class PumpedCoins:
    # We avoid buying coins already pumped in case Mr. McAfee tweets about said coins again

    __pumped_coins_path = os.path.join(os.path.dirname(__file__), "pumped_coins.txt")
    with open(__pumped_coins_path, 'rb') as f:
        pumped_coins = pickle.load(f)

    @classmethod
    def add(cls, coin):
        cls.pumped_coins.append(coin)
        with open(cls.__pumped_coins_path, 'wb') as f:
            pickle.dump(cls.pumped_coins, f)
