def create_labbook_b07_1(inDir, outDir, progress_callback=None):
    import h5py
    import numpy as np
    import pandas as pd
    import os
    import re
    import fnmatch

    dirname = inDir
    savelocation = os.path.join(outDir, 'all_data_contents.xlsx')
    file_list = fnmatch.filter(os.listdir(inDir), "*.nxs")
    total_files = len(file_list)

    # ---------------------- DATA EXTRACTION ----------------------
    def extract_data_from_file(filepath):
        filename_only = os.path.basename(filepath)
        match = re.search(r'b07-1-(\d+)\.nxs', filename_only)
        file_number = match.group(1) if match else filename_only

        try:
            with h5py.File(filepath, 'r') as f:
                print(f"🔹 Processing: {filename_only}")

                # -------- ENTRY --------
                entry = "entry" if "entry" in f else "entry1"

                row = {
                    "Filename": filename_only,
                    "filename": file_number,
                    "technique": "XPS",
                    "Comments": "",
                    "Status": "OK"
                }


                # -------- REGION --------
                try:
                    region_list = f[f"{entry}/analyser/region_list"][()]

                    # If it's a numpy array, take first element
                    if isinstance(region_list, np.ndarray):
                        region = region_list[0] if region_list.size > 0 else ""
                    else:
                        region = region_list

                    # Decode bytes if needed
                    if isinstance(region, bytes):
                        region = region.decode("utf-8")

                    # Final cleanup (removes things like [b'...'] leftovers)
                    region = str(region).strip("[]").replace("b'", "").replace("'", "")

                except Exception:
                    region = ""
                row["region"] = region
                # -------- DATE / TIME --------
                try:
                    start_time = f[f"{entry}/diamond_scan/start_time"][()].decode("utf-8")
                    row["Date"] = start_time[:10]
                    row["Time"] = start_time[11:16]
                except Exception:
                    row["Date"] = ""
                    row["Time"] = ""

                # -------- FIND INSTRUMENT GROUP --------
                base = None
                try:
                    instrument_groups = list(f[f"{entry}/instrument"].keys())

                    for g in instrument_groups:
                        if region.lower() in g.lower():
                            base = f"{entry}/instrument/{g}"
                            break

                    if base is None and instrument_groups:
                        base = f"{entry}/instrument/{instrument_groups[0]}"

                except Exception:
                    base = None

                # -------- ENERGY VALUES --------
                def get_scalar(path):
                    try:
                        val = f[path][()]
                        val = np.atleast_1d(val).squeeze()
                        return float(val) if val.size else ""
                    except Exception:
                        return ""

                if base:
                    row["Photon Energy (eV)"] = get_scalar(f"{base}/excitation_energy")
                    row["Pass Energy (eV)"] = get_scalar(f"{base}/pass_energy")
                else:
                    row["Photon Energy (eV)"] = ""
                    row["Pass Energy (eV)"] = ""

                # -------- POSITION VALUES --------
                row["X (mm)"] = get_scalar(f"{entry}/instrument/sm2_xp/value")
                row["Y (mm)"] = get_scalar(f"{entry}/instrument/sm2_yp/value")
                row["Z(mm)"] = get_scalar(f"{entry}/instrument/sm2_zp/value")

                print(f"✅ Extracted: {row['filename']} | Region: {row['region']}")
                if progress_callback:
                    progress_callback(f"✅ Extracted: {row['filename']} | Region: {row['region']}")

                return row

        except OSError as e:
            print(f"❌ Skipping unreadable file '{filepath}': {e}")
            return {
                "Filename": filename_only,
                "filename": file_number,
                "region": "Unreadable file",
                "technique": "XPS",
                "Comments": "",
                "Date": "",
                "Time": "",
                "Photon Energy (eV)": "",
                "Pass Energy (eV)": "",
                "X (mm)": "",
                "Y (mm)": "",
                "Z(mm)": "",
                "Status": "Unreadable"
            }

    # ---------------------- MAIN DATAFRAME ----------------------
    rows = []
    for i, filename in enumerate(sorted(os.listdir(dirname)), 1):
        if filename.endswith('.nxs'):
            

            full_path = os.path.join(dirname, filename)
            row = extract_data_from_file(full_path)
            if row:
                rows.append(row)

    df = pd.DataFrame(rows)

    new_order = [
        'filename', 'technique', 'region',
        'Photon Energy (eV)', 'Pass Energy (eV)',
        'X (mm)', 'Y (mm)', 'Z(mm)',
        'Comments', 'Date', 'Time'
    ]

    df = df.reindex(columns=new_order).fillna("")
    print("✅ DataFrame creation complete")

    # ---------------------- ROUNDING ----------------------
    df_rounded = df.copy()
    cols_to_round = df_rounded.columns.difference(['filename', 'region', 'Comments'])

    for col in cols_to_round:
        try:
            df_rounded[col] = pd.to_numeric(df_rounded[col])
        except Exception:
            pass

    df_rounded[cols_to_round] = df_rounded[cols_to_round].apply(
        lambda x: x.round(1) if pd.api.types.is_numeric_dtype(x) else x
    )

    # Clean region formatting
    df_rounded["region"] = df_rounded["region"].apply(
        lambda x: x.replace("(", "_(").replace(")", ")")
        if isinstance(x, str) and x.startswith("(")
        else x
    )

    # ---------------------- SAVE EXCEL ----------------------
    try:
        with pd.ExcelWriter(
            savelocation,
            engine="xlsxwriter",
            engine_kwargs={"options": {"nan_inf_to_errors": True}}
        ) as writer:

            workbook = writer.book
            worksheet = workbook.add_worksheet("Data")
            writer.sheets["Data"] = worksheet

            header_format = workbook.add_format({"bold": True, "border": 1})
            even_row_format = workbook.add_format({"bold": True})
            odd_row_format = workbook.add_format({"bold": False})

            date_banner_format = workbook.add_format({
                "bold": True,
                "font_size": 18,
                "bg_color": "#39FF14",
                "align": "center",
                "valign": "vcenter"
            })

            # Header
            for col_num, col_name in enumerate(df_rounded.columns):
                worksheet.write(0, col_num, col_name, header_format)
                worksheet.set_column(col_num, col_num, 18)

            excel_row = 1
            prev_date = None
            n_cols = len(df_rounded.columns)

            for _, row in df_rounded.iterrows():
                current_date = row.get("Date", "")

                if current_date and current_date != prev_date:
                    worksheet.merge_range(
                        excel_row, 0, excel_row, n_cols - 1,
                        f" {current_date}", date_banner_format
                    )
                    worksheet.set_row(excel_row, 36)
                    excel_row += 1
                    prev_date = current_date

                is_bold_row = (excel_row % 2 == 0)
                row_format = even_row_format if is_bold_row else odd_row_format
                worksheet.set_row(excel_row, None, row_format)

                for col_num, value in enumerate(row):
                    worksheet.write(excel_row, col_num, value)

                excel_row += 1

        print("✅ Saved Excel file!")

    except Exception as e:
        raise RuntimeError(f"Excel file may be open or locked.\n{e}")

    print(" Excel sheet produced by hardworking script goblins: ლ༼ ಥ 益 ಥ ༽ლ")