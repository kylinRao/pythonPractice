from multiprocessing import Pool
import os


def get_image_paths(folder):
    return (os.path.join(folder, f)
            for f in os.listdir(folder)
            if 'jpeg' in f)

def fun(args):
    print args

if __name__ == '__main__':


    pool = Pool()
    pool.map(fun, xrange(0,199))
    pool.close()
    pool.join()