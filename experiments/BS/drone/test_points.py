from geodesy import haversine

def haversine_v(coord1: object, coord2: object):
    import math

    # Coordinates in decimal degrees (e.g. 2.89078, 12.79797)
    lon1, lat1 = coord1
    lon2, lat2 = coord2

    R = 6371000  # radius of Earth in meters
    phi_1 = math.radians(lat1)
    phi_2 = math.radians(lat2)

    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + math.cos(phi_1) * math.cos(phi_2) * math.sin(delta_lambda / 2.0) ** 2
    
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    meters = R * c  # output distance in meters
    km = meters / 1000.0  # output distance in kilometers

    meters = round(meters, 3)
    km = round(km, 3)


    return meters


points = ((50.86227366666667, 4.685484),
(50.8618866901574, 4.684993376407921),
(50.8628174478198, 4.683956636462093), 
(50.862059301978924, 4.682930456918715), 
(50.86169474668278, 4.680829746205712), 
(50.861023979468186, 4.679089260840485), 
(50.85999189432477, 4.676872293048831), 
(50.85989246571537, 4.6766121987027285), 
(50.85983795640913, 4.676094035407898))

for p in points[1:]:
    print(haversine_v(points[0],p))
          
print('**********************')
for p in points[1:]:
    print(haversine(points[0][0],p[0],points[0][1],p[1]))
    
