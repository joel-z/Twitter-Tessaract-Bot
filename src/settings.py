# We use this in case the coin pumps so hard that from the time we retrieve prices to the time we buy the coin, the
# price moved by 20% for example, so we discount the volitality for the buy quantity to set higher bid price
# by 20% in this setting:
volitality_threshold = 1.2

# Bitcion buy quantity
# The bot will buy the coin with <bitcoin_buy_quantity/volitality_threshold> up to <bitcoin_buy_quantity> bitcoin.
bitcoin_buy_quantity = 0.1

# Sell order will be placed at <price> * <sell_order_multiplier>, meaning that if it is set to 2, it will sell at 100% gains, if at 1.5, it will sell for 50%
sell_order_multiplier = 2

coin_of_the_day_filter = True


# Should have trade permissions
# Create bittrex auth at https://bittrex.com/Manage#sectionApi
class BittrexAuth:
    api_key = "1"
    api_secret = "1"


# Create twitter auth at https://apps.twitter.com/
class TwitterAuth:
    consumer_key = "SY6yBWjAclcTNOFtiFONWnvnH"
    consumer_secret = "BTl48rHf99Gbga6DOo07GnlzsdD95gkN0MBTqVssBYdrR3vdyd"
    access_token = "942365078871007233-k6FTu0D1kik8DBKtbbTupch6zmLFWrq"
    access_token_secret = "iRvdE16bOJTkLSYkzJAqJCQA4qEMAtlwZqawYBhQYsJFQ"


assert len(BittrexAuth.api_key) > 0
assert len(BittrexAuth.api_secret) > 0
assert len(TwitterAuth.consumer_key) > 0
assert len(TwitterAuth.consumer_secret) > 0
assert len(TwitterAuth.access_token) > 0
assert len(TwitterAuth.access_token_secret) > 0
