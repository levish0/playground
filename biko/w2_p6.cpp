#include <iostream>
#include <deque>
#include <vector>
using namespace std;

int main() {
    int N, K;
    cin >> N >> K;

    vector<int> A(N);
    for (int i = 0; i < N; i++) {
        cin >> A[i];
    }

    deque<int> dq;

    for (int i = 0; i < K; i++) {
        while (!dq.empty() && A[dq.back()] <= A[i]) {
            dq.pop_back();
        }
        dq.push_back(i);
    }

    cout << A[dq.front()] << "\n";

    for (int i = K; i < N; i++) {
        while (!dq.empty() && dq.front() <= i - K) {
            dq.pop_front();
        }

        while (!dq.empty() && A[dq.back()] <= A[i]) {
            dq.pop_back();
        }

        dq.push_back(i);
        cout << A[dq.front()] << "\n";
    }
    
    return 0;
}