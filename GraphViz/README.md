# GraphViz and the 'tree' command

The first script ('_convert_tree_to_graphviz.py_' will convert the output of the 'tree' command to GraphViz format.

The second script ('_convert_graphviz_to_pdf.py_') will take the dot file from the first script and create a GraphViz diagram in PDF format.

## Dependencies

Use the [pip] package manager to install the 'graphviz' module.

```bash
pip install graphviz
```

## Usage

```bash
tree [/path/to/make/tree] > tree_output.txt
```
```bash
python convert_tree_to_graphviz.py
```
```bash
python convert_graphviz_to_pdf.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
