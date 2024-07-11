import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler

# 读取数据
data = pd.read_csv('hangseng_index.csv')
dates = pd.to_datetime(data['date'])
highs = data['high'].values

# 标准化数据
scaler = MinMaxScaler(feature_range=(0, 1))
highs = scaler.fit_transform(highs.reshape(-1, 1))

# 构建LSTM模型
def build_model():
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(3, 1)))
    model.add(LSTM(50, return_sequences=False))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

# 生成训练数据
def create_dataset(data, time_step=3):
    X, y = [], []
    for i in range(len(data) - time_step - 1):
        a = data[i:(i + time_step), 0]
        X.append(a)
        y.append(data[i + time_step, 0])
    return np.array(X), np.array(y)

time_step = 3
X, y = create_dataset(highs, time_step)

X = X.reshape(X.shape[0], X.shape[1], 1)
model = build_model()
model.fit(X, y, epochs=100, batch_size=1, verbose=2)

# 假设你提供了某三个星期的数据
three_weeks_data = np.array([...])  # 替换为你的数据
three_weeks_data = scaler.transform(three_weeks_data.reshape(-1, 1)).reshape(-1)

# 匹配数据段
def find_best_match(model, three_weeks_data, original_data, time_step):
    best_index = 0
    best_score = float('inf')
    for i in range(len(original_data) - time_step - 1):
        segment = original_data[i:(i + time_step)].reshape(1, time_step, 1)
        predicted = model.predict(segment)
        score = np.mean((predicted.flatten() - three_weeks_data) ** 2)
        if score < best_score:
            best_score = score
            best_index = i
    return best_index

best_index = find_best_match(model, three_weeks_data, highs, time_step)
print("最佳匹配起始位置索引:", best_index)

# 获取对应的接下来一个星期的数据
next_week_data = highs[best_index + time_step: best_index + time_step + 7]
print("接下来一个星期的数据:", scaler.inverse_transform(next_week_data))

# 假设换算规则是 y = a * x
def find_conversion_rule(original, transformed):
    a = np.mean(transformed / original)
    return a

a = find_conversion_rule(highs[best_index:best_index+time_step].flatten(), three_weeks_data)
print("换算规则参数 a:", a)

# 根据换算规则，计算出下一星期的数据最高值
next_week_highs = a * scaler.inverse_transform(next_week_data)
print("换算后下一星期的最高值:", next_week_highs)
