"""
i06-2 Labbook script
Adapted from Mike's i09 labbook code for offline i06-2 LEEM/LEED/LaserPEEM.
"""


# --- Technique & image/scan classification ---
#  - fov_a == 0 → LEED
#  - stv == 0 and no STV sweep → LASERPEEM
#  - otherwise → LEEM (default)
#  - STV/OBJ sweeps → treat as video/scan

# Row formats by technique:
#  - LEED rows = yellow
#  - LEEM rows = blue
#  - LASERPEEM rows = turquoise
#  (videos/scans in bold)


import h5py
import numpy as np
import pandas as pd
import os
import socket
import re

# ---------------------- PATH SETUP ---------------------- (Make sure hostname, datapaths are correct & with double \\)
hostname = socket.gethostname()

if hostname == "DESKTOP-FKQN57G":
    outDir = "C:\\Users\\nsf001\\OneDrive - The University of Nottingham(1)\\beamtime jan 26\\"
    inDir = 'C:\\Users\\nsf001\\The University of Nottingham(1)\\Surface Structure - Duncan - Beamtime data\\2026\\01_i09_Jan_AHHD_3mTerPP\\'
elif hostname == "LUIN82194":
    outDir = "C:\\Users\\pcxss14\\OneDrive - The University of Nottingham\\Desktop\\Attempt_code_for_LEEMtime\\Ailish_LEEMtime_March26\\mm42012-1\\"
    inDir = "C:\\Users\\pcxss14\\OneDrive - The University of Nottingham\\Desktop\\Attempt_code_for_LEEMtime\\Ailish_LEEMtime_March26\\mm42012-1\\"

dirname = inDir
savelocation = os.path.join(outDir, "i06_LEEM_Labbook_cc.xlsx")

