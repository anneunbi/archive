#include <bits/stdc++.h>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n)) return 0;
    vector<pair<long long,long long>> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i].first >> a[i].second;

    sort(a.begin(), a.end(), [](auto &x, auto &y){
        if (x.second != y.second) return x.second < y.second;
        return x.first < y.first;
    });

    vector<long long> pts;
    long long last = LLONG_MIN;
    for (auto &iv : a) {
        long long l = iv.first, r = iv.second;
        if (pts.empty() || last < l || last > r) {
            last = r;
            pts.push_back(last);
        }
    }

    cout << (int)pts.size() << "\n";
    for (int i = 0; i < (int)pts.size(); ++i) {
        if (i) cout << ' ';
        cout << pts[i];
    }
    if (!pts.empty()) cout << "\n";
    return 0;
}
