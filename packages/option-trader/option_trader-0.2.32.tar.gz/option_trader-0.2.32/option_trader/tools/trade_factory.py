
import pandas as pd

from option_trader.consts   import strategy as st
from option_trader.settings import app_settings  as settings    
from option_trader.consts   import asset

from option_trader.utils.data_getter import pick_option_long, pick_option_short, afterHours
from option_trader.utils.data_getter import get_price_history,get_option_leg_details 
from option_trader.utils.data_getter import pick_vertical_call_spreads, pick_vertical_put_spreads
from option_trader.utils.data_getter import pick_call_butterfly, pick_put_butterfly, pick_iron_butterfly
from option_trader.utils.data_getter import pick_iron_condor, get_next_earning_date, get_option_exp_date
from option_trader.utils.predictor  import predict_price_range

from option_trader.settings.trade_config import entryCrit, riskManager, runtimeConfig, marketCondition

def weekly_stock_play(self):
    
    if settings.DATABASES == 'sqlite3':              

        amount = self.risk_mgr.weekly_stock_trade_amount                       

        stop_percent = self.risk_mgr.weekly_stock_trade_stop_percent

        init_balance = self.get_initial_balance()

        cash_balance = self.get_cash_position()

        if cash_balance < (stop_percent / 100)  * init_balance:
            self.logger.info('cash low than %.2f %%' % stop_percent) 
            return      

        watchlist = self.get_default_watchlist()
        if len(watchlist) == 0:
            self.logger.info('Empty watchlist!!') 
            return 
                        
        candidates = self.user.site.get_monitor_df(filter=watchlist)[['symbol', '10d change%']]
        candidates.sort_values('10d change%', inplace=True)
        symbol = candidates.head(1).symbol.values[0]

        quote = get_price_history(symbol, period='1d')

        stock_price = quote['Close'][-1]

        q = amount // stock_price

        if q <= 0:
            return
        
        trade_rec = self.create_stockSummary(symbol, quote, q)  
        
    return trade_rec


def get_watchlist_trade_targets( watchlist,
                       strategy_list,
                       risk_mgr = riskManager(),
                       entry_crit=entryCrit(),
                       runtime_config=runtimeConfig()):   

    candidates = pd.DataFrame()  # on

    for symbol in watchlist:
        df = get_trade_targets(symbol, strategy_list, risk_mgr, entry_crit, runtime_config)
        candidates = pd.concat([candidates, df])      

    return candidates

