# -*- coding: utf-8 -*-
"""
Created on Mon Feb 23 11:40:19 2026

@author: bramc44
"""

import os
import h5py
import numpy as np
import pandas as pd
import re
import traceback
from datetime import datetime

def create_labbook_flexpes(InDir, OutDir, progress_callback=None):
    # --------- FileCount --------
    all_files = os.listdir(InDir)

    # Count XPS files
    xps_files = [
        f for f in all_files
        if f.startswith("XPS_") and f.endswith(".txt")
    ]

    # Count H5 files
    h5_files = [
        f for f in all_files
        if f.endswith(".h5")
    ]

    file_list = xps_files + h5_files
    total_files = len(file_list)
    # --------- Storage ---------
    all_for_save = []
    
    # --------- Columns ---------
    columns_order = [
        'filename', 'technique', 'region', 'Photon Energy (eV)', 'Pass Energy (eV)',
        'X (mm)', 'Y (mm)', 'Z(mm)', 'Polar (deg)', 'Comments', 'Date', 'Time'
    ]
    
    # --------- FLEXPES XPS processing ---------
    def append_to_all_save_xps(date_of_acq, time_of_acq, filename, region_name, photon_energy,
                               pass_energy, X ,Y ,Z, polar):
        try:
            dt_obj = datetime.strptime(date_of_acq, "%Y-%m-%d")
            date_of_acq = dt_obj.strftime("%d/%m/%Y")
        except:
            pass

        if len(time_of_acq.split(':')) == 2:
            time_of_acq += ":00"

        all_for_save.append([
            os.path.splitext(filename)[0],  
            "XPS",
            region_name,
            photon_energy,
            pass_energy,
            X,
            Y,
            Z,
            polar,
            "",
            date_of_acq,
            time_of_acq
        ])

    def XPS_reader(file_path):
        filename = os.path.basename(file_path)
        try:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                file_data = f.read()
            part = re.split('\n', file_data)
            num_of_regions = int(part[1][-4:])
        except Exception:
            print(f"⚠️ Could not determine number of regions for file {filename}")
            return

        for i in range(num_of_regions):
            section_region = r'\[Region'
            region_pre_part = re.split(section_region, file_data)[i+1]
            region_part = re.split('\n', region_pre_part)

            dia_offset = 3 if region_part[5].startswith('Dimen') else 0

            try:
                region_name = region_part[1][12:]
                photon_energy = float(region_part[11+dia_offset][18:])
                pass_energy = float(region_part[9+dia_offset][12:])
                date_of_acq = region_part[33+dia_offset][5:]
                time_of_acq = region_part[34+dia_offset][5:]
            except Exception as e:
                print(f"⚠️ Metadata extraction failed for file {filename}: {e}")
                continue

            X = Y = Z = polar = np.nan
            for line in region_part:
                if line.startswith("X="):
                    X = float(line.split("=")[1])
                elif line.startswith("Y="):
                    Y = float(line.split("=")[1])
                elif line.startswith("Z="):
                    Z = float(line.split("=")[1])
                elif line.lower().startswith("polar="):
                    polar = float(line.split("=")[1])

            append_to_all_save_xps(date_of_acq, time_of_acq, filename, region_name,
                                   photon_energy, pass_energy, X, Y, Z, polar)

    # --------- NEXAFS processing ---------
    def append_nexafs_to_labbook(nexafs_folder, df_labbook):
        for file in sorted(os.listdir(nexafs_folder)):
            if not file.endswith('.h5'):
                continue

            full_path = os.path.join(nexafs_folder, file)
            try:
                with h5py.File(full_path, 'r') as f:
                    processed_entries = 0
                    for entry_key in f.keys():
                        if not entry_key.startswith('entry'):
                            continue

                        date_val = "not found"
                        time_val = "not found"
                        region = "region not defined in script"
                        photon_energy = "n/a"
                        pass_energy = "enter manually"
                        X = Y = Z = "not found"
                        polar = "not found"
                        comments = ""

                        start_time_ds = f[entry_key].get('start_time')
                        if start_time_ds is not None:
                            raw_date_time = start_time_ds[()]
                            if isinstance(raw_date_time, bytes):
                                raw_date_time = raw_date_time.decode('utf-8')
                            parts = str(raw_date_time).split("T")
                            if len(parts) == 2:
                                try:
                                    dt_obj = datetime.strptime(parts[0], "%Y-%m-%d")
                                    date_val = dt_obj.strftime("%d/%m/%Y")
                                except:
                                    date_val = parts[0]
                                time_val = parts[1].split(".")[0]
                                if len(time_val.split(':')) == 2:
                                    time_val += ":00"

                        measurement = f[entry_key].get('measurement')
                        if measurement is not None:
                            mp_x = measurement.get('pcap_mp01_x')
                            mp_y = measurement.get('pcap_mp01_y')
                            mp_z = measurement.get('pcap_mp01_z')
                            mp_polar = measurement.get('pcap_mp01_polar')

                            if mp_x is not None and len(mp_x) > 0:
                                X = float(np.mean(mp_x))
                            if mp_y is not None and len(mp_y) > 0:
                                Y = float(np.mean(mp_y))
                            if mp_z is not None and len(mp_z) > 0:
                                Z = float(np.mean(mp_z))
                            if mp_polar is not None and len(mp_polar) > 0:
                                polar = float(np.mean(mp_polar))

                            pcap_energy_av = measurement.get('pcap_energy_av')#assigning NEXAFS regions
                            if pcap_energy_av is not None and len(pcap_energy_av) > 0:
                                mean_energy = np.mean(pcap_energy_av)
                                if 270 <= mean_energy <= 330:
                                    region = "C KLL"
                                elif 380 <= mean_energy <= 430:
                                    region = "N KLL"

                        entry_number = entry_key.replace("entry", "")
                        row = [
                            entry_number,
                            "NEXAFS",
                            region,
                            photon_energy,
                            pass_energy,
                            X, Y, Z,
                            polar,
                            comments,
                            date_val,
                            time_val
                        ]
                        df_labbook.loc[len(df_labbook)] = row
                        processed_entries += 1

                    print(f"✅ Processed NEXAFS {file} ({processed_entries} entries)")
                    if progress_callback:
                        progress_callback(f"✅ Processed NEXAFS {file} ({processed_entries} entries)")

            except Exception as e:
                print(f"⚠️ Skipped NEXAFS {file}: {e}")
                traceback.print_exc(limit=1)

        return df_labbook

    # --------- Group NEXAFS function ---------
    def group_nexafs_measurements(df):
        grouped_rows = []
        i = 0

        while i < len(df):
            row = df.iloc[i]

            if row["technique"] != "NEXAFS":
                grouped_rows.append(row)
                i += 1
                continue

            if '-' in str(row["filename"]):
                grouped_rows.append(row)
                i += 1
                continue

            start_idx = i
            try:
                start_entry = int(row["filename"])
            except ValueError:
                grouped_rows.append(row)
                i += 1
                continue

            j = i + 1
            while j < len(df):
                next_row = df.iloc[j]
                if (
                    next_row["technique"] == "NEXAFS" and
                    next_row["region"] == row["region"] and
                    next_row["X (mm)"] == row["X (mm)"] and
                    next_row["Y (mm)"] == row["Y (mm)"] and
                    next_row["Z(mm)"] == row["Z(mm)"] and
                    next_row["Polar (deg)"] == row["Polar (deg)"] and
                    '-' not in str(next_row["filename"])
                ):
                    j += 1
                else:
                    break

            end_entry = int(df.iloc[j-1]["filename"])
            new_row = row.copy()
            if end_entry != start_entry:
                new_row["filename"] = f"{start_entry}-{end_entry}"
            else:
                new_row["filename"] = str(start_entry)

            grouped_rows.append(new_row)
            i = j

        return pd.DataFrame(grouped_rows).reset_index(drop=True)
    # Ensure columns are strings to avoid .str accessor errors
    
    # --------- Process XPS ---------
    xps_files = sorted(f for f in os.listdir(InDir) if f.startswith("XPS_") and f.endswith(".txt"))
    for file_name in xps_files:
        full_path = os.path.join(InDir, file_name)
        try:
            XPS_reader(full_path)
            print(f"Processed XPS {file_name}")
            if progress_callback:
                progress_callback(f"Processed XPS {file_name}")
        except Exception as e:
            print(f"⚠️ Skipped XPS {file_name}: {e}")
            if progress_callback:
                progress_callback(f"⚠️ Skipped XPS {file_name}: {e}")
            traceback.print_exc(limit=1)

    df_labbook = pd.DataFrame(all_for_save, columns=columns_order)
    df_labbook = append_nexafs_to_labbook(InDir, df_labbook)
    for col in ['filename', 'region', 'Comments']:
        df_labbook[col] = df_labbook[col].astype(str)
    # --------- Chronological sorting ---------
    df_labbook['Time'] = df_labbook['Time'].apply(lambda t: t if len(str(t).split(':'))==3 else str(t)+":00")
    df_labbook['DateTime'] = pd.to_datetime(
        df_labbook['Date'] + ' ' + df_labbook['Time'],
        format="%d/%m/%Y %H:%M:%S",
        errors='coerce'
    )
    df_labbook = df_labbook.sort_values(by='DateTime', ascending=True).drop(columns='DateTime')

    # --------- Round positions and group NEXAFS ---------
    round_cols = ['X (mm)', 'Y (mm)', 'Z(mm)', 'Polar (deg)']
    placeholder = -9999

    for col in round_cols:
        df_labbook[col] = pd.to_numeric(df_labbook[col], errors='coerce').fillna(placeholder)
        df_labbook[col] = df_labbook[col].round(1)

    df_labbook = group_nexafs_measurements(df_labbook)

    for col in round_cols:
        df_labbook[col] = df_labbook[col].replace(placeholder, '')

    df_labbook = group_nexafs_measurements(df_labbook)

    # --------- Save CSV ---------
    csv_path = os.path.join(OutDir, 'flexpes_labbook.csv')

    try:
        df_labbook.to_csv(csv_path, index=False)
        print(f"✅ flexpes labbook saved: {csv_path}")
        if progress_callback:
            progress_callback(" Excel sheet produced by hardworking script goblins: ლ༼ ಥ 益 ಥ ༽ლ")

    except Exception as e:
        error_msg = f"CSV file may be open or locked.\n{e}"
        print("⚠️", error_msg)
        if progress_callback:
            progress_callback(error_msg)
            raise RuntimeError(error_msg)