import os
from dateutil.parser import parse as parse_date
import sys
import argparse
import logging
from time import gmtime
from time import strftime
from pathlib import Path
import json

from multiprocessing import Pool
import multiprocessing
from logging.handlers import QueueHandler, QueueListener

FPS = 10
import psycopg2


def worker_init(q):
    # all records from worker processes go to qh and then into q
    qh = QueueHandler(q)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(qh)


def logger_init():
    q = multiprocessing.Queue()
    # this is the handler for all log records
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(levelname)s: %(asctime)s - %(process)s - %(message)s")
    )

    # ql gets records from the queue and sends them to the handler
    ql = QueueListener(q, handler)
    ql.start()

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    # add the handler to the logger so records from this process are handled
    logger.addHandler(handler)

    return ql, q


def init_logging(timestamps=False):
    """Set up logging for use by various classifier pipeline scripts.

    Logs will go to stderr.
    """

    fmt = "%(process)d %(thread)s:%(levelname)7s %(message)s"
    if timestamps:
        fmt = "%(asctime)s " + fmt
    logging.basicConfig(
        stream=sys.stderr, level=logging.INFO, format=fmt, datefmt="%Y-%m-%d %H:%M:%S"
    )


def parse_args():
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    return args


import json


def main():
    q_listener, q = logger_init()
    args = parse_args()
    p = Path("./trackdata.json")
    with p.open() as f:
        rec_meta = json.load(f)
    process(rec_meta)


def process(rec_meta):
    conn = psycopg2.connect(
        database="cacodb",
        host="localhost",
        user="user10",
        password="password",
    )
    print("Updating", len(rec_meta))
    for track_id, track_update in rec_meta.items():
        print("updating", track_id)
        try:
            cursor = conn.cursor()
            cursor.execute(
                f'SELECT "data","RecordingId","AlgorithmId" FROM "Tracks" t where t."id" = {track_id} and t."archivedAt" is null'
            )
            row = cursor.fetchone()
            if row is None:
                print("no data for ", track_id, track_update)
                continue
            data, rec_id, algorithm_id = row
            data["original"] = True
            # create original copy and archive original
            sql = """INSERT INTO "Tracks"("data","RecordingId","AlgorithmId","archivedAt")
             VALUES(%s,%s,%s,NOW())"""
            cursor.execute(sql, (json.dumps(data), rec_id, algorithm_id))
            # conn.commit()

            # update orignal with tighter track
            del data["original"]
            remove_last = data["frame_end"] - track_update["frame_end"]
            data["positions"] = data["positions"][
                : len(data["positions"]) - remove_last
            ]
            print("Removing last", remove_last)
            assert remove_last == 0
            data["frame_end"] = track_update["frame_end"]
            data["end_s"] = track_update["frame_end"] / 10.0
            data["tightened"] = True
            sql = """Update "Tracks" set "data" = %s where "id"=%s"""
            cursor.execute(sql, (json.dumps(data), track_id))
            conn.commit()

        except Exception as e:
            print("ERROR", e)
    #
    #     update_cmd = 'Update "Tracks" set data=%s where id=%s'
    # try:
    #     r_id = 0
    #     cursor = conn.cursor()
    #     cursor.execute(
    #         f'SELECT id FROM "Recordings" r where r."recordingDateTime"  > \'{AFTER_DATE}\''
    #     )
    #     for (r_id,) in cursor:
    #         track_cursor = conn.cursor()
    #         track_cursor.execute(
    #             f'SELECT id,data FROM "Tracks" t where t."RecordingId"  = {r_id} and t."AlgorithmId" = 89'
    #         )
    #         for t_id, data in track_cursor:
    #             tracker_version = data["tracker_version"]
    #             if tracker_version != "IRTrackExtractor-10":
    #                 print(
    #                     f"Incorrect tracker version {r_id} - {t_id} tracker {tracker_version}"
    #                 )
    #                 continue
    #             for pos in data["positions"]:
    #                 pos["frame_number"] -= 1
    #             data["frame_start"] -= 1
    #             data["frame_end"] -= 1
    #             data["tracker_version"] = f"{tracker_version}-Fixed"
    #             update_cur = conn.cursor()
    #             # execute the UPDATE  statement
    #             update_cur.execute(update_cmd, (json.dumps(data), t_id))
    #             # get the number of updated rows
    #             updated_rows = update_cur.rowcount
    #             # Commit the changes to the database
    #             conn.commit()
    #             # Close communication with the PostgreSQL database
    #             update_cur.close()
    #             print("updated data for track", t_id, " count", updated_rows)
    #             # break
    #         # break
    # except:
    #     logging.error("Error processing %s", r_id, exc_info=True)


if __name__ == "__main__":
    main()
