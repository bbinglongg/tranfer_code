import pandas as pd

# 读取数据
intraday_data = pd.read_csv('Simulation_INTRADAY_DATA_HSI.csv')
daily_data = pd.read_csv('daily.csv')
dummay_data = pd.read_csv('Dummay_data.csv')

def extract_daily_change(data):
    data['date'] = pd.to_datetime(data['date'])
    data.set_index('date', inplace=True)
    data['change'] = data['current'].pct_change()
    daily_change = data.resample('D').last()['change']
    return daily_change.dropna()

dummy_daily_change = extract_daily_change(dummay_data)

def find_matching_period(daily_change, historical_data):
    historical_data['date'] = pd.to_datetime(historical_data['date'])
    historical_data.set_index('date', inplace=True)
    historical_data['change'] = historical_data['收市'].pct_change()

    for start in range(len(historical_data) - len(daily_change) + 1):
        match = True
        for i in range(len(daily_change)):
            if abs(historical_data['change'].iloc[start + i] - daily_change.iloc[i]) > 1e-6:
                match = False
                break
        if match:
            return historical_data.index[start]

    return None

matching_start_date = find_matching_period(dummy_daily_change, daily_data)

def get_predicted_max_value(matching_start_date, historical_data):
    matching_period = historical_data.loc[matching_start_date:matching_start_date + pd.DateOffset(weeks=3)]
    next_week = historical_data.loc[matching_start_date + pd.DateOffset(weeks=3):matching_start_date + pd.DateOffset(weeks=4)]
    return next_week['最高'].max()

predicted_max_value = get_predicted_max_value(matching_start_date, daily_data)

def find_masking_formula(dummay_data, intraday_data):
    # 计算前3个星期的masking系数
    dummy_max = dummay_data['current'].max()
    historical_max = intraday_data['current'].max()
    masking_coefficient = dummy_max / historical_max
    return masking_coefficient

masking_coefficient = find_masking_formula(dummay_data, intraday_data)

def apply_masking_coefficient(value, coefficient):
    return value * coefficient

adjusted_max_value = apply_masking_coefficient(predicted_max_value, masking_coefficient)
