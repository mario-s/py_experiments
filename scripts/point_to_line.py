from geopy.distance import geodesic
from geographiclib.geodesic import Geodesic

#A straight line between two points, p1 and p2, on the earth surface is a geodesic.
#The closest point on a geodesic to another point p3, is referred to as the interception point x.

# Define the coordinates of points p1, p2, and p3
p1 = (52.643605, 13.533826)  # Example latitude and longitude for point 1
p2 = (52.644021, 13.535629)  # Example latitude and longitude for point 2
p3 = (52.643826, 13.535369)  # Example latitude and longitude for point 3

# Calculate the geodesic distance between p1 and p2
line_distance = geodesic(p1, p2).meters

# Calculate the azimuth (bearing) from p1 to p2
g = Geodesic.WGS84.Inverse(p1[0], p1[1], p2[0], p2[1])
bearing_p1_p2 = g['azi1']

# Calculate the geodesic distance and destination point x from p1 to p3
dest_point = Geodesic.WGS84.Direct(p1[0], p1[1], bearing_p1_p2, geodesic(p1, p3).meters)
x = (dest_point['lat2'], dest_point['lon2'])
print(f"Interception point x: {x}")

# Calculate the geodesic distance between p3 and x
dist = geodesic(p3, x).meters
print(f"Distance p3 <-> x: {dist}")
