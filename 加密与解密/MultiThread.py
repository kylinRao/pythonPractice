from multiprocessing.dummy import Pool as ThreadPool
import datetime
import timeit
def Mprint(a):
    print a


def multiThread(fun,args):
    pool = ThreadPool(8)
    pool.map(fun, args)
    pool.close()
    pool.join()
if __name__ == '__main__':
    bt = datetime.datetime.now()
    multiThread(Mprint,xrange(0,100))
    et = datetime.datetime.now()
    ct = et - bt
    print ct
