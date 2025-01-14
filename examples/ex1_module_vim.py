import cv2

from classes.modules.module_vim import ModuleVim


def nothing(x):
    """
    Trackbar callback function

    Args:
        x: Any
    """
    pass

def update_get_data_from_trackbars(module_vim: ModuleVim):
    """
    The function updates the rendering variables

    Args:
        module_vim (ModuleVim): Object of class ModuleVim
    """
    new_is_segmentation = bool(cv2.getTrackbarPos('new_is_segmentation', 'Trackbars'))
    new_is_draw_rectangle = bool(cv2.getTrackbarPos('new_is_draw_rectangle', 'Trackbars'))
    new_is_draw_point = bool(cv2.getTrackbarPos('new_is_draw_point', 'Trackbars'))
    new_count_draw_points = int(cv2.getTrackbarPos('new_count_draw_points', 'Trackbars'))
    new_is_draw_start_position = bool(cv2.getTrackbarPos('new_is_draw_start_position', 'Trackbars'))

    module_vim.is_segmentation = new_is_segmentation
    module_vim.is_draw_rectangle = new_is_draw_rectangle
    module_vim.is_draw_point = new_is_draw_point
    module_vim.count_draw_points = new_count_draw_points
    module_vim.is_draw_start_position = new_is_draw_start_position


if __name__ == '__main__':

    # Creating window
    cv2.namedWindow('Trackbars')

    # Creating trackbars for boolean variables
    cv2.createTrackbar('new_is_segmentation', 'Trackbars', 0, 1, nothing)
    cv2.createTrackbar('new_is_draw_rectangle', 'Trackbars', 0, 1, nothing)
    cv2.createTrackbar('new_is_draw_point', 'Trackbars', 0, 1, nothing)
    cv2.createTrackbar('new_count_draw_points', 'Trackbars', 1, 100, nothing)
    cv2.createTrackbar('new_is_draw_start_position', 'Trackbars', 0, 1, nothing)
    module_vim = ModuleVim('C:\\Users\\user\\PycharmProjects\\SSUGT_inclinometer\\3.mp4')
    update_get_data_from_trackbars(module_vim)
    module_vim.start_stream()

    video_is_started = True
    while module_vim.is_streaming:
        update_get_data_from_trackbars(module_vim)

        module_vim.update_data()
        frame, frame_original, fps, esp32_name, center_bubbles_px, points, is_camera = (
            module_vim.frame, module_vim.frame_original, module_vim.fps, module_vim.esp32_name,
            module_vim.center_bubbles_px,
            module_vim.points, module_vim.is_camera)

        cv2.imshow('frame', frame)
        cv2.waitKey(1)
