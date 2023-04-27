import pickle
import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import tensorflow as tf

# 定义一个随机种子的值
SEED = 1
# 设置numpy的随机种子
np.random.seed(SEED)
# 设置python的随机种子
random.seed(SEED)
# 设置tensorflow的随机种子
tf.random.set_seed(SEED)

# 读取数据文件
data = pd.read_csv('AutoModelling\DataPreprocess\MergedData\data.csv')

# 将数据分为输入和输出
X = data[['temperature','latitude','longitude', 'is_weekend', 'hour']]
y = data['status']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# 训练线性回归模型
model = LinearRegression()

# 训练模型并保存历史记录
history = model.fit(X_train, y_train)

# 进行预测
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

# # 使用pickle模块的dump函数将history对象保存到一个文件中
# with open('AutoModelling\Model\Linear\History\history.pkl', 'wb') as f:
#     pickle.dump(history, f)

# 绘制图像
plt.scatter(y_test, y_pred)
plt.xlabel('True Values')
plt.ylabel('Predictions')
plt.xlim(1,2.5)
plt.ylim(1,2.5)
plt.text(0.95, 0.95, 'MSE: {:.4f}'.format(mse), transform=plt.gca().transAxes)
fig2 = plt.gcf()
plt.show()
fig2.savefig('AutoModelling\Results\LinearSimpleScatter.png')

# 计算准确率
y_pred = y_pred.tolist()
y_test = y_test.tolist()
accuracy = [y_pred[i] - y_test[i] for i in range(len(y_pred))]
plt.hist(accuracy, bins=20, density=False)
# 计算频率密度和区间中点
density, bins = np.histogram(accuracy, bins=20, density=False)
x = (bins[1:] + bins[:-1]) / 2 # 区间中点

# 绘制密度曲线
plt.plot(x, density)

# 添加横轴和纵轴标签
plt.xlabel("Prediction error")
plt.ylabel("Frequency")
fig3 = plt.gcf()
plt.show()
fig3.savefig('AutoModelling\Results\LinearAccuracyScatter.png')


