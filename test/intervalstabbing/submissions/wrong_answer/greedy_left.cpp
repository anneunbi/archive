#include <bits/stdc++.h>
using namespace std;

// intentionally suboptimal: picks left endpoints instead of right endpoints
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    if (!(cin >> n)) return 0;
    vector<pair<long long,long long>> a(n);
    for (int i = 0; i < n; ++i) cin >> a[i].first >> a[i].second;

    sort(a.begin(), a.end()); // by left, then right

    vector<long long> pts;
    int i = 0;
    while (i < n) {
        long long p = a[i].first; // choose left endpoint (suboptimal)
        pts.push_back(p);
        ++i;
        while (i < n && a[i].first <= p && p <= a[i].second) ++i;
    }

    cout << (int)pts.size() << "\n";
    for (int j = 0; j < (int)pts.size(); ++j) {
        if (j) cout << ' ';
        cout << pts[j];
    }
    if (!pts.empty()) cout << "\n";
    return 0;
}
