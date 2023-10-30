import os
import sys
import shutil
from jinja2 import Environment, PackageLoader
from . import __path__ as package_dirs

def init_dev_dir(app_name):
    """Create an app development directory.

    The development director is creaded as a subdirectory of the
    current working directory.  The name argument is the name of
    the app and the directory name is the lower cased app name
    with spaces replaced by underscores..
    """
    work_dir = app_name.lower().replace(' ', '_')
    template_dir = os.path.join(package_dirs[0], 'templates')
    os.mkdir(work_dir)
    env = Environment(
        loader=PackageLoader('bundle_app', 'templates'),
    )
    template = env.get_template('info.jinja2')
    with open(os.path.join(work_dir, 'info.toml'), 'w') as info_toml:
        info_toml.write(template.render(app_name=app_name))
    template = env.get_template('sdef.jinja2')
    with open(os.path.join(work_dir, '%s.sdef'%app_name), 'w') as sdef:
        sdef.write(template.render(app_name=app_name))
    src_icon_path = os.path.join(template_dir, 'AppIcon.icns')
    dst_icon_path = os.path.join(work_dir, '%s.icns'%app_name)
    shutil.copy(src_icon_path, dst_icon_path)
    main_ex_path = os.path.join(template_dir, 'main_ex')
    shutil.copytree(main_ex_path, os.path.join(work_dir, 'main_ex'))
    py_main_path = os.path.join(template_dir, 'main.py')
    shutil.copy(py_main_path, os.path.join(work_dir, 'main.py'))
    py_main_path = os.path.join(template_dir, 'superfluous.txt')
    shutil.copy(py_main_path, os.path.join(work_dir, 'superfluous.txt'))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Please provide the name for your new app as an argument.")
        sys.exit(1)
    init_dev_dir(sys.argv[1])
