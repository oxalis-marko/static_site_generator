from dir_copy import dir_cp
from gen_html import generate_pages_recursive

src = "/home/oxalis/projects/static_site/static"
dst = "/home/oxalis/projects/static_site/public"

from_path = "/home/oxalis/projects/static_site/content/index.md"
template_path = "/home/oxalis/projects/static_site/template.html"
dest_path = "/home/oxalis/projects/static_site/public/index.html"

dir_path_content = "/home/oxalis/projects/static_site/content"
dest_dir_path = "/home/oxalis/projects/static_site/public"

def main():
    #dir_cp(src, dst)
    generate_pages_recursive(dir_path_content, template_path, dest_dir_path)

main()