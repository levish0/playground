use similar::{ChangeTag, TextDiff};
use std::collections::HashMap;

#[derive(Debug, Clone)]
pub struct DocumentVersion {
    pub version: usize,
    pub content: String,
    pub author: String,
    pub timestamp: u64,
}

#[derive(Debug, Clone)]
pub struct BlameLine {
    pub line_number: usize,
    pub content: String,
    pub author: String,
    pub version: usize,
    pub timestamp: u64,
}

pub struct DocumentBlame {
    versions: Vec<DocumentVersion>,
    blame_info: Vec<BlameLine>,
}

impl DocumentBlame {
    pub fn new() -> Self {
        Self {
            versions: Vec::new(),
            blame_info: Vec::new(),
        }
    }

    /// 새로운 문서 버전 추가
    pub fn add_version(&mut self, content: String, author: String, timestamp: u64) {
        let version = self.versions.len();
        let doc_version = DocumentVersion {
            version,
            content,
            author,
            timestamp,
        };
        self.versions.push(doc_version);

        // blame 정보 업데이트
        self.update_blame();
    }

    /// blame 정보 계산 및 업데이트
    fn update_blame(&mut self) {
        if self.versions.is_empty() {
            return;
        }

        // 첫 번째 버전인 경우
        if self.versions.len() == 1 {
            let first_version = &self.versions[0];
            self.blame_info = first_version
                .content
                .lines()
                .enumerate()
                .map(|(i, line)| BlameLine {
                    line_number: i + 1,
                    content: line.to_string(),
                    author: first_version.author.clone(),
                    version: first_version.version,
                    timestamp: first_version.timestamp,
                })
                .collect();
            return;
        }

        // 이전 버전과 현재 버전 비교
        let prev_version = &self.versions[self.versions.len() - 2];
        let curr_version = &self.versions[self.versions.len() - 1];

        let diff = TextDiff::from_lines(&prev_version.content, &curr_version.content);

        // 새로운 blame 정보 구성
        let mut new_blame = Vec::new();
        let mut old_line_idx = 0;
        let mut new_line_number = 1;

        for change in diff.iter_all_changes() {
            match change.tag() {
                ChangeTag::Equal => {
                    // 변경되지 않은 라인 - 기존 blame 정보 유지
                    if old_line_idx < self.blame_info.len() {
                        let mut blame_line = self.blame_info[old_line_idx].clone();
                        blame_line.line_number = new_line_number;
                        new_blame.push(blame_line);
                    }
                    old_line_idx += 1;
                    new_line_number += 1;
                }
                ChangeTag::Delete => {
                    // 삭제된 라인 - blame에서 제거
                    old_line_idx += 1;
                }
                ChangeTag::Insert => {
                    // 새로 추가된 라인 - 현재 버전 정보로 blame 생성
                    new_blame.push(BlameLine {
                        line_number: new_line_number,
                        content: change.value().trim_end().to_string(),
                        author: curr_version.author.clone(),
                        version: curr_version.version,
                        timestamp: curr_version.timestamp,
                    });
                    new_line_number += 1;
                }
            }
        }

        self.blame_info = new_blame;
    }

    /// 특정 라인의 blame 정보 가져오기
    pub fn get_line_blame(&self, line_number: usize) -> Option<&BlameLine> {
        self.blame_info
            .iter()
            .find(|blame| blame.line_number == line_number)
    }

    /// 전체 blame 정보 가져오기
    pub fn get_blame(&self) -> &[BlameLine] {
        &self.blame_info
    }

    /// blame 정보를 텍스트로 출력
    pub fn format_blame(&self) -> String {
        let mut result = String::new();

        for blame_line in &self.blame_info {
            result.push_str(&format!(
                "{:4} ({:10} v{:2} {}) {}\n",
                blame_line.line_number,
                blame_line.author,
                blame_line.version,
                format_timestamp(blame_line.timestamp),
                blame_line.content
            ));
        }

        result
    }

    /// 작성자별 라인 수 통계
    pub fn get_author_stats(&self) -> HashMap<String, usize> {
        let mut stats = HashMap::new();

        for blame_line in &self.blame_info {
            *stats.entry(blame_line.author.clone()).or_insert(0) += 1;
        }

        stats
    }
}

fn format_timestamp(timestamp: u64) -> String {
    // 간단한 타임스탬프 포맷팅 (실제로는 chrono crate 등을 사용하는 것이 좋음)
    format!("{}", timestamp)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_document_blame() {
        let mut blame = DocumentBlame::new();

        // 첫 번째 버전
        blame.add_version(
            "line 1\nline 2\nline 3".to_string(),
            "alice".to_string(),
            1000,
        );

        // 두 번째 버전 - line 2 수정, line 4 추가
        blame.add_version(
            "line 1\nmodified line 2\nline 3\nline 4".to_string(),
            "bob".to_string(),
            2000,
        );

        // 세 번째 버전 - line 1 수정
        blame.add_version(
            "modified line 1\nmodified line 2\nline 3\nline 4".to_string(),
            "charlie".to_string(),
            3000,
        );

        println!("{}", blame.format_blame());

        // 작성자별 통계
        let stats = blame.get_author_stats();
        println!("Author stats: {:?}", stats);
    }
}

// 사용 예제
fn main() {
    let mut document_blame = DocumentBlame::new();

    // 문서의 각 버전을 순서대로 추가
    document_blame.add_version(
        "Hello World\nThis is the first line\nEnd of document".to_string(),
        "Alice".to_string(),
        1640995200, // 2022-01-01
    );

    document_blame.add_version(
        "Hello World\nwhat the fuck This is the modified first line\nThis is a new line\nEnd of document".to_string(),
        "Bob".to_string(),
        1641081600, // 2022-01-02
    );

    document_blame.add_version(
        "Hello Worlds\nBeautiful World\nThis is the modified first line\nThis is a new line\nEnd of modified document".to_string(),
        "Charlie".to_string(),
        1641168000, // 2022-01-03
    );

    // blame 정보 출력
    println!("Document Blame:");
    println!("{}", document_blame.format_blame());

    // 특정 라인의 blame 정보 확인
    if let Some(blame_info) = document_blame.get_line_blame(2) {
        println!("\nLine 2 blame: {:?}", blame_info);
    }

    // 작성자별 통계
    println!("\nAuthor Statistics:");
    for (author, lines) in document_blame.get_author_stats() {
        println!("{}: {} lines", author, lines);
    }
}