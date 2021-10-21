"""
This script will split a large gpx file into smaller chunks, depending on th maximum amount of points in a file.
"""
import click
import logging
from pathlib import Path
import os

import gpxpy
import gpxpy.gpx
import haversine as hs

class Writer:

    def __init__(self, dest_dir):
        self.dest_dir = dest_dir

    def write(self, file, segment):
        logging.debug(f"writing {len(segment.points)} points to {file}")
        gpx = gpxpy.gpx.GPX()
        gpx_track = gpxpy.gpx.GPXTrack()
        gpx.tracks.append(gpx_track)
        gpx_track.segments.append(segment)

        with open(os.path.join(self.dest_dir, file), "w") as f:
            f.write(gpx.to_xml())

class Splitter:

    def __init__(self, dest_dir, log):
        self.writer = Writer(dest_dir)
        self.logger = logging.getLogger(Splitter.__name__)
        if log:
            self.logger.setLevel(logging.DEBUG)

    def debug_enabled(func):
        def func_wrapper(self, name):
            if self.logger.isEnabledFor(logging.DEBUG):
                return func(self, name)
        return func_wrapper

    def split(self, source, max_segment_points=500):
        self.logger.debug(f"Splitting file {source} into files in {self.writer.dest_dir}")

        file_name = lambda name: lambda count: f"{name}_{str(count)}.gpx"
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
                        self.__write(next_name(output_count), track_segment)
                        output_count += 1
                        track_segment = gpxpy.gpx.GPXTrackSegment()
                        track_segment.points.append(point)

        #ensure that we save file when number of all points is below max points per file
        if len(track_segment.points) > 1:
            self.__write(next_name(output_count), track_segment)

    def __write(self, name, track_segment):
        self.__log_track_length(track_segment)
        self.writer.write(name, track_segment)

    @debug_enabled
    def __log_track_length(self, track_segment):
        start = track_segment.points[0]
        end = track_segment.points[-1]
        p1 = (start.latitude, start.longitude)
        p2 = (end.latitude, end.longitude)
        dist = hs.haversine(p1, p2)
        self.logger.debug(f"Track length: {dist} km")


@click.command()
@click.argument("source")
@click.option("-o", "--output", help="Output directory", default=".")
@click.option("-p", "--points",
    help="Maximum number of points per result file.", default=500)
@click.option("-l", "--log", help="Log output.", default=False)
def _main(source, output, points, log):
    splitter = Splitter(output, log)
    splitter.split(source, max_segment_points=points)

if __name__ == "__main__":
    _main()
