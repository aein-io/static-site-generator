import os
import shutil
from generate_content import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def copy_static_files(src_dir, dest_dir):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    os.mkdir(dest_dir)

    src_items = os.listdir(src_dir)

    for item in src_items:
        src_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)

        if os.path.isfile(src_path):
            print(f"Copying item: {item}")
            shutil.copy(src_path, dest_path)
            print(f"Content copied: {dest_path}")
        else:
            copy_static_files(src_path, dest_path)


def main():
    copy_static_files(dir_path_static, dir_path_public)
    generate_pages_recursive(
        dir_path_content, template_path, dir_path_public)


if __name__ == "__main__":
    main()
