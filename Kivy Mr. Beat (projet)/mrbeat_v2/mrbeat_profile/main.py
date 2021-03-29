import timeit
from array import array

nb_samples = 44100

buf = array('h', b"\x00\x00" * nb_samples)

buf1 = array('h', b"\x00\x00" * nb_samples)
buf2 = array('h', b"\x00\x00" * nb_samples)
buf3 = array('h', b"\x00\x00" * nb_samples)
buf4 = array('h', b"\x00\x00" * nb_samples)
bufs = [buf1, buf2, buf3, buf4]

def func1():
    for i in range(0, nb_samples):
        buf[i] = 0
    return buf


def func2():
    return buf[0:nb_samples]


# mixer
def func3():
    for i in range(0, nb_samples):
        buf[i] = 0
        for j in range(0, len(bufs)):
            buf[i] += bufs[j][i]


def func4():
    s = [sum(x) for x in zip(*bufs)]
    return array('h', s)


def func5():
    s = map(sum, zip(*bufs))
    return array('h', s)


# print(timeit.repeat(setup="from __main__ import func1",
#                    stmt="func1()", repeat=3, number=100))
# print(timeit.repeat(setup="from __main__ import func2",
#                     stmt="func2()", repeat=3, number=100))
#print(timeit.repeat(setup="from __main__ import func3",
#                    stmt="func3()", repeat=3, number=100))
print(timeit.repeat(setup="from __main__ import func4",
                    stmt="func4()", repeat=3, number=100))
print(timeit.repeat(setup="from __main__ import func5",
                    stmt="func5()", repeat=3, number=100))
