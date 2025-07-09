use diffy::{create_patch, Line};
use std::collections::HashMap;

#[derive(Debug, Clone)]
pub struct DocumentVersion {
    pub version_id: String,  // usize에서 String으로 변경
    pub content: String,
    pub author: String,
    pub timestamp: u64,
}

#[derive(Debug, Clone)]
pub struct BlameLine {
    pub line_number: usize,
    pub content: String,
    pub author: String,
    pub version_id: String,  // usize에서 String으로 변경
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

    /// 새로운 문서 버전 추가 (버전명을 직접 지정) - 개별 추가용
    pub fn add_version(&mut self, version_id: String, content: String, author: String, timestamp: u64) {
        let doc_version = DocumentVersion {
            version_id,
            content,
            author,
            timestamp,
        };
        self.versions.push(doc_version);

        // blame 정보 업데이트
        self.update_blame();
    }

    /// 여러 버전을 한 번에 추가하고 최종 blame 계산 - 위키 DB 조회용
    pub fn build_from_revisions(&mut self, revisions: Vec<DocumentVersion>) {
        // 타임스탬프 순으로 정렬 (가장 오래된 것부터)
        let mut sorted_revisions = revisions;
        sorted_revisions.sort_by_key(|v| v.timestamp);

        self.versions = sorted_revisions;

        // 모든 버전을 순차적으로 처리하여 최종 blame 계산
        self.build_blame_from_all_versions();
    }

    /// 모든 버전을 순차적으로 처리하여 blame 정보 구축
    fn build_blame_from_all_versions(&mut self) {
        if self.versions.is_empty() {
            return;
        }

        // 첫 번째 버전으로 초기화
        let first_version = &self.versions[0];
        self.blame_info = first_version
            .content
            .lines()
            .enumerate()
            .map(|(i, line)| BlameLine {
                line_number: i + 1,
                content: line.to_string(),
                author: first_version.author.clone(),
                version_id: first_version.version_id.clone(),
                timestamp: first_version.timestamp,
            })
            .collect();

        // 나머지 버전들을 순차적으로 적용
        for i in 1..self.versions.len() {
            self.apply_version_diff(i);
        }
    }

    /// 특정 버전의 diff를 현재 blame에 적용
    fn apply_version_diff(&mut self, version_index: usize) {
        let prev_version = &self.versions[version_index - 1];
        let curr_version = &self.versions[version_index];

        // Diffy로 diff 생성
        let patch = create_patch(&prev_version.content, &curr_version.content);

        // 새로운 blame 정보 구성
        let mut new_blame = Vec::new();
        let mut old_line_idx = 0;
        let mut new_line_number = 1;

        // 각 hunk를 순회하여 변경사항 처리
        for hunk in patch.hunks() {
            // hunk 시작 전까지의 변경되지 않은 라인들
            let old_start = hunk.old_range().start();
            while old_line_idx < old_start {
                if old_line_idx < self.blame_info.len() {
                    let mut blame_line = self.blame_info[old_line_idx].clone();
                    blame_line.line_number = new_line_number;
                    new_blame.push(blame_line);
                }
                old_line_idx += 1;
                new_line_number += 1;
            }

            // hunk 내의 변경사항 처리
            for line in hunk.lines() {
                match line {
                    Line::Context(content) => {
                        // 변경되지 않은 라인 - 기존 blame 정보 유지
                        if old_line_idx < self.blame_info.len() {
                            let mut blame_line = self.blame_info[old_line_idx].clone();
                            blame_line.line_number = new_line_number;
                            new_blame.push(blame_line);
                        }
                        old_line_idx += 1;
                        new_line_number += 1;
                    }
                    Line::Delete(_) => {
                        // 삭제된 라인 - blame에서 제거
                        old_line_idx += 1;
                    }
                    Line::Insert(content) => {
                        // 새로 추가된 라인 - 현재 버전 정보로 blame 생성
                        new_blame.push(BlameLine {
                            line_number: new_line_number,
                            content: content.trim_end().to_string(),
                            author: curr_version.author.clone(),
                            version_id: curr_version.version_id.clone(),
                            timestamp: curr_version.timestamp,
                        });
                        new_line_number += 1;
                    }
                }
            }
        }

        // 마지막 hunk 이후 남은 라인들 처리
        while old_line_idx < self.blame_info.len() {
            let mut blame_line = self.blame_info[old_line_idx].clone();
            blame_line.line_number = new_line_number;
            new_blame.push(blame_line);
            old_line_idx += 1;
            new_line_number += 1;
        }

        self.blame_info = new_blame;
    }

