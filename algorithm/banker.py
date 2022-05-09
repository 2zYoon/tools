from pprint import pprint

import sys
import itertools


def list_arithmetic(cmd, l1, l2):
    size = len(l1)

    assert(len(l1) == len(l2))

    ret = [0 for i in range(size)]

    if cmd == "add":
        for i in range(size):
            ret[i] = l1[i] + l2[i]
        return ret

    elif cmd == "sub":
        for i in range(size):
            ret[i] = l1[i] - l2[i]
        return ret

    else:
        raise ValueError


def list_is_nonneg(l):
    ret = True
    for i in l:
        ret = ret and (i >= 0)
    return ret

def test():
    print(list_arithmetic("add", [1, 2, 3], [4,5,6]))    
    print(list_arithmetic("sub", [1, 2, 3], [4,5,6]))    
    print(list_is_nonneg([4, 2, -1]))
    print(list_is_nonneg([4, 2, 1]))

def banker_verify(dat, seq):
    avail_ = dat["available"][:]
    max_ = dat["max"][:]
    alloc_ = dat["alloc"][:]
    
    sequence = list(map(int, seq.split(",")))

    ok = True
    step = 1
    for i in sequence:
        need_ = list_arithmetic("sub", max_[i], alloc_[i])
        avail_ = list_arithmetic("sub", avail_, need_)
        print("Step {}:\tGrant {} to P{} -> {} available -> ".format(step, need_, i, avail_), end="")
        
        if not list_is_nonneg(avail_):  
            print("Oops...")  
            ok = False
            break

        avail_ = list_arithmetic("add", avail_, max_[i])
        print("P{} releases {} -> {} available".format(i, max_[i], avail_))        
        
        step += 1

    if ok:
        print("\nThe given sequence {} is feasible".format(sequence))
    else:
        print("\nThe given sequence {} is infeasible".format(sequence))

def banker_find(dat):
    seq_all = list(itertools.permutations(list(range(dat["nP"])), dat["nP"]))
    
    l_feasible = []

    for seq in seq_all:
        avail_ = dat["available"][:]
        max_ = dat["max"][:]
        alloc_ = dat["alloc"][:]

        ok = True

        for i in seq:
            need_ = list_arithmetic("sub", max_[i], alloc_[i])
            avail_ = list_arithmetic("sub", avail_, need_)

            if not list_is_nonneg(avail_):
                ok = False
                break

            avail_ = list_arithmetic("add", avail_, max_[i])
            print("avail2", avail_)

        if ok:
            l_feasible.append(seq)
    
    for i in l_feasible:
        print(i)

    if len(l_feasible) == 0:
        print("This system is unsafe!")

def read_input(fname):
    ret = dict()
    with open(fname, "r") as f:
        ret["nP"] = int(f.readline().split(" ")[1])
        ret["nR"] = int(f.readline().split(" ")[1])
        
        # allocation
        f.readline() 
        ret["alloc"] = []
        for i in range(ret["nP"]):
            tmp = list(map(int, f.readline().split(" ")))
            if len(tmp) != ret["nR"]:
                raise ValueError

            ret["alloc"].append(tmp)
        
        # max
        f.readline() 
        ret["max"] = []
        for i in range(ret["nP"]):
            tmp = list(map(int, f.readline().split(" ")))
            if len(tmp) != ret["nR"]:
                raise ValueError

            ret["max"].append(tmp)
        
        # available
        f.readline()
        ret["available"] = list(map(int, f.readline().split(" ")))
        
    return ret

if __name__ == "__main__":
    cmd = sys.argv[2]
    
    if cmd == "find":
        banker_find(read_input(sys.argv[1]))
    elif cmd == "verify":
        banker_verify(read_input(sys.argv[1]), sys.argv[3])
    elif cmd == "test":
        test()
    