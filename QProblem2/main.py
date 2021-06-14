from bisect import bisect_left, bisect_right

with open('QProblem2/3.txt') as fl:
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
    md = []
    for j in range(len(m_list)):
        for k in range(len(a_list)):
            md.append([m_list[j] + a_list[k], j, k])
    md.sort()
    mds = [a[0] for a in md]

    step = 0
    for s in s_list:
        step += 1
        # print(step)
        ind = bisect_left(mds, s)
        if ind == len(mds):
            res.append([md[ind - 1][1], md[ind - 1][2]])
        elif ind == 0:
            res.append([md[0][1], md[0][2]])
        elif abs(mds[ind] - s) < abs(mds[ind - 1] - s):
            res.append([md[ind][1], md[ind][2]])
        else:
            res.append([md[ind - 1][1], md[ind - 1][2]])
    T -= 1

with open('QProblem2/output.txt', 'w') as fl_out:
    for j, k in res:
        fl_out.write(f'{j + 1} {k + 1}\n')
