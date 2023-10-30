import os
import sys
import subprocess
import shutil
import glob
import toml
from zipfile import PyZipFile, ZIP_DEFLATED

class BadModule(Exception):
    pass

class Zipper:

    def __init__(self):
        with open("info.toml") as info_toml:
            self.info = info = toml.load(info_toml)
        self.app_name = app_name = info['CFBundleDisplayName']
        self.bundle = bundle = app_name + '.app'
        self.prefix = prefix = os.path.join(bundle, 'Contents',
            'Frameworks', 'Python.framework', 'Versions', 'Current')
        self.app_python = python = os.path.join(prefix, 'bin', 'python3')
        result = subprocess.run([python, '--version'], capture_output=True)
        result.check_returncode()
        major, minor, _ = result.stdout.decode('utf-8').split()[1].split('.')
        self.lib_dir = os.path.join(prefix, 'lib', f'python{major}.{minor}')
        self.lib_zip = os.path.join(prefix, 'lib', f'python{major}{minor}.zip')
        self.stdlib = os.listdir(self.lib_dir)
        self.lib_dynload = os.path.join(self.lib_dir, 'lib-dynload')
        self.package_dir = os.path.join(self.lib_dir, 'site-packages')
        self.frameworks = os.path.join(self.bundle, 'Contents', 'Frameworks')
        
    def check_module(self, name):
        module_path = os.path.join(self.lib_dir, name)
        if not os.path.exists(module_path):
            raise BadModule('%s does not exist.' % module_path)
        init_path = os.path.join(module_path, '__init__.py')
        if os.path.isdir(module_path):
            if not os.path.exists(init_path):
                raise BadModule('%s is not a package.'%module_path)
        elif not name.endswith('.py'):
            raise BadModule('%s is not a python script.'%module_path)
        return module_path

    def remove_module(self, name):
        try:
            module_path = self.check_module(name)
        except BadModule:
            return
        if os.path.isdir(module_path):
            shutil.rmtree(module_path)
        elif os.path.exists(module_path):
            os.unlink(module_path)

    def zip_module(self, name):
        try:
            module_path = self.check_module(name)
        except BadModule:
            return
        with PyZipFile(self.lib_zip, 'a', ZIP_DEFLATED) as pyzip:
            pyzip.writepy(module_path)
        self.remove_module(name)

    def purge_extensions(self, module_name):
        extensions = os.path.join(self.lib_dynload, '_%s*'%module_name)
        for extension in glob.glob(extensions):
            os.unlink(extension)

    def purge_superfluous(self):
        with open('superfluous.txt') as text_file:
            names = [line.strip()
                        for line in text_file.readlines()
                        if line and line[0] != '#']
        for name in names:
            self.remove_module(name)
        # Some special cases
        if 'curses' in names:
            self.purge_extensions('curses')
        if 'test' in names:
            self.purge_extensions('test')
        if 'ssl' in names:
            self.purge_extensions('ssl')
            shutil.rmtree(os.path.join(self.bundle, 'Contents',
                'Frameworks', 'OpenSSL.framework'))
        # Clean the bin and include directories:
        bin_dir = os.path.join(self.prefix, 'bin')
        for bin_file in os.listdir(bin_dir):
            if not bin_file.startswith('python'):
                os.unlink(os.path.join(bin_dir, bin_file))
        shutil.rmtree(os.path.join(self.package_dir, 'bin'))
        for framework in os.listdir(self.frameworks):
            if framework == 'Python.framework':
                continue
            bin_dir = os.path.join(framework, 'Versions', 'Current',
                                       'bin')
            if os.path.exists(bin_dir):
                shutil.rmtree(bin_dir)
            include_dir = os.path.join(framework, 'Versions', 'Current',
                                       'include')
            if os.path.exists(include_dir):
                shutil.rmtree(include_dir)
        # Remove pip
        pip_dirs = glob.glob(os.path.join(self.package_dir, 'pip*'))
        for dir in pip_dirs:
            shutil.rmtree(dir)
        # Remove the Python shared library
        os.unlink(os.path.join(self.prefix, 'Python'))

    def zip_standard_lib(self):
        for name in self.stdlib:
            if name not in ('zipimport.py', 'site.py'):
                self.zip_module(name)
                self.remove_module(name)

    def clean_pycache(self):
        pycache = os.path.join(self.lib_dir, '__pycache__')
        names = set(os.path.splitext(m)[0] for m in os.listdir(self.lib_dir))
        for pyc_file in os.listdir(pycache):
            pyc_path = os.path.join(pycache, pyc_file)
            parts = pyc_file.split('.')
            if not parts[0] in names:
                os.unlink(pyc_path)
            elif parts[2] != 'pyc':
                os.unlink(pyc_path)

    def streamline(self):
        self.purge_superfluous()
        self.zip_standard_lib()
        self.clean_pycache()
