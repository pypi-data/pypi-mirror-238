from matplotlib import style
import numpy as np
import matplotlib.pyplot as plt

print(plt.style.available)

# creating an array of data for plot
data = np.random.randn(50)
  
# using the style for the plot
plt.style.use('ggplot')
  
# creating plot
plt.plot(data, linestyle=":", linewidth=2)
  
# show plot
plt.show()