    /// blame 정보 계산 및 업데이트 (단일 버전 추가용)
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
                    version_id: first_version.version_id.clone(),
                    timestamp: first_version.timestamp,
                })
                .collect();
            return;
        }

        // 단일 버전 추가 시 마지막 버전만 적용
        let version_index = self.versions.len() - 1;
        self.apply_version_diff(version_index);
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
                "{:4} ({:10} {:12} {}) {}\n",
                blame_line.line_number,
                blame_line.author,
                blame_line.version_id,
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

    /// 버전별 라인 수 통계
    pub fn get_version_stats(&self) -> HashMap<String, usize> {
        let mut stats = HashMap::new();

        for blame_line in &self.blame_info {
            *stats.entry(blame_line.version_id.clone()).or_insert(0) += 1;
        }

        stats
    }

    /// 사용 중인 diff 알고리즘 정보
    pub fn diff_algorithm(&self) -> &'static str {
        "Diffy (Myers)"
    }

    /// 상세한 diff 정보 출력 (디버깅용)
    pub fn show_diff(&self) -> String {
        if self.versions.len() < 2 {
            return "No diff available".to_string();
        }

        let prev_version = &self.versions[self.versions.len() - 2];
        let curr_version = &self.versions[self.versions.len() - 1];

        let patch = create_patch(&prev_version.content, &curr_version.content);

        format!("{}", patch)
    }

    /// 모든 버전 정보 가져오기
    pub fn get_versions(&self) -> &[DocumentVersion] {
        &self.versions
    }

    /// 특정 버전 정보 가져오기
    pub fn get_version(&self, version_id: &str) -> Option<&DocumentVersion> {
        self.versions.iter().find(|v| v.version_id == version_id)
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
    fn test_wiki_blame_from_db_revisions() {
        let mut blame = DocumentBlame::new();

        // DB에서 조회한 리비전들 (시간순으로 정렬되지 않은 상태)
        let revisions = vec![
            DocumentVersion {
                version_id: "hotfix-v1.2".to_string(),
                content: "modified line 1\nmodified line 2\nline 3\nline 4".to_string(),
                author: "charlie".to_string(),
                timestamp: 3000,
            },
            DocumentVersion {
                version_id: "initial".to_string(),
                content: "line 1\nline 2\nline 3".to_string(),
                author: "alice".to_string(),
                timestamp: 1000,
            },
            DocumentVersion {
                version_id: "feature-branch".to_string(),
                content: "line 1\nmodified line 2\nline 3\nline 4".to_string(),
                author: "bob".to_string(),
                timestamp: 2000,
            },
        ];

        // 한 번에 모든 리비전 처리
        blame.build_from_revisions(revisions);

        println!("Wiki blame from DB revisions:");
        println!("{}", blame.format_blame());

        // 작성자별 통계
        let stats = blame.get_author_stats();
        println!("Author stats: {:?}", stats);

        // 버전별 통계
        let version_stats = blame.get_version_stats();
        println!("Version stats: {:?}", version_stats);
    }

    #[test]
    fn test_document_blame_with_custom_versions() {
        let mut blame = DocumentBlame::new();

        println!("Using {} diff algorithm", blame.diff_algorithm());

        // 첫 번째 버전
        blame.add_version(
            "initial".to_string(),
            "line 1\nline 2\nline 3".to_string(),
            "alice".to_string(),
            1000,
        );

        // 두 번째 버전 - line 2 수정, line 4 추가
        blame.add_version(
            "feature-branch".to_string(),
            "line 1\nmodified line 2\nline 3\nline 4".to_string(),
            "bob".to_string(),
            2000,
        );

        // 세 번째 버전 - line 1 수정
        blame.add_version(
            "hotfix-v1.2".to_string(),
            "modified line 1\nmodified line 2\nline 3\nline 4".to_string(),
            "charlie".to_string(),
            3000,
        );

        println!("{}", blame.format_blame());

        // 작성자별 통계
        let stats = blame.get_author_stats();
        println!("Author stats: {:?}", stats);

        // 버전별 통계
        let version_stats = blame.get_version_stats();
        println!("Version stats: {:?}", version_stats);

        // diff 정보 출력
        println!("\nLast diff:");
        println!("{}", blame.show_diff());
    }

    #[test]
    fn test_version_lookup() {
        let mut blame = DocumentBlame::new();

        blame.add_version(
            "v1.0.0".to_string(),
            "first line\nsecond line\nthird line".to_string(),
            "alice".to_string(),
            1000,
        );

        blame.add_version(
            "v1.1.0".to_string(),
            "first line\nmodified second line\nthird line".to_string(),
            "bob".to_string(),
            2000,
        );

        // 특정 버전 정보 확인
        if let Some(version) = blame.get_version("v1.0.0") {
            println!("Version v1.0.0: {:?}", version);
        }

        // 특정 라인의 blame 정보 확인
        if let Some(blame_info) = blame.get_line_blame(2) {
            assert_eq!(blame_info.author, "bob");
            assert_eq!(blame_info.version_id, "v1.1.0");
            println!("Line 2 blame: {:?}", blame_info);
        }
    }
}

