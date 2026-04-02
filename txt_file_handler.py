# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 10:47:17 2026

@author: bramc44
"""
import os
import re
import numpy as np

def spectrasummer(spectralist, data_dict):
    if not spectralist:
        raise ValueError("spectralist is empty.")

    first_key = str(spectralist[0])
    if first_key not in data_dict:
        raise KeyError(f"{first_key} not found in data_dict.")

    spectrax = data_dict[first_key][:, 0]
    summed = np.zeros_like(spectrax)

    for spec_id in spectralist:
        key = str(spec_id)

        if key not in data_dict:
            raise KeyError(f"{key} not found in data_dict.")

        spectra = data_dict[key]

        # Optional safety check: matching energy axes
        if not np.array_equal(spectra[:,0], spectrax):
            raise ValueError(f"Energy axis mismatch for {key}")

        summed += spectra[:, 1]

    return np.column_stack((spectrax, summed))


def normaliser(spectra):
    y = spectra[:, 1]
    ymin = np.min(y)
    ymax = np.max(y)

    if ymax == ymin:
        raise ValueError("Cannot normalise: spectrum is flat.")

    return (y - ymin) / (ymax - ymin)

def load_spectra_from_folder(folder_path, progress_callback=None):
    data_dict = {}

    pattern = re.compile(
        r"(?:(?P<prefix>NEXAFS|XPS)[-_])?(?P<id>[0-9]+)[-_ ]?(?P<desc>.*)\.txt$"
    )

    txt_files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    total_files = len(txt_files)

    for idx, filename in enumerate(txt_files):

        full_path = os.path.join(folder_path, filename)

        key_filename = filename
        if key_filename.startswith("i09-"):
            key_filename = key_filename[4:]
        if key_filename.startswith("b07-1-"):
            key_filename = key_filename[6:]
        match = pattern.search(key_filename)
        if not match:
            continue

        prefix = match.group("prefix")
        file_id = int(match.group("id"))
        desc = match.group("desc").strip().replace(" ", "_")

        if prefix == "NEXAFS":
            key = f"{prefix}_{file_id}"
        elif prefix == "XPS":
            key = f"{file_id}_{desc}" if desc else f"{file_id}"
        else:
            key = f"{file_id}_{desc}" if desc else f"{file_id}"

        try:
            data = np.loadtxt(full_path)
            data_dict[key] = data

            if progress_callback:
                progress_callback(f"Loading {filename}")

        except Exception as e:
            print(f"Failed to load {filename}: {e}")

    return data_dict