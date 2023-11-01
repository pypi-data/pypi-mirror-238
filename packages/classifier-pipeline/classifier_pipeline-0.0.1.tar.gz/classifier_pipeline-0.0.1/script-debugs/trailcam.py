import argparse
import os
import logging
from datetime import datetime
import math
from track.trackextractor import TrackExtractor
from ml_tools.logs import init_logging
from ml_tools.tools import Rectangle
from config.config import Config
from config.classifyconfig import ModelConfig
from load.irtrackextractor import Background, get_diff_back_filtered
import cv2
import numpy as np
from ml_tools.imageprocessing import (
    detect_objects,
    normalize,
    detect_objects_ir,
    theshold_saliency,
    detect_objects_both,
    resize_and_pad,
)
from pathlib import Path
from track.region import Region
from ml_tools.kerasmodel import KerasModel
import tensorflow as tf
from ml_tools.preprocess import preprocess_movement, preprocess_ir


# merge all regions that the midpoint is within the max(width,height) from the midpoint of another region
# keep merging until no more merges are possible, tihs works paticularly well from the IR videos where
# the filtered image is quite fragmented
def merge_components(rectangles):
    min_mass = 10
    min_size = 10
    min_mass_percent = 0.1
    rectangles = [
        r
        for r in rectangles
        if r[4] > min_mass or (r[2] > min_size and r[3] > min_size)
    ]

    # rectangles = [r for r in rectangles if r[4] / (r[2] * r[3]) > min_mass_percent]
    # filter out regions with small mass  and samll width / height
    #  numbers may need adjusting
    rectangles = sorted(rectangles, key=lambda s: s[4], reverse=False)
    MAX_GAP = 20
    rect_i = 0
    rectangles = list(rectangles)
    outer_loops = 0
    while rect_i < len(rectangles):
        outer_loops += 1
        rect = rectangles[rect_i]
        merged = False
        mid_x = rect[2] / 2.0 + rect[0]
        mid_y = rect[3] / 2.0 + rect[1]
        index = 0
        while index < len(rectangles):
            r_2 = rectangles[index]
            if r_2[0] == rect[0]:
                index += 1
                continue
            r_mid_x = r_2[2] / 2.0 + r_2[0]
            r_mid_y = r_2[3] / 2.0 + r_2[1]
            distance = (mid_x - r_mid_x) ** 2 + (r_mid_y - mid_y) ** 2
            distance = distance**0.5

            # widest = max(rect[2], rect[3])
            # hack short cut just take line from mid points as shortest distance subtract biggest width or hieght from each
            distance = (
                distance - max(rect[2], rect[3]) / 2.0 - max(r_2[2], r_2[3]) / 2.0
            )
            within = r_2[0] > rect[0] and (r_2[0] + r_2[2]) <= (rect[0] + rect[2])
            within = (
                within and r_2[1] > rect[1] and (r_2[1] + r_2[3]) <= (rect[1] + rect[3])
            )

            if distance < MAX_GAP and not within:
                cur_right = rect[0] + rect[2]
                cur_bottom = rect[0] + rect[2]

                rect[0] = min(rect[0], r_2[0])
                rect[1] = min(rect[1], r_2[1])
                rect[2] = max(cur_right, r_2[0] + r_2[2])
                rect[3] = max(rect[1] + rect[3], r_2[1] + r_2[3])
                rect[2] -= rect[0]
                rect[3] -= rect[1]
                rect[4] += r_2[4]

                # print("second merged ", rect)
                merged = True
                # break
                del rectangles[index]
            else:
                index += 1
                # print("not mered", rect, r_2, distance)
        # if merged:
        #     rect_i = 0
        # else:
        rect_i += 1
    # rectangles = [r for r in rectangles if r[4] / (r[2] * r[3]) > min_mass_percent]

    return rectangles


