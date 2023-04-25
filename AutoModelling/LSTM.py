import pickle
import random
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error

# 定义一个随机种子的值
SEED = 1
# 设置numpy的随机种子
np.random.seed(SEED)
# 设置python的随机种子
random.seed(SEED)
# 设置tensorflow的随机种子
tf.random.set_seed(SEED)

# 读取数据文件
data = pd.read_csv('Modelling\DataPreprocess\MergedData\data.csv')

# 将数据分为输入和输出
X = data[['temperature','latitude','longitude', 'is_weekend', 'hour']]
y = data['status']

# 将数据分为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 对数据进行标准化处理
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 将输入转换为3D张量形式（样本数，时间步长，特征数）
X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1]))
X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1]))

# 定义LSTM模型架构
model = tf.keras.Sequential([
    tf.keras.layers.LSTM(64, input_shape=(1, 5)),
    tf.keras.layers.Dense(1)
])

# 编译模型
model.compile(optimizer='adam', loss='mse')

# 训练模型并保存历史记录
history = model.fit(X_train, y_train, epochs=200, validation_data=(X_test, y_test))

# 绘制学习曲线
plt.figure(figsize=(6, 6))
plt.plot(history.history['loss'], label='train loss')
plt.plot(history.history['val_loss'], label='test loss')
plt.xlabel('iterations')
plt.ylabel('loss')
plt.legend()
plt.title('loss curve')
fig = plt.gcf()
plt.show()
fig.savefig('Modelling\Results\LSTMLearningCurve.png')

# 使用pickle模块的dump函数将history对象保存到一个文件中
with open('Modelling\Model\LSTM\History\history.pkl', 'wb') as f:
    pickle.dump(history, f)

tf.saved_model.save(model, 'Modelling\Model\LSTM\Model')

# 进行预测
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

# 绘制图像
plt.scatter(y_test, y_pred)
plt.xlabel('True Values')
plt.ylabel('Predictions')
plt.xlim(1,2.5)
plt.ylim(1,2.5)
plt.text(0.95, 0.95, 'MSE: {:.4f}'.format(mse), transform=plt.gca().transAxes)
fig2 = plt.gcf()
plt.show()
fig2.savefig('Modelling\Results\LSTMSimpleScatter.png')

# 计算准确率
y_pred = y_pred.tolist()
y_test = y_test.tolist()
y_pred = [item for sublist in y_pred for item in sublist]
accuracy = [y_pred[i] - y_test[i] for i in range(len(y_pred))]
plt.hist(accuracy, bins=200, density=True)
# 计算频率密度和区间中点
density, bins = np.histogram(accuracy, bins=200, density=True)
x = (bins[1:] + bins[:-1]) / 2 # 区间中点

# 绘制密度曲线
plt.plot(x, density)

# 添加横轴和纵轴标签
plt.xlabel("Accuracy")
plt.ylabel("Frequency Density")
fig3 = plt.gcf()
plt.show()
fig3.savefig('Modelling\Results\LSTMAccuracyScatter.png')
