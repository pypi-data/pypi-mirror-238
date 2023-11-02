"""

Author Giampaolo Ferraro

Date December 2020

Some tools to evaluate a model

"""
import argparse
import logging
import pickle
import sys
import os
import json
import pickle
from config.config import Config
from ml_tools.kerasmodel import KerasModel
from ml_tools import tools
from ml_tools.trackdatabase import TrackDatabase
from ml_tools.dataset import Dataset
from pathlib import Path
from ml_tools.logs import init_logging
import cv2
import numpy as np


def load_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--config-file", help="Path to config file to use")

    args = parser.parse_args()
    return args


args = load_args()
init_logging()
config = Config.load_from_file(args.config_file)

base_dir = Path(config.tracks_folder)
db_file = base_dir / "dataset.hdf5"
dataset = Dataset(db_file, "dataset", config)
tracks_loaded, total_tracks = dataset.load_clips()
out_dir = Path("./bad-tracks")
out_dir.mkdir(exist_ok=True)
track_meta = {}
dataset.tracks = [t for t in dataset.tracks if t.clip_id == 40340]
for t in dataset.tracks:
    if t.label in ["false-positive", "insect"]:
        continue
    regions = t.regions_by_frame.values()
    masses = [r.mass for r in regions if r.mass > 0]
    std = np.std(masses)
    logging.info("%s %s - Mass is %s", t.track_id, len(masses), masses)
    lower_thresh = 0
    if len(masses) <= 20:
        lower_thresh = 0
    else:
        q = len(masses) // 2
        q = min(q, 25)
        lower_thresh = np.percentile(masses, q=q)
    logging.info(
        "%s LOwer thresh is %s from q %s std is %s", t.label, lower_thresh, q, std
    )
    lower_thresh = min(lower_thresh, std)
    if t.label == "rodent":
        lower_thresh = 0
    # elif t.label == "hedgehog":
    #    lower_thresh = min(lower_thresh,1000)
    logging.info("%s LOwer thresh is %s", t.label, lower_thresh)
    trailing_nothing = 0
    last_region = None
    bad_frames = []
    for region in reversed(regions):
        if region.mass > lower_thresh:
            # last_region = region
            bad_frames.append(region.frame_number)

            break
        trailing_nothing += 1
        bad_frames.append(region.frame_number)
    if trailing_nothing > 0:
        logging.info(
            "%s Have track %s ends at %s with %s trialing zeros should end at %s",
            t.label,
            t.unique_id,
            len(regions),
            trailing_nothing,
            region.frame_number,
        )
        clip_dir = out_dir / str(t.clip_id)
        clip_dir.mkdir(exist_ok=True)
        frames = dataset.db.get_track(
            str(t.clip_id), str(t.track_id), frame_numbers=bad_frames - t.start_frame
        )
        for f in frames[-2:]:
            cv2.imwrite(
                f"{clip_dir}/{t.label}-{t.track_id}-{f.frame_number}-{f.region.mass}.png",
                f.thermal,
            )
            track_meta[t.track_id] = {
                "rec_id": t.clip_id,
                "frame_end": int(region.frame_number),
            }
out = Path("./trackdata.json")
with out.open("w") as f:
    json.dump(track_meta, f)
# print("Havve track", t, mass_history)
