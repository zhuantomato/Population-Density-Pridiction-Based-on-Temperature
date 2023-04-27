import pickle
import random
import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import keras_tuner as kt
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
data = pd.read_csv('AutoModelling\DataPreprocess\MergedData\data.csv')

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
def build_model(hp):
    model = tf.keras.Sequential([
        tf.keras.layers.SimpleRNN(hp.Int('units', min_value=32, max_value=128, step=16), input_shape=(1, 5)),
        tf.keras.layers.Dense(1)
    ])
    # 编译模型
    model.compile(optimizer=tf.keras.optimizers.Adam(
        hp.Choice('learning_rate',values=[1e-2, 1e-3, 1e-4])),
                  loss='mse')
    return model

# 使用Keras Tuner搜索最优参数
tuner=kt.BayesianOptimization(
    build_model,
    objective='val_loss',
    max_trials=10,
    directory = 'AutoAdjustedModels',
    project_name = 'RNN'
    )

# 训练模型并保存历史记录
tuner.search(X_train, y_train,epochs = 100, validation_data=(X_test, y_test))

# 获取最优模型
best_model = tuner.get_best_models(num_models=1)[0]
# 将最优模型保存为文件
best_model.save('AutoAdjustedModels\RNN\RNNSimple.h5')

# 进行预测
y_pred = best_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)

# 绘制图像
plt.scatter(y_test, y_pred)
plt.xlabel('True Values')
plt.ylabel('Predictions')
plt.xlim(1,2.5)
plt.ylim(1,2.5)
plt.text(0.95, 0.95, 'MSE: {:.4f}'.format(mse), transform=plt.gca().transAxes)
fig = plt.gcf()
plt.show()
fig.savefig('AutoModelling\Results\RNNSimpleScatter.png')

# 计算准确率
y_pred = y_pred.tolist()
y_test = y_test.tolist()
y_pred = [item for sublist in y_pred for item in sublist]
accuracy = [y_pred[i] - y_test[i] for i in range(len(y_pred))]
# 绘制图像
plt.hist(accuracy, bins=20, density=False)
# 计算频率密度和区间中点
density, bins = np.histogram(accuracy, bins=20, density=False)
x = (bins[1:] + bins[:-1]) / 2 # 区间中点

# 绘制密度曲线
plt.plot(x, density)

# 添加横轴和纵轴标签
plt.xlabel("Prediction error")
plt.ylabel("Frequency")
fig2 = plt.gcf()
plt.show()
fig2.savefig('AutoModelling\Results\RNNAccuracyScatter.png')