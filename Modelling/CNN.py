import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error

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

# 将输入转换为4D张量形式（样本数，时间步长，特征数，通道数）
X_train = np.reshape(X_train, (X_train.shape[0], 1, X_train.shape[1], 1))
X_test = np.reshape(X_test, (X_test.shape[0], 1, X_test.shape[1], 1))

# 定义CNN模型架构
model = tf.keras.Sequential([
    tf.keras.layers.Conv2D(64, kernel_size=(1, 5), activation='relu', input_shape=(1, 5, 1)),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(1)
])

# 编译模型
model.compile(optimizer='adam', loss='mse')

# 训练模型
model.fit(X_train, y_train, epochs=100)

# 评估模型性能
mse = model.evaluate(X_test, y_test)
print('MSE:', mse)

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
plt.savefig('Modelling\Results\CNNSimpleScatter.png')
