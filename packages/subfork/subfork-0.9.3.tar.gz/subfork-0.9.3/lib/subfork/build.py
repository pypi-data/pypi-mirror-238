#!/usr/bin/env python
#
# Copyright (c) 2022-2023 Subfork. All rights reserved.
#

__doc__ = """
Contains build classes and functions.
"""

import os
import shutil

from subfork import config
from subfork import minify
from subfork import util
from subfork.logger import log


class InvalidTemplate(Exception):
    """Exception class for template errors"""


def is_subpath(filepath, directory):
    """
    Returns True if both `filepath` and `directory` have a common prefix.
    """

    d = os.path.join(os.path.realpath(directory), "")
    f = os.path.realpath(filepath)

    return os.path.commonprefix([f, d]) == d


def normalize_path(path, start=os.getcwd()):
    """Returns a normalized relative path."""

    npath = os.path.normpath(path)
    if start is None or is_subpath(path, start):
        return os.path.relpath(npath, start=start).replace("\\", "/")

    return os.path.abspath(npath).replace("\\", "/")


def copy_file(src, dst, minimize=config.AUTO_MINIMIZE):
    """Copies a file, with optional minimization.

    :param src: source file path
    :param dst: destination file path
    :param minimize: minimize destination file (optional)
    """

    if not os.path.isfile(src):
        log.error("file not found: %s", src)
        return

    # get relative file path and extension
    _, ext = util.splitext(src)
    name = normalize_path(src)

    if not ext:
        log.error("could not determine file ext: %s" % name)
        return

    if minimize and ext in (".js", ".css", ".css3"):
        log.info("minimizing %s", name)
        minimized_src = minify.minify_file(src)
        if minimized_src:
            util.write_file(dst, minimized_src)
        elif os.path.isfile(src):
            copy_file(src, dst, minimize=False)
    else:
        if os.path.getsize(src) > 1e6:  # 1MB size limit
            log.error("file too large %s" % src)
            return
        else:
            log.info("copying %s", name)
            log.debug("copy %s -> %s", src, dst)
            dirname = os.path.dirname(dst)
            log.debug("dirname %s", dirname)
            if not os.path.exists(dirname):
                log.debug("makedirs %s", dirname)
                os.makedirs(dirname, exist_ok=True)
            shutil.copy(src, dst)

    if not dst or not os.path.exists(dst):
        log.error("copy failed")

    return dst


def create_build_template(source, build_root):
    """Creates a build template.yaml file that confirms to build tree.

    :param template_file: path to template.yaml file
    :param build_root: build output root directory
    :returns: path to template.yaml build file
    """

    if not os.path.isfile(source):
        raise Exception("template file not found: %s" % source)

    template_data = util.read_template(source)
    template_data["template_folder"] = "templates"
    template_data["static_folder"] = "static"

    build_file = os.path.join(build_root, "template.yaml")
    util.write_template(build_file, template_data)

    return build_file


def build(template_file, build_root=None):
    """Creates a build directory for a given template.yaml file.
    The build directory has the following structure:

        build
          |- templates
          |    `- <page>.html
          |- static
          |    `- <file>.ext
          `- template.yaml

    :param template_file: path to template.yaml file
    :param build_root: build output root directory
    :returns: path to template.yaml build file
    """

    if not os.path.exists(template_file):
        log.error("file not found: %s" % template_file)
        return

    # read the template file
    log.info("template: %s" % os.path.abspath(template_file))
    root_directory = os.path.dirname(template_file)
    template_data = util.read_template(template_file)

    # domain is a required template setting
    if "domain" not in template_data:
        raise InvalidTemplate("missing domain value")

    # get some template settings
    minimize = template_data.get("minimize", config.AUTO_MINIMIZE)
    template_folder = template_data.get("template_folder", "templates")
    static_folder = template_data.get("static_folder", "static")

    # create the build folders
    if not build_root:
        build_root = os.path.join(root_directory, "build")

    if os.path.exists(build_root):
        log.warning("deleting existing build: %s" % build_root)
        shutil.rmtree(build_root)

    build_template_folder = os.path.join(build_root, "templates")  # template_folder)
    build_static_folder = os.path.join(build_root, "static")  # static_folder)

    # make the temp folders
    try:
        os.makedirs(build_root, exist_ok=True)
        os.makedirs(build_template_folder, exist_ok=True)
        os.makedirs(build_static_folder, exist_ok=True)
    except Exception as err:
        log.exception("error making build dirs")
        raise Exception("could not make build directories")

    # copy the template file to template.yaml file (expected name)
    build_template_file = os.path.join(build_root, "template.yaml")
    create_build_template(template_file, build_root)

    # build template files
    template_folder_root = os.path.join(root_directory, template_folder)
    page_count = 0
    seen_files = []
    for _name, pageconfig in template_data.get("pages", {}).items():
        filename = pageconfig.get("file")
        if not filename:
            raise InvalidTemplate("missing file on %s" % _name)
        if len(filename) > 30:
            raise InvalidTemplate("filename too long %s" % filename)

        src = os.path.join(template_folder_root, filename)
        dst = os.path.join(build_template_folder, filename)

        if src not in seen_files:
            copy_file(src, dst, pageconfig.get("minimize", minimize))
            seen_files.append(src)

        page_count += 1
        if page_count > 50:
            raise InvalidTemplate("too many pages")

    # build static files
    static_folder_root = os.path.join(root_directory, static_folder)
    file_count = 0
    for src in util.walk(static_folder_root):
        dst = os.path.join(
            root_directory,
            build_static_folder,
            util.normalize_path(src, static_folder_root),
        )
        copy_file(src, dst, minimize)
        file_count += 1
        if file_count > 50:
            raise InvalidTemplate("too many files")

    return build_template_file
