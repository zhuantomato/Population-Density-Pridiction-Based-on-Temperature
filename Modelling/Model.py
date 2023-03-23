'''
Author: Ruijie Ni 1924975712@qq.com
Date: 2023-03-23 19:21:41
LastEditors: Ruijie Ni 1924975712@qq.com
LastEditTime: 2023-03-23 19:22:11
FilePath: \Population-Density-Pridiction-Based-on-Temperature\Modelling\Model.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import tensorflow as tf

# 定义一个简单的神经网络模型
model = tf.keras.Sequential([
    tf.keras.layers.Dense(64, activation='relu', input_shape=(2,)),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(1)
])

# 编译模型
model.compile(optimizer='adam', loss='mse')

# 训练模型
model.fit(numeric_data[['status', '温度']], numeric_data['人口密度'], epochs=100)

# 进行预测
predictions = model.predict([[3, 25], [1, 20], [2, 15]])

# 打印预测结果
print(predictions)