import argparse
import hcl2
from pathlib import Path
from .utils.terraformblocks import Variable, Resource, Data, Module
from .utils.tablegenerator import generate_confluence_table, generate_markdown_table

def get_tf_files(root_dir):
    """Retrieve only .tf files from the current directory."""
    return [file for file in root_dir.glob("*.tf") if file.is_file()]


blocks = {"variable": Variable, "resource": Resource, "data":Data, "module": Module}

def main():
    root_dir = Path.cwd()

    parser = argparse.ArgumentParser(description="Terraform Configuration Parser")
    parser.add_argument('-l', '--list', nargs='*', help='Set flag for attributes', required=False, default=[])
    parser.add_argument('--format', choices=['markdown', 'confluence'], default='confluence', help='Output format')
    parser.add_argument('--include-depends', action='store_true', help='Include dependency analysis')
    parser.add_argument('--include-depends-vars', action='store_true', help='Include dependency analysis with variables')

    args = parser.parse_args()

    result = {}
    table = []

    for file in get_tf_files(root_dir):
        with file.open("r", encoding="utf-8") as f:
            d = hcl2.load(f)
            for block_type, cls in blocks.items():
                result[block_type] = result.get(block_type, []) + [cls(block) for block in d.get(block_type, [])]
        
    ids = [j.id for i in result.values() for j in i]

    table = [
        [j.Resource_type, j.Resource, j.Resource_name] + j.get_attr(args.list) +
        ([", ".join(j.depends_on(ids))] if args.include_depends else []) +
        ([", ".join(j.depends_on_incl_vars(ids))] if args.include_depends_vars else [])
        for i in result.values() for j in i]

    def headers(array):
        """Generate dynamic headers for the table output."""
        return ["Resource Type", "Resource", "Resource Name"] + array + (["Depends On"] if args.include_depends or args.include_depends_vars else [])

    # Sort results by resource type
    table = sorted(table, key=lambda x: x[0])

    # Generate output in the selected format
    if args.format == 'markdown':   
        generate_markdown_table(headers(args.list), table, "tfdoc.md")
    elif args.format == 'confluence':
        generate_confluence_table(headers(args.list), table, "tfdoc.confluence.txt")

if __name__ == "__main__":
    main()
