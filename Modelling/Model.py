import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

# 读取数据文件
data = pd.read_csv('/content/drive/MyDrive/FinalProject/Population-Density-Pridiction-Based-on-Temperature/Modelling/DataPreprocess/Weather/data.csv')

# 将数据分为输入和输出
X = data[['temperature', 'is_weekend', 'hour']]
y = data['status']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 训练线性回归模型
model = LinearRegression()
model.fit(X, y)

# 预测结果
y_pred = model.predict(X_test)

# 绘制图像
plt.scatter(y_test, y_pred)
plt.xlabel('True Values')
plt.ylabel('Predictions')
plt.show()