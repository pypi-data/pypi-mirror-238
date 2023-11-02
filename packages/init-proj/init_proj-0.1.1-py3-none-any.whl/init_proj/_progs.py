import contextlib
import datetime
import os
import subprocess
import sys
from argparse import ArgumentParser
from datetime import datetime
from importlib import resources

import tomli_w


class Prog:
    def get_name(self, key, /):
        func = self.__getattribute__("name_" + key)
        ans = func()
        if type(ans) in [tuple, list]:
            ans = os.path.join(*ans)
        return ans
    def calc(self, key, /):
        func = self.__getattribute__("calc_" + key)
        return func()
    def init_project(self):
        self.project_dir = os.path.abspath(os.path.join(self.r, self.n))
        if os.path.exists(self.project_dir):
            raise FileExistsError
        if not self.git:
            os.mkdir(self.project_dir)
            return
        args = [
            'git',
            'init',
            self.project_dir,
        ]
        subprocess.run(args=args, check=True)
    def git_commit(self, message, *, allow_empty=False):
        if not self.git:
            return
        with contextlib.chdir(self.project_dir):
            args="git stage .".split()
            subprocess.run(args=args, check=True)
            args=[
                'git',
                'commit',
                '--message',
                message,
            ]
            if allow_empty:
                args.append("--allow-empty")
            if self.git_author is not None:
                args.append('--author')
                args.append(self.git_author)
            subprocess.run(args=args, check=True)
    def __getattr__(self, key):
        if type(key) is not str:
            raise TypeError
        if key.startswith('__'):
            raise KeyError
        if not key.startswith('_'):
            return getattr(self, "_" + key)
        key = key[1:]
        if key.endswith("_textfile"):
            text = getattr(self, key[:-9] + "_text")
            if text is None:
                ans = None
            else:
                ans = self.get_name(key)
                with open(ans, "w") as s:
                    s.write(text)
        elif key.endswith("_dir"):
            ans = self.get_name(key)
            os.mkdir(ans)
        else:
            ans = self.calc(key)
        setattr(self, '_' + key, ans)
        return ans
    def __init__(self, args):
        ns = self.parser.parse_args(args=args)
        kwargs = vars(ns)
        for k, v in kwargs.items():
            setattr(self, k, v)
    def run(self):
        self.init_project()
        with contextlib.chdir(self.project_dir):
            self.git_commit("Initial Commit", allow_empty=True)
            self.pyproject_textfile
            self.setup_textfile
            self.gitignore_textfile
            self.manifest_textfile
            self.init_textfile
            self.main_textfile
            self.git_commit("Version 0.0.0")
    def name_src_dir(self):
        return "src"
    def name_pkg_dir(self):
        return self.src_dir, self.n
    def name_init_textfile(self):
        return self.pkg_dir, '__init__.py'
    def name_main_textfile(self):
        return self.pkg_dir, '__main__.py'
    def name_pyproject_textfile(self):
        return "pyproject.toml"
    def name_license_textfile(self):
        return "LICENSE.txt"
    def name_readme_textfile(self):
        return "README.rst"
    def name_manifest_textfile(self):
        return "MANIFEST.in"
    def name_setup_textfile(self):
        return "setup.cfg"
    def name_gitignore_textfile(self):
        return ".gitignore"
    def calc_init_text(self):
        ans = resources.read_text("init_proj.drafts", "init.txt")
        return ans
    def calc_main_text(self):
        ans = resources.read_text("init_proj.drafts", "main.txt")
        ans = ans.format(n=self.n)
        return ans
    def calc_manifest_text(self):
        return ""
    def calc_license_text(self):
        if self.a is None:
            return None
        ans = resources.read_text("init_proj.drafts", "license.txt")
        ans = ans.format(y=self.y, a=self.a)
        return ans
    def calc_gitignore_text(self):
        if not self.git:
            return None
        ans = resources.read_text("init_proj.drafts", "gitignore.txt")
        return ans
    def calc_git_author(self):
        if self.author is None:
            return None
        ans = self.author
        if self.e is not None:
            ans = f"{ans} <{self.e}>"
        return ans
    def calc_author(self):
        if self.a is None:
            return self.e
        else:
            return self.a
    def calc_parser(self):
        ans = ArgumentParser(fromfile_prefix_chars="@")
        ans.add_argument('--name', '-n', dest='n', default='a', type=self.nameType)
        ans.add_argument('--description', '-d', dest='d')
        ans.add_argument('--author', '-a', dest='a', type=self.stripType)
        ans.add_argument('--email', '-e', dest='e', type=self.stripType)
        ans.add_argument('--root', '-r', dest='r', default='.')
        ans.add_argument('--year', '-y', dest='y', default=datetime.now().year)
        ans.add_argument('--requires-python', '-v', dest='v', default=self.default_requires_python())
        ans.add_argument('--no-git', dest='git', default=True, action='store_false')
        return ans
    def calc_readme_text(self):
        blocknames = "heading overview installation license credits".split()
        blocks = [getattr(self, x + "_rst_block") for x in blocknames]
        blocks = [x for x in blocks if x is not None]
        blocks = ['\n'.join(x) for x in blocks if type(x) is not str]
        ans = "\n\n".join(blocks)
        return ans
    def calc_heading_rst_block(self):
        lining = "=" * len(self.n)
        ans = [lining, self.n, lining]
        return ans
    def calc_overview_rst_block(self):
        if self.d is None:
            return None
        heading = "Overview"
        lining = "-" * len(heading)
        ans = [heading, lining, "", self.d]
        return ans
    def calc_installation_rst_block(self):
        heading = "Installation"
        lining = "-" * len(heading)
        sentence = f"To install {self.n}, you can use `pip`. Open your terminal and run:"
        codestart = ".. code-block:: bash"
        codeline = f"    pip install {self.n}"
        ans = [heading, lining, "", sentence, "", codestart, "", codeline]
        return ans
    def calc_license_rst_block(self):
        if self.license_textfile is None:
            return None
        heading = "License"
        lining = "-" * len(heading)
        sentence = "This project is licensed under the MIT License."
        ans = [heading, lining, "", sentence]
        return ans
    def calc_credits_rst_block(self):
        if self.author is None:
            return None
        heading = "Credits"
        lines = list()
        lines.append(heading)
        lines.append("-" * len(heading))
        if self.a is not None:
            lines.append("- Author: " + self.a)
        if self.e is not None:
            lines.append("- Email: " + self.e)
        lines.append("")
        lines.append(f"Thank you for using {self.n}!")
        return lines
    def calc_setup_text(self):
        return ""
    def calc_pyproject_text(self):
        return tomli_w.dumps(self.pyproject_data)
    def calc_pyproject_data(self):
        ans = dict()
        ans['build-system'] = self.build_system_data
        ans['project'] = self.project_data
        return ans
    def calc_build_system_data(self):
        return {
            "requires" : ["setuptools>=61.0.0"],
            "build-backend" : "setuptools.build_meta",
        }
    def calc_description(self):
        if self.d is None:
            return self.n
        else:
            return self.d
    def calc_project_data(self):
        ans = dict()
        ans['name'] = self.n
        ans['version'] = "0.0.0"
        ans['description'] = self.description
        if self.license_textfile is not None:
            ans['license'] = {'file' : self.license_textfile}
        ans['readme'] = self.readme_textfile
        if self.authors is not None:
            ans['authors'] = self.authors
        ans['classifiers'] = self.classifiers
        ans['keywords'] = []
        ans['dependencies'] = []
        ans['requires-python'] = self.v
        return ans
    def calc_classifiers(self):
        ans = list()
        if self.license_textfile is not None:
            ans.append("License :: OSI Approved :: MIT License")
        ans.append("Programming Language :: Python")
        ans.append("Programming Language :: Python :: 3")
        return ans
    def calc_authors(self):
        if self.author is None:
            return None
        if self.e is None:
            return [dict(name=self.author)]
        else:
            return [dict(name=self.author, email=self.e)]
    @staticmethod
    def default_requires_python():
        assert sys.version_info[0] == 3
        return f">=3.{sys.version_info[1]}"
    @staticmethod
    def nameType(value, /):
        value = Prog.stripType(value)
        normpath = os.path.normpath(value)
        assert value == normpath
        x, y = os.path.split(value)
        assert x == ""
        return value
    @staticmethod
    def stripType(value, /):
        value = str(value)
        value = value.strip()
        return value