// 위키 DB 사용 예제
fn main() {
    let mut document_blame = DocumentBlame::new();

    println!("Wiki Document Blame using {} diff algorithm\n", document_blame.diff_algorithm());

    // 방법 1: DB에서 모든 리비전을 조회해서 한 번에 처리 (권장)
    let db_revisions = vec![
        DocumentVersion {
            version_id: "rev-003".to_string(),
            content: "Hello Worlds\nBeautiful World\nThis is the modified first line\nThis is a new line\nEnd of modified document".to_string(),
            author: "Charlie".to_string(),
            timestamp: 1641168000, // 2022-01-03
        },
        DocumentVersion {
            version_id: "rev-001".to_string(),
            content: "Hello World\nThis is the first line\nEnd of document".to_string(),
            author: "Alice".to_string(),
            timestamp: 1640995200, // 2022-01-01
        },
        DocumentVersion {
            version_id: "rev-002".to_string(),
            content: "Hello World\nThis is the modified first line\nThis is a new line\nEnd of document".to_string(),
            author: "Bob".to_string(),
            timestamp: 1641081600, // 2022-01-02
        },
    ];

    // 한 번에 모든 리비전 처리 (내부에서 타임스탬프 순으로 정렬됨)
    document_blame.build_from_revisions(db_revisions);

    // blame 정보 출력
    println!("Wiki Document Blame:");
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

    // 버전별 통계
    println!("\nVersion Statistics:");
    for (version, lines) in document_blame.get_version_stats() {
        println!("{}: {} lines", version, lines);
    }

    // 모든 버전 정보 출력
    println!("\nAll versions (sorted by timestamp):");
    for version in document_blame.get_versions() {
        println!("Version: {} by {} at {}", version.version_id, version.author, version.timestamp);
    }

    println!("{}", "\n".to_owned() + "=".repeat(50).as_str());
    println!("방법 2: 개별 버전 추가 (실시간 업데이트용)");
    println!("{}", "=".repeat(50));

    // 방법 2: 개별 버전을 순차적으로 추가 (실시간 업데이트용)
    let mut realtime_blame = DocumentBlame::new();

    realtime_blame.add_version(
        "rev-001".to_string(),
        "Hello World\nThis is the first line\nEnd of document".to_string(),
        "Alice".to_string(),
        1640995200,
    );

    realtime_blame.add_version(
        "rev-002".to_string(),
        "Hello World\nThis is the modified first line\nThis is a new line\nEnd of document".to_string(),
        "Bob".to_string(),
        1641081600,
    );

    println!("Realtime blame after 2 revisions:");
    println!("{}", realtime_blame.format_blame());
}