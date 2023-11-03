import os
import re
import utils
import json
from config import default_config


class Router:
    def __init__(self, app):
        self.app = app
        try:
            self.config = default_config
            with open("router.config.json", "r") as custom_config:
                for key, val in json.load(custom_config).items():
                    self.config[key] = val
        except:
            pass

    def __generate_routes(self, root, files):
        if len(files) == 0:
            return
        files_ = list(
            filter(
                lambda file: not (
                    str(file).startswith("__")
                    or str(file).endswith("__")
                    or str(file).split(".")[-1] in self.config.get("ext_exclude_list")
                    or str(file).split(".")[-1]
                    not in self.config.get("ext_include_list")
                )
                or str(file) == self.config.get("default_index"),
                files,
            )
        )

        if files_.__len__() == 0:
            return

        root_path = root[6:] + "/"
        routes = [
            {
                "module": __import__(
                    re.sub(r"\\|/", ".", root[2:]) + "." + file.split(".")[0],
                    fromlist=[""],
                ),
                "path": utils.normalizepath(
                    root_path
                    + (
                        ""
                        if file == self.config.get("default_index")
                        else file.split(".")[0]
                    )
                ),
                "handler": file,
            }
            for file in files_
        ]

        return filter(lambda route: "main" in dir(route.get("module")), routes)

    def __routes_stacks(self):
        routes_stacks = []
        for root, dirs, files in os.walk(self.config.get("root_dir")):
            routes_ = self.__generate_routes(root, files=files)
            if not routes_:
                continue
            routes_stacks.append(routes_)
        return routes_stacks

    def __parse_routes(self, stacks):
        routes = []
        for stack in stacks:
            for route in stack:
                module = route.get("module")
                routes.append(
                    {
                        "rule": route.get("path"),
                        "methods": module.methods
                        if "methods" in dir(module)
                        else ["GET"],
                        "view_func": module.main,
                        "endpoint": route.get("handler", ""),
                    }
                )

        return routes

    def run(self):
        for route in utils.pipe([self.__routes_stacks(), self.__parse_routes]):
            self.app.add_url_rule(**route)