def save_background_stills(source, background_file):
    background = Background()
    # for f in os.listdir(str(source)1):
    images = list(source.glob("./*.JPG"))
    i = 0
    medians = []
    for img_file in images:
        print("loading", img_file)
        still = cv2.imread(str(img_file))
        gray = cv2.cvtColor(still, cv2.COLOR_BGR2GRAY)
        gray = gray[:-100, :-100]
        new_shape = np.uint16([gray.shape[1] * 0.2, gray.shape[0] * 0.2])
        smaller = cv2.resize(gray, new_shape)

        print("max is", np.amax(gray), "min", np.amin(gray), np.median(gray))
        medians.append(np.median(gray))
    min_median = np.amin(np.array(medians))
    print("min median is", min_median)
    # min_median = 74
    for img_file in images:
        print("loading", img_file)
        still = cv2.imread(str(img_file))
        gray = cv2.cvtColor(still, cv2.COLOR_BGR2GRAY)
        gray = gray[:-100, :-100]
        new_shape = np.uint16([gray.shape[1] * 0.2, gray.shape[0] * 0.2])
        this_median = np.median(gray)
        min_diff = this_median - min_median

        print("shift pixels by", min_diff)
        gray = gray - min_diff
        gray[gray < 0] = 0
        smaller = cv2.resize(gray, new_shape)
        # cv2.imshow("s", smaller)
        # cv2.moveWindow("s", 0, 0)
        # cv2.waitKey(100)
        if i == 0:
            background.set_background(gray, 1)
        else:
            background._background += gray
            background.frames += 1
            # break
        i += 1

    for img_file in images:
        still = cv2.imread(str(img_file))
        gray = cv2.cvtColor(still, cv2.COLOR_BGR2GRAY)
        gray = gray[:-100, :-100]
        min_diff = this_median - min_median

        print("shift pixels by", min_diff)
        gray = gray - min_diff
        gray[gray < 0] = 0
        filtered = get_diff_back_filtered(
            background.background,
            gray,
            20,
        )
        background.update_background(gray, filtered)

        smaller = cv2.resize(filtered, new_shape)

        cv2.imshow("s", smaller)
        cv2.moveWindow("s", 0, 0)
        cv2.waitKey(100)
    # vidcap.release()
    # 1 / 0
    # background, stats = normalize(background.background, new_max=255)

    print("saving background too ", background_file)
    cv2.imwrite(str(background_file), np.uint8(background.background))
    return background.background


def save_background(source, background_file):
    background = Background()
    vidcap = cv2.VideoCapture(str(source))
    i = 0
    while True:
        success, image = vidcap.read()
        if not success:
            break
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = gray[:-100, :-100]
        if i < 10:
            i += 1
            continue
        if i == 10:
            background.set_background(gray, 1)

        else:
            background._background += gray
            background.frames += 1
            # break
        i += 1
    vidcap.release()
    print("saving background too ", background_file)
    cv2.imwrite(str(background_file), background.background)
    return background.background

    # background = cv2.GaussianBlur(background, (15,15), 0)
    # cv2.imshow("background", np.uint8(background))
    # cv2.moveWindow("background", 0, 0)
    # cv2.waitKey(100)


