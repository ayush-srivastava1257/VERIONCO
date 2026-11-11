"""
Universal GDC WSI Downloader for Kaggle, Colab, and Local environments.

Can be run from command line:
    python download_wsi_batch.py --batch 1
Or directly imported / run inside a Kaggle / Jupyter cell:
    from download_wsi_batch import download_batch
    download_batch(batch=1)
"""

import os
import sys
import argparse
import urllib.request
import ssl
import hashlib
from pathlib import Path
import pandas as pd

def download_file(file_id, filename, expected_md5, output_path):
    url = f"https://api.gdc.cancer.gov/data/{file_id}"
    ctx = ssl.create_default_context()
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if output_path.exists():
        # verify md5
        h = hashlib.md5()
        with open(output_path, "rb") as f:
            while chunk := f.read(1024 * 1024):
                h.update(chunk)
        if h.hexdigest().lower() == str(expected_md5).lower():
            print(f"  [EXISTS & VERIFIED] {filename}")
            return True
        else:
            print(f"  [CORRUPTED - REDOWNLOADING] {filename}")
            try:
                output_path.unlink()
            except Exception:
                pass

    temp_path = output_path.with_suffix(".tmp")
    h = hashlib.md5()
    try:
        with urllib.request.urlopen(url, context=ctx) as response, open(temp_path, "wb") as out_file:
            while chunk := response.read(2 * 1024 * 1024):
                h.update(chunk)
                out_file.write(chunk)
        
        if h.hexdigest().lower() != str(expected_md5).lower():
            print(f"  [ERROR: MD5 MISMATCH] {filename}")
            temp_path.unlink()
            return False
            
        if temp_path.exists():
            temp_path.rename(output_path)
        print(f"  [DOWNLOADED] {filename}")
        return True
    except Exception as e:
        print(f"  [FAILED] {filename}: {e}")
        if temp_path.exists():
            try:
                temp_path.unlink()
            except Exception:
                pass
        return False

def find_manifest_path(batch_num=1, custom_path=None):
    if custom_path and Path(custom_path).exists():
        return Path(custom_path)
    
    candidates = [
        Path(f"manifest_batch_{batch_num}.csv"),
        Path(f"gdc_manifest_batch_{batch_num}.txt"),
        Path(f"data/manifests/manifest_batch_{batch_num}.csv"),
        Path(f"data/manifests/gdc_manifest_batch_{batch_num}.txt"),
        Path("manifest_annotated.csv"),
        Path("data/manifests/manifest_annotated.csv"),
    ]
    
    # Check current script directory if available
    if "__file__" in globals():
        script_dir = Path(__file__).resolve().parent
        candidates.extend([
            script_dir / f"manifest_batch_{batch_num}.csv",
            script_dir / f"gdc_manifest_batch_{batch_num}.txt",
        ])

    for c in candidates:
        if c and c.exists():
            return c

    # Search Kaggle input datasets recursively
    kaggle_input = Path("/kaggle/input")
    if kaggle_input.exists():
        patterns = [
            f"*manifest*batch_{batch_num}*.csv",
            f"*manifest*batch_{batch_num}*.txt",
            f"*batch_{batch_num}*.csv",
            f"*batch_{batch_num}*.txt",
            "*manifest*.csv",
            "*manifest*.txt",
        ]
        for pat in patterns:
            hits = list(kaggle_input.rglob(pat))
            if hits:
                return hits[0]

    return None

def download_batch(batch=1, manifest=None, output_dir=None, max_slides=0):
    """
    Main function callable directly inside Kaggle/Colab/Jupyter notebooks.
    """
    if output_dir is None:
        if Path("/kaggle").exists():
            output_dir = "/kaggle/working/gdc_wsi_download"
        else:
            output_dir = "./gdc_wsi_download"
            
    manifest_path = find_manifest_path(batch_num=batch, custom_path=manifest)

    if not manifest_path or not manifest_path.exists():
        print(f"Error: manifest for batch {batch} not found.")
        print("Searched current directory, data/manifests, and /kaggle/input/.")
        print("Please pass the exact manifest path: download_batch(manifest='/path/to/manifest.csv')")
        return False

    print(f"Loading manifest: {manifest_path}")
    if manifest_path.suffix == ".csv":
        df = pd.read_csv(manifest_path)
        id_col = "file_id" if "file_id" in df.columns else ("id" if "id" in df.columns else df.columns[0])
        fn_col = "filename" if "filename" in df.columns else ("file_name" if "file_name" in df.columns else df.columns[1])
        md5_col = "md5_expected" if "md5_expected" in df.columns else ("md5" if "md5" in df.columns else ("md5sum" if "md5sum" in df.columns else df.columns[2]))
    else:
        df = pd.read_csv(manifest_path, sep="\t")
        id_col = "id" if "id" in df.columns else df.columns[0]
        fn_col = "filename" if "filename" in df.columns else df.columns[1]
        md5_col = "md5" if "md5" in df.columns else df.columns[2]

    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if max_slides > 0:
        df = df.head(max_slides)

    print(f"Downloading {len(df)} slides to {out_dir}...")
    success = 0
    for idx, row in df.iterrows():
        print(f"[{idx+1}/{len(df)}] {row[fn_col]} ({row[id_col]})")
        # GDC standard hierarchy: out_dir / file_id / filename
        target_path = out_dir / str(row[id_col]) / str(row[fn_col])
        if download_file(row[id_col], row[fn_col], row[md5_col], target_path):
            success += 1

    print(f"\n==================================================")
    print(f"Download complete: {success}/{len(df)} slides in {out_dir}")
    print(f"==================================================")
    return True

def main():
    parser = argparse.ArgumentParser(description="Download TCGA-LUAD WSI batch from GDC")
    parser.add_argument("--batch", type=int, default=1, help="Batch number (1 to 7)")
    parser.add_argument("--manifest", type=str, default="", help="Path to manifest file")
    parser.add_argument("--output_dir", type=str, default="", help="Directory to save downloaded WSIs")
    parser.add_argument("--max_slides", type=int, default=0, help="Optional limit on number of slides to download")
    
    # parse_known_args prevents crashing inside Jupyter/Colab when kernel -f argument is passed!
    args, unknown = parser.parse_known_args()
    
    out_dir = args.output_dir if args.output_dir else None
    manifest = args.manifest if args.manifest else None
    
    download_batch(
        batch=args.batch,
        manifest=manifest,
        output_dir=out_dir,
        max_slides=args.max_slides
    )

if __name__ == "__main__":
    main()