# ---------------------- DATA EXTRACTION ----------------------
def extract_data_from_file(filepath):
    filename_only = os.path.basename(filepath)
    match = re.search(r"i06-2-(\d+)\.nxs", filename_only)
    file_number = match.group(1) if match else filename_only

    try:
        with h5py.File(filepath, "r") as f:
            print(f"🔹 Processing: {filename_only}")

            row = {
                "filename": file_number,
                "status": "OK",
            }

            # --- Date / Time from diamond_scan/start_time ---
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

            # --- Helper to get scalar ---
            def get_scalar(path):
                try:
                    v = f[path][()]
                    v = np.array(v).squeeze()
                    return float(v)
                except Exception:
                    return ""
                        
                # --- FOV and base stv/obj ---
            fov_a      = get_scalar("entry/instrument/leem/fov_a")
            stv_scalar = get_scalar("entry/instrument/leem/stv")
            obj_scalar = get_scalar("entry/instrument/leem/obj")
            
            # --- Sample position (fsm x/y) ---
            fsm_x = get_scalar("entry/instrument/ps/x")
            fsm_y = get_scalar("entry/instrument/ps/y")
        
            # --- Swept stv / obj arrays (if present) ---
            stv_start = stv_scalar
            stv_end   = stv_scalar
            obj_start = obj_scalar
            obj_end   = obj_scalar
        
            try:
                stv_vals = f["entry/instrument/leem_stv/value"][()]
                stv_vals = np.array(stv_vals).astype(float)
                if stv_vals.size > 0:
                    stv_start = float(stv_vals.min())
                    stv_end   = float(stv_vals.max())
            except Exception:
                pass
        
            try:
                obj_vals = f["entry/instrument/leem_obj/value"][()]
                obj_vals = np.array(obj_vals).astype(float)
                if obj_vals.size > 0:
                    obj_start = float(obj_vals.min())
                    obj_end   = float(obj_vals.max())
            except Exception:
                pass
        
            row["fov_um"]        = fov_a
            row["start_stv_V"]   = stv_start
            row["end_stv_V"]     = stv_end
            row["start_obj_mA"]  = obj_start
            row["end_obj_mA"]    = obj_end
            row["fsm_x"]         = fsm_x
            row["fsm_y"]         = fsm_y
            
            # --- Technique & image/scan classification ---
             # LASERPEEM: base STV is 0 and no STV sweep
            is_laserpeem = (stv_scalar == 0) and (stv_start == stv_end)
             
            if fov_a == 0:
                 technique = "LEED"
            elif is_laserpeem:
                 technique = "LASERPEEM"
            elif fov_a == 1:
                 technique = "LEEM"
            else:
                 technique = "LEEM"  # if in doubt, treat as LEEM
            
            has_stv_sweep = (stv_start != stv_end)
            has_obj_sweep = (obj_start != obj_end)
            has_sweep     = has_stv_sweep or has_obj_sweep
            
            if technique == "LEED":
                 if has_sweep:
                     image_type = "LEED scan (video)"
                 else:
                     image_type = "LEED image"
            elif technique == "LASERPEEM":
                 image_type = "PEEM image"
            else:  # LEEM
                 if has_sweep:
                     image_type = "LEEM scan (video)"
                 else:
                     image_type = "LEEM image"

            
           
            # --- Parse scan details into separate columns (robust) ---
            n_images  = ""
            step      = ""
            exposure  = ""

            parts = scan_command.split()
            if len(parts) >= 2 and parts[0] == "scan":
                scan_target = parts[1]
            else:
                scan_target = ""

            try:
                if scan_target == "ds":
                    start_val = float(parts[2])
                    stop_val  = float(parts[3])
                    step_val  = float(parts[4])
                    exp_val   = float(parts[-1])

                    n_imgs = int((stop_val - start_val) / step_val + 1)

                    n_images = n_imgs
                    step = step_val
                    exposure = exp_val

                elif scan_target == "t":
                    exp_val = float(parts[-1])
                    n_images = 1
                    step = ""
                    exposure = exp_val

                elif scan_target == "leem_stv":
                    stv_start_cmd = float(parts[2])
                    stv_stop_cmd  = float(parts[3])
                    stv_step_cmd  = float(parts[4])
                    exp_val       = float(parts[-1])

                    n_imgs = int((stv_stop_cmd - stv_start_cmd) / stv_step_cmd + 1)

                    n_images = n_imgs
                    step = stv_step_cmd
                    exposure = exp_val

                elif scan_target == "leem_obj":
                    obj_start_cmd = float(parts[2])
                    obj_stop_cmd  = float(parts[3])
                    obj_step_cmd  = float(parts[4])
                    exp_val       = float(parts[-1])

                    n_imgs = int((obj_stop_cmd - obj_start_cmd) / obj_step_cmd + 1)

                    n_images = n_imgs
                    step = obj_step_cmd
                    exposure = exp_val

            except Exception:
                pass

            row["technique"]         = technique
            row["image_type"]        = image_type
            row["no_of_images"]      = n_images
            row["step"]              = step
            row["exposure_time_s"]   = exposure

            print(
                f"✅ Extracted: {row['filename']} | Tech: {row['technique']} | "
                f"Type: {row['image_type']} | FOV: {row['fov_um']} | "
                f"stv {row['start_stv_V']}→{row['end_stv_V']} | "
                f"obj {row['start_obj_mA']}→{row['end_obj_mA']}"
            )
            return row

    except OSError as e:
        print(f"❌ Skipping unreadable file '{filepath}' — likely unfinished: {e}")
        row = {
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
        return row

# ---------------------- MAIN DATAFRAME CREATION ----------------------
rows = []
for filename in sorted(os.listdir(dirname)):
    if filename.endswith(".nxs"):
        full_path = os.path.join(dirname, filename)
        row = extract_data_from_file(full_path)
        if row:
            rows.append(row)

df = pd.DataFrame(rows)

# ---------------------- ADD COMMENTS COLUMN ----------------------
df["comments"] = ""

# ---------------------- COLUMN ORDER AND FILL ----------------------
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
df = df.reindex(columns=new_order)
df = df.fillna("")
print("✅ DataFrame creation complete, safe to proceed.")

# ---------------------- ROUND NUMERIC COLUMNS ----------------------
df_rounded = df.copy()

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
        df_rounded[col] = pd.to_numeric(df_rounded[col])
        if col == "exposure_time_s":
            df_rounded[col] = df_rounded[col].round(2)
        else:
            df_rounded[col] = df_rounded[col].round(1)
    except Exception:
        pass

df_rounded = df_rounded.fillna("")

# ---------------------- PRETTY HEADERS FOR EXCEL ----------------------
df_out = df_rounded.rename(columns={
    "filename":        "Filename",
    "technique":       "Technique",
    "image_type":      "Image type",
    "fov_um":          "FOV (µm)",
    "fsm_x":           "X-coordinate (on sample) ",   #incase of surface mapping
    "fsm_y":           "Y-coordinate (on sample)",   #incase of surface mapping
    "start_stv_V":     "Start stv (V)",
    "end_stv_V":       "End stv (V)",
    "start_obj_mA":    "Start obj (mA)",
    "end_obj_mA":      "End obj (mA)",
    "no_of_images":    "No. of images",
    "step":            "Step",
    "exposure_time_s": "Exposure time (s)",
    "scan_command":    "Scan command",
    "comments":        "Comments",
    "date":            "Date",
    "time":            "Time",
})

# ---------------------- SAVE WITH DATE BANNERS (xlsxwriter) ----------------------
try:
    with pd.ExcelWriter(
        savelocation,
        engine="xlsxwriter",
        engine_kwargs={"options": {"nan_inf_to_errors": True}},
    ) as writer:
        workbook  = writer.book
        worksheet = workbook.add_worksheet("Data")
        writer.sheets["Data"] = worksheet

        # ---- Formats ----
        header_format = workbook.add_format(
            {
                "bold": True,
                "border": 1,
                "bg_color": "#D9E1F2",
                "align": "left",
                "valign": "vcenter",
            }
        )
        date_banner_format = workbook.add_format(
            {
                "bold": True,
                "font_size": 18,
                "font_color": "white",
                "bg_color": "#4472C4",  # darker blue
                "align": "center",
                "valign": "vcenter",
            }
        )


        # Row formats: LEED (yellow), LEEM (blue), LASERPEEM (turqoise), with/without bold
        leed_format = workbook.add_format({
            "bold": False,
            "bg_color": "#FFF2CC",
            "align": "left",
        })
        leed_bold_format = workbook.add_format({
            "bold": True,
            "bg_color": "#FFF2CC",
            "align": "left",
        })
        leem_format = workbook.add_format({
            "bold": False,
            "bg_color": "#D9E1F2",
            "align": "left",
        })
        leem_bold_format = workbook.add_format({
            "bold": True,
            "bg_color": "#D9E1F2",
            "align": "left",
        })
        # NEW: LASERPEEM formats 
        laserpeem_format = workbook.add_format({
            "bold": False,
            "bg_color": "#AFE4DE",  # turquoise
            "align": "left",
        })
        laserpeem_bold_format = workbook.add_format({
            "bold": True,
            "bg_color": "#AFE4DE",  
            "align": "left",
        })
        default_format = workbook.add_format({
            "bold": False,
            "align": "left",
        })

        
        # ---- Write header row ----
        for col_num, col_name in enumerate(df_out.columns):
            worksheet.write(0, col_num, col_name, header_format)
            worksheet.set_column(col_num, col_num, 18)

        # Freeze header row
        worksheet.freeze_panes(1, 0)

        excel_row = 1
        prev_date = None
        n_cols = len(df_out.columns)

        # Locate columns once
        cols_list = list(df_out.columns)
        image_type_col = cols_list.index("Image type")
        technique_col  = cols_list.index("Technique")

        for _, row in df_out.iterrows():
            current_date = row.get("Date", "")

            # Insert date banner when date changes
            if current_date and current_date != prev_date:
                worksheet.merge_range(
                    excel_row,
                    0,
                    excel_row,
                    n_cols - 1,
                    f" {current_date}",
                    date_banner_format,
                )
                worksheet.set_row(excel_row, 36)
                excel_row += 1
                prev_date = current_date

            # Determine row format: technique + bold if video/scan
           
            technique_val  = str(row.iloc[technique_col]).strip()
            image_type_val = str(row.iloc[image_type_col]).strip().lower()
            
            is_video_or_scan = ("video" in image_type_val or "scan" in image_type_val)
            
            if technique_val == "LEED":
                row_format = leed_bold_format if is_video_or_scan else leed_format
            elif technique_val == "LEEM":
                row_format = leem_bold_format if is_video_or_scan else leem_format
            elif technique_val == "LASERPEEM":  # NEW
                row_format = laserpeem_bold_format if is_video_or_scan else laserpeem_format
            else:
                row_format = default_format

            
            worksheet.set_row(excel_row, None)

            # Write all cells with the row format
            for col_num, value in enumerate(row):
               if col_num < n_cols:
                   worksheet.write(excel_row, col_num, value, row_format)

            excel_row += 1

    print("✅ Saved Excel file!")

except Exception as e:
    print("⚠️ Excel file may be open or locked.")
    print(e)

print(" Excel sheet produced by hardworking script goblins: ლ༼ ಥ 益 ಥ ༽ლ")
