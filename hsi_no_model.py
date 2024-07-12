import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error
from scipy.optimize import minimize

# 假设你有一个CSV文件包含了过去一年的恒生指数每日最高值
data = pd.read_csv('hangseng_index.csv')

# 读取日期和最高值
dates = pd.to_datetime(data['date'])
highs = data['high']

# 将数据标准化以便处理
highs = (highs - highs.mean()) / highs.std()

# 定义一个函数用于匹配数据段
def find_best_match(three_weeks_data, original_data):
    best_index = 0
    best_score = float('inf')
    n = len(three_weeks_data)
    for i in range(len(original_data) - n + 1):
        score = mean_squared_error(three_weeks_data, original_data[i:i+n])
        if score < best_score:
            best_score = score
            best_index = i
    return best_index

# 假设你提供了某三个星期的数据
three_weeks_data = np.array([...])  # 填入具体数据

# 标准化处理你提供的数据
three_weeks_data = (three_weeks_data - three_weeks_data.mean()) / three_weeks_data.std()

# 找到最匹配的数据段
best_index = find_best_match(three_weeks_data, highs)
print("最佳匹配起始位置索引:", best_index)

# 获取对应的接下来一个星期的数据
next_week_data = highs[best_index + len(three_weeks_data): best_index + len(three_weeks_data) + 7]
print("接下来一个星期的数据:", next_week_data)

# 假设换算规则是 y = a * x
# 定义损失函数以找到最佳换算规则
def loss_function(params, original, transformed):
    a = params[0]
    predicted = a * original
    return mean_squared_error(predicted, transformed)

# 初始化参数
initial_params = [1.0]

# 优化换算规则参数
result = minimize(loss_function, initial_params, args=(three_weeks_data, highs[best_index:best_index+len(three_weeks_data)]))
a = result.x[0]
print("换算规则参数 a:", a)

# 根据换算规则，计算出下一星期的数据最高值
next_week_highs = a * next_week_data
print("换算后下一星期的最高值:", next_week_highs)

