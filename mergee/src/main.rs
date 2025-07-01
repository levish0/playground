use difflib::sequencematcher::{Match, SequenceMatcher};
use std::collections::HashMap;

/// Result of a 3-way merge operation
#[derive(Debug, Clone)]
pub struct MergeResult {
    /// The merged text with conflict markers if conflicts exist
    pub merged_text: String,
    /// Whether the merge had conflicts
    pub has_conflict: bool,
}

/// Simple 3-way merge for strings
pub struct SimpleMerge3;

impl SimpleMerge3 {
    /// Merge two strings with a common base
    ///
    /// # Arguments
    /// * `base` - The common ancestor text
    /// * `ours` - Our version of the text
    /// * `theirs` - Their version of the text
    ///
    /// # Returns
    /// A `MergeResult` containing the merged text and conflict status
    pub fn merge_strings(base: &str, ours: &str, theirs: &str) -> MergeResult {
        let base_lines: Vec<&str> = base.lines().collect();
        let ours_lines: Vec<&str> = ours.lines().collect();
        let theirs_lines: Vec<&str> = theirs.lines().collect();

        Self::merge_lines(&base_lines, &ours_lines, &theirs_lines)
    }

    /// Merge with custom conflict markers
    pub fn merge_strings_with_markers(
        base: &str,
        ours: &str,
        theirs: &str,
        start_marker: &str,
        mid_marker: &str,
        end_marker: &str
    ) -> MergeResult {
        let base_lines: Vec<&str> = base.lines().collect();
        let ours_lines: Vec<&str> = ours.lines().collect();
        let theirs_lines: Vec<&str> = theirs.lines().collect();

        Self::merge_lines_with_markers(&base_lines, &ours_lines, &theirs_lines, start_marker, mid_marker, end_marker)
    }

    fn merge_lines(base: &[&str], ours: &[&str], theirs: &[&str]) -> MergeResult {
        Self::merge_lines_with_markers(base, ours, theirs, "<<<<<<< HEAD", "=======", ">>>>>>> MERGE")
    }

    fn merge_lines_with_markers(
        base: &[&str],
        ours: &[&str],
        theirs: &[&str],
        start_marker: &str,
        mid_marker: &str,
        end_marker: &str
    ) -> MergeResult {
        let regions = Self::find_merge_regions(base, ours, theirs);
        let mut result_lines = Vec::new();
        let mut has_conflict = false;

        for region in regions {
            match region {
                MergeRegion::Unchanged { base_start, base_end } => {
                    for i in base_start..base_end {
                        result_lines.push(base[i].to_string());
                    }
                }
                MergeRegion::OursOnly { ours_start, ours_end } => {
                    for i in ours_start..ours_end {
                        result_lines.push(ours[i].to_string());
                    }
                }
                MergeRegion::TheirsOnly { theirs_start, theirs_end } => {
                    for i in theirs_start..theirs_end {
                        result_lines.push(theirs[i].to_string());
                    }
                }
                MergeRegion::Conflict { ours_start, ours_end, theirs_start, theirs_end } => {
                    has_conflict = true;
                    result_lines.push(start_marker.to_string());
                    for i in ours_start..ours_end {
                        result_lines.push(ours[i].to_string());
                    }
                    result_lines.push(mid_marker.to_string());
                    for i in theirs_start..theirs_end {
                        result_lines.push(theirs[i].to_string());
                    }
                    result_lines.push(end_marker.to_string());
                }
            }
        }

        MergeResult {
            merged_text: result_lines.join("\n"),
            has_conflict,
        }
    }

    fn find_merge_regions(base: &[&str], ours: &[&str], theirs: &[&str]) -> Vec<MergeRegion> {
        let sync_regions = Self::find_sync_regions(base, ours, theirs);
        let mut regions = Vec::new();

        let mut base_idx = 0;
        let mut ours_idx = 0;
        let mut theirs_idx = 0;

        for (base_start, base_end, ours_start, ours_end, theirs_start, theirs_end) in sync_regions {
            // Handle the gap before this sync region
            if base_idx < base_start || ours_idx < ours_start || theirs_idx < theirs_start {
                let ours_len = ours_start - ours_idx;
                let theirs_len = theirs_start - theirs_idx;

                if ours_len > 0 && theirs_len > 0 {
                    // Check if ours and theirs are the same
                    let ours_slice = &ours[ours_idx..ours_start];
                    let theirs_slice = &theirs[theirs_idx..theirs_start];

                    if ours_slice == theirs_slice {
                        // Same change on both sides
                        regions.push(MergeRegion::OursOnly {
                            ours_start: ours_idx,
                            ours_end: ours_start,
                        });
                    } else {
                        // Conflict
                        regions.push(MergeRegion::Conflict {
                            ours_start: ours_idx,
                            ours_end: ours_start,
                            theirs_start: theirs_idx,
                            theirs_end: theirs_start,
                        });
                    }
                } else if ours_len > 0 {
                    // Only ours changed
                    regions.push(MergeRegion::OursOnly {
                        ours_start: ours_idx,
                        ours_end: ours_start,
                    });
                } else if theirs_len > 0 {
                    // Only theirs changed
                    regions.push(MergeRegion::TheirsOnly {
                        theirs_start: theirs_idx,
                        theirs_end: theirs_start,
                    });
                }
            }

            // Add the sync region (unchanged)
            if base_start < base_end {
                regions.push(MergeRegion::Unchanged {
                    base_start,
                    base_end,
                });
            }

            base_idx = base_end;
            ours_idx = ours_end;
            theirs_idx = theirs_end;
        }

        regions
    }

