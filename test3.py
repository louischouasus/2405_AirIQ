import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import PolyCollection


def sierpinski(n):
    def quotientAndRemainderZero(elem, n):
        quotient = elem // n
        remainder = elem % n
        return quotient & remainder == 0

    quotientAndRemainderZero = np.frompyfunc(quotientAndRemainderZero, 2, 1)

    nums = np.arange(n**2)
    nums = nums[np.where(quotientAndRemainderZero(nums, n))]
    return (nums % n, nums // n)


# 在每個 x, y 建立一個三角形
def tri(x, y):
    return [[x, y], [x + 1, y], [x, y + 1]]


tri = np.frompyfunc(tri, 2, 1)

n = 32
x, y = sierpinski(n)

ax = plt.gca()
print(tri(x, y))
ax.add_collection(PolyCollection(tri(x, y)))
ax.set_xlim([0, n])
ax.set_ylim([0, n])
plt.show()
