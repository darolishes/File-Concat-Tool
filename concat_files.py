import argparse
from pathlib import Path
import math
from typing import List, Tuple, Set
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm
import re
from pygments import highlight
from pygments.lexers import get_lexer_for_filename, TextLexer
from pygments.formatters import TerminalFormatter
from pygments.util import ClassNotFound

def should_ignore(path: Path, ignore_patterns: Set[str]) -> bool:
    """
    Check if a given path should be ignored based on the ignore patterns.

    :param path: The path to check
    :param ignore_patterns: Set of patterns to ignore
    :return: True if the path should be ignored, False otherwise
    """
    return any(pattern in path.parts for pattern in ignore_patterns)

def get_file_paths(root_dir: Path, ignore_patterns: Set[str], file_extensions: Set[str]) -> List[Path]:
    """
    Get all file paths in the root directory that match the given extensions and are not ignored.

    :param root_dir: The root directory to search
    :param ignore_patterns: Set of patterns to ignore
    :param file_extensions: Set of file extensions to include
    :return: List of file paths
    """
    return [
        file for file in root_dir.rglob('*')
        if file.is_file() and file.suffix in file_extensions and not should_ignore(file, ignore_patterns)
    ]

def write_concatenated_file(output_file: Path, file_paths: List[Path], start_index: int, end_index: int, output_format: str) -> None:
    """
    Write the contents of multiple files into a single output file.

    :param output_file: The path to the output file
    :param file_paths: List of file paths to concatenate
    :param start_index: Starting index in the file_paths list
    :param end_index: Ending index in the file_paths list
    :param output_format: The desired output format ('txt' or 'md')
    """
    with output_file.open('w', encoding='utf-8') as outfile:
        for file_path in file_paths[start_index:end_index]:
            try:
                content = file_path.read_text(encoding='utf-8')
                if output_format == 'md':
                    outfile.write(f'## File: {file_path}\n\n')
                    try:
                        lexer = get_lexer_for_filename(file_path)
                    except ClassNotFound:
                        lexer = TextLexer()

                    # Use TerminalFormatter for ANSI color codes
                    formatter = TerminalFormatter()
                    highlighted = highlight(content, lexer, formatter)

                    # Remove ANSI color codes for plain text
                    clean_content = re.sub(r'\x1b\[[0-9;]*m', '', highlighted)

                    # Write the clean, highlighted content as a Markdown code block
                    outfile.write(f"```{lexer.aliases[0] if lexer.aliases else ''}\n{clean_content.strip()}\n```\n\n")
                else:
                    outfile.write(f'// File: {file_path}\n{content}\n\n')
            except Exception as e:
                print(f"Could not process file {file_path}: {e}")

def concatenate_files(file_paths: List[Path], output_file: Path, start_index: int, end_index: int, output_format: str) -> None:
    """
    Concatenate a subset of files into a single output file.

    :param file_paths: List of file paths to concatenate
    :param output_file: The path to the output file
    :param start_index: Starting index in the file_paths list
    :param end_index: Ending index in the file_paths list
    :param output_format: The desired output format ('txt' or 'md')
    """
    write_concatenated_file(output_file, file_paths, start_index, end_index, output_format)

def process_files(root_dir: Path, output_dir: Path, num_files: int, ignore_patterns: Set[str], file_extensions: Set[str], output_format: str) -> None:
    """
    Process all files in the root directory and concatenate them into the specified number of output files.

    :param root_dir: The root directory to search for files
    :param output_dir: The directory to save the output files
    :param num_files: The number of output files to create
    :param ignore_patterns: Set of patterns to ignore
    :param file_extensions: Set of file extensions to include
    :param output_format: The desired output format ('txt' or 'md')
    """
    file_paths = get_file_paths(root_dir, ignore_patterns, file_extensions)
    files_per_output = math.ceil(len(file_paths) / num_files)

    with ProcessPoolExecutor() as executor:
        futures = []
        for i in range(num_files):
            output_file = output_dir / f'concatenated_part_{i+1}.{output_format}'
            start_index = i * files_per_output
            end_index = min((i + 1) * files_per_output, len(file_paths))
            futures.append(executor.submit(concatenate_files, file_paths, output_file, start_index, end_index, output_format))

        for future in tqdm(as_completed(futures), total=num_files, desc="Concatenating files"):
            future.result()

def parse_arguments() -> Tuple[Path, Path, int, Set[str], Set[str], str]:
    """
    Parse command-line arguments.

    :return: Tuple containing root_directory, output_directory, number_of_files, ignore_patterns, file_extensions, and output_format
    """
    parser = argparse.ArgumentParser(description="Concatenate files into a specified number of output files.")
    parser.add_argument('-r', '--root_directory', type=Path, required=True, help='Path to the root directory')
    parser.add_argument('-o', '--output_directory', type=Path, required=True, help='Path to the output directory')
    parser.add_argument('-n', '--number_of_files', type=int, required=True, help='Number of output files')
    parser.add_argument('-i', '--ignore', type=str, help='Comma-separated list of patterns to ignore', default='')
    parser.add_argument('-e', '--extensions', type=str, help='Comma-separated list of file extensions to include', default='.js,.jsx,.css,.html,.json,.md,.mdx,.txt,.py,.sh,.yaml,.yml,.tsx,.ts')
    parser.add_argument('-f', '--format', type=str, choices=['txt', 'md'], default='txt', help='Output format: txt or md')

    args = parser.parse_args()
    ignore_patterns = set(args.ignore.split(',')) if args.ignore else set()
    file_extensions = set(args.extensions.split(','))
    return args.root_directory, args.output_directory, args.number_of_files, ignore_patterns, file_extensions, args.format

if __name__ == "__main__":
    # Parse command-line arguments
    root_dir, output_dir, num_files, ignore_patterns, file_extensions, output_format = parse_arguments()

    try:
        # Create output directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        # Process and concatenate files
        process_files(root_dir, output_dir, num_files, ignore_patterns, file_extensions, output_format)
        print(f"All files have been successfully concatenated into {num_files} {output_format} files.")
    except Exception as e:
        print(f"An error occurred: {e}")