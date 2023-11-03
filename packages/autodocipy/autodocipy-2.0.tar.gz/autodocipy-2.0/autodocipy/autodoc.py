import os
import re
import os
import shutil
import openai
import argparse
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

load_dotenv()

TEMPLATE = "{text}\n\n\n Write a README.md using above information for github"

class AutoDocPy:
    def __init__(self, source_dir, output_dir):
        """
        initalize source_dir, output_dir
        """
        self.source_dir = source_dir
        self.output_dir = output_dir

    def should_ignore(self, path):
        """
        igores files like .git, __pycache__
        """
        ignore_list = [".git", "__pycache__"]
        for item in ignore_list:
            if item in path:
                return True
        return False

    def parse_comments(self, file_path):
        """
        parses string literals from a python file
        """
        comments = {}
        with open(file_path, 'r') as file:
            lines = file.readlines()

        current_item = None
        docstring = None
        in_docstring = False

        for line in lines:
            if re.match(r'\s*def\s+\w+\(.*\):', line) or re.match(r'\s*class\s+\w+\(.*\):', line):
                current_item = line.strip()
                docstring = ""
                in_docstring = False

            if current_item:
                if not in_docstring:
                    if line.strip().startswith('"""') or line.strip().startswith("'''"):
                        docstring = line.strip('"\'').strip()
                        in_docstring = True
                elif in_docstring:
                    docstring += line.strip() + '\n'
                    if line.strip().endswith('"""') or line.strip().endswith("'''"):
                        in_docstring = False
                        comments[current_item] = docstring.strip('"\'').strip()
        return comments

    def generate_documentation(self):
        """
        Base function which calls should_ignore, parse_comments, create_and_build_mkdocs_project function
        to generate and configure generate documentation offline
        which can be served using mkdocs on 8000 port
        """
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        for root, _, files in os.walk(self.source_dir):
            if self.should_ignore(root): 
                continue
            folder_name = root.split("/")[-1]
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    comments = self.parse_comments(file_path)
                    if comments != {}:
                        self.generate_file_documentation(file, comments, folder_name)
        self.create_and_build_mkdocs_project("autodoc")


    def generate_file_documentation(self, file_name, comments, folder_name):
        """
        Creates offline md documentation for each file in python folder
        """
        module_dir = os.path.join(self.output_dir, folder_name)
        if not os.path.exists(module_dir):
            os.makedirs(module_dir)

        output_path = os.path.join(module_dir, f"{os.path.splitext(file_name)[0]}.md")

        with open(output_path, 'w') as output_file:
            output_file.write(f"# Documentation for file {file_name} in Folder {folder_name}\n\n")
            
            for item, comment in comments.items():
                output_file.write(f"## {item}\n")
                output_file.write(f"{comment[:-3]}\n\n")
        if not os.path.exists("autodoc/alldoc"):
            os.makedirs("autodoc/alldoc")
        module_dir = os.path.join("autodoc/alldoc")
        output_path = os.path.join(module_dir, "all.md")
        with open(output_path, 'a') as output_file:
            output_file.write(f"# Documentation for file {file_name} in Folder {folder_name}\n\n")
            for item, comment in comments.items():
                output_file.write(f"## {item}\n")
                output_file.write(f"{comment[:-3]}\n\n")

    def create_and_build_mkdocs_project(self, mkdocs_project_dir):
        """
        Configures mkdocs
        """
        os.system(f"mkdocs new {mkdocs_project_dir}")
        shutil.rmtree(os.path.join(mkdocs_project_dir, 'docs')) 
        shutil.move(self.output_dir, os.path.join(mkdocs_project_dir, 'docs'))
        os.chdir(mkdocs_project_dir)

    def generate_readme(self):
        """
        Generates AUTODOCREADME.md using openai
        """
        text = ""
        with open("autodoc/alldoc/all.md", 'r') as file:
            text = file.read()
        if text is None:
            return
        openai.api_key = os.getenv("OPENAI_KEY")
        prompt = PromptTemplate(template=TEMPLATE, input_variables=["text"])
        llm = OpenAI(openai_api_key="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")
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        res = llm_chain.run(text)
        with open("AUTODOCREADME.md", 'w') as output_file:
            output_file.write(res)

def generate_documentation():
    """
    initialize source_dir, output_dir and calls method generate_documentation in class AutoDocpy 
    """
    source_dir = "."
    output_dir = "docs"
    autodoc = AutoDocPy(source_dir, output_dir)
    autodoc.generate_documentation()

def generate_readme():
    """
    initialize source_dir, output_dir and calls method generate_readme in class AutoDocpy 
    """
    source_dir = "."
    output_dir = "docs"
    autodoc = AutoDocPy(source_dir, output_dir)
    autodoc.generate_readme()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["doc", "readme"], help="Command to execute")
    # parser.add_argument("--key", help="OpenAI API Key")
    args = parser.parse_args()
    print(args)
    if args.command == "doc":
        generate_documentation()
    elif args.command == "readme":
        generate_readme()
       