    fn find_sync_regions(base: &[&str], ours: &[&str], theirs: &[&str]) -> Vec<(usize, usize, usize, usize, usize, usize)> {
        let base_ours_matches = Self::get_matching_blocks(base, ours);
        let base_theirs_matches = Self::get_matching_blocks(base, theirs);

        let mut sync_regions = Vec::new();
        let mut i = 0;
        let mut j = 0;

        while i < base_ours_matches.len() && j < base_theirs_matches.len() {
            let ours_match = &base_ours_matches[i];
            let theirs_match = &base_theirs_matches[j];

            // Find intersection in base
            let base_start = ours_match.first_start.max(theirs_match.first_start);
            let base_end = (ours_match.first_start + ours_match.size)
                .min(theirs_match.first_start + theirs_match.size);

            if base_start < base_end {
                let len = base_end - base_start;
                let ours_start = ours_match.second_start + (base_start - ours_match.first_start);
                let theirs_start = theirs_match.second_start + (base_start - theirs_match.first_start);

                sync_regions.push((
                    base_start,
                    base_end,
                    ours_start,
                    ours_start + len,
                    theirs_start,
                    theirs_start + len,
                ));
            }

            // Advance the match that ends first
            if ours_match.first_start + ours_match.size <= theirs_match.first_start + theirs_match.size {
                i += 1;
            } else {
                j += 1;
            }
        }

        // Add final sync region
        sync_regions.push((base.len(), base.len(), ours.len(), ours.len(), theirs.len(), theirs.len()));

        sync_regions
    }

    fn get_matching_blocks(seq1: &[&str], seq2: &[&str]) -> Vec<Match> {
        SequenceMatcher::new(seq1, seq2).get_matching_blocks()
    }
}

#[derive(Debug, Clone)]
enum MergeRegion {
    Unchanged {
        base_start: usize,
        base_end: usize,
    },
    OursOnly {
        ours_start: usize,
        ours_end: usize,
    },
    TheirsOnly {
        theirs_start: usize,
        theirs_end: usize,
    },
    Conflict {
        ours_start: usize,
        ours_end: usize,
        theirs_start: usize,
        theirs_end: usize,
    },
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_no_conflict() {
        let base = "line1\nline2\nline3";
        let ours = "line1\nmodified2\nline3";
        let theirs = "line1\nline2\nmodified3";

        let result = SimpleMerge3::merge_strings(base, ours, theirs);
        println!("{:?}", result);
        assert!(!result.has_conflict);
        assert_eq!(result.merged_text, "line1\nmodified2\nmodified3");
    }

    #[test]
    fn test_with_conflict() {
        let base = "line1\nline2\nline3";
        let ours = "line1\nours_change\nline3";
        let theirs = "line1\ntheirs_change\nline3";

        let result = SimpleMerge3::merge_strings(base, ours, theirs);

        assert!(result.has_conflict);
        assert!(result.merged_text.contains("<<<<<<< HEAD"));
        assert!(result.merged_text.contains("======="));
        assert!(result.merged_text.contains(">>>>>>> MERGE"));
    }

    #[test]
    fn test_custom_markers() {
        let base = "line1\nline2\nline3";
        let ours = "line1\nours_change\nline3";
        let theirs = "line1\ntheirs_change\nline3";

        let result = SimpleMerge3::merge_strings_with_markers(
            base, ours, theirs,
            "<<< CONFLICT START",
            "--- SEPARATOR ---",
            ">>> CONFLICT END"
        );

        assert!(result.has_conflict);
        assert!(result.merged_text.contains("<<< CONFLICT START"));
        assert!(result.merged_text.contains("--- SEPARATOR ---"));
        assert!(result.merged_text.contains(">>> CONFLICT END"));
    }
}

fn main() {}