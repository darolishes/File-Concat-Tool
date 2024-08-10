# File Concat Tool

## Overview
**File Concat Tool** is a versatile and extensible command-line tool designed to concatenate multiple files into one or more output files. It supports a wide range of file formats including JavaScript, HTML, CSS, Markdown, PDF, and more. The tool is ideal for developers, technical writers, and anyone needing to merge files across various formats.

## Features
- **Multiple File Format Support**: Concatenate files in various formats including `.js`, `.jsx`, `.css`, `.html`, `.md`, `.pdf`, and more.
- **Flexible Output**: Specify the number of output files to split the concatenated content.
- **Ignore Patterns**: Easily exclude specific files or directories using ignore patterns.
- **Extensible**: Easily extend the tool to support additional file types and formats.
- **Simple CLI Interface**: Intuitive and easy-to-use command-line interface.

## Installation
You can clone the repository and use the tool directly from the command line.

```sh
git clone https://github.com/yourusername/file-concat-tool.git
cd file-concat-tool
python concat_files.py -h

## Usage

The tool provides a simple CLI interface. Below is the basic usage:

sh

Code kopieren

`python concat_files.py -r path/to/your/files -o path/to/output -n 4 -i node_modules,.DS_Store` 

### Command-Line Arguments

- `-r`, `--root_directory`: Path to the directory containing files to concatenate (required).
- `-o`, `--output_directory`: Path to the output directory where concatenated files will be saved (required).
- `-n`, `--number_of_files`: Number of output files to create (required).
- `-i`, `--ignore`: Comma-separated list of folders or files to ignore (optional).

### Example

sh

Code kopieren

`python concat_files.py -r ./src -o ./output -n 3 -i node_modules,.DS_Store` 

This command concatenates all `.js`, `.jsx`, `.css`, `.html` files in the `./src` directory into 3 output files in the `./output` directory, ignoring files in `node_modules` and `.DS_Store`.

## Extending the Tool

The tool is designed to be easily extendable. To add support for additional file types:

1. Modify the `get_file_paths` function to include additional file extensions.
2. Add any required handling for specific file types within the `write_concatenated_file` function.
3. (Optional) Add new command-line arguments if your extension requires additional input.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your improvements or new features.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Roadmap

- [ ]  Add support for Markdown (`.md`) files.
- [ ]  Implement PDF concatenation support.
- [ ]  Add unit tests for different file types.
- [ ]  Improve error handling and logging.
- [ ]  Create a Homebrew formula for macOS users.

## Contact

For any inquiries, please contact Your Name.

markdown

Code kopieren

 ``### Hinweise zur Erweiterung:
- **Dateitypen hinzufügen**: Um die Unterstützung für weitere Dateitypen (wie `.md`, `.pdf`) hinzuzufügen, können Sie die bestehenden Funktionen `get_file_paths` und `write_concatenated_file` erweitern.
- **Dateiformate behandeln**: PDF-Dateien und andere binäre Formate benötigen möglicherweise spezielle Bibliotheken (z.B. `PyPDF2` für PDF) und zusätzliche Logik, um korrekt verarbeitet zu werden.
- **Weitere Kommandozeilenoptionen**: Erwägen Sie, zusätzliche Optionen hinzuzufügen, z.B. eine Option zur Festlegung spezifischer Formatierungsanforderungen für Markdown-Dateien.

### Repository-Struktur:`` 

file-concat-tool/ ├── README.md ├── LICENSE ├── concat\_files.py ├── requirements.txt # Optional: Für Abhängigkeiten, falls Erweiterungen hinzugefügt werden └── tests/ # Optional: Für Unit-Tests, wenn Sie diese implementieren
