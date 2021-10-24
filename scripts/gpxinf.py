import gpxpy
import gpxpy.gpx

#this script was created in order to overcome some issues with GPS data from a Garmin device which was not accepted by strava
#it uses https://github.com/tkrajina/gpxpy

gpx_file = open('falsy.gpx', 'r')
gpx = gpxpy.parse(gpx_file)

#create a list of time stamps
times = []

for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            time = point.time
            times.append(time)
            print('Point at ({0},{1}) -> {2} @ {3}'.format(point.latitude, point.longitude, point.elevation, time))

#sort and print first and last
#if the last is not identical with the last one from the above loop, we found the cause for the strava data error
times.sort()
print('First {0}, Last {1}'.format(times[0], times[-1]))
