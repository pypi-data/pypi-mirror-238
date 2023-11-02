#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ===============================================================================
#
# Copyright (c) 2020 <> All Rights Reserved
#
#
# File: /c/Users/Administrator/chatopera/store/sdk/python/chatoperastore/chatoperastore.py
# Author: Hai Liang Wang
# Date: 2023-10-27:09:27:26
#
# ===============================================================================

"""
   
"""
__copyright__ = "Copyright (c) 2020 . All Rights Reserved"
__author__ = "Hai Liang Wang"
__date__ = "2023-10-27:09:27:26"

import os, sys

curdir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, curdir)

if sys.version_info[0] < 3:
    raise RuntimeError("Must be using Python 3")
else:
    unicode = str

import gzip
import shutil
import tarfile
from .wget import download
from .logger import Logger, LN
from .exceptions import LicensedfileDownloadException

# Get ENV
ENVIRON = os.environ.copy()
logger = Logger(LN(__file__))

LICENSE_STORE_PROVIDER = os.getenv("LICENSE_STORE_PROVIDER", "https://store.chatopera.com")
ERROR_CODES = dict({
    404: "License not found",
    406: "Licensed file metadata error",  # bad file extenstion of Licensedfile of productModel
    400: "Bad Request",  # File download interrupt
    402: "Need purchase valid license from  Chatopera License Store, https://store.chatopera.com",
    # need purchase valid license from license store
    424: "Licensedfile not exist of productModel",
    501: "Product not exist or peer product model does not contain licensed file",
    500: "Product model not found",
})


def download_licensedfile(license_id, save_to_filepath, serverinst_id=None, service_name=None):
    '''
    Download Licensed file
    license_id: License Id
    save_to_filepath: Dir, or File path. If it is a dir, filename would be set as ProductModel's licensedfile name, it
                    is passed in header. If it is a filepath, as a filename, would use in default.
    '''
    if not license_id:
        raise ValueError("licenseId is required for download licensed file")

    if not (isinstance(license_id, str) and license_id.strip()):
        raise ValueError("licenseId should be a string and not blank.")

    dl_url = "%s/dl/%s.gz" % (LICENSE_STORE_PROVIDER, license_id)

    if serverinst_id or service_name:
        dl_url += "?"

    if serverinst_id:
        dl_url += "serverId=%s" % serverinst_id

    if service_name:
        if not dl_url.endswith("?"):
            dl_url += "&"
        dl_url += "servicename=%s" % service_name

    try:
        logger.info("dl_url %s" % dl_url)
        return download(dl_url, save_to_filepath)
    except BaseException as e:
        if isinstance(e, LicensedfileDownloadException):
            if e.errcode in ERROR_CODES:
                logger.error("Error %s %s" % (e.errcode, ERROR_CODES[e.errcode]))
            else:
                print("[download_licensedfile] error")
                print(e)
        else:
            print(e)

        if save_to_filepath and os.path.exists(save_to_filepath) and save_to_filepath.endswith(".gz"):
            os.remove(save_to_filepath)

        raise e


def remove_ext_gz(file_path):
    '''
    get filename and remove ext .gz
    '''
    filename = os.path.basename(file_path)
    idx = filename.rfind(".gz")
    if idx >= 0:
        filename = filename[:idx]
    return filename


def extract_licensedfile(dl_file_path, extract_to_path, tarball=False):
    '''
    dl_file_path: downloaded file path
    extract_to_path: extract to root dir
    tarball: is extract as tar.gz file
    Filepath extracted, read doc, https://gitlab.chatopera.com/chatopera/chatopera.store/issues/105
    '''

    if (not dl_file_path) or (not isinstance(dl_file_path, str)):
        raise TypeError("dl_file_path must be none empty str")

    if (not extract_to_path) or (not isinstance(extract_to_path, str)):
        raise TypeError("extract_to_path must be none empty str")

    if not os.path.exists(dl_file_path):
        raise FileNotFoundError("File %s not found" % dl_file_path)

    if not os.path.exists(extract_to_path):
        raise FileNotFoundError("Dir %s not found" % extract_to_path)

    logger.info("extract %s to %s" % (dl_file_path, extract_to_path))

    if dl_file_path.endswith(".tar.gz") or (dl_file_path.endswith(".gz") and ".tar_" in dl_file_path):
        tarball = True

    if tarball:
        f = tarfile.open(dl_file_path)
        f.extractall(extract_to_path)
        f.close()
    else:
        fout_path = os.path.join(extract_to_path, remove_ext_gz(dl_file_path))
        logger.info("File extracted as %s" % fout_path)
        with gzip.open(dl_file_path, 'rb') as f_in:
            with open(fout_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    return True
