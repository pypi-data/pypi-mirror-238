from ml_tools.logs import init_logging
from config.config import Config
import numpy as np
import matplotlib.pyplot as plt
import threading
import math
from ml_tools.trackdatabase import TrackDatabase, special_datasets
import os
from PIL import Image, ImageDraw, ImageFont
import matplotlib as mpl
from ml_tools.datasetstructures import TrackHeader
from ml_tools.kerasmodel import KerasModel
from ml_tools.preprocess import preprocess_movement, preprocess_ir
from classify.trackprediction import TrackPrediction
import cv2

mpl.rcParams["figure.raise_window"] = False

# mpl.use("Agg")
labels = [
    "possum",
    "bird",
    "hedgehog",
    "cat",
    "false-positive",
    "nothing",
    "unknown",
    "part",
]

SKIP_TRACK = 9
SKIP_CLIP = 10
ALL_FP = 0
FP_ANIMAL = "f"
NOTHING_ANIMAL = "z"


clip_tag = None
track_tag = None
i_choice = None
skip_confirmed = True
label = None
# 2"possum"

import argparse


class Line:
    def __init__(self, m, c):
        self.m = m
        self.c = c

    def is_below(self, point):
        return not self.is_above(point)

    def is_above(self, point):
        y_value = self.y_res(point[0])
        if point[1] > y_value:
            return True
        return False

    def is_left(self, point):
        x_value = self.x_res(point[1])
        if point[0] < x_value:
            return True
        return False

    def is_right(self, point):
        return not self.is_left(point)

    def y_res(self, x):
        return x * self.m + self.c

    def x_res(self, y):
        return (y - self.c) / self.m
        # return x * self.m + self.c


# 0, 180
# -> 180,410
m = 1.28
LEFT_BOTTOM = Line(1.28, 180)
# LEFT_BOTTOM = Line(5 / 14, 160)


# 640, 218
# 475, 415
m = (415 - 218) / 475 - 640
m = -1.2
RIGHT_BOTTOM = Line(-1.2, 979)
# y = mx + c
print("RIGHT BOTTOM", RIGHT_BOTTOM.x_res(415))

# y=-21/16x+1030
# BACK_TOP = Line(0, 245)
# BACK_BOTTOM = Line(0, 230)

LEFT = 1
BOTTOM = 2
RIGHT = 4
TOP = 8
MIDDLE = 16


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-m",
        "--model",
        help="Path to model file to use, will override config model",
    )
    parser.add_argument("-w", "--weights", help="Weights to load into model")

    args = parser.parse_args()
    return args


def show_trap_info(image):
    image = cv2.resize(image, (640, 480))
    print("image is", image.shape)
    in_trap = False
    wait = 100
    start = (0, 480 - int(LEFT_BOTTOM.y_res(0)))
    end = (int(LEFT_BOTTOM.x_res(480)), 0)
    image = cv2.line(image, start, end, (0, 255, 0), 10)
    # start = (640, 480 - int(RIGHT_BOTTOM.y_res(475)))
    start = (int(RIGHT_BOTTOM.x_res(480)), 0)
    print(start)
    end = (int(RIGHT_BOTTOM.x_res(0)), 480)
    print(end)
    image = cv2.line(image, start, end, (0, 255, 0), 10)
    cv2.imshow("i", image)
    cv2.waitKey()


def main():
    init_logging()
    args = parse_args()
    img = cv2.imread("/home/gp/Downloads/newtrap.png", 0)
    show_trap_info(img)
    retur
    config = Config.load_from_file(None)
    db_file = os.path.join(config.tracks_folder, "dataset.hdf5")
    model = None
    if args.model is not None:
        model = KerasModel()
        model.load_model(args.model, training=False, weights=args.weights)

    db = TrackDatabase(db_file)
    ids = db.get_all_clip_ids(label=label)
    trigger_trap(db, ids, model)


