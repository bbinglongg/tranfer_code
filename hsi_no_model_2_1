import pandas as pd
import numpy as np

# 读取过去一年的数据（假设数据已经读取为pandas DataFrame）
historical_data = pd.read_csv('historical_data.csv')  # 包含日期和最高值的csv文件
historical_data['date'] = pd.to_datetime(historical_data['date'])
historical_data = historical_data.set_index('date')

# 读取并处理给定的三个星期的数据（假设数据已经读取为pandas DataFrame）
week_data = pd.read_csv('week_data.csv')  # 包含日期和最高值的csv文件
week_data['date'] = pd.to_datetime(week_data['date'])
week_data = week_data.set_index('date')

# 假设处理后的数据是乘以某个数，例如乘以1.1
processed_week_data = week_data * 1.1

# 计算涨跌情况
def calculate_changes(data):
    return data.pct_change().dropna()

historical_changes = calculate_changes(historical_data['high'])
week_changes = calculate_changes(processed_week_data['high'])

# 找到匹配的时间段
def find_matching_periods(historical_changes, week_changes):
    matching_periods = []
    week_length = len(week_changes)
    for i in range(len(historical_changes) - week_length + 1):
        if (historical_changes.iloc[i:i+week_length].values == week_changes.values).all():
            matching_periods.append(historical_changes.index[i])
    return matching_periods

matching_periods = find_matching_periods(historical_changes, week_changes)

# 计算相似度以找到最匹配的时间段
def calculate_similarity(historical_data, week_data, periods):
    min_similarity = float('inf')
    best_period = None
    for period in periods:
        historical_segment = historical_data.loc[period:period+pd.DateOffset(days=len(week_data)-1)]
        similarity = np.sum((historical_segment['high'].values - week_data['high'].values) ** 2)
        if similarity < min_similarity:
            min_similarity = similarity
            best_period = period
    return best_period

best_period = calculate_similarity(historical_data, processed_week_data, matching_periods)

# 找出换算的规则
historical_segment = historical_data.loc[best_period:best_period+pd.DateOffset(days=len(week_data)-1)]
conversion_factor = np.mean(processed_week_data['high'].values / historical_segment['high'].values)

# 使用该规则预测接下来那个星期的最大值
next_week_prediction = historical_data.loc[best_period+pd.DateOffset(days=len(week_data)):best_period+pd.DateOffset(days=len(week_data)*2-1)]
predicted_max = next_week_prediction['high'].max() * conversion_factor

# 输出这个最大值
print(f"Predicted maximum value for the next week: {predicted_max}")
