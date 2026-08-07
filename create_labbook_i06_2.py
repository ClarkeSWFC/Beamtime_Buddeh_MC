def create_labbook_i06_2(inDir, outDir, progress_callback=None):
    """
    Generate an i06-2 LEEM/LEED/LaserPEEM labbook.

    Parameters
    ----------
    inDir : str
        Folder containing .nxs files.
    outDir : str
        Folder to save the Excel labbook.
    progress_callback : callable, optional
        Function taking a string argument for GUI progress updates.
    """

    import os
    import re
    import h5py
    import numpy as np
    import pandas as pd

    dirname = inDir
    savelocation = os.path.join(outDir, "i06_LEEM_Labbook.xlsx")

    file_list = sorted([f for f in os.listdir(dirname) if f.endswith(".nxs")])

    # ------------------------------------------------------------------
    # DATA EXTRACTION
    # ------------------------------------------------------------------

    def extract_data_from_file(filepath):

        filename_only = os.path.basename(filepath)
        match = re.search(r"i06-2-(\d+)\.nxs", filename_only)
        file_number = match.group(1) if match else filename_only

        try:
            with h5py.File(filepath, "r") as f:

                msg = f"🔹 Processing: {filename_only}"
                print(msg)
                if progress_callback:
                    progress_callback(msg)

                row = {
                    "filename": file_number,
                    "status": "OK",
                }

                # ---------------- Date / Time ----------------

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

                # ---------------- Scan command ----------------

                try:
                    scan_command = f["entry/diamond_scan/scan_command"][()]
                    if isinstance(scan_command, bytes):
                        scan_command = scan_command.decode("utf-8")
                    scan_command = str(scan_command)
                except Exception:
                    scan_command = ""

                row["scan_command"] = scan_command

                # ---------------- Helper ----------------

                def get_scalar(path):
                    try:
                        value = f[path][()]
                        value = np.array(value).squeeze()
                        return float(value)
                    except Exception:
                        return ""

                # ---------------- Scalars ----------------

                fov_a = get_scalar("entry/instrument/leem/fov_a")
                stv_scalar = get_scalar("entry/instrument/leem/stv")
                obj_scalar = get_scalar("entry/instrument/leem/obj")

                fsm_x = get_scalar("entry/instrument/ps/x")
                fsm_y = get_scalar("entry/instrument/ps/y")

                stv_start = stv_scalar
                stv_end = stv_scalar
                obj_start = obj_scalar
                obj_end = obj_scalar

                try:
                    stv_vals = np.array(
                        f["entry/instrument/leem_stv/value"][()]
                    ).astype(float)

                    if stv_vals.size > 0:
                        stv_start = float(stv_vals.min())
                        stv_end = float(stv_vals.max())

                except Exception:
                    pass

                try:
                    obj_vals = np.array(
                        f["entry/instrument/leem_obj/value"][()]
                    ).astype(float)

                    if obj_vals.size > 0:
                        obj_start = float(obj_vals.min())
                        obj_end = float(obj_vals.max())

                except Exception:
                    pass

                row.update(
                    {
                        "fov_um": fov_a,
                        "fsm_x": fsm_x,
                        "fsm_y": fsm_y,
                        "start_stv_V": stv_start,
                        "end_stv_V": stv_end,
                        "start_obj_mA": obj_start,
                        "end_obj_mA": obj_end,
                    }
                )

                # ---------------- Classification ----------------

                is_laserpeem = (stv_scalar == 0) and (stv_start == stv_end)

                if fov_a == 0:
                    technique = "LEED"
                elif is_laserpeem:
                    technique = "LASERPEEM"
                elif fov_a == 1:
                    technique = "LEEM"
                else:
                    technique = "LEEM"

                has_stv_sweep = stv_start != stv_end
                has_obj_sweep = obj_start != obj_end
                has_sweep = has_stv_sweep or has_obj_sweep

                if technique == "LEED":
                    image_type = (
                        "LEED scan (video)"
                        if has_sweep
                        else "LEED image"
                    )

                elif technique == "LASERPEEM":
                    image_type = "PEEM image"

                else:
                    image_type = (
                        "LEEM scan (video)"
                        if has_sweep
                        else "LEEM image"
                    )

                # ---------------- Scan parsing ----------------

                n_images = ""
                step = ""
                exposure = ""

                parts = scan_command.split()

                if len(parts) >= 2 and parts[0] == "scan":
                    scan_target = parts[1]
                else:
                    scan_target = ""

                try:

                    if scan_target == "ds":

                        start_val = float(parts[2])
                        stop_val = float(parts[3])
                        step_val = float(parts[4])
                        exp_val = float(parts[-1])

                        n_images = int(
                            (stop_val - start_val) / step_val + 1
                        )

                        step = step_val
                        exposure = exp_val

                    elif scan_target == "t":

                        n_images = 1
                        exposure = float(parts[-1])

                    elif scan_target == "leem_stv":

                        start_val = float(parts[2])
                        stop_val = float(parts[3])
                        step_val = float(parts[4])
                        exp_val = float(parts[-1])

                        n_images = int(
                            (stop_val - start_val) / step_val + 1
                        )

                        step = step_val
                        exposure = exp_val

                    elif scan_target == "leem_obj":

                        start_val = float(parts[2])
                        stop_val = float(parts[3])
                        step_val = float(parts[4])
                        exp_val = float(parts[-1])

                        n_images = int(
                            (stop_val - start_val) / step_val + 1
                        )

                        step = step_val
                        exposure = exp_val

                except Exception:
                    pass

                row.update(
                    {
                        "technique": technique,
                        "image_type": image_type,
                        "no_of_images": n_images,
                        "step": step,
                        "exposure_time_s": exposure,
                    }
                )

                msg = (
                    f"✅ Extracted: {file_number} | "
                    f"{technique} | {image_type}"
                )

                print(msg)

                if progress_callback:
                    progress_callback(msg)

                return row

        except OSError:

            msg = f"❌ Skipping unreadable file: {filename_only}"

            print(msg)

            if progress_callback:
                progress_callback(msg)

            return {
                "filename": file_number,
                "status": "File unreadable",
                "date": "",
                "time": "",
                "scan_command": "",
                "fov_um": "",
                "fsm_x": "",
                "fsm_y": "",
                "start_stv_V": "",
                "end_stv_V": "",
                "start_obj_mA": "",
                "end_obj_mA": "",
                "technique": "buggered measurement",
                "image_type": "",
                "no_of_images": "",
                "step": "",
                "exposure_time_s": "",
            }

    # ------------------------------------------------------------------
    # BUILD DATAFRAME
    # ------------------------------------------------------------------

    rows = []

    for filename in file_list:
        row = extract_data_from_file(os.path.join(dirname, filename))
        if row:
            rows.append(row)

    df = pd.DataFrame(rows)
    # Convert date and time to a sortable datetime
    df["datetime"] = pd.to_datetime(
        df["date"] + " " + df["time"],
        errors="coerce"
    )

    # Sort chronologically
    df = df.sort_values("datetime")
    
    # Remove helper column
    df = df.drop(columns="datetime").reset_index(drop=True)
    df["comments"] = ""

    new_order = [
        "filename",
        "technique",
        "image_type",
        "fov_um",
        "fsm_x",
        "fsm_y",
        "start_stv_V",
        "end_stv_V",
        "start_obj_mA",
        "end_obj_mA",
        "no_of_images",
        "step",
        "exposure_time_s",
        "scan_command",
        "comments",
        "date",
        "time",
    ]

    df = df.reindex(columns=new_order).fillna("")

    # ------------------------------------------------------------------
    # ROUND NUMBERS
    # ------------------------------------------------------------------

    df_round = df.copy()

    for col in [
        "fov_um",
        "start_stv_V",
        "end_stv_V",
        "start_obj_mA",
        "end_obj_mA",
        "no_of_images",
        "step",
        "exposure_time_s",
    ]:

        try:
            df_round[col] = pd.to_numeric(df_round[col])

            if col == "exposure_time_s":
                df_round[col] = df_round[col].round(2)
            else:
                df_round[col] = df_round[col].round(1)

        except Exception:
            pass

    df_round = df_round.fillna("")

    # ------------------------------------------------------------------
    # HEADERS
    # ------------------------------------------------------------------

    df_out = df_round.rename(columns={
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

    # ------------------------------------------------------------------
    # WRITE EXCEL
    # ------------------------------------------------------------------

    try:

        with pd.ExcelWriter(
            savelocation,
            engine="xlsxwriter",
            engine_kwargs={"options": {"nan_inf_to_errors": True}},
        ) as writer:

            workbook = writer.book
            worksheet = workbook.add_worksheet("Data")
            writer.sheets["Data"] = worksheet

            header = workbook.add_format({
                "bold": True,
                "border": 1,
                "bg_color": "#D9E1F2",
                "align": "left",
                "valign": "vcenter",
            })

            banner = workbook.add_format({
                "bold": True,
                "font_size": 18,
                "font_color": "white",
                "bg_color": "#4472C4",
                "align": "center",
                "valign": "vcenter",
            })

            def fmt(colour, bold=False):
                return workbook.add_format({
                    "bg_color": colour,
                    "bold": bold,
                    "align": "left",
                })

            leed = fmt("#FFF2CC")
            leed_bold = fmt("#FFF2CC", True)

            leem = fmt("#D9E1F2")
            leem_bold = fmt("#D9E1F2", True)

            laser = fmt("#AFE4DE")
            laser_bold = fmt("#AFE4DE", True)

            default = workbook.add_format({"align": "left"})

            for c, name in enumerate(df_out.columns):
                worksheet.write(0, c, name, header)
                worksheet.set_column(c, c, 18)

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
                        excel_row,
                        0,
                        excel_row,
                        n_cols - 1,
                        f" {current_date}",
                        banner,
                    )

                    worksheet.set_row(excel_row, 36)

                    excel_row += 1
                    prev_date = current_date

                technique = str(row.iloc[tech_idx]).strip()
                image_type = str(row.iloc[type_idx]).lower()

                is_scan = ("scan" in image_type) or ("video" in image_type)

                if technique == "LEED":
                    row_fmt = leed_bold if is_scan else leed
                elif technique == "LEEM":
                    row_fmt = leem_bold if is_scan else leem
                elif technique == "LASERPEEM":
                    row_fmt = laser_bold if is_scan else laser
                else:
                    row_fmt = default

                worksheet.set_row(excel_row, None)

                for col, value in enumerate(row):
                    worksheet.write(excel_row, col, value, row_fmt)

                excel_row += 1

        print("✅ Saved Excel file!")

        if progress_callback:
            progress_callback("✅ Saved Excel file!")

    except Exception as e:
        raise RuntimeError(
            f"Excel file may be open or locked.\n{e}"
        )

    print("Excel sheet produced by hardworking script goblins: ლ༼ ಥ 益 ಥ ༽ლ")

    return savelocation