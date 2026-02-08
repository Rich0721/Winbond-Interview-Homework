import os
import argparse

from datetime import datetime
from Directory.Directory import Directory
from File.File import File
from File.WordFile import WordFile
from File.ImageFile import ImageFile
from File.TextFile import TextFile

from constants import IMAGE_EXTENSIONS, TAB_LENGTH, TEXT_EXTENSIONS, WORD_EXTENSIONS


def build_tree(root_path:str, extension:str = None) -> Directory:
    root_dir = Directory(name=os.path.basename(root_path) or root_path, parent=None)
    mapping = {".": root_dir, "": root_dir}

    for dirpath, dirnames, filenames in os.walk(root_path):
        rel = os.path.relpath(dirpath, root_path)
        if rel == ".":
            current = root_dir
            mapping["."] = root_dir
        else:
            if rel not in mapping:
                name = os.path.basename(rel)
                parent_rel = os.path.dirname(rel)
                parent = mapping.get(parent_rel, root_dir)
                current = Directory(name=name, parent=parent)
                parent.add_directory(current)
                mapping[rel] = current
            else:
                current = mapping[rel]

        for f in filenames:
            full_path = os.path.join(dirpath, f)
            name, ext = os.path.splitext(f)
            size = os.path.getsize(full_path)
            created = datetime.fromtimestamp(os.path.getctime(full_path)).isoformat()
            file_dict = {"full_path": full_path, "name": name, "extension": ext, "size": size, "createdTime": created}
            
            if ext in WORD_EXTENSIONS:
                file_obj = WordFile(**file_dict)
            elif ext in IMAGE_EXTENSIONS:
                file_obj = ImageFile(**file_dict)
            elif ext in TEXT_EXTENSIONS:
                file_obj = TextFile(**file_dict)
            if (extension is None) or (ext == extension):
                current.add_file(file_obj)

    return root_dir


def print_tree(directory: Directory, indent="", is_last=True, dir_display=True):
    connector = "└── " if is_last else "├── "
    if len(indent) == TAB_LENGTH:
        print(f"{indent}{connector}{directory.name}[目錄]")
    elif len(indent) > TAB_LENGTH:
        print(f"{indent}{connector}{directory.name}[子目錄]")
    else:
        print(f"根目錄({directory.name})")
    
    next_indent = indent + ("    " if is_last else "│   ")

    items = directory.children + directory.files
    for i, item in enumerate(items):
        is_last_item = (i == len(items) - 1)
        item_connector = "└── " if is_last_item else "├── "
        human_readable_size = to_human_readable_size(item.size) if isinstance(item, File) else None
        
        if isinstance(item, Directory) and (dir_display or len(item.files) > 0 or any(len(child.files) > 0 for child in item.children)):
            print_tree(item, next_indent, is_last_item, dir_display=dir_display)
        elif isinstance(item, File):
            print(f"{next_indent}{item_connector}{item.to_string(human_readable_size)}")


def calucate_directory_size(directory: Directory) -> float:
    total_size = sum(file.size for file in directory.files if file.size is not None)
    for child in directory.children:
        total_size += calucate_directory_size(child)
    return total_size


def print_directory_size(directory: Directory, name: str = None):
    d = find_directory_by_name(directory, name) if name else directory

    if d is None:
        print(f"找不到目錄: {name}")
        return

    size = calucate_directory_size(d)
    human_readable_size = to_human_readable_size(size)
    print(f"{d.name} 目錄大小: {human_readable_size}")


def find_directory_by_name(directory: Directory, name: str) -> Directory:
    if directory.name == name:
        return directory
    
    for child in directory.children:
        result = find_directory_by_name(child, name)
        if result is not None:
            return result
    return None

def to_tree_as_xml(directory: Directory, indent="") -> str:
    xml = f'{indent}<{directory.name}>\n'
    
    for file in directory.files:
        human_readable_size = to_human_readable_size(file.size)
        xml += f'{indent}  {file.to_xml(human_readable_size)}\n'

    for child in directory.children:
        xml += to_tree_as_xml(child, indent + "  ")
    
    xml += f'{indent}</{directory.name}>\n'
    return xml


def to_human_readable_size(size_bytes: float) -> str:
    if size_bytes is None:
        return None
    
    for unit in ["B", "KB", "MB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    
    return f"{size_bytes:.2f} GB"


def main():
    parser = argparse.ArgumentParser(description="File processing tool")

    parser.add_argument("--root_dir", type=str, required=True,
                        help="Root directory to scan")

    parser.add_argument("--extension", type=str, default=None,
                        help="File extension filter, e.g. .docx")

    parser.add_argument("--target_dir", type=str, default=None,
                        help="Output directory")

    parser.add_argument("--calucate_size", action="store_true",
                        help="Calculate file sizes")

    parser.add_argument("--xml_tree", action="store_true",
                        help="Generate XML tree output")

    args = parser.parse_args()

    root_dir = build_tree(args.root_dir, args.extension)
    if args.calucate_size:
        print_directory_size(root_dir, args.target_dir)
    elif args.xml_tree:
        print(to_tree_as_xml(root_dir))
    else:
        print_tree(root_dir, dir_display=(args.extension is None)) 



if __name__ == "__main__":
    main()
    
