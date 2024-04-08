#!/usr/bin/python3
"""
Generate gitignore file
"""
import argparse


def main(args=None):
    parser = argparse.ArgumentParser(
            prog="Generate gitignore file",
            description="""
            Generates gitignore file for specified project type
            """)
    parser.add_argument('project', type=str)
    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args.split())


    if args.project in projects:
        gitignore_text = projects[args.project]
        try:
            with open(".gitignore", "x", encoding="utf-8") as f:
                f.write(gitignore_text)
                f.close()
            print(f".gitignore file was generated for the {args.project} project")
        except OSError as e:
            print(e)
    else:
        print("[!] No such template\n\nAvailable templates:")
        for pr in projects:
            print(f"\t{pr}")


if __name__ == "__main__":
    main()
