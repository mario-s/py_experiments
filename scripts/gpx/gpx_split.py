"""
This script will split a large gpx file into smaller chunks, depending on th maximum amount of points in a file.
"""
import click
import logging
import os
from pathlib import Path

import gpxpy
import gpxpy.gpx
import haversine as hs

#create logger
logger = logging.getLogger('splitter')
# create console handler with a debug log level
ch = logging.StreamHandler()
formatter = logging.Formatter('- %(name)s - %(levelname)-8s: %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class Distance:

    def points(p1, p2):
        return hs.haversine(p1, p2)

    def track_length(points):
        len = 0
        prev_point = None
        for p in points:
            if not prev_point is None:
                len += Distance.points(prev_point, p)
            prev_point = p
        return len


class Writer:

    def __init__(self, dest_dir):
        self.dest_dir = dest_dir

    def write(self, name, segment):
        file = f"{name}.gpx"
        logger.debug(f"writing {len(segment.points)} points to {file}")
        gpx = gpxpy.gpx.GPX()
        gpx.name = name
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)
        gpx_track.segments.append(segment)

        with open(os.path.join(self.dest_dir, file), "w") as f:
            f.write(gpx.to_xml())


class Splitter:

    def __init__(self, writer):
        self.writer = writer

    def debug_enabled(func):
        def func_wrapper(self, name):
            if logger.isEnabledFor(logging.DEBUG):
                return func(self, name)
        return func_wrapper

    def split(self, source, max_segment_points=500):
        logger.debug(f"Splitting file {source} into files in {self.writer.dest_dir}")

        file_name = lambda name: lambda count: f"{name}_{str(count)}"
        next_name = file_name(Path(source).name.rsplit('.gpx')[0])

        output_count = 1
        with open(source, "rb") as f:
            gpx = gpxpy.parse(f)

        track_segment = gpxpy.gpx.GPXTrackSegment()

        for track in gpx.tracks:
            for segment in track.segments:
                for point in segment.points:
                    track_segment.points.append(point)

                    if len(track_segment.points) >= max_segment_points:
                        self.__write(next_name(output_count), track_segment)
                        output_count += 1
                        track_segment = gpxpy.gpx.GPXTrackSegment()
                        track_segment.points.append(point)

        #ensure that we save file when number of all points is below max points per file
        if len(track_segment.points) > 1:
            self.__write(next_name(output_count), track_segment)

    def __write(self, name, track_segment):
        self.__log_track_len(track_segment)
        self.writer.write(name, track_segment)

    @debug_enabled
    def __log_track_len(self, track_segment):
        points = [(p.latitude, p.longitude) for p in track_segment.points]
        logger.debug(f"Track length: {Distance.track_length(points)} km")


@click.command()
@click.argument("source")
@click.option("-o", "--output", help="Output directory", default=".")
@click.option("-p", "--points",
    help="Maximum number of points per result file.", default=500)
@click.option("-l", "--log", help="Log output.", default=False)
def _main(source, output, points, log):
    writer = Writer(output)
    splitter = Splitter(writer)
    if log:
        logger.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)

    splitter.split(source, max_segment_points=points)

if __name__ == "__main__":
    _main()
