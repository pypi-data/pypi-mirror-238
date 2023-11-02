STYLE_NORMAL = """
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;700&display=swap');

* {
    font-family: 'Poppins', sans-serif;
    margin: 0;
}

.CenterText {
    text-align: center;
}

.Main {
    padding: 0.75rem;
}


p, h1, h2, h3, h4, h5, h6 {
    margin: 0.5rem;
}

.HBox {
    display: -webkit-box;
    display: flex;
    -webkit-box-pack: center;
}

.HBox > * {
    -webkit-box-flex: 1;
    -webkit-flex: 1;
    flex: 1;
    
}

.HCenterContent {
    display: flex;
    justify-content: center;
}

.Image {
    width: 300px;
}

.HBarPlot {
    width: 100%;
}

.Map {
    width: 100%;
}

table {
    border-collapse: collapse;
    width: 100%;
}
  
td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
}
  
tr:nth-child(even) {
   background-color: #dddddd;
}

.tfoot {
    font-weight: bold;
}

@media print {
    .NoBreak {
        page-break-inside: avoid;
        break-inside: avoid;
    }
    .PageBreak {
        page-break-after: always;
    }
}

@media not print {
    .Main {
      width: 210mm;
      background-color: white;
    }
    body {
        display: flex;
        justify-content: center;
        background-color: gray;
    }
}
"""