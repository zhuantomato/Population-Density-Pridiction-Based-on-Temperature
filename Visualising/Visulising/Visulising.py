import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

data_path = ('HumanModelling\DataPreprocess\MergedData\data.csv')
df = pd.read_csv(data_path)
plt.scatter(df['hour'], df['status'])
plt.xlabel('Hour')
plt.ylabel('Status')
plt.show()
plt.scatter(df['temperature'], df['status'])
plt.xlabel('Temperature')
plt.ylabel('Status')
plt.show()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(df['hour'], df['temperature'], df['status'])
ax.set_xlabel('Hour')
ax.set_ylabel('Temperature')
ax.set_zlabel('Status')
plt.show()
