from multiprocessing import Pool
import time


def f(x):
    # time.sleep(x)
    while (1):
        pass

    return x*x


if __name__ == '__main__':
    with Pool(10) as p:
        print(p.map(f, [1, 2, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]))

    print("alldoen")
