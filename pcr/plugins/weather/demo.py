import matplotlib.pyplot as plt
import numpy as np

if __name__ == '__main__':
    fig= plt.figure(num=1,figsize=(4,4),facecolor='blue')
    ax = fig.add_subplot(111)
    ax.plot([1,2,3,4],[1,2,3,4])
    plt.show()