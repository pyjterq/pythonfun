import time


def task():
    result = 0
    for i in range(100000000):
        result += i
    return result


def benchmark(process):
    start_time = time.time()
    result = process()
    stop_time = time.time()
    execution_time = stop_time - start_time

    return {'result': result, 'execution_time': execution_time}


print(benchmark(task))
