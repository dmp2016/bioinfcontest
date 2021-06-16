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


with open('QProblem3/test3') as fl:
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


def tree_rec(root: TreeV):
    for ind in range(len(root.Children)):
        tree[root.Children[ind]].BrancnNum = root.BranchNum + ind
    for ind in root.Children:
        tree_rec(tree[ind])


tree[1].BranchNum = 0
tree_rec(tree[1])

print(f'Количество веток: {max([tree[item].BranchNum for item in tree])}')

print(f'Максимальная глубина: {max([tree[v].Level for v in tree])}')

n_dis = int(data[3])
print(f'Количество болезней: {n_dis}')
D_m_list = sorted([list(map(int, data[4 + cur_dis].split()[1:])) for cur_dis in range(n_dis)], reverse=True)

cache = dict()


def LCA_cache(q: int, d: int) -> int:
    if (q, d) in cache:
        return cache[(q, d)]
    if (d, q) in cache:
        return cache[(d, q)]

    dd = [(d, q)]

    while tree[q].Level > tree[d].Level:
        q = tree[q].Parent
        dd.append((d, q))

    while tree[q].Level < tree[d].Level:
        d = tree[d].Parent
        dd.append((d, q))

    while q != d:
        q = tree[q].Parent
        d = tree[d].Parent
        dd.append((d, q))

    for d in dd:
        cache[d] = q
    return q


def LCA(q: int, d: int) -> int:
    while tree[q].Level > tree[d].Level:
        q = tree[q].Parent

    while tree[q].Level < tree[d].Level:
        d = tree[d].Parent

    while q != d:
        q = tree[q].Parent
        d = tree[d].Parent

    return q


@lru_cache(maxsize=1000000)
def LCA_rec(q: int, d: int) -> int:
    if tree[q].Level > tree[d].Level:
        return LCA_rec(tree[q].Parent, d)

    if tree[q].Level < tree[d].Level:
        return LCA_rec(q, tree[d].Parent)

    if q != d:
        return LCA_rec(tree[q].Parent, tree[d].Parent)


def get_max_for_q(q: int, D_m_ind: int) -> float:
    res = -math.inf
    lca_opt = 0
    for d in D_m_list[D_m_ind]:
        if d < lca_opt:
            break
        lca_cur = LCA(q, d)
        if ic_list[lca_cur] > res:
            res = ic_list[lca_cur]
            lca_opt = lca_cur
    return res


n_pat = int(data[4 + n_dis])
print(f'Количество пациентов: {n_pat}')
res = []
step = 0
for cur_pat in range(n_pat):
    if step % 50 == 0:
        print(step)
    step += 1
    Q_p = list(map(int, data[5 + n_dis + cur_pat].split()[1:]))
    opt_val = -math.inf
    opt_dis = None
    for D_m_ind in range(len(D_m_list)):
        cur_val = 0
        for q in Q_p:
            cur_val += get_max_for_q(q, D_m_ind)
        # sum([get_max_for_q(q, D_m_ind) for q in Q_p])
        if cur_val > opt_val:
            opt_dis = D_m_ind
            opt_val = cur_val
    res.append(opt_dis)

with open('output.txt', 'w') as fl:
    for dis_ind in res:
        fl.write(f'{dis_ind + 1}\n')
    fl.flush()
