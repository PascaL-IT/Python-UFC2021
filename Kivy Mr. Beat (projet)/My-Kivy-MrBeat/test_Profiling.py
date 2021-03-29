import timeit
from array import array

nb_samples = 44100
buf = array('h', bytes(2) * nb_samples)  # idem que array('h', b"\x00\x00" * nb_samples)
print(f"0. buf={type(buf)} : len={len(buf)}")
if len(buf) <= 24 : print(f"0. { buf } ")

buffer1 = array('h', bytes(2) * nb_samples)  # idem que array('h', b"\x00\x00" * nb_samples)
buffer2 = array('h', bytes(2) * nb_samples)  # idem que array('h', b"\x00\x00" * nb_samples)
buffer3 = array('h', bytes(2) * nb_samples)  # idem que array('h', b"\x00\x00" * nb_samples)
buffer4 = array('h', bytes(2) * nb_samples)  # idem que array('h', b"\x00\x00" * nb_samples)
buffers = [buffer1, buffer2, buffer3, buffer4]

def func1():
    for i in range(0, nb_samples):
        buf[i] = 0
    return buf

def func2():
    return buf[0:nb_samples]

def func3(): # as in mixer
    for i in range(0, nb_samples):
        buf[i] = 0
        for j in range(0, len(buffers)):
            buf[i] += buffers[j][i]
    return buf

# mesure with timeit (profiling of variosu functions)
setup1 = "from  __main__ import func1"
stmt1 = "func1()"
setup2 = "from  __main__ import func2"
stmt2 = "func2()"
setup3 = "from  __main__ import func3"
stmt3 = "func3()"

times = timeit.repeat(setup=setup1, stmt=stmt1, repeat=3, number=100)
print('\n1. times={}'.format(times))
buf1 = func1()
print(f"1. buf1={type(buf1)} : len={len(buf1)}")
if len(buf1) <= 24 : print(f"1. { buf1 } ")

times = timeit.repeat(setup=setup2, stmt=stmt2, repeat=3, number=100)
print('\n2. times={}'.format(times))
buf2 = func2()
print(f"2. buf2={type(buf2)} : len={len(buf2)}")
if len(buf2) <= 24 : print(f"2. { buf2 } ")

times = timeit.repeat(setup=setup3, stmt=stmt3, repeat=3, number=100)
print('\n3. times={}'.format(times))
buf3 = func3()
print(f"3. buf3={type(buf3)} : len={len(buf3)}")
if len(buf3) <= 24 : print(f"3. { buf3 } ")

# sum of two or more lists (approches)
setup4 = "from  __main__ import func4"
stmt4 = "func4()"
setup5 = "from  __main__ import func5"
stmt5 = "func5()"

def func4(): # approach1
    buf4 = [sum(x) for x in zip(*buffers)]
    return array('h', buf4)

def func5(): # approach2
    buf5 = list(map(sum, zip(*buffers)))
    return array('h', buf5)


times = timeit.repeat(setup=setup4, stmt=stmt4, repeat=3, number=100)
print('\n4. times={}'.format(times))
buf4 = func4()
print(f"4. buf4={type(buf4)} : len={len(buf4)}")
if len(buf4) <= 24 : print(f"4. { buf4 } ")

times = timeit.repeat(setup=setup5, stmt=stmt5, repeat=3, number=100)
print('\n5. times={}'.format(times))
buf5 = func5()
print(f"5. buf5={type(buf5)} : len={len(buf5)}")
if len(buf5) <= 24 : print(f"5. { buf5 } ")

# func5 > func4 > (5x) > func3 !!!