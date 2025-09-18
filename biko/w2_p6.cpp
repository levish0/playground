#include <iostream>
#include <deque>
#include <vector>

int main() {
    std::ios_base::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int N, K;
    std::cin >> N >> K;

    std::vector<int> A(N);
    for (int i = 0; i < N; i++) {
        std::cin >> A[i];
    }

    std::deque<int> dq;

    for (int i = 0; i < K; i++) {
        while (!dq.empty() && A[dq.back()] <= A[i]) {
            dq.pop_back();
        }
        dq.push_back(i);
    }

    std::cout << A[dq.front()] << "\n";


    for (int i = K; i < N; i++) {
        while (!dq.empty() && dq.front() <= i - K) {
            dq.pop_front();
        }

        while (!dq.empty() && A[dq.back()] <= A[i]) {
            dq.pop_back();
        }

        dq.push_back(i);
        std::cout << A[dq.front()] << "\n";
    }
    
    return 0;
}