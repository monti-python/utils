import argparse
import pathlib
import time

# Rename files in a directory so that they contain their creation time in the 
# filename, in the format YYYYMMDD_HHMMSS
def rename_chronologically_readable(directory: pathlib.Path, dry_run: bool):
    if not directory.is_dir():
        raise ValueError("Directory does not exist")
    for file in directory.iterdir():
        if file.is_file():
            creation_time = file.stat().st_mtime
            ts_fmt = time.strftime("%Y%m%d_%H%M%S", time.localtime(creation_time))
            # Add a number to the end of the filename if it already exists
            new_path = directory / (ts_fmt + file.suffix)
            i = 1
            while new_path.exists():
                new_path = directory / (ts_fmt + f'_{i}' + file.suffix)
                i += 1
            print(f'{file.name} -> {new_path.name}')
            if not dry_run:
                file.rename(new_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', '-p', type=pathlib.Path,
                        help='path to the directory containing the files')
    parser.add_argument('--dry-run', action='store_true', default=False, 
                        help='dry run mode')
    args = parser.parse_args()

    rename_chronologically_readable(args.path, args.dry_run)