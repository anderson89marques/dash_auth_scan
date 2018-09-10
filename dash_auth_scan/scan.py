"""Scan paths and create routes"""
import glob
import importlib
import logging
import os
import pkgutil

LOG = logging.getLogger(__name__)
LOG.setLevel(logging.DEBUG)
CH = logging.StreamHandler()
LOG.addHandler(CH)


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
        LOG.debug('SCANNING ROUTES...')
        modules = pkgutil.iter_modules([self.base_dir])
        self.scan_pkg(modules, '/', self.apps_pkg)
        LOG.debug(f'routes: {list(self.routes.keys())}')

    def scan_pkg(self, modules, pathname, apps_pkg):
        mod, mod_name = None, None
        for f, name, ispkg in modules:
            if ispkg:
                # adding pkg name to the route
                mod = importlib.import_module(f'{apps_pkg}.{name}')
                mod_name = name
                path_url = f'{pathname}{name}'

                if not hasattr(mod, 'layout'):
                    LOG.debug(
                        f"WARNING: Module <{mod}> has no attribute 'layout' and route was not added")
                else:
                    self.routes[path_url] = mod.layout
                # calling again self.scan_pkg to load modules and subpackages of this package
                pkg_modules = pkgutil.iter_modules([f'{f.path}/{name}'])
                self.scan_pkg(
                    pkg_modules, f'{path_url}/', f'{apps_pkg}.{name}')
            else:
                mod = importlib.import_module(f'{apps_pkg}.{name}')
                mod_name = name

                if not hasattr(mod, 'layout'):
                    LOG.debug(
                        f"WARNING: Module <{mod}> has no attribute 'layout' and route was not added")
                    continue

                path_url = f'{pathname}{name}'
                if name == 'index':
                    path_url = '/'
                self.routes[path_url] = mod.layout
        return True
