from glom import glom


def calculate_meter_specific_time(segments_table, lap_times):
    last_100m = 0
    last_200m = 0
    last_500m = 0

    split_times = {}
    for lap_time in lap_times:
        split_times[lap_time["distance"]] = int(lap_time["time"])

    for segment in segments_table:
        segment_range = glom(segment, "Segment").split(" -- ")

        if int(segment_range[1]) % 100 == 0:
            lap_100m = split_times[segment_range[1]] - last_100m
            segment["100 m"] = lap_100m
            last_100m += lap_100m

        if int(segment_range[1]) % 200 == 0:
            lap_200m = split_times[segment_range[1]] - last_200m
            segment["200 m"] = lap_200m
            last_200m += lap_200m

        if int(segment_range[1]) % 500 == 0:
            lap_500m = split_times[segment_range[1]] - last_500m
            segment["500 m"] = lap_500m
            last_500m += lap_500m

    return segments_table
