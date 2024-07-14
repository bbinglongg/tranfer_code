import pandas as pd

# 读取数据
intraday_data = pd.read_csv('Simulation_INTRADAY_DATA_HSI.csv')
daily_data = pd.read_csv('daily.csv')
dummay_data = pd.read_csv('Dummay_data.csv')

# 提取前3周数据的涨跌符号 
def extract_daily_trend(data):
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)
    data['trend'] = (data['current'] > data['current'].shift(1)).astype(int)
    daily_trend = data.resample('D').last()['trend']
    return daily_trend.dropna()

dummy_daily_trend = extract_daily_trend(dummay_data)

# 提取历史数据的涨跌符号 
def extract_historical_trend(data):
    data['date'] = pd.to_datetime(data['日期'])
    data.set_index('date', inplace=True)
    data['trend'] = (data['最高'] > data['最高'].shift(1)).astype(int)
    return data['trend'].dropna()

historical_trend = extract_historical_trend(daily_data)

# 匹配时间段 
def find_matching_period(daily_trend, historical_trend):
    for start in range(len(historical_trend) - len(daily_trend) + 1):
        match = True
        for i in range(len(daily_trend)):
            if historical_trend.iloc[start + i] != daily_trend.iloc[i]:
                match = False
                break
        if match:
            return historical_trend.index[start]
    return None

matching_start_date = find_matching_period(dummy_daily_trend, historical_trend)

# 预测最后一周的最高值 
def get_predicted_max_value(matching_start_date, historical_data):
    next_week_start = matching_start_date + pd.DateOffset(weeks=3)
    next_week_end = next_week_start + pd.DateOffset(weeks=1)
    next_week = historical_data.loc[next_week_start:next_week_end]
    return next_week['最高'].max()

predicted_max_value = get_predicted_max_value(matching_start_date, daily_data)

# 找出masking的规律 
def find_masking_formula(dummay_data, intraday_data):
    dummy_max = dummay_data['current'].max()
    historical_max = intraday_data['current'].max()
    masking_coefficient = dummy_max / historical_max
    return masking_coefficient

masking_coefficient = find_masking_formula(dummay_data, intraday_data)

def apply_masking_coefficient(value, coefficient):
    return value * coefficient

adjusted_max_value = apply_masking_coefficient(predicted_max_value, masking_coefficient)
