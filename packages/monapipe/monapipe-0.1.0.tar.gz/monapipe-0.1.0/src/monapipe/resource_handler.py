# SPDX-FileCopyrightText: 2022 Georg-August-Universität Göttingen
#
# SPDX-License-Identifier: CC0-1.0

import glob
import importlib
import os
import shutil
import subprocess
import sys
import urllib.request
from typing import Any

from monapipe.config import DATAVERSE


class ResourceHandler:
    """Wrapper class for resources."""

    def __init__(self, path: str):
        # The path to the resource directory.
        self.path = path

        # The name of the resource (must be the same as the name of the directory in `resources`).
        self.name = os.path.basename(os.path.normpath(self.path))

        # The module to load the resource from.
        self.module = importlib.import_module(
            ".".join(["monapipe", "resources", self.name, "load"])
        )

        # The resource object.
        self._ = None

    def clear(self):
        """Clear the resource object."""
        self._ = None

    def delete(self):
        """Delete the resource files."""
        dir_contents = os.listdir(self.path)
        for content in dir_contents:
            if content not in ["load.py", "__init__.py"]:
                content_path = os.path.join(self.path, content)
                if os.path.isdir(content_path):
                    shutil.rmtree(content_path)
                else:
                    os.remove(content_path)

    def download(self):
        """Download the resource files from `data.goettingen-resarch-online.de` using the DOI from `SETTINGS`."""
        doi_key = "doi_" + self.name
        if doi_key in DATAVERSE:
            doi = DATAVERSE[doi_key]

            # check if the resource files have been downloaded/unzipped
            downloaded_and_unzipped = False
            if os.path.exists(os.path.join(self.path, "MANIFEST.TXT")):
                downloaded_and_unzipped = True

            if not downloaded_and_unzipped:
                # delete the resource files if download isn't complete/unzipped
                self.delete()

                # download the resource files from `data.goettingen-research-online.de`
                print("Downloading files for %s ..." % self.name)
                url = (
                    "https://data.goettingen-research-online.de/api/access/dataset/:persistentId/?persistentId="
                    + doi
                )
                _download_from_url(url, self.path)

                # unzip the `dataverse_files.zip`
                if os.path.exists(os.path.join(self.path, "dataverse_files.zip")):
                    print("Unzipping files for %s ..." % self.name)
                    shutil.unpack_archive(os.path.join(self.path, "dataverse_files.zip"), self.path)

                    # if the files were double-zipped, also unzip the inner directory
                    if self.name + ".zip" in os.listdir(self.path):
                        shutil.unpack_archive(
                            os.path.join(self.path, self.name + ".zip"), self.path
                        )
                        os.remove(os.path.join(self.path, self.name + ".zip"))

            # if the files are in an inner directory of the same name as the resource directory,
            # move all files from the inner directory one level up and delete the inner directory
            if os.path.isdir(os.path.join(self.path, self.name)):
                shutil.copytree(os.path.join(self.path, self.name), self.path, dirs_exist_ok=True)
                shutil.rmtree(os.path.join(self.path, self.name))

            # sometimes, one or more files are missing in `dataverse_files.zip` because they were too large to be downloaded;
            # this is indicated in `MANIFEST.TXT`
            if os.path.exists(os.path.join(self.path, "MANIFEST.TXT")):
                with open(os.path.join(self.path, "MANIFEST.TXT")) as file:
                    missing_file_lines = sorted([line for line in file if "skipped" in line])
                    for missing_file_line in missing_file_lines:
                        missing_file = missing_file_line.split()[0]
                        if (
                            len(
                                glob.glob(
                                    os.path.join(self.path, "**", missing_file), recursive=True
                                )
                            )
                            == 0
                        ):
                            # if the file is really missing, print instructions to the user for manual download
                            error_msg = missing_file_line + "\n"
                            error_msg += "To download the missing file yourself, perform the following steps:\n"
                            error_msg += (
                                "1. Go to the resource page: https://data.goettingen-research-online.de/dataset.xhtml?persistentId="
                                + doi
                                + "\n"
                            )
                            error_msg += "2. Search the missing file (Files > Change View: Tree) and click on it, which directs you to the file page.\n"
                            error_msg += "3. From the file's metadata, copy the following fields: 'File Path' and 'File Persistent ID' (or, if the latter is missing: 'Download URL').\n"
                            error_msg += "4. Manually download the missing file in Python:\n\n"
                            error_msg += "\timport monapipe.resource_handler as resources\n\n"
                            error_msg += (
                                '\tresources.get_resource_handler("'
                                + self.name
                                + '").download_resource_file(file_path, file_persistent_id_or_download_url)\n'
                            )
                            raise Exception(error_msg)

    def download_resource_file(self, file_path: str, file_persistent_id_or_download_url: str):
        """Download a (missing) resource file.
            This function is meant to be used when resource files could not be downloaded automatically.

        Args:
            file_path: The destination path of the file, relative to `self.path`.
            file_persistent_id_or_download_url: DOI or URL for download.

        """
        while file_path.startswith(self.name + "/"):
            file_path = file_path[len(self.name) + 1 :]
        path = os.path.join(self.path, os.path.normpath(file_path))
        if os.path.exists(path):
            if file_persistent_id_or_download_url.startswith("doi:"):
                url = (
                    "https://data.goettingen-research-online.de/api/access/datafile/:persistentId/?persistentId="
                    + file_persistent_id_or_download_url
                )
            else:
                url = file_persistent_id_or_download_url
            _download_from_url(url, path)

    def provide(self):
        """Load the resource, if not already loaded, and save it in `self._`."""
        if self._ is None:
            self.download()
            self._ = self.module.load()


def access(name: str, clear_resource: bool = False) -> Any:
    """Returns a resource object.

    Args:
        name: Name of the resource.
        clear_resource: If True, the resource is cleared and loaded again.

    Returns:
        The resource loaded from `monapipe.resources.[name]`.

    """
    resource_handler = get_resource_handler(name)
    if clear_resource:
        resource_handler.clear()
    resource_handler.provide()
    return resource_handler._


def get_resource_handler(name: str) -> ResourceHandler:
    """Get the resource handler by resource name.

    Args:
        name: Name of the resource directory.

    Returns:
        The corresponding resource handler.

    """
    path = ".".join(["monapipe", "resources", name, "load"])
    module = importlib.import_module(path)
    return getattr(module, "RESOURCE_HANDLER")


def _download_from_url(url: str, path: str):
    """Download a file from a given URL.

    Args:
        url: The URL.
        path: The destination path.

    """
    api_key = DATAVERSE["api_token"]
    if api_key != "":
        curl_args = ["curl", "-L", "-O", "-J"]
        curl_args.extend(["-H", "X-Dataverse-key:" + api_key])
        subprocess.run(curl_args + [url], cwd=path, shell=False, check=False)
    else:
        try:
            urllib.request.urlretrieve(url=url, filename=os.path.join(path, "dataverse_files.zip"))
        except Exception as e:
            error_msg = f"Download failed for {url}\n{repr(e)}"
            sys.exit(error_msg)
