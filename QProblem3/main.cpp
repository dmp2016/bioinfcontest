#include <iostream>
#include <algorithm>
#include <vector>
#include <map>
#include <string>

using namespace std;

int const C_MIN_INT = -2000000000;

struct TreeV
{
    int IC;
    int Parent;
    int Level;
    vector<int> Children;
    int BranchNum;
};

// map<pair<int, int>, int> anc_cache;
vector<vector<int>> anc_cache;
vector<TreeV> tree;
int base = 100;


int find_k_anc(int p10, int k)
{
    int p2 = 1;
    int p = p10;
    int p3 = 0;
    while (k)
    {
        int dm = k % base;
        if (dm)
            p = anc_cache[p][p3 + dm];
            // p = anc_cache[make_pair(p, p2 * dm)];
        k /= base;
        p2 *= base;
        p3 += base;
    }
    return p;
}

void prepare_anc_cache1()
{
    vector<int> front;
    front.push_back(1);
    while (front.size() > 0)
    {
        for (int i = 0; i < front.size(); i++)
        {
            int p = front[i];
            anc_cache[p].resize(600);
            int p2 = 1, base2 = 1, p3 = 0;
            while (tree[p].Level >= p2)
            {
                // anc_cache[make_pair(p, p2)] = find_k_anc(tree.at(p).Parent, p2 - 1);
                anc_cache[p][p3 + p2 / base2] = find_k_anc(tree[p].Parent, p2 - 1);
                p2 += base2;
                if (p2 % (base2 * base) == 0)
                {
                    base2 *= base;
                    p2 = base2;
                    p3 += base;
                }
            }
        }
        vector<int> new_front;
        for (int i = 0; i < front.size(); i++)
            for (int j = 0; j < tree[front[i]].Children.size(); j++)
                new_front.push_back(tree[front[i]].Children[j]);
        front = new_front;
    }
}

int LCA1(int q, int d)
{
    if (tree[q].BranchNum == tree[d].BranchNum)
        return (tree[q].Level < tree[d].Level) ? q : d;

    if (tree[q].Level > tree[d].Level)
        q = find_k_anc(q, tree[q].Level - tree[d].Level);

    if (tree[q].Level < tree[d].Level)
        d = find_k_anc(d, tree[d].Level - tree[q].Level);

    int cm;
    if (q != d)
    {
        int left = 0, right = tree[d].Level;
        while (left < right - 1)
        {
            int mid = (left + right) / 2;
            int anc1 = find_k_anc(q, mid), anc2 = find_k_anc(d, mid);
            if (anc1 != anc2)
                left = mid;
            else
                right = mid;
        }
        cm = find_k_anc(q, right);
    }
    else
        cm = q;

    return cm;
}

bool const DComp (int const & a, int const & b)
{
    return tree[a].Level > tree[b].Level;
}

int main(int argc, char *argv[])
{
    char *inp_file, *out_file;
    int pat_from, pat_to;
    if (argc == 5)
    {
        inp_file = argv[1];
        out_file = argv[2];
        pat_from = stoi(argv[3]);
        pat_to = stoi(argv[4]);
    }
    else
    {
        cout << "Error. 4 parameters expected.";
        return 1;
    }
    cout << "Input file: " << inp_file << endl;
    cout << "Output file: " << out_file << endl;
    cout << "From: " << pat_from << endl;
    cout << "To: " << pat_to << endl;
	freopen(inp_file, "r", stdin);
    int n_tree;
    cin >> n_tree;
    anc_cache.resize(n_tree + 1);
    tree.resize(n_tree + 1);
    tree[1].BranchNum = 0;
    tree[1]. Level = 0;
    tree[1].Parent = 0;
    for (int i = 2; i <= n_tree; i++)
    {
        int parent;
        cin >> parent;
        tree[i].Parent = parent;
        tree[i].Level = tree[parent].Level + 1;
        tree[parent].Children.push_back(i);
    }

    int n_ic = n_tree;
    vector<int> ic_list;
    ic_list.resize(n_ic + 1);
    ic_list.resize(n_ic + 1);
    for (int i = 1; i <= n_ic; i++)
    {
        int ic;
        cin >> ic;
        ic_list[i] = ic;
    }

    int n_D;
    vector<vector<int>> D;
    cin >> n_D;
    D.resize(n_D + 1);
    for (int i = 1; i <= n_D; i++)
    {
        int n_d;
        cin >> n_d;
        for (int j = 0; j < n_d; j++)
        {
            int d;
            cin >> d;
            D[i].push_back(d);
        }
        sort(D[i].begin(), D[i].end(), DComp);
    }

    int n_Q;
    cin >> n_Q;
    vector<vector<int>> Q;
    Q.resize(n_Q + 1);
    for (int i = 1; i <= n_Q; i++)
    {
        int n_q;
        cin >> n_q;
        for (int j = 0; j < n_q; j++)
        {
            int q;
            cin >> q;
            Q[i].push_back(q);
        }
    }

    vector<int> tree_stack;
    tree_stack.push_back(1);
    int cur_branch = 0;
    while (tree_stack.size() > 0)
    {
        int cur = tree_stack[tree_stack.size() - 1];
        tree_stack.pop_back();
        if (tree[cur].Children.size() > 0)
            tree[tree[cur].Children[0]].BranchNum = tree[cur].BranchNum;
        for (int i = 1; i < tree[cur].Children.size(); i++)
        {
            cur_branch += 1;
            tree[tree[cur].Children[i]].BranchNum = cur_branch;
        }
        for (int i = 0; i < tree[cur].Children.size(); i++)
            tree_stack.push_back(tree[cur].Children[i]);
    }
    cout << "Tree size: " << n_tree << endl;
    cout << "Branch amount: " << cur_branch << endl;
    cout << "Decea amount: " << n_D << endl;
    cout << "Patient amount: " << n_Q << endl;

    prepare_anc_cache1();

    vector<int> res;
    if (pat_to == 0)
        pat_to = n_Q;
    for (int cur_pat = pat_from; cur_pat <= pat_to; cur_pat ++)
    {
        if (cur_pat % 100 == 0)
            cout << cur_pat << endl;
        int opt_val = C_MIN_INT;
        int opt_dis;
        for (int d_num = 1; d_num <= n_D; d_num++)
        {
            int cur_val = 0;
            for (int q_ind = 0; q_ind < Q[cur_pat].size(); q_ind++)
            {
                int q = Q[cur_pat][q_ind];
                int cur_max = C_MIN_INT;
                for (int d_ind = 0; d_ind < D[d_num].size(); d_ind++)
                {
                    int d = D[d_num][d_ind];
                    int lca_cur = LCA1(q, d);
                    if (ic_list[lca_cur] > cur_max)
                        cur_max = ic_list[lca_cur];
                }
                cur_val += cur_max;
            }
            if (cur_val > opt_val)
            {
                opt_dis = d_num;
                opt_val = cur_val;
            }
        }
        res.push_back(opt_dis);
        if (cur_pat % 5000 == 0)
        {
            freopen(out_file, "w", stdout);
            for (int i = 0; i < res.size(); i++)
                cout << res[i] << endl;
            freopen("CON", "w", stdout);
        }
    }

    freopen(out_file, "w", stdout);
    for (int i = 0; i < res.size(); i++)
        cout << res[i] << endl;

	return 0;
}
