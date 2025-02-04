import numpy as np


def get_new_points(points: np.ndarray, sep: str = ';'):
    results_points_text_x: str = ''
    results_points_text_y: str = ''
    for row_points in points.tolist():
        for i, point in enumerate(row_points):
            match i:
                case 0:
                    results_points_text_x += str(point) + ','
                case 1:
                    results_points_text_y += str(point) + ','
    results_points_text_x = results_points_text_x.rstrip(',')
    results_points_text_y = results_points_text_y.rstrip(',')
    return results_points_text_x, results_points_text_y
