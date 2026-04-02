# -*- coding: utf-8 -*-
"""
Created on Sat Feb 21 10:39:36 2026

@author: bramc44
"""

import os
import fnmatch
import numpy as np
import h5py
import re
def select_energy_intensity(data_group):
    
    # ---------------- ENERGY ----------------
    energy = None

    for key in ['excitation_energy', 'energies']:
        if key in data_group:
            try:
                e_data = data_group[key][()]
                e_data = np.array(e_data).reshape(-1)

                if e_data.size > 1:
                    energy = e_data
                    break
            except Exception:
                pass

    # ---------------- INTENSITY ----------------
    intensity = None

    for key in ['total_intensity', 'image_data']:
        if key in data_group:
            try:
                i_data = data_group[key][()]
                i_data = np.array(i_data)

                # Flatten multidimensional data
                if i_data.ndim > 1:
                    i_data = i_data.reshape(-1)

                if i_data.size > 1:
                    intensity = i_data
                    break
            except Exception:
                pass

    # ---------------- FINAL VALIDATION ----------------
    if energy is None or intensity is None:
        return None, None

    if len(energy) != len(intensity):
        return None, None

    return energy, intensity

def get_data_nexus_i09(filepath):

    try:
        with h5py.File(filepath, 'r') as f:

            # ---------------- ENTRY HANDLING ----------------
            entry_group = None

            if "entry" in f:
                entry_group = "entry"
            elif "entry1" in f:
                entry_group = "entry1"

            if entry_group is None:
                return None, None, None, 1

            entry = f[entry_group]

            # Iterate only through GROUPS (ignore scalar datasets)
            for name, obj in entry.items():

                if not isinstance(obj, h5py.Group):
                    continue  # skip scalar datasets like end_time

                data_group = obj

                # ---------------- ENERGY ----------------
                energy = None

                for e_name in ['excitation_energy', 'energies']:
                    if e_name in data_group:
                        e_data = np.array(data_group[e_name][()])
                        if e_data.size > 1:
                            energy = e_data.reshape(-1)
                            break

                # ---------------- INTENSITY ----------------
                intensity = None
                use_total_intensity = False

                for i_name in ['total_intensity', 'image_data']:
                    if i_name in data_group:
                        i_data = np.array(data_group[i_name][()])
                        if i_data.size > 1:
                            intensity = i_data
                            if i_name == 'total_intensity':
                                use_total_intensity = True
                            break

                if intensity is not None:
                    intensity = intensity.reshape(-1)

                # ---------------- NORMALISE BY sm5amp8 ----------------
                if use_total_intensity and 'sm5amp8' in data_group:
                    sm5 = np.array(data_group['sm5amp8'][()]).reshape(-1)

                    if len(sm5) == len(intensity):
                        intensity = intensity / sm5
                    else:
                        print(f"Warning: sm5amp8 mismatch in {filepath}")

                # ---------------- FINAL CHECK ----------------
                if energy is not None and intensity is not None:
                    if len(energy) == len(intensity):

                        filename = os.path.basename(filepath)

                        
                        # --- Recursively search entire file for energy_mode ---
                        energy_mode_str = ""

                        def find_energy_mode(group):
                            for key, item in group.items():

                                # If this is the dataset we want
                                if key == "energy_mode":
                                    value = item[()]

                                    # Convert numpy arrays to scalar
                                    if isinstance(value, np.ndarray):
                                        if value.size > 0:
                                            value = value.flatten()[0]

                                    # Decode bytes
                                    if isinstance(value, bytes):
                                        value = value.decode("utf-8")

                                    return str(value).strip().replace(" ", "_")

                                # Recurse into subgroups
                                if isinstance(item, h5py.Group):
                                    result = find_energy_mode(item)
                                    if result:
                                        return result

                            return None


                        try:
                            result = find_energy_mode(f)   # search entire file
                            if result:
                                energy_mode_str = result
                        except Exception as e:
                            print(f"Energy mode search failed in {filepath}: {e}")

                        print("Energy mode found:", energy_mode_str)
                        # --- Build data_name ---
                        filename = os.path.basename(filepath)
                        
                        if energy_mode_str:
                            data_name = f"{filename[:-4]} {name}_{energy_mode_str}"
                        else:
                            data_name = f"{filename[:-4]} {name}"

                        return energy, intensity, data_name, 0

        return None, None, None, 1

    except Exception as e:
        print(f"Failed to read {filepath}: {e}")
        return None, None, None, 1