def trigger_trap(db, clip_ids, model):
    missed = []
    false_trigger = []
    correct_triggers = []
    total = 0
    total_animals = 0
    fps_skipped = 0
    animals_skipped = []
    total = 0
    for clip_id, track_ids in clip_ids.items():
        total += len(track_ids)
        continue
        clip_meta = db.get_clip_meta(clip_id)
        tracks = []
        # if clip_id != "110":
        # continue
        for track_id in track_ids:
            if track_id in special_datasets:
                continue

            track_meta = db.get_track_meta(clip_id, track_id)
            track = TrackHeader.from_meta(clip_id, clip_meta, track_meta)
            tracks.append(track)
        tracks = sorted(tracks, key=lambda x: x.start_frame)
        triggers = []
        remove = []

        for track in tracks:
            direction = 0
            frame_keys = list(track.regions_by_frame.keys())
            frame_keys.sort()
            animal = track.label in ["cat", "possum", "hedgehog"]
            hasregions = False
            frames = db.get_track(clip_id, track.track_id, original=False)

            track_prediction = TrackPrediction(track.track_id, model.labels)
            for i, frame in enumerate(frame_keys):
                region = track.regions_by_frame[frame]
                if region.bottom < 200:
                    break
                if direction == 0:
                    if region.left < 100:
                        direction |= LEFT
                    if region.right > (640 - 100):
                        direction |= RIGHT
                    if region.bottom > (480 - 100):
                        direction |= BOTTOM
                    if direction == 0:
                        if region.bottom < 300:
                            direction |= TOP
                        else:
                            direction = MIDDLE
                    # print(
                    #     "Track direction is", direction, region, clip_id, track.track_id
                    # )
                prediction = predict_frame(model, frames[i])
                track_prediction.classified_frame(frame, prediction, 1)
                track_prediction.normalize_score()
                predicted_tag = track_prediction.predicted_tag()
                score = track_prediction.max_score
                if predicted_tag == "false-positive" and score > 0.8:
                    print("skipping fp", track.track_id)
                    # if i > 2 or i == len(frame_keys) - 1:
                    #     print("done with", track.track_id)
                    #     fps_skipped += 1
                    #     if animal:
                    #         animals_skipped.append(f"{clip_id}-{track.track_id}")
                    #     break
                    continue
                print(
                    "is a ",
                    track.label,
                    " prediction is ",
                    predicted_tag,
                    score,
                    track.track_id,
                )
                p = (region.right, 480 - region.bottom)
                inside = (
                    LEFT_BOTTOM.is_below(p)
                    and LEFT_BOTTOM.is_right(p)
                    # or IRTrackExtractor.RIGHT_BOTTOM.is_above(region)
                    # or IRTrackExtractor.BACK_BOTTOM.is_above(region)
                )
                p = (region.left, 480 - region.bottom)
                inside = inside and (
                    RIGHT_BOTTOM.is_below(p) and RIGHT_BOTTOM.is_left(p)
                )
                p = (region.left, 480 - region.bottom)

                # inside = inside and (BACK_BOTTOM.is_below(p))

                if not inside:
                    continue
                hasregions = True
                # print("checking region", region.right)
                if region.width < 60 or region.height < 40:
                    continue

                if direction & LEFT and region.left > 40:
                    triggers.append((track, region))
                    break

                elif direction & RIGHT and region.right < 580:
                    triggers.append((track, region))
                    break

                if direction & TOP and region.bottom > 300:
                    triggers.append((track, region))
                    break

                if direction & BOTTOM and region.bottom < 480 - 50:
                    triggers.append((track, region))
                    break

                if direction & MIDDLE and region.left > 40 and region.right < 580:
                    triggers.append((track, region))
                    break
            if not hasregions:
                remove.append(track)
        if predicted_tag == "false-positive" and score > 0.8 and animal:
            animals_skipped.append(f"{clip_id}-{track.track_id}")
        for t in remove:
            tracks.remove(t)
        labels = set([track.label for track in tracks])
        print(f"For {clip_id} have {len(triggers)} triggers labels are {labels}")
        animal = "cat" in labels or "possum" in labels or "hedgehog" in labels
        if len(labels) > 0:
            total += 1
            # print("total for", clip_id)
        if animal:
            total_animals += 1
        if animal and len(triggers) == 0:
            print(f"Missing trigger {clip_id}")
            missed.append(clip_id)
        # if not animal and len(triggers) > 1:
        # print(f"Shouldnt have triggers but do {clip_id} ")
        # false_trigger.append(clip_id)

        triggered = False
        for track, region in triggers:
            animal = track.label in ["cat", "possum", "hedgehog"]
            if not animal and not triggered:
                false_trigger.append(f"{clip_id}-{track.track_id}")
            if animal and not triggered:
                correct_triggers.append(track.clip_id)
            triggered = True
            print(
                f"Trigger for {track.clip_id} - {track.track_id} on region {region} frame {region.frame_number} with tag {track.label}"
            )
    print("total is", total)
    print("missg triggers", len(missed), missed)
    print("false triggers", len(false_trigger), false_trigger)
    print("correct_triggers triggers", len(correct_triggers), correct_triggers)
    print("fpps skipped", fps_skipped)
    print("animals skipped", len(animals_skipped), animals_skipped)

    print("total animals", total_animals, " total ", total)


def predict_track(model, track, frames):
    output = []
    for f in frames:
        res = predict_frame(model, frames)
        if res is None:
            continue

    track_prediction = TrackPrediction(track.track_id, model.labels)

    track_prediction.classified_clip(output, output, None)
    track_prediction.normalize_score()
    print(
        track_prediction.predicted_tag(),
        track_prediction.max_score,
        " vs ",
        track.label,
    )
    return track_prediction


def predict_frame(model, f):
    if f.region.blank:
        return None
    if f.region.width == 0 or f.region.height == 0:
        logging.warn("No width or height for frame %s", f.region.frame_number)
        return None

    preprocessed = preprocess_ir(
        f.copy(),
        (
            # 150,
            # 150
            model.params.frame_size,
            model.params.frame_size,
        ),
        False,
        f.region,
        model.preprocess_fn,
    )

    preprocessed = np.float32(preprocessed)
    output = model.model.predict(preprocessed[np.newaxis, :])
    return output


if __name__ == "__main__":
    main()

    # frames = db.get_track(clip_id, tracks[0].track_id, original=True)
    # image = np.uint8(frames[0].thermal)
    # import cv2
    #
    # start = (0, 480 - int(LEFT_BOTTOM.y_res(0)))
    #
    # end = (140, 480 - int(LEFT_BOTTOM.y_res(140)))
    # print("start ", start, " to ", end)
    # cv2.line(image, start, end, (100, 100, 100), 9)
    #
    # start = (615, 480 - int(RIGHT_BOTTOM.y_res(615)))
    #
    # end = (460, 480 - int(RIGHT_BOTTOM.y_res(460)))
    # print("start ", start, " to ", end)
    # cv2.line(image, start, end, (100, 100, 100), 9)
    #
    # cv2.imshow("first", image)
    # cv2.waitKey(1000)
