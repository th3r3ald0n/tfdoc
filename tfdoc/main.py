import argparse
import hcl2
from pathlib import Path


def parse_arguments():
    parser = argparse.ArgumentParser(description="Terraform Documentation Generator CLI")
    parser.add_argument('-l', '--list', nargs='*', help='Attributes to extract seperated by space e.g., -l description name', default=[])
    parser.add_argument('--include-dependson', action='store_true', help='Include the "Depends on" column')
    return parser.parse_args()


def generate_markdown_table(headers, rows, file_path):
    """Generates a Markdown table and writes it to a file."""
    with open(file_path, "w") as file:
        file.write(f"| {' | '.join(headers)} |\n")
        file.write(f"|{'-|'.join(['-' * len(h) for h in headers])}-|\n")
        for row in rows:
            file.write(f"| {' | '.join(map(str, row))} |\n")


def get_attr(d, keys):
    """Fetches attribute values from a dictionary, returning None for missing keys."""
    return [d.get(key, None) for key in keys]


def extract_strings(obj):
    """Recursively extracts string representations from nested structures."""
    if isinstance(obj, dict):
        return [str(value) for v in obj.values() for value in extract_strings(v)]
    if isinstance(obj, list):
        return [str(item) for v in obj for item in extract_strings(v)]
    return [str(obj)]


def process_tf_files(root_dir, attribute_list, include_dependson):
    """Parses Terraform (.tf) files, extracts variable and resource information."""
    ids, var_result, result = [], [], []

    for file in root_dir.rglob("*.tf"):
        with file.open(encoding="utf-8") as f:
            d = hcl2.load(f)

        if "variable" in d:
            for v in d["variable"]:
                var_name = list(v.keys())[0]
                config = v[var_name]
                var_result.append([var_name] + get_attr(config, ["type", "description"]))

        if "resource" in d:
            for r in d["resource"]:
                resource_type = list(r.keys())[0]
                config = r[resource_type]
                name = list(config.keys())[0]
                ids.append(f"{resource_type}.{name}")

    for file in root_dir.rglob("*.tf"):
        with file.open(encoding="utf-8") as f:
            d = hcl2.load(f)

        if "resource" in d:
            for r in d["resource"]:
                resource_type = list(r.keys())[0]
                config = r[resource_type]
                name = list(config.keys())[0]
                result_string = " ".join(extract_strings(config[name]))
                dependencies = [i for i in ids if i in result_string] if include_dependson else []
                result.append([resource_type, name] + get_attr(config[name], attribute_list) + ( [dependencies] if include_dependson else []))

    return var_result, result


def main():
    args = parse_arguments()
    root_dir = Path.cwd()

    var_result, result = process_tf_files(root_dir, args.list, args.include_dependson)
    result.sort(key=lambda x: x[0])

    generate_markdown_table(["Variable", "Type", "Description"], var_result, "tfdocs_vars.md")
    headers = ["Resource", "Resource name"] + (args.list if args.list else []) + (["Depends on"] if args.include_dependson else [])
    generate_markdown_table(headers, result, "tdocs.md")

    print("Markdown tables generated: tfdocs.md, tfdocs_vars.md")


if __name__ == "__main__":
    main()
