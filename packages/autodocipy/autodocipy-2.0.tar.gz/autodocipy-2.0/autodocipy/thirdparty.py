import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser(description='Custom wrapper for mkdocs serve')
    parser.add_argument('additional_args', nargs=argparse.REMAINDER, help='Additional arguments to pass to mkdocs serve')
    args = parser.parse_args()
    try:
        if not args.additional_args:
            args.additional_args = ["material"]
        command = ['mkdocs', 'serve', '--theme'] + args.additional_args
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running 'mkdocs serve': {e}")
    
if __name__ == "__main__":
    main()
