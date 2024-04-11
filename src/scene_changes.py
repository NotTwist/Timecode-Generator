import cv2
import numpy as np
from tqdm.auto import tqdm


def scene_change_detector(frames):
    scene_changes = []
    scene_changes_frames = []
    vis = []
    metric_values = []

    def get_brightness_hist(frame):
        return cv2.calcHist([cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)], [0], None, [256], [0, 256])

    def get_color_hist(frame):
        color_hist = []
        for i in range(3):
            color_hist.append(cv2.calcHist([frame], [i], None, [256], [0, 256]))
        return color_hist

    def pixel_metric(frame, prev_frame):  # mse
        return np.mean((frame.astype(np.int32) - prev_frame) ** 2)

    def abs_metric(frame, prev_frame):
        return np.sum(np.absolute(frame.astype(np.int32) - prev_frame))

    def brightness_metric(frame_hist, prev_frame_hist):
        return 1 - (cv2.compareHist(prev_frame_hist, frame_hist, method=cv2.HISTCMP_CORREL) + 1) / 2

    def color_metric(frame_color_hist, prev_frame_color_hist):
        color_values = np.zeros(3)
        for i in range(3):
            color_values[i] = (cv2.compareHist(prev_frame_color_hist[i], frame_color_hist[i],
                                               method=cv2.HISTCMP_CORREL) + 1) / 2.0
        return 1 - np.mean(color_values)

    def edge_metric(frame, prev_frame):
        ddepth = cv2.CV_64F
        gray1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
        sobelx1 = cv2.Sobel(gray1, ddepth, 1, 0, ksize=5)
        sobelx2 = cv2.Sobel(gray2, ddepth, 1, 0, ksize=5)
        sobely1 = cv2.Sobel(gray1, ddepth, 0, 1, ksize=5)
        sobely2 = cv2.Sobel(gray2, ddepth, 0, 1, ksize=5)

        diff_sobel_x = np.abs(sobelx1 - sobelx2)
        diff_sobel_y = np.abs(sobely1 - sobely2)
        diff_sobel = cv2.addWeighted(diff_sobel_x, 0.5, diff_sobel_y, 0.5, 0)

        mse = np.mean(diff_sobel)
        return mse

    def create_edge(frame):
        gray1 = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Apply Gaussian blur to reduce noise and smoothen edges
        blurred1 = cv2.GaussianBlur(src=gray1, ksize=(3, 5), sigmaX=0.5)
        # Perform Canny edge detection
        edges1 = cv2.Canny(blurred1, 70, 135)
        return edges1

    def canny_edge(frame_edge, prev_frame_edge):
        return np.mean((frame_edge.astype(np.int32) - prev_frame_edge) ** 2)

    # abs
    a_abs = -1
    b_abs = 4
    c_abs = 4
    window_abs = 5
    abs_values = []
    # mse
    a_mse = -1
    b_mse = 4
    c_mse = 4
    window_mse = 5
    mse_values = []
    # bright
    a_bright = -1
    b_bright = 15
    c_bright = 15
    window_bright = 15
    bright_values = []
    # color
    a_color = -1
    b_color = 15
    c_color = 15
    window_color = 15
    color_values = []
    # canny_edge
    a_canny = -1
    b_canny = 2
    c_canny = 8
    window_canny = 10
    canny_values = []

    thresh_values = []
    prev_frame = None
    prev_frame_hist = None
    prev_frame_color_hist = None
    prev_frame_edge = None


    for idx, frame in tqdm(enumerate(frames), leave=False):
        if prev_frame is not None:
            metrics = []
            # MSE

            mse_value = pixel_metric(frame, prev_frame)
            m = np.mean(mse_values[max(idx - window_mse, 0):idx])
            std = np.std(mse_values[max(idx - window_mse, 0):idx])
            mse_thresh = a_mse * mse_values[-1] + b_mse * m + std * c_mse
            mse_values.append(mse_value)
            metrics.append((mse_value, mse_thresh))

            # ABS

            abs_value = abs_metric(frame, prev_frame)
            m = np.mean(abs_values[max(idx - window_abs, 0):idx])
            std = np.std(abs_values[max(idx - window_abs, 0):idx])
            abs_thresh = a_abs * abs_values[-1] + b_abs * m + std * c_abs
            abs_values.append(abs_value)
            metrics.append((abs_value, abs_thresh))

            # BRIGHTNESSS
            # save histogram of previous frame

            frame_hist = get_brightness_hist(frame)
            if prev_frame_hist is None:
                prev_frame_hist = get_brightness_hist(prev_frame)
            bright_value = brightness_metric(frame_hist, prev_frame_hist)
            prev_frame_hist = frame_hist
            m = np.mean(bright_values[max(idx - window_bright, 0):idx])
            std = np.std(bright_values[max(idx - window_bright, 0):idx])
            bright_thresh = a_bright * bright_values[-1] + b_bright * m + std * c_bright
            bright_values.append(bright_value)
            metrics.append((bright_value, bright_thresh))

            # COLOR
            # save histogram of previous frame

            frame_color_hist = get_color_hist(frame)
            if prev_frame_color_hist is None:
                prev_frame_color_hist = get_color_hist(prev_frame)
            color_value = color_metric(frame_color_hist, prev_frame_color_hist)
            prev_frame_color_hist = frame_color_hist
            m = np.mean(color_values[max(idx - window_color, 0):idx])
            std = np.std(color_values[max(idx - window_color, 0):idx])
            color_thresh = a_color * color_values[-1] + b_color * m + std * c_color
            color_values.append(color_value)
            metrics.append((color_value, color_thresh))

            # CANNY EDGE DETECTION

            frame_edge = create_edge(frame)
            if prev_frame_edge is None:
                prev_frame_edge = create_edge(prev_frame)
            canny_edge_value = canny_edge(frame_edge, prev_frame_edge)
            m = np.mean(canny_values[max(idx - window_canny, 0):idx])
            std = np.std(canny_values[max(idx - window_canny, 0):idx])
            canny_thresh = a_canny * canny_values[-1] + b_canny * m + std * c_canny
            canny_values.append(canny_edge_value)
            metrics.append((canny_edge_value, canny_thresh))

            # #sliding window with metric values
            # values[:-1] = values[1:]
            # values[-1] = metric_value

            # voting by majority
            votes = 0
            if color_value > color_thresh:
                votes += 2
            if bright_value > bright_thresh:
                votes += 1
            if mse_value > mse_thresh:
                votes += 1
            if abs_value > abs_thresh:
                votes += 1
            if canny_edge_value > canny_thresh:
                votes += 1
            if votes >= 4 and idx > 2:
                scene_changes.append(idx)
                scene_changes_frames.append(frame)
            metric_values.append([abs_value, mse_value, bright_value, color_value, canny_edge_value])
        else:
            metric_values.append([0, 0, 0, 0, 0])
            mse_values.append(0)
            mse_values.append(0)
            abs_values.append(0)
            canny_values.append(0)
            bright_values.append(0)
            color_values.append(0)
        prev_frame = frame

        ###  END CODE HERE  ###

    return scene_changes, scene_changes_frames
