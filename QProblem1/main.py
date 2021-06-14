with open(r'QProblem1/2.txt') as fl_inp:
    data = fl_inp.read().splitlines()

res = []
n_test = int(data[0])
cur_ind = 1
while n_test:
    a, b = map(int, data[cur_ind].split())
    cur_ind += 1
    h = []
    for i in range(b):
        s = ''
        for j in range(a):
            s += data[cur_ind + j][i]
        h.append(s)
    k = 0
    dh = dict()
    for cm in set(h):
        k += 1
        dh[cm] = k
    res.append([k, [dh[s] for s in h]])
    cur_ind += a
    n_test -= 1

with open(r'QProblem1/output1.txt', 'w') as fl_out:
    for elem1, elem2 in res:
        fl_out.write(f'{elem1}\n{" ".join(map(str, elem2))}\n')
    fl_out.flush()
