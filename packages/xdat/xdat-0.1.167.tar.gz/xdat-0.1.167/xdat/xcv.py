import numpy as np
import pandas as pd
from scriptine import path
import cv2
from tqdm import tqdm
import matplotlib.pyplot as plt
from . import xplots, xstats


def angle_difference(a1, a2):
    return 180 - np.abs(np.abs(a1 - a2) - 180)


def kp_angle_dist(kp1, kp2):
    return angle_difference(kp1.angle, kp2.angle)


def kp_euclidean_distance(kp1, kp2):
    """Compute pairwise Euclidean distances between two keypoints."""

    dx = kp1.pt[0] - kp2.pt[0]
    dy = kp1.pt[1] - kp2.pt[1]
    distance = np.sqrt(dx**2 + dy**2)
    return distance


def kp_relative_distances(keypoint, keypoints, kp_dist_func=kp_euclidean_distance):
    """Compute distances from the given keypoint to all other keypoints."""

    return [kp_dist_func(keypoint, kp) for kp in keypoints]


def match_spatial_consistency(match, matches, query_keypoints, train_keypoints):
    return match_consistency(match, matches, query_keypoints, train_keypoints, kp_dist_func=kp_euclidean_distance)


def match_angle_consistency(match, matches, query_keypoints, train_keypoints):
    return match_consistency(match, matches, query_keypoints, train_keypoints, kp_dist_func=kp_angle_dist)


def match_consistency(match, matches, query_keypoints, train_keypoints, kp_dist_func=kp_euclidean_distance):
    # Extract keypoints for the current match
    query_kp = query_keypoints[match.queryIdx]
    train_kp = train_keypoints[match.trainIdx]

    # Extract keypoints for all matches
    matched_query_kps = [query_keypoints[m.queryIdx] for m in matches]
    matched_train_kps = [train_keypoints[m.trainIdx] for m in matches]

    # Compute relative distances in both query and train images
    query_distances = kp_relative_distances(query_kp, matched_query_kps, kp_dist_func=kp_dist_func)
    train_distances = kp_relative_distances(train_kp, matched_train_kps, kp_dist_func=kp_dist_func)

    # Compute difference between the sets of distances
    difference = np.abs(np.array(query_distances) - np.array(train_distances))

    # Return the mean difference (or any other metric of your choice)
    return np.mean(difference)


def match_analysis(matches, kp1, kp2):
    """ Given kp matches, return a df with added analysis """

    rows = []

    for match in matches:
        kp_a = kp1[match.queryIdx]
        kp_b = kp2[match.trainIdx]

        angle_diff = angle_difference(kp_a.angle, kp_b.angle)
        spatial_consist = match_spatial_consistency(match, matches, kp1, kp2)
        angle_consist = match_angle_consistency(match, matches, kp1, kp2)

        row = {
            'kp_dist': match.distance,
            'angle_diff': angle_diff,
            'spatial_consistency': spatial_consist,
            'angle_consistency': angle_consist
        }

        rows.append(row)

    df_matches = pd.DataFrame(rows)
    return df_matches


def match_score(df_matches, plot=False):
    """ Given a match analysis df (see match_analysis)m returns a match score """

    df = df_matches.sort_values('kp_dist')
    df['score'] = df.kp_dist * df.spatial_consistency * df.angle_consistency * 0.000001

    if plot:
        xplots.plot_multi(df, kind='hist', y='kp_dist', hist_range=[0, 100])
        xplots.plot_multi(df, kind='kde', y='score', xlim=[0, 1])
        xplots.plot_multi(df, kind='line', x='kp_dist', y='angle_diff')
        xplots.plot_multi(df, kind='line', x='kp_dist', y='spatial_consistency')
        xplots.plot_multi(df, kind='line', x='kp_dist', y='angle_consistency')
        xplots.plot_multi(df, kind='line', x='kp_dist', y='score')

    # identical image
    if df.score.sum() == 0:
        return 0

    score, score_density = xstats.x_kde_mode(df.score.to_numpy())

    return score


def process_video(video_in_path, video_out_path=None, frames_folder=None, plot_idx=None, max_frames=None, quality=90, pfunc=None, every=1):
    video_in_path = path(video_in_path)
    vidcap = cv2.VideoCapture(video_in_path)

    fps = vidcap.get(cv2.CAP_PROP_FPS)
    frame_count = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_size = (width, height)
    print('frame size=', frame_size)

    if frames_folder:
        frames_folder = path(frames_folder)
        frames_folder.ensure_dir()

    out = None
    if video_out_path:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(video_out_path, fourcc, fps, frame_size)
        out.set(cv2.VIDEOWRITER_PROP_QUALITY, quality)

    for idx in tqdm(range(frame_count)):
        success, image = vidcap.read()

        if not success:
            print(f'{idx}) error reading image')
            break

        if idx % every != 0:
            continue

        if pfunc:
            image = pfunc(image, frame=idx)

        if out:
            out.write(image)

        if frames_folder:
            frame_name = f"{video_in_path.namebase}__frame{idx:05d}.jpg"
            # frame_path = frames_folder.joinpath(video_in_path.namebase)
            # frame_path.ensure_dir()
            frame_path = frames_folder.joinpath(frame_name)
            cv2.imwrite(frame_path, image)

        if plot_idx == idx:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            plt.imshow(image_rgb)
            plt.axis('off')
            plt.tight_layout()
            plt.show()

        if max_frames is not None and idx >= max_frames * every:
            break

    if out:
        out.release()
