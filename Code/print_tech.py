import matplotlib.pyplot as plt
import pandas as pd 
import seaborn as sns


data = {i: i*2 for i in range(15)}

df = pd.DataFrame(data.items(), columns=['num', 'sq_num'])

f_string = 10
fig, ax = plt.subplots()
sns.lineplot(data=df, x='num', y='sq_num')
plt.xlabel(f"{f_string}" + r"$x=10$num")
plt.show()