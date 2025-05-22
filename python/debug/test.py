

from typing import Tuple


x:dict[Tuple[int, int], str] = {}

for i in range(5):
    for j in range(5):
        k = 5 - j

        x[i, k] = str(i) + str(k)
        print(str(i) + str(k))


print(x)
print(x.get((3,30)))