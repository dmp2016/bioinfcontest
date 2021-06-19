import math
from dataclasses import dataclass
from functools import lru_cache
import sys
from typing import List


sys.setrecursionlimit(100000)


@dataclass
class TreeV:
    IC: float
    Parent: int
    Level: int
    Children: List[int]
    BranchNum: int


with open('QProblem3_1/test4') as fl:
    # with open('test3') as fl:
    data = fl.read().splitlines()

n_tree = int(data[0])
print(f'Количество вершин: {n_tree}')
parents = [None] + list(map(int, data[1].split()))
ic_list = dict([(i + 1, d) for i, d in enumerate(map(int, data[2].split()))])
ic_list[None] = 0
tree = dict()

for v, (p, ic) in enumerate(zip(parents, ic_list)):
    tree[v + 1] = TreeV(IC=ic, Parent=p, Level=tree[p].Level + 1 if p else 0, Children=[], BranchNum=0)
    if p:
        tree[p].Children.append(v + 1)


tree[1].BranchNum = 0
tree_stack = [tree[1]]
cur_branch = 0
while tree_stack:
    root = tree_stack.pop()
    if root.Children:
        tree[root.Children[0]].BranchNum = root.BranchNum
    for ind in range(1, len(root.Children)):
        cur_branch += 1
        tree[root.Children[ind]].BranchNum = cur_branch
    for ind in root.Children:
        tree_stack.append(tree[ind])

print(f'Количество веток: {max([tree[item].BranchNum for item in tree])}')

print(f'Максимальная глубина: {max([tree[v].Level for v in tree])}')

n_dis = int(data[3])
print(f'Количество болезней: {n_dis}')
D_m_list = [sorted(list(map(int, data[4 + cur_dis].split()[1:])), key=lambda x: tree[x].Level, reverse=True) for cur_dis in range(n_dis)]


anc_cache = dict()
base = 10


def find_k_anc(p: int, k: int) -> int:
    p2 = 1
    while k:
        dm = k % base
        if dm:
            p = anc_cache[(p, p2*dm)]
        k //= base
        p2 *= base
    return p


def prepare_anc_cache1():
    front = [1]
    while front:
        for p in front:
            p2 = 1
            base2 = 1
            while tree[p].Level >= p2:
                anc_cache[(p, p2)] = find_k_anc(tree[p].Parent, p2 - 1)
                p2 += base2
                if p2 % (base2 * base) == 0:
                    base2 *= base
                    p2 = base2
        front = [ch for v in front for ch in tree[v].Children]


branch_cache = dict()
def LCA(q: int, d: int) -> int:
    b1, b2 = tree[q].BranchNum, tree[d].BranchNum
    if b1 == b2:
        return q if tree[q].Level < tree[d].Level else d
    else:
        cm = branch_cache.get((b1, b2)) or branch_cache.get((b2, b1))
        if not cm:
            while tree[q].Level > tree[d].Level:
                q = find_k_anc(q, tree[q].Level - tree[d].Level)
                # q = tree[q].Parent

            while tree[q].Level < tree[d].Level:
                d = find_k_anc(d, tree[d].Level - tree[q].Level)
                # d = tree[d].Parent

            if q != d:
                left, right = 0, tree[d].Level
                while left < right - 1:
                    mid = (left + right) // 2
                    anc1, anc2 = find_k_anc(q, mid), find_k_anc(d, mid)
                    if anc1 != anc2:
                        left = mid
                    else:
                        right = mid
                cm = find_k_anc(q, right)
            else:
                cm = q

            # while q != d:
            #     q = tree[q].Parent
            #     d = tree[d].Parent
            # if q != cm:
            #     print("fail")
            # cm = q
            branch_cache[(b1, b2)] = cm
            return cm
        if tree[q].Level < tree[cm].Level:
            return q
        elif tree[d].Level < tree[cm].Level:
            return d
        else:
            return cm


def LCA1(q: int, d: int) -> int:
    b1, b2 = tree[q].BranchNum, tree[d].BranchNum
    if b1 == b2:
        return q if tree[q].Level < tree[d].Level else d
    if tree[q].Level > tree[d].Level:
        q = find_k_anc(q, tree[q].Level - tree[d].Level)
        # q = tree[q].Parent

    if tree[q].Level < tree[d].Level:
        d = find_k_anc(d, tree[d].Level - tree[q].Level)
        # d = tree[d].Parent

    if q != d:
        left, right = 0, tree[d].Level
        while left < right - 1:
            mid = (left + right) // 2
            anc1, anc2 = find_k_anc(q, mid), find_k_anc(d, mid)
            if anc1 != anc2:
                left = mid
            else:
                right = mid
        cm = find_k_anc(q, right)
    else:
        cm = q

    return cm


def get_max_for_q(q: int, D_m_ind: int) -> float:
    res = -math.inf
    lca_cur = 1
    for d in D_m_list[D_m_ind]:
        if tree[d].Level < tree[lca_cur].Level or tree[q].Level < tree[lca_cur].Level:
            break
        lca_cur = LCA(q, d)
        if ic_list[lca_cur] > res:
            res = ic_list[lca_cur]
    return res


prepare_anc_cache1()
print('Ready')
n_pat = int(data[4 + n_dis])
print(f'Количество пациентов: {n_pat}')
res = []
step = 0
for cur_pat in range(70, n_pat):
    if step % 2 == 0:
        print(step)
    if step % 10 == 0:
        with open('output_base1.txt', 'w') as fl:
            for dis_ind in res:
                fl.write(f'{dis_ind + 1}\n')
            fl.flush()

    step += 1
    Q_p = sorted(list(map(int, data[5 + n_dis + cur_pat].split()[1:])), key=lambda x: tree[x].Level, reverse=True)
    opt_val = -math.inf
    opt_dis = None
    for D_m_ind in range(len(D_m_list)):
        # cur_val = 0
        # for q in Q_p:
        #     cur_val += get_max_for_q(q, D_m_ind)
        cur_val = sum([get_max_for_q(q, D_m_ind) for q in Q_p])
        if cur_val > opt_val:
            opt_dis = D_m_ind
            opt_val = cur_val
    res.append(opt_dis)

with open('output_base1.txt', 'w') as fl:
    for dis_ind in res:
        fl.write(f'{dis_ind + 1}\n')
    fl.flush()