def convert_nexus_folder_i09(input_dir, output_dir, progress_callback=None):
    """
    Converts all .nxs files in input_dir to .txt files in output_dir.
    Returns a summary dictionary for GUI feedback.
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    spectra_dir = os.path.join(output_dir, "spectra as .txt files")
    os.makedirs(spectra_dir, exist_ok=True)
    file_list = fnmatch.filter(os.listdir(input_dir), "*.nxs")
    total_files = len(file_list)
    converted = 0
    failed = 0

    for filename in file_list:
        filepath = os.path.join(input_dir, filename)

        energy, intensity, data_name, state = get_data_nexus_i09(filepath)
        
        # ---- Skip if data_name contains XPS or RESPES ----
        if data_name is not None:
            upper_name = data_name.upper()
            skip_terms = ["XSW", "RESPES", "RPES"] 
            if any(term in upper_name for term in skip_terms):
                print(f"Skipping dataset: {data_name}")
                continue
            
        if state == 0 and energy is not None and len(energy) > 1:
            data = np.column_stack((energy, intensity))

            save_path = os.path.join(spectra_dir, data_name + ".txt")
            np.savetxt(save_path, data, delimiter='\t')

            converted += 1
        else:
            failed += 1
        if progress_callback:
            progress_callback(f"Processed {filename}")
    return {
        "total_files": len(file_list),
        "converted": converted,
        "failed": failed
    }

def get_data_nexus_b07_1(filepath):
    try:
        with h5py.File(filepath, 'r') as f:

            # ---------------- HELPER: recursive search ----------------
            def find_dataset(group, target_name):
                for key, item in group.items():

                    if key == target_name:
                        value = item[()]

                        # Flatten arrays
                        if isinstance(value, np.ndarray):
                            value = value.squeeze()

                        # Decode bytes
                        if isinstance(value, bytes):
                            value = value.decode("utf-8")

                        return value

                    # Recurse into subgroups
                    if isinstance(item, h5py.Group):
                        result = find_dataset(item, target_name)
                        if result is not None:
                            return result

                return None

            # ---------------- GET DATA ----------------
            energy = find_dataset(f, "binding_energy")
            intensity = find_dataset(f, "spectrum")
            energy_mode = find_dataset(f, "energy_mode")
            region_raw = find_dataset(f, "region_list")

            # -------- CLEAN REGION --------
            region = ""

            if isinstance(region_raw, np.ndarray):
                if region_raw.ndim == 0:
                    region = region_raw.item()
                elif region_raw.size > 0:
                    region = region_raw.flatten()[0]
            else:
                region = region_raw

            if isinstance(region, bytes):
                region = region.decode("utf-8")

            region = str(region).strip().replace(" ", "_")

            if not region:
                region = "unknown_region"
            # ---------------- VALIDATION ----------------
            if energy is None or intensity is None:
                return None, None, None, 1

            energy = np.array(energy).reshape(-1)
            intensity = np.array(intensity).reshape(-1)

            if len(energy) != len(intensity):
                return None, None, None, 1

            # ---------------- CLEAN ENERGY MODE ----------------
            if isinstance(energy_mode, bytes):
                energy_mode = energy_mode.decode("utf-8")

            if energy_mode is None:
                energy_mode_str = ""
            else:
                energy_mode_str = str(energy_mode).strip().replace(" ", "_")

            # ---------------- BUILD NAME ----------------
            filename = os.path.basename(filepath)

            if energy_mode_str:
                data_name = f"{filename[:-4]}_{region}_{energy_mode_str}"
            else:
                data_name = f"{filename[:-4]}_{region}"

            return energy, intensity, data_name, 0

    except Exception as e:
        print(f"Failed to read {filepath}: {e}")
        return None, None, None, 1
def convert_nexus_folder_b07_1(input_dir, output_dir, progress_callback=None):
    """
    Converts all .nxs files in input_dir to .txt files in output_dir.
    Returns a summary dictionary for GUI feedback.
    """

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    spectra_dir = os.path.join(output_dir, "spectra as .txt files")
    os.makedirs(spectra_dir, exist_ok=True)
    file_list = fnmatch.filter(os.listdir(input_dir), "*.nxs")
    total_files = len(file_list)
    converted = 0
    failed = 0

    for filename in file_list:
        filepath = os.path.join(input_dir, filename)

        energy, intensity, data_name, state = get_data_nexus_b07_1(filepath)
        
        # ---- Skip if data_name contains XPS or RESPES ----
        if data_name is not None:
            upper_name = data_name.upper()
            skip_terms = ["XSW", "RESPES", "RPES"] 
            if any(term in upper_name for term in skip_terms):
                print(f"Skipping dataset: {data_name}")
                continue
            
        if state == 0 and energy is not None and len(energy) > 1:
            data = np.column_stack((energy, intensity))

            save_path = os.path.join(spectra_dir, data_name + ".txt")
            np.savetxt(save_path, data, delimiter='\t')

            converted += 1
        else:
            failed += 1
        if progress_callback:
            progress_callback(f"Processed {filename}")
    return {
        "total_files": len(file_list),
        "converted": converted,
        "failed": failed
    }

def extract_value(lines, key):
    """Helper: find first line containing 'key=' and return float value, else np.nan."""
    for line in lines:
        if key + "=" in line:
            try:
                return float(line.split("=")[1])
            except ValueError:
                pass
    return np.nan


def convert_data_folder_flexpes(
        input_dir,
        output_dir,
        file_done_callback=None,
        status_callback=None
    ):
    """
    Convert XPS text files and NEXAFS H5 files in input_dir
    to cleaned txt files in output_dir.

    Progress bar steps once per file.
    Status text updates per entry/region.
    """

    spectra_dir = os.path.join(output_dir, "spectra as .txt files")
    os.makedirs(spectra_dir, exist_ok=True)

    # ==============================
    # Helper: Process XPS TXT file
    # ==============================

    def process_xps_file(filename):

        full_path = os.path.join(input_dir, filename)

        if status_callback:
            status_callback(f"Processing {filename}")

        with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
            file_data = f.read()

        part = file_data.splitlines()

        try:
            num_of_regions = int(part[1][-4:])
        except Exception:
            num_of_regions = 1

        for i in range(num_of_regions):

            try:
                region_pre_part = re.split(r'\[Region', file_data)[i + 1]
            except IndexError:
                continue

            region_part = region_pre_part.splitlines()

            region_name = region_part[1][12:].strip().replace('/', '_')

            # -------- Energy Scale --------
            energy_type = ""
            for line in region_part:
                if line.startswith("Energy Scale="):
                    energy_type = line.split("=", 1)[1].strip().lower()
                    energy_type = energy_type.replace(" ", "_")
                    break

            if energy_type:
                region_name_with_energy = f"{region_name}_{energy_type}"
            else:
                region_name_with_energy = region_name

            # -------- Data Block --------
            match = re.search(
                r'\[Data ' + str(i + 1) + r'\]\s*([\s\S]*?)(?=\n\[|$)',
                region_pre_part
            )

            if not match:
                continue

            data_block = match.group(1).strip()
            lines = [l for l in data_block.splitlines() if l.strip()]
            if not lines:
                continue

            ncols = len(re.split(r'\s+', lines[0].strip()))

            try:
                data_values = np.array(
                    re.split(r'\s+', data_block.strip()),
                    dtype=float
                )
                data = data_values.reshape(-1, ncols)
            except Exception:
                continue

            save_filename = f"{filename.split('.txt')[0]}_{region_name_with_energy}.txt"
            save_path = os.path.join(spectra_dir, save_filename)

            np.savetxt(save_path, data, fmt="%.8e")

            if status_callback:
                status_callback(f"Saved: {save_filename}")

        # ✅ Move progress bar ONCE per XPS file
        if file_done_callback:
            file_done_callback()

    # ==============================
    # Helper: Process NEXAFS H5 file
    # ==============================

    def process_nexafs_file(h5_filename):

        full_path = os.path.join(input_dir, h5_filename)

        if status_callback:
            status_callback(f"Processing {h5_filename}")

        try:
            with h5py.File(full_path, 'r') as f:

                for entry_key in f.keys():

                    if not entry_key.startswith('entry'):
                        continue

                    measurement = f[entry_key].get('measurement')
                    if measurement is None:
                        continue

                    ch3 = measurement.get('b107a_em_03_ch3')
                    ch2 = measurement.get('b107a_em_03_ch2')
                    pcap_energy = measurement.get('pcap_energy_av')

                    if ch3 is None or ch2 is None or pcap_energy is None:
                        continue

                    ch3 = np.array(ch3)
                    ch2 = np.array(ch2)
                    pcap_energy = np.array(pcap_energy)

                    ch2_safe = np.where(ch2 == 0, np.nan, ch2)
                    ratio = ch3 / ch2_safe

                    data = np.column_stack((pcap_energy, ratio))

                    save_filename = f"{entry_key.split('entry')[-1]}_NEXAFS.txt"
                    save_path = os.path.join(spectra_dir, save_filename)

                    np.savetxt(save_path, data, fmt="%.8e")

                    # ✅ Status updates per entry
                    if status_callback:
                        status_callback(
                            f"{h5_filename} → {entry_key} saved"
                        )

        except Exception as e:
            if status_callback:
                status_callback(f"Failed: {h5_filename} ({e})")

        # ✅ Move progress bar ONCE per H5 file
        if file_done_callback:
            file_done_callback()

    # ==============================
    # Batch Processing
    # ==============================

    xps_files = sorted(
        f for f in os.listdir(input_dir)
        if f.startswith("XPS_") and f.endswith(".txt")
    )

    h5_files = sorted(
        f for f in os.listdir(input_dir)
        if f.endswith(".h5")
    )

    # --- Process XPS files ---
    for filename in xps_files:
        process_xps_file(filename)

    # --- Process H5 files ---
    for filename in h5_files:
        process_nexafs_file(filename)

    if status_callback:
        status_callback("Conversion complete!")