"""Scan paths and create routes"""
import glob
import importlib
import os
import pkgutil


class Scan:
    def __init__(self, root_dir: str = None):
        if not root_dir:
            raise TypeError("root_dir don't can be None")
        self.routes = {}
        self.root_dir = root_dir
        self.apps_pkg = 'apps'
        self.base_dir = os.path.join(self.root_dir, self.apps_pkg)

    def scan(self):
        """Import the modules and set the pathname to that module"""
        modules = pkgutil.iter_modules([self.base_dir])
        mod, mod_name = None, None
        for f, name, ispkg in modules:
            if ispkg:
                pkg_modules = pkgutil.iter_modules([f'{f.path}/{name}'])
                # verify if app module is in package
                if not any([True for pkgm in list(pkg_modules) if pkgm.name == 'app']):
                    print(
                        f"WARNING: Package <{name}> has no attribute app module")
                    continue
                mod = importlib.import_module(f'{self.apps_pkg}.{name}.app')
                mod_name = f'{name}.app'
            else:
                mod = importlib.import_module(f'{self.apps_pkg}.{name}')
                mod_name = name

            if not hasattr(mod, 'layout'):
                print(
                    f"WARNING: Module <{mod_name}> has no attribute 'layout' and route not")
                continue

            pathname = f'/{name}'
            if name == 'index':
                pathname = '/'

            self.routes[pathname] = mod.layout

