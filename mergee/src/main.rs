use merge3::{CustomMarkers, Merge3};

fn main() {
    let base = vec![
        "what!!!\n"
    ];

    let this = vec![
        "string\n"
    ];

    let other = vec![
        "striawefwefng\n"
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
