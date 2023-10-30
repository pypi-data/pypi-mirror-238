
import pandas as pd
import pyqstrat as pq
import numpy as np


def build_example_strategy(stop_pct: float = -0.002, ret_threshold: float = 0.002) -> pq.Strategy:
    # read 1 minute price bars
    filename = pq.find_in_subdir('.', 'AAPL.csv.gz')
    aapl = pd.read_csv(filename)[['timestamp', 'c']]
    aapl.timestamp = pd.to_datetime(aapl.timestamp)
    # the date corresponding to each 1minute timestamp
    aapl['date'] = aapl.timestamp.values.astype('M8[D]') 
    # compute overnight return
    aapl['overnight_ret'] = np.where(aapl.date > aapl.date.shift(1), aapl.c / aapl.c.shift(1) - 1, np.nan)
    aapl['overnight_ret_negative'] = (aapl.overnight_ret < ret_threshold)  # whether overnight return is below threshold
    # mark points just before EOD. We enter a marker order at these points so we have one bar to get filled
    aapl['eod'] = np.where(aapl.date.shift(-2) > aapl.date, True, False)  
    # if the price drops by 1% after we enter in the morning take our loss and get out
    aapl['bod_price'] = np.where(aapl.date > aapl.date.shift(1), aapl.c, np.nan)
    aapl.bod_price = aapl.bod_price.ffill()
    aapl['symbol'] = 'AAPL'
    stop_return_func = pq.PriceFuncArrays(aapl.symbol.values, aapl.timestamp.values, np.full(len(aapl), -0.1))
    aapl['stop'] = (aapl.c < (aapl.bod_price * (1 + stop_pct)))

    strat_builder = pq.StrategyBuilder(data=aapl)   
    strat_builder.add_contract('AAPL')
    # add the stop price so we can refer to it in
    strat_builder.add_series_indicator('c', 'c')
    # convert timestamps from nanoseconds (pandas convention) to minutes so they are easier to view
    timestamps = aapl.timestamp.values.astype('M8[m]')  
    prices = aapl.c.values
    # create a dictionary from contract name=>timestamp => price for use in the price function
    price_dict = {'AAPL': {timestamps[i]: prices[i] for i in range(len(timestamps))}}
    # create the price function that the strategy will use for looking up prices 
    price_function = pq.PriceFuncDict(price_dict=price_dict)
    strat_builder.set_price_function(price_function)

    # BracketOrderEntryRule allows us to enter trades and get out with a limited loss when a stop is hit.
    # This enters market orders, if you want to use limit orders, set the limit_increment argument
    entry_rule = pq.BracketOrderEntryRule(
        reason_code='POS_OVERNIGHT_RETURN',  # this is useful to know why we entered a trade
        price_func=price_function, 
        long=True,  # whether we enter a long or short position
        percent_of_equity=0.1,  # set the position size so that if the stop is hit, we lose no more than this
        # stop price is used for position sizing.  Also, we will not enter if the price is already below 
        # stop price for long trades and vice versa
        stop_return_func=stop_return_func,
        single_entry_per_day=True)  # if we are stopped out, do we allow re-entry later in the day

    # ClosePositionExitRule fully exits a position using either a market or limit order
    # In this case, we want to exit at EOD so we are flat overnight
    exit_rule_stop = pq.ClosePositionExitRule(   
        reason_code='STOPPED_OUT',
        price_func=price_function)
    
    # Exit when the stop price is reached
    exit_rule_eod = pq.ClosePositionExitRule(
        reason_code='EOD',
        price_func=price_function)

    # Setup the rules we setup above so they are only called when the columns below in our data dataframe are true
    # position filters allow you to choose when the rule runs, "zero" orders it to run only when 
    # we don't have a current position, positive and negative similarly run the rule when we
    # are currently long or short respectively
    strat_builder.add_series_rule('overnight_ret_negative', entry_rule, position_filter='zero')
    strat_builder.add_series_rule('eod', exit_rule_eod, position_filter='positive')
    strat_builder.add_series_rule('stop', exit_rule_stop, position_filter='positive')

    # create the strategy and run it
    strategy = strat_builder()
    return strategy
