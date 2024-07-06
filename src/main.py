from dir_copy import dir_cp
from gen_html import generate_page

src = "/home/oxalis/projects/static_site/static"
dst = "/home/oxalis/projects/static_site/public"

from_path = "/home/oxalis/projects/static_site/content/index.md"
template_path = "/home/oxalis/projects/static_site/template.html"
dest_path = "/home/oxalis/projects/static_site/public/index.html"

def main():
    #dir_cp(src, dst)
    generate_page(from_path, template_path, dest_path) 

main()