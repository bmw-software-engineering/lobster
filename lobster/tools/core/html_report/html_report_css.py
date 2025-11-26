CSS = """

/* Item styles */
#custom-data-banner {
    position: absolute;
    top: 1rem;
    right: 2rem;
    font-size: 0.9rem;
    color: white;
}

.item-ok,
.item-partial,
.item-missing,
.item-justified {
    border: 1px solid #000;
    border-radius: 0.5rem;
    margin-top: 0.4rem;
    padding: 0.25rem;
}

.item-ok:target,
.item-partial:target,
.item-missing:target,
.item-justified:target {
    border-width: 3px;
    border-color: #000;
}

.subtle-ok,
.subtle-partial,
.subtle-missing,
.subtle-justified {
    padding-left: 0.2rem;
}

.item-partial {
    background-color: #ffffee;
}

.item-justified {
    background-color: #eeeeee;
}

.subtle-ok {
    border-left: 0.2rem solid #88ff88;
}

.subtle-partial {
    border-left: 0.2rem solid #ffff88;
}

.subtle-missing {
    border-left: 0.2rem solid #ff8888;
}

.subtle-justified {
    border-left: 0.2rem solid #888888;
}

.item-name {
    font-size: 125%;
    font-weight: bold;
}

.attribute {
    margin-top: 0.5rem;
}

/* Tables */
thead tr {
    font-weight: bold;
}

tbody tr.alt {
    background-color: #eeeeee;
}

/* Text */
blockquote {
    font-style: italic;
    border-left: 0.2rem solid gray;
    padding-left: 0.4rem;
    margin-left: 0.5rem;
}

/* Footer */
footer {
    margin-top: 1rem;
    padding: 0.2rem;
    text-align: right;
    color: #666666;
    font-size: 0.7rem;
}

/* Columns layout */
.columns {
    display: flex;
}

.columns .column {
    flex: 45%;
}

/* Table styling */
thead tr {
    font-weight: bold;
}

tbody tr.alt {
    background-color: #eeeeee;
}

/* Text formatting */
blockquote {
    font-style: italic;
    border-left: 0.2rem solid gray;
    padding-left: 0.4rem;
    margin-left: 0.5rem;
}

/* Footer styling */
footer {
    margin-top: 1rem;
    padding: 0.2rem;
    text-align: right;
    color: #666666;
    font-size: 0.7rem;
}

.button {
    background-color: #818589;
    border: none;
    border-radius: 5px;
    color: white;
    padding: 12px 25px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 14px;
    margin: 4px 2px;
    cursor: pointer
}

.button active:before {
    position: absolute;
    left: 0;
    top: 0;
    display: inline-block;
    width: 0;
    height: 0;
    border-style: solid;
    border-width: 15px 15px 0 0;
    border-color: #333 transparent transparent transparent
}

.buttonActive.button {
    text-decoration: none;
    border: 5px solid #000000
}

.buttonOK {
    background-color: #04AA6D;
    color: white;
    border: 2px solid #04AA6D;
    border-radius: 5px
}

.buttonOK:hover {
    background-color: #026641;
    color: white;
    border: 2px solid #026641
}

.buttonActive.buttonOK {
    text-decoration: none;
    border: 5px solid #026641
}

.buttonPartial {
    background-color: #17a2b8;
    color: white;
    border: 2px solid #17a2b8;
    border-radius: 5px
}

.buttonPartial:hover {
    background-color: #0e616e;
    color: white;
    border: 2px solid #0e616e
}

.buttonActive.buttonPartial {
    text-decoration: none;
    border: 5px solid #0e616e
}

.buttonMissing {
    background-color: #f44336;
    color: white;
    border: 2px solid #f44336;
    border-radius: 5px
}

.buttonMissing:hover {
    background-color: #a91409;
    color: white;
    border: 2px solid #a91409
}

.buttonActive.buttonMissing {
    text-decoration: none;
    border: 5px solid #a91409
}

.buttonJustified {
    background-color: #6c757d;
    color: white;
    border: 2px solid #6c757d;
    border-radius: 5px
}

.buttonJustified:hover {
    background-color: #41464b;
    color: white;
    border: 2px solid #41464b
}

.buttonActive.buttonJustified {
    text-decoration: none;
    border: 5px solid #41464b
}

.buttonWarning {
    background-color: #ffbf00;
    color: white;
    border: 2px solid #ffbf00;
    border-radius: 5px
}

.buttonWarning:hover {
    background-color: #997300;
    color: white;
    border: 2px solid #997300
}

.buttonActive.buttonWarning {
    text-decoration: none;
    border: 5px solid #997300
}

.buttonBlue {
    background-color: #0000ff;
    color: white;
    border: 2px solid #0000ff;
    border-radius: 5px
}

.buttonBlue:hover {
    background-color: #000099;
    color: white;
    border: 2px solid #000099
}

.buttonActive.buttonBlue {
    text-decoration: none;
    border: 5px solid #000099
}

.js-plotly-plot {
    z-index: 1;
    position: relative;
}
"""
