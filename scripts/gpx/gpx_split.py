"""
This script will split a large gpx file into smaller chunks, depending on th maximum amount of points in a file.
"""
import click
import logging
from pathlib import Path
import os

import gpxpy
import gpxpy.gpx


def write_gpx(dest_dir, file, segment):
    logging.debug(f"writing {len(segment.points)} points to {file}")
    gpx = gpxpy.gpx.GPX()
    gpx_track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(gpx_track)
    gpx_track.segments.append(segment)

    with open(os.path.join(dest_dir, file), "w") as f:
        f.write(gpx.to_xml())

def split_gpx(source, dest_dir, max_segment_points=500):
    logging.debug(f"Splitting file {source} into files in {dest_dir}")

    file_name = lambda name: lambda count: name + "_" + str(count) + ".gpx"
    name = Path(source).name.rsplit('.gpx')[0]
    next_name = file_name(name)

    output_count = 1
    with open(source, "rb") as f:
        gpx = gpxpy.parse(f)

    track_segment = gpxpy.gpx.GPXTrackSegment()

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                track_segment.points.append(point)

                if len(track_segment.points) >= max_segment_points:
                    write_gpx(dest_dir, next_name(output_count), track_segment)
                    output_count += 1
                    track_segment = gpxpy.gpx.GPXTrackSegment()
                    track_segment.points.append(point)

    if len(track_segment.points) > 1:
        write_gpx(dest_dir, next_name(output_count), track_segment)


@click.command()
@click.argument("source")
@click.option("-o", "--output", help="Output directory", default=".")
@click.option("-p", "--points",
    help="Maximum number of points per result file.", default=500)
@click.option("-d", "--debug", help="Turn on debug loggin.", default=False)
def _main(source, output, points, debug):
    if debug:
        logging.basicConfig(level=logging.DEBUG)

    split_gpx(source, output, max_segment_points=points)

if __name__ == "__main__":
    _main()
