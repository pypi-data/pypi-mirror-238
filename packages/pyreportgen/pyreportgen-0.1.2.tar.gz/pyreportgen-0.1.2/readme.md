# Pyreportgen
This is a pyton library for creating reports and other content in the form of a pdf using python.


## Requirements.
- `wkhtmltopdf`

## Example 
```py
import pyreportgen as rg 
import pyreportgen.layout as layout

report = rg.Report([
    rg.Header("Hello World"),
    rg.Text("This is a sample of how to use pyreportgen"),
    Layout.HBox([
        rg.Text("This is a paragraph in a box."),
        rg.Text("These will be placed next to each other"),
        rg.Text("All the boxes will have equal space regardless of content.")
    ])
])

report.pdf("out.pdf")
```