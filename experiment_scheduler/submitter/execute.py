import argparse
import yaml

def parse_args():
    parser = argparse.ArgumentParser(description='Execute exeperiments.')
    parser.add_argument('-f', '--file')
    return parser.parse_args()


def main():
    args = parse_args()
    file_path = args.file

    with open(file_path) as f:
        yaml_def = yaml.load(f, Loader=yaml.FullLoader)

    return yaml_def