def get_trade_targets( symbol,
                       strategy_list,
                       risk_mgr = riskManager(),
                       entry_crit=entryCrit(),
                       runtime_config=runtimeConfig()):   

    exp_date_list = get_option_exp_date(symbol, min_days_to_expire=risk_mgr.open_min_days_to_expire, max_days_to_expire=runtime_config.max_days_to_expire)

    predictlist = predict_price_range(symbol, target_date_list=exp_date_list)       

    trade_rec_list = []
            
    candidates = pd.DataFrame()  # one per symbol        
    
    for strategy in strategy_list:
        if strategy   == st.LONG_CALL:
            df = pick_option_long( symbol, 
                                    asset.CALL, 
                                    predictlist,                
                                    min_pnl = entry_crit.min_pnl,                                    
                                    min_win_prob = entry_crit.min_chance_of_win,         
                                    max_strike_ratio=runtime_config.max_strike_ratio,                    
                                    max_bid_ask_spread=runtime_config.max_bid_ask_spread,
                                    min_open_interest=entry_crit.min_open_interest)           
        elif strategy == st.LONG_PUT:
            df = pick_option_long( symbol, 
                                    asset.PUT, 
                                    predictlist,                
                                    min_pnl = entry_crit.min_pnl,                                    
                                    min_win_prob = entry_crit.min_chance_of_win,         
                                    max_strike_ratio=runtime_config.max_strike_ratio,                    
                                    max_bid_ask_spread=runtime_config.max_bid_ask_spread,
                                    min_open_interest=entry_crit.min_open_interest)              
        elif strategy == st.COVERED_CALL:
            df = pick_option_short( symbol, 
                                    asset.CALL, 
                                    predictlist,                
                                    min_pnl = entry_crit.min_pnl,                                    
                                    min_win_prob = entry_crit.min_chance_of_win,         
                                    max_strike_ratio=runtime_config.max_strike_ratio,                    
                                    max_bid_ask_spread=runtime_config.max_bid_ask_spread,
                                    min_open_interest=entry_crit.min_open_interest)  
        elif strategy == st.SHORT_PUT:
            df = pick_option_short( symbol, 
                                    asset.PUT, 
                                    predictlist,                
                                    min_pnl = entry_crit.min_pnl,                                    
                                    min_win_prob = entry_crit.min_chance_of_win,         
                                    max_strike_ratio=runtime_config.max_strike_ratio,                    
                                    max_bid_ask_spread=runtime_config.max_bid_ask_spread,
                                    min_open_interest=entry_crit.min_open_interest)                    
        elif strategy == st.CREDIT_CALL_SPREAD:
            df = pick_vertical_call_spreads(symbol,                          
                                            predictlist,
                                            credit=True,
                                            max_spread = runtime_config.max_spread,                        
                                            min_win_prob = entry_crit.min_chance_of_win,
                                            min_pnl = entry_crit.min_pnl,
                                            max_strike_ratio= runtime_config.max_strike_ratio,                    
                                            max_bid_ask_spread= runtime_config.max_bid_ask_spread,
                                            min_open_interest= entry_crit.min_open_interest)                       
        elif strategy == st.DEBIT_CALL_SPREAD:
            df = pick_vertical_call_spreads(symbol,                          
                                            predictlist,
                                            credit=False,
                                            max_spread = runtime_config.max_spread,                        
                                            min_win_prob = entry_crit.min_chance_of_win,
                                            min_pnl = entry_crit.min_pnl,
                                            max_strike_ratio= runtime_config.max_strike_ratio,                    
                                            max_bid_ask_spread= runtime_config.max_bid_ask_spread,
                                            min_open_interest= entry_crit.min_open_interest)                                    
        elif strategy==  st.CREDIT_PUT_SPREAD:
            df = pick_vertical_put_spreads(symbol,                          
                                            predictlist,
                                            credit=True,
                                            max_spread = runtime_config.max_spread,                        
                                            min_win_prob = entry_crit.min_chance_of_win,
                                            min_pnl = entry_crit.min_pnl,
                                            max_strike_ratio= runtime_config.max_strike_ratio,                    
                                            max_bid_ask_spread= runtime_config.max_bid_ask_spread,
                                            min_open_interest= entry_crit.min_open_interest)                      
        elif strategy == st.DEBIT_PUT_SPREAD:
            df = pick_vertical_put_spreads(symbol,                          
                                            predictlist,
                                            credit=False,
                                            max_spread = runtime_config.max_spread,                        
                                            min_win_prob = entry_crit.min_chance_of_win,
                                            min_pnl = entry_crit.min_pnl,
                                            max_strike_ratio= runtime_config.max_strike_ratio,                    
                                            max_bid_ask_spread= runtime_config.max_bid_ask_spread,
                                            min_open_interest= entry_crit.min_open_interest)                    
        elif strategy==  st.CREDIT_IRON_CONDOR:
            df = pick_iron_condor(symbol,
                                predictlist,
                                credit=True,                                           
                                max_spread = runtime_config.max_spread,
                                min_price = entry_crit.min_price_to_short,                              
                                min_win_prob=entry_crit.min_chance_of_win,
                                min_pnl = entry_crit.min_pnl,
                                max_strike_ratio=runtime_config.max_strike_ratio,                    
                                max_bid_ask_spread=runtime_config.max_bid_ask_spread,
                                min_open_interest=entry_crit.min_open_interest)
        elif strategy == st.DEBIT_IRON_CONDOR:         
            df = pick_iron_condor(symbol,
                                predictlist,
                                credit=False,                                           
                                max_spread = runtime_config.max_spread,
                                min_price = 0.0,                              
                                min_win_prob=entry_crit.min_chance_of_win,
                                min_pnl = entry_crit.min_pnl,
                                max_strike_ratio=runtime_config.max_strike_ratio,                    
                                max_bid_ask_spread=runtime_config.max_bid_ask_spread,
                                min_open_interest=entry_crit.min_open_interest)              
        elif strategy == st.CREDIT_PUT_BUTTERFLY:
            df = pick_put_butterfly(symbol,                          
                                    predictlist,
                                    credit=True,       
                                    max_spread = runtime_config.max_spread,
                                    min_price = entry_crit.min_price_to_short,                              
                                    min_win_prob = entry_crit.min_chance_of_win,
                                    min_pnl = entry_crit.min_pnl,
                                    max_strike_ratio=runtime_config.max_strike_ratio,                    
                                    max_bid_ask_spread=runtime_config.max_bid_ask_spread,
                                    min_open_interest=entry_crit.min_open_interest)                                         
        elif strategy == st.CREDIT_CALL_BUTTERFLY:
            df = pick_call_butterfly(symbol,                          
                                    predictlist,
                                    credit=True,       
                                    max_spread = runtime_config.max_spread,
                                    min_price = entry_crit.min_price_to_short,                              
                                    min_win_prob = entry_crit.min_chance_of_win,
                                    min_pnl = entry_crit.min_pnl,
                                    max_strike_ratio=runtime_config.max_strike_ratio,                    
                                    max_bid_ask_spread=runtime_config.max_bid_ask_spread,
                                    min_open_interest=entry_crit.min_open_interest)                                      
        elif strategy == st.DEBIT_PUT_BUTTERFLY:
            df = pick_put_butterfly(symbol,                          
                                    predictlist,
                                    credit=False,       
                                    max_spread = runtime_config.max_spread,
                                    min_price = entry_crit.min_price_to_short,                              
                                    min_win_prob = entry_crit.min_chance_of_win,
                                    min_pnl = 0.0,
                                    max_strike_ratio=runtime_config.max_strike_ratio,                    
                                    max_bid_ask_spread=runtime_config.max_bid_ask_spread,
                                    min_open_interest=entry_crit.min_open_interest)           
        elif strategy == st.DEBIT_CALL_BUTTERFLY:
            df = pick_call_butterfly(symbol,                          
                                    predictlist,
                                    credit=False,       
                                    max_spread = runtime_config.max_spread,
                                    min_price = entry_crit.min_price_to_short,                              
                                    min_win_prob = entry_crit.min_chance_of_win,
                                    min_pnl = 0.0,
                                    max_strike_ratio=runtime_config.max_strike_ratio,                    
                                    max_bid_ask_spread=runtime_config.max_bid_ask_spread,
                                    min_open_interest=entry_crit.min_open_interest)   
        elif strategy == st.IRON_BUTTERFLY:
            df = pick_iron_butterfly(symbol,                          
                                    predictlist,
                                    credit=True,
                                    max_spread = runtime_config.max_spread,
                                    min_price = entry_crit.min_price_to_short,                               
                                    min_win_prob= entry_crit.min_chance_of_win,
                                    min_pnl = entry_crit.min_pnl,
                                    max_strike_ratio= runtime_config.max_strike_ratio,                    
                                    max_bid_ask_spread= runtime_config.max_bid_ask_spread,
                                    min_open_interest = entry_crit.min_open_interest)                   
        elif strategy == st.REVERSE_IRON_BUTTERFLY:
            df = pick_iron_butterfly(symbol,                          
                                    predictlist,
                                    credit=False,
                                    max_spread = runtime_config.max_spread,
                                    min_price = 0.0,                              
                                    min_win_prob= entry_crit.min_chance_of_win,
                                    min_pnl = entry_crit.min_pnl,
                                    max_strike_ratio= runtime_config.max_strike_ratio,                    
                                    max_bid_ask_spread= runtime_config.max_bid_ask_spread,
                                    min_open_interest = entry_crit.min_open_interest)                                
        else:
            print('Unsupported strategy %s' % strategy)
            continue                   

        candidates = pd.concat([candidates, df])      

        print('%s %s %d' %(symbol, strategy, df.shape[0]))

    ''''
    if candidates.shape[0] > 0:         

        candidates.sort_values([position_summary.WIN_PROB, position_summary.PNL],  ascending=False, inplace=True)                                                

        df = pd.read_sql_query("SELECT * FROM position_summary WHERE status = '"+asset.OPENED+"'", self.db_conn)   

        candidates = candidates.groupby([position_summary.SYMBOL, position_summary.EXP_DATE, position_summary.STRATEGY]).first()

        for index, opt in candidates.iterrows():  

            symbol =   index[0]
            exp_date = index[1]
            strategy = index[2]

            if df[(df[position_summary.SYMBOL]==symbol) & (df[position_summary.EXP_DATE] == exp_date) & (df[position_summary.STRATEGY] == strategy)].shape[0] > 0:
                continue

            if strategy == st.COVERED_CALL:
                shares = self.get_stock_open_shares(symbol)
                q = shares // 100
                if q == 0:
                    self.logger.info('No enough %s shared %.2f to sell covered call' % (symbol, shares))
                    continue                    
            if strategy == st.SHORT_PUT:
                cash_avail = self.get_cash_position()
                if cash_avail < 10000:
                    self.logger.info('No enough cash %.2f to sell put' % (cash_avail))
                    continue

                q = (10000 // (100* df[position_summary.MAX_LOSS]))
                if q == 0:
                    self.logger.info('No enough cash %.2f to sell put %s' % (cash_avail, symbol))
                    continue                    
                else:
                    self.logger.info('No enough %s shared %.2f to sell covered call' % (symbol, shares))
                        
            else:    
                q = self.risk_mgr.max_loss_per_position // (opt[position_summary.MAX_LOSS] * 100)
                if q == 0:
                    self.logger.info('max loss %.2f exceeded max per position risk %.2f' % (opt[position_summary.MAX_LOSS] * 100, self.risk_mgr.max_loss_per_position))
                    continue

            trade_rec = self.create_position_summary(symbol, exp_date, strategy, opt, q)  

            if len(trade_rec) > 0:
                trade_rec_list.append(trade_rec)

        self.logger.debug('%d option strategy order created' % len(trade_rec_list))
        '''
    return candidates


if __name__ == '__main__':

    import sys

    sys.path.append(r'\Users\jimhu\option_trader\src')

    risk_mgr = riskManager()
    runtime_config = runtimeConfig()

    risk_mgr.open_min_days_to_expire = 1
    runtime_config.max_days_to_expire = 5

    df = get_trade_targets( 'MSFT', [st.CREDIT_IRON_CONDOR], risk_mgr=risk_mgr, runtime_config=runtime_config)

    print(df.shape[0])