def detect_images(source, background, model):
    images = list(source.glob("./*.JPG"))
    images.sort()
    new_shape = np.uint16([background.shape[1] * 0.2, background.shape[0] * 0.2])

    i = 0

    prev = None
    prev_name = None
    for img_file in images:
        # print(img_file.name)
        # if img_file.name != "Z-IMAG0010.JPG" and img_file.name != "IMAG0065.JPG"  and img_file.name != "IMAG0039.JPG":
        # continue

        print("loading", img_file, " comparing to", prev_name)
        still = cv2.imread(str(img_file))
        gray = cv2.cvtColor(still, cv2.COLOR_BGR2GRAY)
        gray = gray[:-100, :-100]
        # fgMask = backSub.apply(gray)
        if prev is None:
            prev = gray.copy()
            prev_name = img_file
            continue
        # gray = gray[1500:, 0:1500]
        # background = background[1500:, 0:1500]
        # new_shape = np.uint16([background.shape[1] * 0.2, background.shape[0] * 0.2])
        backSub = cv2.createBackgroundSubtractorMOG2()
        fgMask = backSub.apply(prev)
        fgMask = backSub.apply(gray)

        smaller_b = cv2.resize(np.uint8(fgMask), new_shape)

        cv2.imshow("background", np.uint8(smaller_b))
        cv2.moveWindow("background", 0, 0)
        cv2.waitKey(100)
        # prev = gray.copy()
        # continue
        # gray = np.uint8(gray)

        prev_m = np.median(prev)
        # prev[prev > 200] =prev_m
        gray_median = np.median(gray)
        filtered = get_diff_back_filtered(
            prev,
            gray,
            np.abs(prev_m - gray_median),
        )

        filtered[gray > 200] = 0
        filtered, stats = normalize(filtered, new_max=255)

        num, mask, component_details, threshed = theshold_saliency(
            fgMask, threshold=0, otsus=True
        )
        print("components??", len(component_details))
        component_details = component_details[1:]
        # component_details = merge_components(component_details)
        mask = mask * 255
        image = gray.copy()
        image = np.stack((image, image, image), axis=2)
        # component_details = classify_all(model, gray)
        # image = cv2.resize(np.uint8(image), new_shape)
        for component in component_details:
            # break

            # print("region mass is", comp)
            # start_point = (int(comp[0]), int(comp[1]))
            # end_point = (
            #     int(comp[0] + comp[2]),
            #     int(comp[1] + comp[3]),
            # )
            r = Region(
                component[0],
                component[1],
                component[2],
                component[3],
                mass=component[4],
                id=0,
                frame_number=0,
            )
            start_point = (r.x, r.y)
            end_point = (
                int(r.x + r.width),
                int(r.y + r.height),
            )
            if r.width < 100 or r.height < 100:
                continue
            image = cv2.rectangle(image, start_point, end_point, (255, 255, 0), 8)
            # label = classify_ir(model, gray, r)
            # image = cv2.putText(
            #     image,
            #     f"{label}",
            #     (int(r.x), int(r.y + 50)),
            #     cv2.FONT_HERSHEY_SIMPLEX,
            #     1,
            #     (255, 0, 0),
            # )
        image_path = Path(img_file)
        image_path = image_path.parent / f"{image_path.name}-classified.jpg"
        cv2.imwrite(str(image_path), np.uint8(image))
        image_path = Path(img_file)
        image_path = image_path.parent / f"{image_path.name}-filtered.jpg"
        cv2.imwrite(str(image_path), np.uint8(fgMask))
        image_path = Path(img_file)
        image_path = image_path.parent / f"{image_path.name}-threshed.jpg"
        cv2.imwrite(str(image_path), np.uint8(threshed))
        #
        # image_path = Path(img_file)
        # image_path = image_path.parent / f"{image_path.name}-saliency.jpg"
        # cv2.imwrite(str(image_path), np.uint8(saliencyMap))
        # continue
        # image = cv2.resize(np.uint8(image), new_shape)
        # smaller_b = cv2.resize(np.uint8(filtered), new_shape)
        # smaller_g = cv2.resize(np.uint8(gray), new_shape)
        # #
        # # cv2.imshow("background", np.uint8(smaller_b))
        # # cv2.moveWindow("background", 0, 0)
        # # cv2.waitKey(5000)
        # cv2.imshow("background", np.uint8(smaller_b))
        # cv2.moveWindow("background", 0, 0)
        # cv2.waitKey(2000)
        # cv2.imshow("background", np.uint8(smaller_g))
        # cv2.moveWindow("background", 0, 0)
        # cv2.waitKey(2000)
        # cv2.imshow("background", np.uint8(image))
        # cv2.moveWindow("background", 0, 0)
        # cv2.waitKey(2000)
        prev = gray.copy()
        prev_name = img_file
    # vidcap.release()


def back_with_no_ref(gray):
    saliency = cv2.saliency.StaticSaliencyFineGrained_create()
    (success, saliencyMap) = saliency.computeSaliency(gray)
    saliencyMap = (saliencyMap * 255).astype("uint8")

    # saliencyMap = gray.copy()
    # saliencyMap[gray> 200] = 0

    salient_mask = saliencyMap > 0
    salient_median = np.median(gray[salient_mask])

    salient_mask = saliencyMap == 0
    background_median = np.median(gray[salient_mask])
    # filtered = squared_median(gray)
    # saliencyMap = cv2.dilate(saliencyMap, (15,15), iterations=30)

    print("sal median", salient_median, " back med", back_median)
    gray = np.float32(gray)
    filtered = gray.copy()

    salient_mask = gray > 200
    filtered[salient_mask] -= salient_median
    salient_mask = gray == 0
    filtered[salient_mask] -= background_median
    # filtered[salient_mask] = 0

    filtered = np.abs(filtered)
    filtered = np.uint8(filtered)
    # filtered = filtered * 2
    print(
        "now we have",
        np.median(filtered),
        np.percentile(filtered, 25),
        len(filtered[filtered < 20]),
    )
    # filtered[filtered < 10] = 0
    # filtered[filtered > 255] = 255


def squared_median(gray):
    box_dim = 1000
    widths = int(math.ceil(gray.shape[1] / box_dim))
    heights = int(math.ceil(gray.shape[0] / box_dim))
    gray = np.float32(gray)
    for i in range(heights):
        for z in range(widths):
            r = Rectangle(z * box_dim, i * box_dim, box_dim, box_dim)
            sub_gray = r.subimage(gray)
            sub_gray -= np.median(sub_gray)
    return np.abs(gray)


