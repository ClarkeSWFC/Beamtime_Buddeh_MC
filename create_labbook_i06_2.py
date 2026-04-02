def create_labbook_i06_2(inDir, outDir, progress_callback=None):
    """
    Fully functionalised i06-2 labbook script.
    Formatting + colouring fully preserved.
    """

    import h5py
    import numpy as np
    import pandas as pd
    import os
    import re

    dirname = inDir
    savelocation = os.path.join(outDir, "i06_LEEM_Labbook.xlsx")

    file_list = [f for f in os.listdir(inDir) if f.endswith(".nxs")]
    total_files = len(file_list)

    # ---------------------- DATA EXTRACTION ----------------------
    def extract_data_from_file(filepath):

        filename_only = os.path.basename(filepath)
        match = re.search(r"i06-2-(\d+)\.nxs", filename_only)
        file_number = match.group(1) if match else filename_only

        try:
            with h5py.File(filepath, "r") as f:

                msg = f"🔹 Processing: {filename_only}"
                print(msg)
                

                row = {
                    "filename": file_number,
                    "status": "OK",
                }

                # --- Date / Time ---
                try:
                    start_time = f["entry/diamond_scan/start_time"][()]
                    if isinstance(start_time, bytes):
                        start_time = start_time.decode("utf-8")
                    start_time = str(start_time)
                    row["date"] = start_time[:10]
                    row["time"] = start_time[11:16]
                except Exception:
                    row["date"] = ""
                    row["time"] = ""

                # --- Scan command ---
                try:
                    scan_command = f["entry/diamond_scan/scan_command"][()]
                    if isinstance(scan_command, bytes):
                        scan_command = scan_command.decode("utf-8")
                    scan_command = str(scan_command)
                except Exception:
                    scan_command = ""

                row["scan_command"] = scan_command

                def get_scalar(path):
                    try:
                        v = f[path][()]
                        v = np.array(v).squeeze()
                        return float(v)
                    except Exception:
                        return ""

                # --- Values ---
                fov_a      = get_scalar("entry/instrument/leem/fov_a")
                stv_scalar = get_scalar("entry/instrument/leem/stv")
                obj_scalar = get_scalar("entry/instrument/leem/obj")

                fsm_x = get_scalar("entry/instrument/ps/x")
                fsm_y = get_scalar("entry/instrument/ps/y")

                stv_start = stv_scalar
                stv_end   = stv_scalar
                obj_start = obj_scalar
                obj_end   = obj_scalar

                try:
                    stv_vals = np.array(f["entry/instrument/leem_stv/value"][()]).astype(float)
                    if stv_vals.size > 0:
                        stv_start = float(stv_vals.min())
                        stv_end   = float(stv_vals.max())
                except Exception:
                    pass

                try:
                    obj_vals = np.array(f["entry/instrument/leem_obj/value"][()]).astype(float)
                    if obj_vals.size > 0:
                        obj_start = float(obj_vals.min())
                        obj_end   = float(obj_vals.max())
                except Exception:
                    pass

                row.update({
                    "fov_um": fov_a,
                    "start_stv_V": stv_start,
                    "end_stv_V": stv_end,
                    "start_obj_mA": obj_start,
                    "end_obj_mA": obj_end,
                    "fsm_x": fsm_x,
                    "fsm_y": fsm_y
                })

                # --- Classification ---
                is_laserpeem = (stv_scalar == 0) and (stv_start == stv_end)

                if fov_a == 0:
                    technique = "LEED"
                elif is_laserpeem:
                    technique = "LASERPEEM"
                else:
                    technique = "LEEM"

                has_sweep = (stv_start != stv_end) or (obj_start != obj_end)

                if technique == "LEED":
                    image_type = "LEED scan (video)" if has_sweep else "LEED image"
                elif technique == "LASERPEEM":
                    image_type = "PEEM image"
                else:
                    image_type = "LEEM scan (video)" if has_sweep else "LEEM image"

                # --- Scan parsing ---
                n_images, step, exposure = "", "", ""

                parts = scan_command.split()
                scan_target = parts[1] if len(parts) >= 2 and parts[0] == "scan" else ""

                try:
                    if scan_target in ["ds", "leem_stv", "leem_obj"]:
                        start_val = float(parts[2])
                        stop_val  = float(parts[3])
                        step_val  = float(parts[4])
                        exp_val   = float(parts[-1])

                        n_images = int((stop_val - start_val) / step_val + 1)
                        step = step_val
                        exposure = exp_val

                    elif scan_target == "t":
                        n_images = 1
                        exposure = float(parts[-1])

                except Exception:
                    pass

                row.update({
                    "technique": technique,
                    "image_type": image_type,
                    "no_of_images": n_images,
                    "step": step,
                    "exposure_time_s": exposure
                })

                msg = f"✅ Extracted: {file_number} | {technique} | {image_type}"
                print(msg)
                if progress_callback:
                    progress_callback(msg)

                return row

        except OSError:
            return {
                "filename": file_number,
                "status": "File unreadable",
                "technique": "buggered measurement"
            }

    # ---------------------- BUILD DATAFRAME ----------------------
    rows = []
    for filename in sorted(file_list):
        full_path = os.path.join(dirname, filename)
        row = extract_data_from_file(full_path)
        if row:
            rows.append(row)

    df = pd.DataFrame(rows)
    df["comments"] = ""
    df = df.fillna("")

    # ---------------------- PRETTY HEADERS ----------------------
    df_out = df.rename(columns={
        "filename": "Filename",
        "technique": "Technique",
        "image_type": "Image type",
        "fov_um": "FOV (µm)",
        "fsm_x": "X-coordinate (on sample)",
        "fsm_y": "Y-coordinate (on sample)",
        "start_stv_V": "Start stv (V)",
        "end_stv_V": "End stv (V)",
        "start_obj_mA": "Start obj (mA)",
        "end_obj_mA": "End obj (mA)",
        "no_of_images": "No. of images",
        "step": "Step",
        "exposure_time_s": "Exposure time (s)",
        "scan_command": "Scan command",
        "comments": "Comments",
        "date": "Date",
        "time": "Time",
    })

    # ---------------------- SAVE WITH FORMATTING ----------------------
    try:
        with pd.ExcelWriter(
            savelocation,
            engine="xlsxwriter",
            engine_kwargs={"options": {"nan_inf_to_errors": True}},
        ) as writer:

            workbook = writer.book
            worksheet = workbook.add_worksheet("Data")
            writer.sheets["Data"] = worksheet

            # ---- Formats ----
            header_format = workbook.add_format({
                "bold": True,
                "border": 1,
                "bg_color": "#D9E1F2"
            })

            date_banner_format = workbook.add_format({
                "bold": True,
                "font_size": 18,
                "font_color": "white",
                "bg_color": "#4472C4",
                "align": "center",
                "valign": "vcenter",
            })

            # Row formats
            leed = workbook.add_format({"bg_color": "#FFF2CC"})
            leed_bold = workbook.add_format({"bg_color": "#FFF2CC", "bold": True})

            leem = workbook.add_format({"bg_color": "#D9E1F2"})
            leem_bold = workbook.add_format({"bg_color": "#D9E1F2", "bold": True})

            laser = workbook.add_format({"bg_color": "#AFE4DE"})
            laser_bold = workbook.add_format({"bg_color": "#AFE4DE", "bold": True})

            default = workbook.add_format({})

            # Header
            for col_num, col_name in enumerate(df_out.columns):
                worksheet.write(0, col_num, col_name, header_format)
                worksheet.set_column(col_num, col_num, 18)

            worksheet.freeze_panes(1, 0)

            excel_row = 1
            prev_date = None
            n_cols = len(df_out.columns)

            cols = list(df_out.columns)
            tech_idx = cols.index("Technique")
            type_idx = cols.index("Image type")

            for _, row in df_out.iterrows():
                current_date = row.get("Date", "")

                if current_date and current_date != prev_date:
                    worksheet.merge_range(
                        excel_row, 0, excel_row, n_cols - 1,
                        f" {current_date}", date_banner_format
                    )
                    excel_row += 1
                    prev_date = current_date

                technique = str(row.iloc[tech_idx])
                image_type = str(row.iloc[type_idx]).lower()
                is_scan = ("scan" in image_type or "video" in image_type)

                if technique == "LEED":
                    fmt = leed_bold if is_scan else leed
                elif technique == "LEEM":
                    fmt = leem_bold if is_scan else leem
                elif technique == "LASERPEEM":
                    fmt = laser_bold if is_scan else laser
                else:
                    fmt = default

                for col_num, value in enumerate(row):
                    worksheet.write(excel_row, col_num, value, fmt)

                excel_row += 1

        print("✅ Saved Excel file!")

    except Exception as e:
        raise RuntimeError(f"Excel file may be open or locked.\n{e}")

    print(" Excel sheet produced by hardworking script goblins: ლ༼ ಥ 益 ಥ ༽ლ")