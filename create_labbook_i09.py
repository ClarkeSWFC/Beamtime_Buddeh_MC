def create_labbook_i09(
    inDir,
    outDir,
    progress_callback=None,
    formatting=None
):
    """
    Fully functionalised version of original labbook script.
    No logic removed. No formatting removed.
    """

    import h5py
    import numpy as np
    import pandas as pd
    import os
    import re
    import fnmatch
    if formatting is None:
        formatting = {}

    xsw_colours = formatting.get(
        "xsw_colours",
        {}
    )
    prep_allocations = formatting.get(
        "prep_allocations",
        []
    )

    dirname = inDir
    savelocation = os.path.join(outDir, 'all_data_contents.xlsx')
    file_list = fnmatch.filter(os.listdir(inDir), "*.nxs")
    total_files = len(file_list) 
    # ---------------------- SUFFIX MAP ----------------------
    suffix_map = {
        "smpmx": "X (mm)",
        "smpmy": "Y (mm)",
        "smpmz": "Z(mm)",
        "smpmpolar": "Polar (deg)",
        "smpmazimuth": "Azimuth (deg)",
        "excitation_energy": "Photon Energy (eV)",
        "pass_energy": "Pass Energy (eV)"
    }

    # ---------------------- DATA EXTRACTION ----------------------
    def extract_data_from_file(filepath):
        filename_only = os.path.basename(filepath)
        match = re.search(r'i09-(\d+)\.nxs', filename_only)
        file_number = match.group(1) if match else filename_only

        try:
            with h5py.File(filepath, 'r') as f:
                print(f"🔹 Processing: {filename_only}")

                # ---------------- ENTRY HANDLING ----------------
                
                if "entry" in f:
                    entry_group = "entry"
                elif "entry1" in f:
                    entry_group = "entry1"
                else:
                    raise KeyError("No 'entry' or 'entry1' group found in file.")

                try:
                    entry_keys = list(f[entry_group].keys())
                    region = entry_keys[0] if entry_keys else ''
                except Exception:
                    region = ''

                row = {
                    "Filename": filename_only,
                    "filename": file_number,
                    "region": region,
                    "Status": "OK"
                }

                try:
                    end_time = f[f"{entry_group}/end_time"][()].decode("utf-8")
                    row["Date"] = end_time[:10]
                    row["Time"] = end_time[11:16]
                except Exception:
                    row["Date"] = ""
                    row["Time"] = ""

                try:
                    instrument_groups = list(f[f"{entry_group}/instrument"].keys())
                    first_instrument = instrument_groups[0] if instrument_groups else None
                except Exception:
                    first_instrument = None

                smpm_base = f"{entry_group}/instrument/smpm"

                for suffix, column_name in suffix_map.items():
                    value = ""

                    if suffix in ["smpmx", "smpmy", "smpmz", "smpmpolar", "smpmazimuth"]:
                        path = f"{smpm_base}/{suffix}"
                        if path in f:
                            try:
                                value = f[path][()]
                            except Exception:
                                value = ""

                    elif suffix in ["excitation_energy", "pass_energy"]:
                        if first_instrument:
                            path = f"{entry_group}/instrument/{first_instrument}/{suffix}"
                            if path in f:
                                try:
                                    value = f[path][()]
                                except Exception:
                                    value = ""

                    if isinstance(value, np.ndarray):
                        value = np.atleast_1d(value).squeeze()
                        if value.size > 0:
                            value = value.flat[0]
                        else:
                            value = ""

                    if column_name == "Photon Energy (eV)":
                        try:
                            value = float(value)
                        except Exception:
                            pass

                    row[column_name] = value if value is not None else ""

                region_lower = region.lower()
                if "xsw" in region_lower:
                    row["technique"] = "XSW"
                elif "current" in region_lower:
                    row["technique"] = "NIXSWR"
                elif any(term in region_lower for term in [
                        "1s", "2p", "3d", "4d", "4f", "survey", "3p",
                        "search", "rough", "3s", "fermi", "vb",
                        "overview", "fe"
                    ]) and not any(x in region_lower for x in ["xsw", "respes", "rpes"]):
                    row["technique"] = "XPS"
                elif any(x in region_lower for x in ["kll", "lmm", "raes"]):
                    row["technique"] = "NEXAFS"
                elif any(x in region_lower for x in ["respes", "rpes"]):
                    row["technique"] = "RESPES"
                else:
                    row["technique"] = "unknown"

                print(f"✅ Extracted: {row['filename']} | Technique: {row['technique']} | Region: {row['region']}")
                if progress_callback:
                    progress_callback(f"✅ Extracted: {row['filename']} | Technique: {row['technique']} | Region: {row['region']}")
                return row

        except OSError as e:
            print(f"❌ Skipping unreadable file '{filepath}' — likely unfinished: {e}")
            row = {
                "Filename": filename_only,
                "filename": file_number,
                "region": "File unreadable, probably unfinished scan",
                "Status": "File unreadable, probably unfinished scan",
                "Date": "",
                "Time": "",
                "technique": "buggered measurement"
            }
            for col in suffix_map.values():
                row[col] = ""
            if progress_callback:
                progress_callback(f"❌ Skipping unreadable file '{filepath}' — likely unfinished: {e}")
            return row

    # ---------------------- MAIN DATAFRAME CREATION ----------------------
    rows = []
    for filename in sorted(os.listdir(dirname)):
        if filename.endswith('.nxs'):
            full_path = os.path.join(dirname, filename)
            row = extract_data_from_file(full_path)
            if row:
                rows.append(row)

    df = pd.DataFrame(rows)

    df["Comments"] = ""

    new_order = [
        'filename', 'technique', 'region', 'Photon Energy (eV)', 'Pass Energy (eV)',
        'X (mm)', 'Y (mm)', 'Z(mm)', 'Polar (deg)', 'Azimuth (deg)',
        'Comments', 'Date', 'Time'
    ]
    df = df.reindex(columns=new_order)
    df = df.fillna("")
    print("✅ DataFrame creation complete, safe to proceed.")



    print("searching gdaterminal.log")
    if progress_callback:
        progress_callback("searching gdaterminal.log")
    xsw_rows = df[df["technique"].str.contains("XSW|RC", case=False, na=False)]
    xsw_filenames_array = np.array(xsw_rows["filename"])
    xsw_filenames_with_extension = [f"{name}.nxs" for name in xsw_filenames_array]

    target_1 = 'NEXT SCAN'
    target_2 = 'NEXT sequence'

    data = []
   
    gda_path = os.path.join(inDir, "gdaterminal.log")
    if os.path.exists(gda_path):
        with open(gda_path, "r") as file:
            lines = file.readlines()
    else:
        print("⚠️ gdaterminal.log not found")
        lines = []

    for i, line in enumerate(lines):
        if any(target in line for target in xsw_filenames_with_extension):
            filename_match = next((target for target in xsw_filenames_with_extension if target in line), None)
            filenumber = filename_match.replace(".nxs", "") if filename_match else ""

            technique = "unknown"
            region = ""
            fwhm = ""

            # Step 1: Look for technique line (XPS sometimes run two within one "SCAN" region, so need to check for "sequence" for these)
            found_line = None
            for offset in range(5, 21):
                j = i - offset
                if j >= 0 and target_1 in lines[j]:
                    found_line = lines[j]
                    break
            if not found_line:
                for offset in range(5, 21):
                    j = i - offset
                    if j >= 0 and target_2 in lines[j]:
                        found_line = lines[j]
                        break

            # Step 2: Extract technique and region
            if found_line:
                match = re.search(r'is\s+(.*?)\s+at', found_line)
                if match:
                    description = match.group(1).strip()
                    if "XP spectra" in description:
                        technique = "XPS"
                    elif "XSW" in description:
                        technique = "XSW"
                    else:
                        technique = "Rocking Curve"

                    # Extract region name from "... "C1s_XSW.seq" at ..."
                    region_match = re.search(r'"(.*?)_', found_line)
                    if region_match:
                        region = region_match.group(1)
                    elif technique == "Rocking Curve":
                        # Default if the reflection isn't specified
                        region = "(111) - not specified in log"

                        # Search around this scan for the reflection line
                        for k in range(i - 60, min(i + 10, len(lines))):
                            if k < 0:
                                continue

                            reflection_match = re.search(
                                r'using the\s*(\([^)]+\))\s*reflection',
                                lines[k]
                            )

                            if reflection_match:
                                region = reflection_match.group(1)
                                break
                        
            else:
                region = "could not find region"

            
            # Step 3: Look for FWHM for every Rocking Curve
            #
            # Successful RC/XSW example:
            #   New Bragg energy is : # keV and the FWHM is # eV
            #
            # Unsuccessful RC example:
            #   width of # eV compared to # eV
            #
            # The FWHM is normally reported AFTER the .nxs filename, so search
            # forward through this scan. We stop if another scan starts, to avoid
            # accidentally assigning the next rocking curve's FWHM to this one.

            if technique in ["XSW", "Rocking Curve"]:

                for k in range(i, len(lines)):

                    fwhm_line = lines[k]

                    # Stop if we have reached the next scan.
                    # This prevents a missing FWHM from accidentally picking up
                    # the value belonging to a later rocking curve.
                    if k > i and "NEXT SCAN" in lines[k]:
                        break

                    # Successful rocking curve / XSW

                    match = re.search(
                        r"New Bragg energy is\s*:?\s*[\d.eE+-]+"
                        r".*?FWHM is\s*([\d.eE+-]+)\s*eV",
                        fwhm_line,
                        re.IGNORECASE
                    )

                    if match:
                        fwhm_value = float(match.group(1))
                        fwhm = f"FWHM = {fwhm_value:.2f} eV"
                        break

                
                    # Unsuccessful rocking curve
                
                    match = re.search(
                        r"width of\s*([\d.eE+-]+)\s*eV\s+compared to",
                        fwhm_line,
                        re.IGNORECASE
                    )

                    if match:
                        fwhm_value = float(match.group(1))
                        fwhm = f"FWHM = {fwhm_value:.2f} eV"
                        break


            if found_line:
                data.append({
                    "filename": filenumber,
                    "technique": technique,
                    "region": region,
                    "fwhm": fwhm
                })


    xsw_details_df = pd.DataFrame(data)


    #%% stickin em together
    final_array = xsw_details_df.copy()

    if final_array.empty:
        print("⚠️ No XSW entries found — override merge skipped")
        df_merged = df.copy()
        if progress_callback:
            progress_callback("⚠️ No XSW entries found")
    else:
        final_array.replace(0, np.nan, inplace=True)

        # Force correct columns explicitly
        final_array.columns = [
            'filename',
            'override_technique',
            'override_region',
            'override_comments'
        ]

        final_array['filename'] = (
            final_array['filename']
            .astype(str)
            .str.replace(r'\.0$', '', regex=True)
            .str.strip()
        )

        df['filename'] = df['filename'].astype(str).str.strip()

        # Merge
        df_merged = df.merge(
            final_array,
            on='filename',
            how='left'
        )

        # Apply overrides
        df_merged['technique'] = df_merged['override_technique'].combine_first(df_merged['technique'])
        df_merged['region'] = df_merged['override_region'].combine_first(df_merged['region'])
        df_merged['Comments'] = df_merged['override_comments'].combine_first(df_merged['Comments'])

        # Drop helper columns
        df_merged.drop(
            columns=['override_technique', 'override_region', 'override_comments'],
            inplace=True
        )


    #%% round the numbers
    df_rounded = df_merged.copy()

    # Exclude non-numeric columns
    cols_to_round = df_rounded.columns.difference(['filename', 'region'])

    for col in cols_to_round:
        try:
            df_rounded[col] = pd.to_numeric(df_rounded[col])
        except Exception:
            # leave column unchanged if it cannot be converted
            pass

    # Round only numeric columns
    df_rounded[cols_to_round] = df_rounded[cols_to_round].apply(
        lambda x: x.round(1) if pd.api.types.is_numeric_dtype(x) else x
    )

    # Clean region names
    df_rounded["region"] = df_rounded["region"].apply(
        lambda x: x.replace("(", "_(").replace(")", ")")
        if isinstance(x, str) and x.startswith("(")
        else x
    )

    #%% formatting XSW for visual clarity
    # inserting blank rows before and after RC–(1–4 XPS)–XSW–(1–4 XPS) blocks (this will work up to 4 haxpes before and after the xsw 
    #- you can change this below but it might get confused if you go too high)
    #there is formatting of colours of different xsw regions included in the next section
    MAX_XPS = 4

    blank = {col: "" for col in df_rounded.columns}
    blank["_prep_colour"] = None
    blank["_prep_id"] = None
    def get_prep_colour(filename):
        try:
            filename = int(filename)
        except Exception:
            return None

        for prep in prep_allocations:
            if prep["start"] <= filename <= prep["end"]:
                return prep.get("colour")

        return None
    df_out = []
    i = 0
    n = len(df_rounded)

    while i < n:
        # Must start with Rocking Curve
        if df_rounded.iloc[i]["technique"] == "Rocking Curve":

            j = i + 1
            xps_before = 0

            # Count XPS before XSW
            while j < n and df_rounded.iloc[j]["technique"] == "XPS" and xps_before < MAX_XPS:
                xps_before += 1
                j += 1

            # Must find XSW next
            if j < n and df_rounded.iloc[j]["technique"] == "XSW":
                j += 1
                xps_after = 0

                # Count XPS after XSW
                while j < n and df_rounded.iloc[j]["technique"] == "XPS" and xps_after < MAX_XPS:
                    xps_after += 1
                    j += 1

                # Valid block if at least 1 XPS on each side
                if xps_before >= 1 and xps_after >= 1:

                    # ----- Insert blank BEFORE block -----
                    if not df_out or any(df_out[-1][col] != "" for col in df_rounded.columns):
                        blank_row = blank.copy()

                        # assign prep colour if possible
                        previous_filename = df_rounded.iloc[i]["filename"]
                        blank_row["filename"] = ""
                        blank_row["_prep_id"] = df_rounded.iloc[i]["filename"]
                        df_out.append(blank_row)

                    # Insert full block
                    for k in range(i, j):
                        df_out.append(df_rounded.iloc[k].to_dict())

                    # ----- Insert blank AFTER block -----
                    if any(df_out[-1][col] != "" for col in df_rounded.columns):
                        blank_row = blank.copy()

                        # assign prep colour if possible
                        previous_filename = df_rounded.iloc[i]["filename"]
                        blank_row["filename"] = ""
                        blank_row["_prep_id"] = df_rounded.iloc[i]["filename"]
                        df_out.append(blank_row)

                    i = j
                    continue

        # Normal row
        df_out.append(df_rounded.iloc[i].to_dict())
        i += 1

    # Convert back to DataFrame
    df_rounded = pd.DataFrame(df_out)
    

    #%% save with date banners (xlsxwriter)
    for col in ["_prep_colour"]:
        if col in df_rounded.columns:
            df_rounded = df_rounded.drop(columns=[col])
    df_rounded = df_rounded.fillna("")
    print(df_rounded[df_rounded["filename"].isin(["310332","310338"])])
    try:
        df_export = df_rounded.drop(
            columns=["_prep_id"],
            errors="ignore"
        )
        with pd.ExcelWriter(
            savelocation,
            engine="xlsxwriter",
            engine_kwargs={"options": {"nan_inf_to_errors": True}}
        ) as writer:

            workbook  = writer.book
            worksheet = workbook.add_worksheet("Data")
            writer.sheets["Data"] = worksheet

            # ---- Formats ----
            header_format = workbook.add_format({
                "bold": True,
                "border": 1
            })

            even_row_format = workbook.add_format({
                "bold": True
            })

            odd_row_format = workbook.add_format({
                "bold": False
            })

            date_banner_format = workbook.add_format({
                "bold": True,
                "font_size": 18,
                "font_color": "black",
                "bg_color": "#39FF14",   # neon green
                "align": "center",
                "valign": "vcenter"
            })

            # ---- XSW Region Formats (preserve alternating bold) ----
            
            
            REGION_FORMATS = {}

            for region, colour in xsw_colours.items():
                
                key = region.lower().replace("_xsw", "")
                
                REGION_FORMATS[key] = (
                    workbook.add_format({
                        "bg_color": colour,
                        "bold": True
                    }),
                    workbook.add_format({
                        "bg_color": colour,
                        "bold": False
                    })
                )
            PREP_FORMATS = []

            for prep in prep_allocations:
                try:
                    PREP_FORMATS.append({
                        "start": int(prep["start"]),
                        "end": int(prep["end"]),
                        "bold_format": workbook.add_format({
                            "bg_color": prep.get("colour", "#FFF2CC"),
                            "bold": True
                        }),
                        "normal_format": workbook.add_format({
                            "bg_color": prep.get("colour", "#FFF2CC"),
                            "bold": False
                        })
                    })
                except Exception:
                    pass
            # ---- Write header row ----
            for col_num, col_name in enumerate(df_export.columns):
                worksheet.write(0, col_num, col_name, header_format)
                worksheet.set_column(col_num, col_num, 18)

            excel_row = 1
            prev_date = None
            n_cols = len(
                df_export.columns.drop("_prep_id", errors="ignore")
            )
            prep_banner_format = {}

            for prep in prep_allocations:
                prep_banner_format[(prep["start"], prep["end"])] = workbook.add_format({
                    "bold": False,
                    "bg_color": prep.get("colour", "#FFF2CC"),
                    "align": "center",
                    "valign": "vcenter"
                })
            for _, row in df_rounded.iterrows():
                current_date = row.get("Date", "")
                try:
                    current_filename = int(row.get("filename", -1))
                except Exception:
                    current_filename = -1


                # Insert prep banner above first scan
                for prep in prep_allocations:
                    if current_filename == int(prep["start"]):

                        worksheet.merge_range(
                            excel_row,
                            0,
                            excel_row,
                            n_cols - 1,
                            prep.get("description", ""),
                            prep_banner_format[
                                (prep["start"], prep["end"])
                            ]
                        )

                        worksheet.set_row(excel_row, 24)
                        excel_row += 1
                        break
                # Insert date banner when date changes
                if current_date and current_date != prev_date:
                    worksheet.merge_range(
                        excel_row,
                        0,
                        excel_row,
                        n_cols - 1,
                        f" {current_date}",
                        date_banner_format
                    )
                    worksheet.set_row(excel_row, 36)
                    excel_row += 1
                    prev_date = current_date

                tech_value = row.get("technique", "")
                region_value = str(row.get("region", "")).lower()
                filename_numeric = pd.to_numeric(
                    row.get("filename", ""),
                    errors="coerce"
                )
                if pd.isna(filename_numeric):
                    filename_numeric = pd.to_numeric(
                        row.get("_prep_id", ""),
                        errors="coerce"
                    )
                # Determine row boldness (alternating for all non-blank rows)
                is_bold_row = (excel_row % 2 == 0)

                # APPLY ROW FORMAT FIRST
                row_format = even_row_format if is_bold_row else odd_row_format
                worksheet.set_row(excel_row, None, row_format)

                export_columns = df_export.columns

                for col_num, col_name in enumerate(export_columns):

                    value = row[col_name]
                    cell_format = None
                    for prep in PREP_FORMATS:
                        if (
                                pd.notna(filename_numeric)
                                and prep["start"] <= filename_numeric <= prep["end"]
                            ):
                            cell_format = (
                                prep["bold_format"]
                                if is_bold_row
                                else prep["normal_format"]
                            )
                            break
                    # Only override REGION cell when technique is XSW
                    if col_name == "region" and tech_value == "XSW":
                        for key, (bold_fmt, normal_fmt) in REGION_FORMATS.items():
                            if key in region_value:
                                cell_format = bold_fmt if is_bold_row else normal_fmt
                                break

                    worksheet.write(excel_row, col_num, value, cell_format)
                    
                excel_row += 1

        print("✅ Saved Excel file!")

    except Exception as e:
        error_msg = f"Excel file may be open or locked.\n{e}"
        print("⚠️", error_msg)
        raise RuntimeError(error_msg)  

    print(" Excel sheet produced by hardworking script goblins: ლ༼ ಥ 益 ಥ ༽ლ")