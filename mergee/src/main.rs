use merge3::{CustomMarkers, Merge3};

fn main() {
    let base = vec![
        "a\n"
    ];

    let this = vec![
        "#include <stdio.h>\n",
        "\n",
        "// Frobs foo heartily\n",
        "int frobnitz(int foo)\n",
        "{\n",
        "    int i;\n",
        "    for(i = 0; i < 10; i++)\n",
        "    {\n",
        "        printf(\"Your answer is: \");\n",
        "        printf(\"%d\\n\", foo);\n",
        "    }\n",
        "}\n",
        "\n",
        "int fact(int n)\n",
        "{\n",
        "    if(n > 1)\n",
        "    {\n",
        "        return fact(n-1) * n;\n",
        "    }\n",
        "    return 1;\n",
        "}\n",
        "\n",
        "int main(int argc, char **argv)\n",
        "{\n",
        "    frobnitz(fact(10));\n",
        "}\n",
    ];

    let other = vec![
        "#include <stdio.h>\n",
        "\n",
        "int fib(int n)\n",
        "{\n",
        "    if(n > 2)\n",
        "    {\n",
        "        return fib(n-1) + fib(n-2);\n",
        "    }\n",
        "    return 1;\n",
        "}\n",
        "\n",
        "// Frobs foo heartily\n",
        "int frobnitz(int foo)\n",
        "{\n",
        "    int i;\n",
        "    for(i = 0; i < 10; i++)\n",
        "    {\n",
        "        printf(\"%d\\n\", foo);\n",
        "    }\n",
        "}\n",
        "\n",
        "int main(int argc, char **argv)\n",
        "{\n",
        "    frobnitz(fib(10));\n",
        "}\n",
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
