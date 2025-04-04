from concurrent.futures import ThreadPoolExecutor, as_completed
import time
list = [0,1,2,3,4,5]


def sleeping(sleep):
    time.sleep(sleep)
    print("done:", sleep)
    return sleep

start = time.time()

with ThreadPoolExecutor() as ex:
    futures = []
    for sleep in list:
        futures.append(ex.submit(sleeping, sleep))

    for future in as_completed(futures):
        print("result:", future.result())


print("done done: ", time.time() - start)
