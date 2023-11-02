import os
import openai
import argparse
from rich.markdown import Markdown
from .constants import ext2language, console, scan_exts
from . import constants
from .utils import construct_prompt
from .dir_summary import dir_summary
from .file_summary import file_summary
from .prompts import FINAL_PROMPT, SYSTEM_PROMPT


def parse_args():
    parser = argparse.ArgumentParser(
        description='pept3: Test-time training for deep MS/MS spectrum prediction improves peptide identification'
    )
    parser.add_argument(
        "--path",
        type=str,
        default="./",
        help='The local path for your code repo/file',
    )
    parser.add_argument(
        "--exts",
        type=str,
        default="py,cpp",
        help='Select your code extension name, split by comma, e.g. py,cpp',
    )
    parser.add_argument(
        "--language",
        type=str,
        default="chinese",
        help='Select your readme language',
    )
    parser.add_argument(
        "--out",
        type=str,
        default="./readme.md",
        help='Select where your readme file should be saved',
    )
    return parser.parse_args()


def prompt_summary(**kwargs):
    final_prompt = FINAL_PROMPT.format(**kwargs)
    final_system = SYSTEM_PROMPT.format(
        **kwargs, human_language=constants.envs['human_language']
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=construct_prompt(final_system, final_prompt),
    )
    return response['choices'][0]['message']['content']


def main():
    args = parse_args()
    local_path = os.path.relpath(args.path)
    constants.envs['human_language'] = args.language
    for ext in args.exts.split(","):
        ext = ext.strip()
        if not ext:
            continue
        if ext in ext2language:
            scan_exts.append(ext)
        else:
            console.log(
                f"Extension [{ext}] is not supported yet, please use one of [{','.join(ext2language.keys())}]"
            )
    if os.path.isfile(local_path):
        summaries = file_summary(local_path)
    else:
        summaries = dir_summary(local_path)
    readme = prompt_summary(
        language=summaries['language'],
        module_summaries=summaries['content'],
        path=local_path,
    )
    console.rule("ReadMe")
    console.print(Markdown(readme))
    with open(args.out, 'w') as f:
        f.write(
            """
<div align="center">
    <a href="https://github.com/gusye1234/gpt-readme">
      <img src="https://img.shields.io/badge/written_in-GPT-green">
    </a>
    <a href="https://github.com/gusye1234/gpt-readme">
      <img src="https://img.shields.io/badge/could_be-Wrong-red">
    </a>
    <a href="https://pypi.org/project/gpt_readme/">
      <img src="https://img.shields.io/pypi/v/gpt_readme.svg">
    </a>
</div>


"""
        )
        f.write(readme)
    console.rule("Done")
