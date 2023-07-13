import os
import cision

combined_csv = os.path.join(cision.OUTPUT_DIR, "combined_cision.csv")
cision.load_cision_files().pipe(cision.save_csv, combined_csv)