import math
from bisect import bisect_left

with open('QProblem2/5.txt') as fl:
    data = fl.read().splitlines()

T = int(data[0])
cur_ind = 0
res = []
while T:
    cur_ind += 1
    M, K, N = map(int, data[cur_ind].split())
    cur_ind += 1
    m_list = list(map(float, data[cur_ind].split()))
    cur_ind += 1
    a_list = list(map(float, data[cur_ind].split()))
    cur_ind += 1
    s_list = list(map(float, data[cur_ind].split()))

    m_ind = [(b, a) for a, b in enumerate(m_list)]
    m_ind.sort()

    m_val = [a for a, _ in m_ind]

    step = 0
    for s in s_list:
        step += 1
        if step % 100 == 0:
            print(step)
        delta = math.inf
        ind_opt_m = 0
        ind_opt_k = 0
        for k in range(len(a_list)):
            r = s - a_list[k]
            ind = bisect_left(m_val, r)
            if ind == len(m_val):
                ind -= 1
            elif ind == 0:
                ind = 0
            elif abs(m_val[ind] - r) > abs(m_val[ind - 1] - r):
                ind -= 1
            new_delta = abs(m_val[ind] - r)
            if delta > new_delta:
                delta = new_delta
                ind_opt_m = ind
                ind_opt_k = k
        res.append([m_ind[ind_opt_m][1], ind_opt_k])
    T -= 1

with open('QProblem2/output.txt', 'w') as fl_out:
    for j, k in res:
        fl_out.write(f'{j + 1} {k + 1}\n')
