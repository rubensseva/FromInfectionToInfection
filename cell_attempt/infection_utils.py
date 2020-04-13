import math
import pymunk


def approximate_circle(radius, num_splits):
    r = radius
    one_section = math.pi * 2 / num_splits
    segments_positions = []
    for i in range(num_splits):
        current_section = i * one_section
        next_section = (i + 1) * one_section
        ax = math.cos(current_section) * r
        ay = math.sin(current_section) * r
        bx = math.cos(next_section) * r
        by = math.sin(next_section) * r
        segments_positions.append([(ax, ay), (bx, by)])
    return segments_positions


def is_within_circle(radius, position):
    return position.x ** 2 + position.y ** 2 < radius ** 2


def convert_points_to_pymunk_segments(body, segments_positions, radius=5):
    return [
        pymunk.Segment(body, segment_positions[0], segment_positions[1], radius,)
        for segment_positions in segments_positions
    ]
