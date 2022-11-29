from django.contrib.staticfiles import finders
import json
import math

from .clean import clean_latitude, clean_longitude

# 1 min ~= 1 NM
PRECISION_IN_DEGREES = 0.01  # ~0.6NM
# 0.001  # ~0.1NM


def process_raw_boundaries(raw_boundaries):
    # from [48°00'00"N, 0°00'00"] to [48.0, 0.0]
    # TODO geojson ?
    boundary = []
    pending = None
    last = None
    try:
        for vertex in raw_boundaries:
            if len(vertex) == 1:
                # the start of a named portion (can be a boundary)
                pending = vertex[0]
            if len(vertex) == 2:
                if pending:
                    # substitutes boundary name with vertices
                    last = _create_boundary_vertices(
                        [last[0], last[1]],
                        [clean_latitude(vertex[0]),
                            clean_longitude(vertex[1])],
                        pending, boundary)
                    pending = None
                last = [clean_latitude(vertex[0]),
                        clean_longitude(vertex[1])]
                boundary.append(last)
                # because the boundaries are represented by one list of vertices only with boundary name aliases, if 2 named portions are back to back in this list, it's handled the same way as if there was only one of them
    except Exception as e:
        print(e)
    return [[b[0] / float(3600), b[1] / float(3600)] for b in boundary]


def _create_boundary_vertices(last_vertex, next_vertex, name, boundary):
    last = None
    for v in get_boundary_portion([last_vertex[0], last_vertex[1]], [next_vertex[0], next_vertex[1]], name):
        last = v
        boundary.append(last)
    return last

# ------------------------------------------------------------------


def get_eastern_boundary():
    file_path = finders.find("boundaries/east_boundary.json")
    with open(file_path, "r") as f:
        return json.load(f)


def get_southern_boundary():
    file_path = finders.find("boundaries/south_boundary.json")
    with open(file_path, "r") as f:
        return json.load(f)


def get_boundary_by_name(name):
    if name in ["Frontière franco-italienne", "Frontière franco-belge", "Frontière franco-luxembourgeoise", "Frontière franco-allemande", "Frontière franco-suisse"]:
        return get_eastern_boundary()
    if name in ["Frontière hispano-andorrane", "Frontière franco-espagnole"]:
        return get_southern_boundary()
    raise ValueError("{} boundary is not defined".format(name))


def get_distance(vertex_a, vertex_b):
    # as we are looking for short distances, no need for spheric geometry
    # cartesian will be accurate enough
    lat_diff = vertex_a[0] - vertex_b[0]
    lon_diff = vertex_a[1] - vertex_b[1]
    return math.sqrt(lat_diff*lat_diff + lon_diff*lon_diff)


def get_index_of_closest_point(ref_in_degrees, boundary):
    best_distance = None
    best_candidate = None
    for index, vertex in enumerate(boundary):
        lat, lon = vertex
        distance = get_distance(ref_in_degrees, [lat, lon])
        if distance <= PRECISION_IN_DEGREES:
            # if result is very close to reference, return this directly
            return index
        if best_distance is None or distance <= best_distance:
            best_distance = distance
            best_candidate = index
    return best_candidate


def closed_range(start, stop):
    step = 1 if stop >= start else -1
    dir = 1 if (step > 0) else -1
    return range(start, stop + dir, step)


def get_boundary_portion(start, end, name):
    start_in_degrees = [start[0]/float(3600), start[1]/float(3600)]
    end_in_degrees = [end[0]/float(3600), end[1]/float(3600)]
    boundary = get_boundary_by_name(name)
    start_index = get_index_of_closest_point(start_in_degrees, boundary)
    end_index = get_index_of_closest_point(end_in_degrees, boundary)
    portion = [start]
    for i in closed_range(start_index, end_index):
        vertex = boundary[i]
        lat = int(vertex[0]*3600)
        lon = int(vertex[1]*3600)
        portion.append([lat, lon])
    return portion
