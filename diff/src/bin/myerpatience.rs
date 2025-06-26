use similar::{ChangeTag, TextDiff, Algorithm};

#[derive(Debug)]
struct DiffResult {
    algorithm: &'static str,
    operations: Vec<String>,
}

fn analyze_diff(old_text: &str, new_text: &str, algorithm: Algorithm) -> DiffResult {
    let diff = TextDiff::configure()
        .algorithm(algorithm)
        .diff_lines(old_text, new_text);

    let mut operations = Vec::new();
    let mut old_line = 1;
    let mut new_line = 1;

    for change in diff.iter_all_changes() {
        match change.tag() {
            ChangeTag::Equal => {
                operations.push(format!("  {}: {}", new_line, change.value().trim_end()));
                old_line += 1;
                new_line += 1;
            }
            ChangeTag::Delete => {
                operations.push(format!("- {}: {}", old_line, change.value().trim_end()));
                old_line += 1;
            }
            ChangeTag::Insert => {
                operations.push(format!("+ {}: {}", new_line, change.value().trim_end()));
                new_line += 1;
            }
        }
    }

    let algorithm_name = match algorithm {
        Algorithm::Myers => "Myers",
        Algorithm::Patience => "Patience",
        Algorithm::Lcs => "LCS",
    };

    DiffResult {
        algorithm: algorithm_name,
        operations,
    }
}

fn compare_algorithms(old_text: &str, new_text: &str, description: &str) {
    println!("=== {} ===", description);
    println!("OLD:");
    for (i, line) in old_text.lines().enumerate() {
        println!("{}: {}", i + 1, line);
    }
    println!("\nNEW:");
    for (i, line) in new_text.lines().enumerate() {
        println!("{}: {}", i + 1, line);
    }
    println!();

    let myers_result = analyze_diff(old_text, new_text, Algorithm::Myers);
    let patience_result = analyze_diff(old_text, new_text, Algorithm::Patience);

    println!("MYERS DIFF:");
    for op in &myers_result.operations {
        println!("{}", op);
    }

    println!("\nPATIENCE DIFF:");
    for op in &patience_result.operations {
        println!("{}", op);
    }

    // 차이점 분석
    if myers_result.operations != patience_result.operations {
        println!("\n🔍 DIFFERENCE DETECTED!");
        println!("Myers operations: {}", myers_result.operations.len());
        println!("Patience operations: {}", patience_result.operations.len());
    } else {
        println!("\n✅ Both algorithms produced identical results");
    }

    println!("{}", "\n".to_owned() + &"=".repeat(60) + "\n");
}

fn main() {
    // 예제 1: 단순한 변경 (두 알고리즘이 같은 결과)
    let old1 = "line 1\nline 2\nline 3";
    let new1 = "line 1\nmodified line 2\nline 3";
    compare_algorithms(old1, new1, "Example 1: Simple modification");

    // 예제 2: 라인 이동 (Patience가 더 나은 결과)
    let old2 = "A\nB\nC\nD\nE";
    let new2 = "A\nC\nD\nB\nE";
    compare_algorithms(old2, new2, "Example 2: Line movement (B moved down)");

    // 예제 3: 코드 블록 이동
    let old3 = "function a() {\n  return 1;\n}\n\nfunction b() {\n  return 2;\n}\n\nfunction c() {\n  return 3;\n}";
    let new3 = "function a() {\n  return 1;\n}\n\nfunction c() {\n  return 3;\n}\n\nfunction b() {\n  return 2;\n}";
    compare_algorithms(old3, new3, "Example 3: Function reordering");

    // 예제 4: 중복된 라인이 있는 경우
    let old4 = "import os\nimport sys\nprint('hello')\nimport json\nprint('world')";
    let new4 = "import os\nimport json\nprint('hello')\nimport sys\nprint('world')";
    compare_algorithms(old4, new4, "Example 4: Duplicate-like content (imports)");

    // 예제 5: 텍스트 블록 이동
    let old5 = "Header\n\nSection A\nContent A1\nContent A2\n\nSection B\nContent B1\nContent B2\n\nFooter";
    let new5 = "Header\n\nSection B\nContent B1\nContent B2\n\nSection A\nContent A1\nContent A2\n\nFooter";
    compare_algorithms(old5, new5, "Example 5: Section reordering");

    // 예제 6: 복잡한 변경 (추가 + 이동)
    let old6 = "def func1():\n    pass\n\ndef func2():\n    pass\n\ndef func3():\n    pass";
    let new6 = "def func1():\n    pass\n\ndef func3():\n    pass\n\ndef new_func():\n    pass\n\ndef func2():\n    pass";
    compare_algorithms(old6, new6, "Example 6: Complex changes (add + move)");
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_algorithm_differences() {
        // 알고리즘 차이가 나는 경우 테스트
        let old_text = "A\nB\nC\nD";
        let new_text = "A\nC\nD\nB";

        let myers = analyze_diff(old_text, new_text, Algorithm::Myers);
        let patience = analyze_diff(old_text, new_text, Algorithm::Patience);

        println!("Myers: {:?}", myers.operations);
        println!("Patience: {:?}", patience.operations);

        // 일반적으로 이 경우 Patience가 더 직관적인 결과를 보여줍니다
        assert_ne!(myers.operations, patience.operations);
    }

    #[test]
    fn test_simple_case() {
        // 단순한 경우에는 두 알고리즘이 같은 결과
        let old_text = "A\nB\nC";
        let new_text = "A\nX\nC";

        let myers = analyze_diff(old_text, new_text, Algorithm::Myers);
        let patience = analyze_diff(old_text, new_text, Algorithm::Patience);

        // 단순한 수정의 경우 보통 같은 결과
        println!("Myers: {:?}", myers.operations);
        println!("Patience: {:?}", patience.operations);
    }
}

// 추가 유틸리티: 알고리즘 성능 비교
#[allow(dead_code)]
fn benchmark_algorithms(old_text: &str, new_text: &str) {
    use std::time::Instant;

    let start = Instant::now();
    let _myers_diff = TextDiff::configure()
        .algorithm(Algorithm::Myers)
        .diff_lines(old_text, new_text);
    let myers_time = start.elapsed();

    let start = Instant::now();
    let _patience_diff = TextDiff::configure()
        .algorithm(Algorithm::Patience)
        .diff_lines(old_text, new_text);
    let patience_time = start.elapsed();

    println!("Performance comparison:");
    println!("Myers: {:?}", myers_time);
    println!("Patience: {:?}", patience_time);
}