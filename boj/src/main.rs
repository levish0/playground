use std::io::{self, BufRead};

const MOD: u64 = 1_000_000_007;

fn main() {
    let stdin = io::stdin();
    let mut lines = stdin.lock().lines();

    let n: usize = lines.next().unwrap().unwrap().trim().parse().unwrap();

    for _ in 0..n {
        let _line = lines.next().unwrap().unwrap();
    }

    let code1_count = calculate_code1_count(n);

    let code2_count = ((n as u64) * (n as u64)) % MOD;

    println!("{} {}", code1_count, code2_count);
}

fn calculate_code1_count(n: usize) -> u64 {
    let mut memo = vec![vec![0u64; n + 2]; n + 2];

    memo[n][n] = 1;

    for i in (1..=n).rev() {
        for j in (1..=n).rev() {
            if memo[i][j] > 0 {
                memo[i - 1][j] = (memo[i - 1][j] + memo[i][j]) % MOD;
                memo[i][j - 1] = (memo[i][j - 1] + memo[i][j]) % MOD;
            }
        }
    }

    let mut total_code1 = 0;

    for j in 0..=n {
        total_code1 = (total_code1 + memo[0][j]) % MOD;
    }

    for i in 1..=n {
        total_code1 = (total_code1 + memo[i][0]) % MOD;
    }

    total_code1
}
