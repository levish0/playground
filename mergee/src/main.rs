use merge3::{CustomMarkers, Merge3};

fn main() {
    let base = vec![
        "line A\n",
        "line B\n",
        "line C\n",
        "line D\n",
        "line E\n",
    ];

    let this = vec![
        "line A\n",  // conflict #1
        "line B\n",                   // same
        "line C modified by THIS\n",  // conflict #2
        "line D\n",                   // same
        "line E modified by THIS\n",  // conflict #3
    ];

    let other = vec![
        "line A\n", // conflict #1
        "line B\n",                   // same
        "line C modified by OTHER\n", // conflict #2
        "line D\n",                   // same
        "line E modified by OTHER\n", // conflict #3
    ];


    let m3 = Merge3::new(&base, &this, &other);

    // 직접 마커 지정 (없애거나 원하는 문자열로 변경 가능)
    let custom_markers = CustomMarkers {
        start_marker: Option::from("<<<<<<<< HEAD\n"),
        mid_marker: Option::from("========\n"),
        end_marker: Option::from(">>>>>>>> NEW\n"),
        ..Default::default()
    };

    for line in m3.merge_lines(true, &custom_markers) {
        print!("{}", line);
    }
}
