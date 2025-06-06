use std::io;

fn main() {
    let stdin = io::stdin();
    let mut input = String::new();
    stdin.read_line(&mut input).unwrap();
    let t: usize = input.trim().parse().unwrap();

    for _ in 0..t {
        let mut input = String::new();
        stdin.read_line(&mut input).unwrap();
        let signal = input.trim();

        if matches_pattern(signal) {
            println!("YES");
        } else {
            println!("NO");
        }
    }
}

fn matches_pattern(s: &str) -> bool {
    let chars: Vec<char> = s.chars().collect();

    fn try_match(chars: &Vec<char>, pos: usize, matched: bool) -> bool {
        if pos >= chars.len() {
            return matched;
        }

        // 01+
        if pos + 1 < chars.len() && chars[pos] == '0' && chars[pos + 1] == '1' {
            if try_match(chars, pos + 2, true) {
                return true;
            }
        }

        // 100+1+
        if pos + 2 < chars.len()
            && chars[pos] == '1'
            && chars[pos + 1] == '0'
            && chars[pos + 2] == '0'
        {
            let mut i = pos + 3;
            while i < chars.len() && chars[i] == '0' {
                i += 1;
            }
            let zeros_end = i;

            for zero_end in (pos + 3)..=zeros_end {
                if zero_end < chars.len() && chars[zero_end] == '1' {
                    let ones_start = zero_end;
                    let mut j = zero_end;

                    while j < chars.len() && chars[j] == '1' {
                        j += 1;
                    }

                    for ones_end in (ones_start + 1)..=j {
                        if try_match(chars, ones_end, true) {
                            return true;
                        }
                    }
                }
            }
        }

        false
    }

    try_match(&chars, 0, false)
}
