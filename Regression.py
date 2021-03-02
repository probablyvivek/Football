#Importing Libraries
import pandas as pd 
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression

#Reading Data
df = pd.read_csv("./Python/Football/Data1032021.csv")
 
#Dataframe Manipulation
df['90s'] = df['Minutes']/90
df = df[df['90s']>=2]
df = df[df['Shots']>0]
df = df[df['Goals']>0]

#Seperating dependent and independent variables
y = df.Goals
x = df.Shots.values.reshape(-1,1)
print(x.shape, y.shape)

model = LinearRegression().fit(x, y)
r_sq = model.score(x, y)
print(r_sq)

# y = mx +c
intercept = model.intercept_
slope = model.coef_
y_pred = intercept + slope*x

#Plot
fig, ax = plt.subplots(figsize = (10,10))
plt.style.use('Solarize_Light2')
plt.scatter(x, y, cmap='summer', edgecolor ='black',  alpha=0.7, zorder=1)
plt.plot(x, y_pred, c ='red',  zorder=2)

#Adding the reference lines
plt.plot([32.5, 32.5, 0], [0, 7, 7], 'k-', lw=1,dashes=[2, 2], zorder=3)

#Labelling
plt.xlabel('Shots')
plt.ylabel('Goals')
plt.title('Relationship Between Goals and Shots Taken by players in ISL 2020-2021', color = 'black', size = 20)

#Saving the File
plt.savefig('linear.jpg', dpi=200)
plt.show()
