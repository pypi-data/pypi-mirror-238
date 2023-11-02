from load.irtrackextractor import IRTrackExtractor
import numpy as np
import json
import logging
from load.cliptrackextractor import ClipTrackExtractor, is_affected_by_ffc
import os.path
from ml_tools import tools
import argparse
from config.config import Config
import time
from load.clip import Clip


def process_file(config, filename):
    """
    Process a file extracting tracks and identifying them.
    :param filename: filename to process
    :param enable_preview: if true an MPEG preview file is created.
    """
    _, ext = os.path.splitext(filename)
    cache_to_disk = False
    if ext == ".cptv":
        track_extractor = ClipTrackExtractor(
            config.tracking, config.use_opt_flow, cache_to_disk
        )
        logging.info("Using clip extractor")

    elif ext in [".avi", ".mp4"]:
        track_extractor = IRTrackExtractor(config.tracking, cache_to_disk)
        logging.info("Using ir extractor")
    else:
        logging.error("Unknown extention %s", ext)
        return False
    base_filename = os.path.splitext(os.path.basename(filename))[0]
    meta_file = os.path.join(os.path.dirname(filename), base_filename + ".txt")
    if not os.path.exists(filename):
        logging.error("File %s not found.", filename)
        return False
    if not os.path.exists(meta_file):
        logging.error("File %s not found.", meta_file)
        return False
    meta_data = tools.load_clip_metadata(meta_file)

    logging.info("Processing file '{}'".format(filename))

    start = time.time()
    clip = Clip(track_extractor.config, filename)
    clip.load_metadata(
        meta_data,
        config.load.tag_precedence,
    )
    track_extractor.parse_clip(clip)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "source",
        help='a CPTV file to process, or a folder name, or "all" for all files within subdirectories of source folder.',
    )
    args = parser.parse_args()
    config = Config.load_from_file(None)

    process_file(config, args.source)


if __name__ == "__main__":
    main()