def classify_all(model, gray):
    new_shape = np.uint16([gray.shape[1] * 0.2, gray.shape[0] * 0.2])
    # gray = cv2.resize(np.uint8(gray), new_shape)
    box_dim = 3000
    widths = int(math.ceil(gray.shape[1] / box_dim))
    heights = int(math.ceil(gray.shape[0] / box_dim))
    animal_regions = []
    for i in range(heights):
        for z in range(widths):
            r = Rectangle(z * box_dim, i * box_dim, box_dim, box_dim)

            print("testing on ", r)
            label = classify_ir(model, gray, r)
            if label != "false-positive":
                animal_regions.append(r)
                print("got", label, r)
                # return animal_regions
    return animal_regions


def classify_ir(model, gray, region):
    # region = Region(
    #     component[0],
    #     component[1],
    #     component[2],
    #     component[3],
    #     mass=component[4],
    #     id=0,
    #     frame_number=0,
    # )
    cropped = region.subimage(gray).copy()
    cropped = np.float32(cropped)
    cropped, stats = normalize(cropped, new_max=255)
    image = np.stack((cropped, cropped, cropped), axis=2)

    image = resize_and_pad(
        image,
        (model.params.frame_size, model.params.frame_size, 3),
        region,
        None,
        True,
    )
    # cv2.imshow("b", np.uint8(image))
    # cv2.moveWindow("b", 0, 0)
    #
    # cv2.waitKey(1000)
    image = tf.keras.applications.inception_v3.preprocess_input(image)
    image = image[np.newaxis, ...]
    prediction = model.model.predict([image])[0]
    best_label = np.argmax(prediction)
    label = model.labels[best_label]
    print("predictred", label, round(prediction[best_label] * 100))
    return label


def video(source, background):
    vidcap = cv2.VideoCapture(str(source))
    i = 0
    new_shape = np.uint16([background.shape[1] * 0.5, background.shape[0] * 0.5])

    while True:
        success, image = vidcap.read()
        if not success:
            break
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = gray[:-100, :-100]

        if i < 10 or i % 3 != 0:
            i += 1
            continue
        diff_window = np.percentile(gray, 75) - np.median(gray)
        print(
            "at frame",
            i / 30,
            " s",
            np.median(gray),
            np.percentile(gray, 75),
            diff_window,
        )
        if i > 0 * 30:
            filtered = get_diff_back_filtered(
                background,
                gray,
                diff_window,
            )
            num, mask, component_details, threshed = theshold_saliency(
                filtered, threshold=0
            )
            # component_details = merge_components(component_details[1:])
            image = cv2.resize(np.uint8(gray), new_shape)
            for comp in component_details:
                if comp[2] < 5 or comp[3] < 5:
                    continue
                print("region mass % is", 100 * comp[4] / (comp[2] * comp[3]))
                start_point = (int(comp[0] * 0.5), int(comp[1] * 0.5))
                end_point = (
                    int(comp[0] * 0.5 + comp[2] * 0.5),
                    int(comp[1] * 0.5 + comp[3] * 0.5),
                )
                image = cv2.rectangle(image, start_point, end_point, (255, 0, 0), 2)
            cv2.imshow("background", np.uint8(image))
            cv2.moveWindow("background", 0, 0)
            cv2.waitKey(100)

        i += 1
    vidcap.release()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "source",
        help='a CPTV file to process, or a folder name, or "all" for all files within subdirectories of source folder.',
    )
    args = parser.parse_args()
    init_logging(None)
    config = Config.load_from_file(None)

    model = KerasModel()
    model_file = config.classify.models[0].model_file
    weights = config.classify.models[0].model_weights

    # model.load_model(model_file, training=False, weights=weights)

    args.source = Path(args.source)
    if args.source.is_dir():
        background_file = args.source / f"{args.source.name}-background.jpg"
    else:
        background_file = args.source.parent
        background_file = background_file / f"{args.source.name}-background.jpg"
    if background_file.exists():
        background = cv2.imread(str(background_file))
        background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)

        print("found backgorund file", background.shape)
    else:
        if args.source.is_dir():
            # calculate fromstilss
            background = save_background_stills(args.source, background_file)

        else:
            background = save_background(args.source, background_file)
    if args.source.is_dir():
        # pass
        num, mask, component_details, threshed = theshold_saliency(
            background, threshold=0, otsus=True
        )
        # cv2.imshow("b", cv2.resize(threshed, (640, 480)))
        # cv2.moveWindow("b", 0, 0)
        # cv2.waitKey(10000)
        # return
        detect_images(args.source, background, model)
    else:
        video(args.source, background)


if __name__ == "__main__":
    main()
