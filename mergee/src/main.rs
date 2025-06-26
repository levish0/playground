use merge3::{CustomMarkers, Merge3};

fn main() {
    let base = vec![
        "    println!(\"debug\");\n",
        "    let x = 1;\n",
        "    println!(\"debug\");\n",
        "    let y = 2;\n",
        "    println!(\"debug\");\n",
        "    let z = 3;\n",
        "    println!(\"debug\");\n",
    ];

    let this = vec![
        "    println!(\"debug\");\n",
        "    let x = 100;\n",        // 같은 라인을 다르게 수정
        "    println!(\"debug\");\n",
        "    let y = 200;\n",        // 같은 라인을 다르게 수정
        "    println!(\"debug\");\n",
        "    let z = 3;\n",
        "    println!(\"debug\");\n",
    ];

    let other = vec![
        "    println!(\"debug\");\n",
        "    let x = 999;\n",        // 또 다르게 수정 
        "    println!(\"debug\");\n",
        "    let y = 888;\n",        // 또 다르게 수정
        "    println!(\"debug\");\n",
        "    let z = 3;\n",
        "    println!(\"debug\");\n",
    ];


    let m3 = Merge3::with_patience_diff(&base, &this, &other);

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
