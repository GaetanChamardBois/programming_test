import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Logic


def check_uniqueness(lst):
    """
    Check if a list contains only unique values.
    Returns True only if all values in the list are unique, False otherwise
    """
    
    return len(set(lst)) == len(lst)
    

def smallest_difference(array):
    """
    Code a function that takes an array and returns the smallest
    absolute difference between two elements of this array
    Please note that the array can be large and that the more
    computationally efficient the better
    """
    # absolute difference is small when elements are small
    # hence, we sort the array and look at the abs diff of its elements
    
    return np.min(np.abs(np.diff(np.sort(array))))


# Finance and DataFrame manipulation


def macd(prices, window_short=13, window_long=26):
    """
    Code a function that takes a DataFrame named prices and
    returns it's MACD (Moving Average Convergence Difference) as
    a DataFrame with same shape
    Assume simple moving average rather than exponential moving average
    The expected output is in the output.csv file   
    """
    macd_df = prices.copy() # create a new df
    
    prices_col = np.array(range(len(prices.columns)))
    
    # We check whether the first column is the date vector
    if type(prices.iloc[0,0]) == str:
        prices_col = np.delete(prices_col,0) # we remove the date from the stock list
        
    macd_df.iloc[:,prices_col] =  (prices.iloc[:,prices_col].rolling(window_short).mean() - 
                    prices.iloc[:,prices_col].rolling(window_long).mean()).round(4)
    
    return macd_df


def sortino_ratio(prices):
    """
    Code a function that takes a DataFrame named prices and
    returns the Sortino ratio for each column
    Assume risk-free rate = 0
    On the given test set, it should yield 0.05457
    """
        
    prices_col = np.array(range(len(prices.columns)))
    
    # We check whether the first column is the date vector
    if type(prices.iloc[0,0]) == str:
        prices_col = np.delete(prices_col,0) # we remove the date from the stock list
    
    ret = prices.iloc[:,prices_col].pct_change()    
    
    std_down = ret[ret<0].std()
    
    return ret.mean() / std_down


def expected_shortfall(prices, level=0.95):
    """
    Code a function that takes a DataFrame named prices and
    returns the expected shortfall at a given level
    On the given test set, it should yield -0.03468
    """
    prices_col = np.array(range(len(prices.columns)))
    
    # We check whether the first column is the date vector
    if type(prices.iloc[0,0]) == str:
        prices_col = np.delete(prices_col,0) # we remove the date from the stock list
    
    # get returns
    ret = prices.iloc[:,prices_col].pct_change() 
    
    # compute VaR
    VaR = - ret.quantile(1-level)
    #return the ES
    return  ret[ret < - VaR].mean()

# Plot


def visualize(prices, path):
    """
    Code a function that takes a DataFrame named prices and
    saves the plot to the given path
    """
    prices_col = np.array(range(len(prices.columns)))
    dates = prices.index # Default
    # We check whether the first column is the date vector
    if type(prices.iloc[0,0]) == str:
        prices_col = np.delete(prices_col,0) # we remove the date from the stock list
        dates = pd.to_datetime(prices.iloc[:,0])
        
    plt.figure(figsize = (10,6))
    plt.plot(dates,prices.iloc[:,prices_col],label=prices.columns[prices_col])
    plt.title('prices')
    plt.legend()
    plt.xlabel('date')
    plt.ylabel('price')
    plt.savefig(path)