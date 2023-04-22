'''
Author: Ruijie Ni 1924975712@qq.com
Date: 2023-04-11 15:14:00
LastEditors: Ruijie Ni 1924975712@qq.com
LastEditTime: 2023-04-11 15:42:09
FilePath: \Population-Density-Pridiction-Based-on-Temperature\Modelling\DNN.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import learning_curve
from sklearn.model_selection import ShuffleSplit
from sklearn.neural_network import MLPClassifier

# 读取数据文件
data = pd.read_csv('/content/drive/MyDrive/FinalProject/Population-Density-Pridiction-Based-on-Temperature/Modelling/DataPreprocess/Weather/data.csv')

# 将数据分为输入和输出
X = data[['temperature', 'is_weekend', 'hour']]
y = data['status']

# 将数据分为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 对数据进行标准化处理
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 定义DNN模型架构
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation='relu', input_shape=(3,)),
    tf.keras.layers.Dense(128, activation='relu'),
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

# 将模型保存到磁盘上
tf.saved_model.save(model, '/content/drive/MyDrive/FinalProject/Population-Density-Pridiction-Based-on-Temperature/Modelling/Model/DNN')

# 绘制图像
plt.scatter(y_test, y_pred)
plt.xlabel('True Values')
plt.ylabel('Predictions')
plt.xlim(1,2.5)
plt.ylim(1,2.5)
plt.text(0.95, 0.95, 'MSE: {:.4f}'.format(mse), transform=plt.gca().transAxes)
plt.savefig('/content/drive/MyDrive/FinalProject/Population-Density-Pridiction-Based-on-Temperature/Modelling/Results/DNNSimpleScatter.png')
