import cv2
import os
import numpy as np
import shutil
from stitching.images import Images
from stitching.feature_detector import FeatureDetector
from stitching.feature_matcher import FeatureMatcher
from stitching.subsetter import Subsetter
from stitching.camera_estimator import CameraEstimator
from stitching.camera_adjuster import CameraAdjuster
from stitching.camera_wave_corrector import WaveCorrector
from stitching.warper import Warper
from stitching.cropper import Cropper
from stitching.exposure_error_compensator import ExposureErrorCompensator
from stitching.seam_finder import SeamFinder
from stitching.blender import Blender
import time

cv2.ocl.setUseOpenCL(False)


def stitch(images, confscore=0.4):
    try:
        indices = []
        confmatrix = None
        print("Stitching start")
        images = Images.of(images)

        medium_imgs = list(images.resize(images.Resolution.MEDIUM))
        low_imgs = list(images.resize(images.Resolution.LOW))
        final_imgs = list(images.resize(images.Resolution.FINAL))

        print("1.1. Feature Extraction...........")
        finder = FeatureDetector(detector="sift", nfeatures=100000)

        starttime = time.time()
        features = [finder.detect_features(img) for img in medium_imgs]
        print(time.time() - starttime)

        print("1.2. Finding Matching Pairs...........")
        starttime = time.time()
        matcher = FeatureMatcher()
        matches = matcher.match_features(features)
        print(time.time() - starttime)
        confmatrix = matcher.get_confidence_matrix(matches)

        print(confmatrix)

        # Subset
        subsetter = Subsetter()
        subsetter = Subsetter(confidence_threshold=confscore)

        indices = subsetter.get_indices_to_keep(features, matches)
        medium_imgs = subsetter.subset_list(medium_imgs, indices)
        low_imgs = subsetter.subset_list(low_imgs, indices)
        final_imgs = subsetter.subset_list(final_imgs, indices)
        features = subsetter.subset_list(features, indices)
        matches = subsetter.subset_matches(matches, indices)

        camera_estimator = CameraEstimator()
        camera_adjuster = CameraAdjuster(confidence_threshold=confscore)
        wave_corrector = WaveCorrector()

        cameras = camera_estimator.estimate(features, matches)
        cameras = camera_adjuster.adjust(features, matches, cameras)
        cameras = wave_corrector.correct(cameras)

        # Warp Images
        starttime = time.time()
        print("1.3. Warping...........")
        warper = Warper()
        # At first, we set the the medium focal length of the cameras as scale:
        warper.set_scale(cameras)
        # Warp low resolution images
        low_sizes = images.get_scaled_img_sizes(Images.Resolution.LOW)
        camera_aspect = images.get_ratio(
            Images.Resolution.MEDIUM, Images.Resolution.LOW
        )  # since cameras were obtained on medium imgs

        warped_low_imgs = list(warper.warp_images(low_imgs, cameras, camera_aspect))
        warped_low_masks = list(
            warper.create_and_warp_masks(low_sizes, cameras, camera_aspect)
        )
        low_corners, low_sizes = warper.warp_rois(low_sizes, cameras, camera_aspect)

        # Warp final resolution images
        final_sizes = images.get_scaled_img_sizes(Images.Resolution.FINAL)
        camera_aspect = images.get_ratio(
            Images.Resolution.MEDIUM, Images.Resolution.FINAL
        )  # since cameras were obtained on medium imgs

        warped_final_imgs = list(warper.warp_images(final_imgs, cameras, camera_aspect))
        warped_final_masks = list(
            warper.create_and_warp_masks(final_sizes, cameras, camera_aspect)
        )
        final_corners, final_sizes = warper.warp_rois(
            final_sizes, cameras, camera_aspect
        )

        # cropper = Cropper()
        # low_corners = cropper.get_zero_center_corners(low_corners)
        # cropper.prepare(warped_low_imgs, warped_low_masks, low_corners, low_sizes)
        # cropped_low_masks = list(cropper.crop_images(warped_low_masks))
        # cropped_low_imgs = list(cropper.crop_images(warped_low_imgs))
        # low_corners, low_sizes = cropper.crop_rois(low_corners, low_sizes)
        # lir_aspect = images.get_ratio(Images.Resolution.LOW, Images.Resolution.FINAL)  # since lir was obtained on low imgs
        # cropped_final_masks = list(cropper.crop_images(warped_final_masks, lir_aspect))
        # cropped_final_imgs = list(cropper.crop_images(warped_final_imgs, lir_aspect))
        # final_corners, final_sizes = cropper.crop_rois(final_corners, final_sizes, lir_aspect)

        seam_finder = SeamFinder(finder="gc_color")  # voronoi
        seam_masks = seam_finder.find(warped_low_imgs, low_corners, warped_low_masks)
        seam_masks = [
            seam_finder.resize(seam_mask, mask)
            for seam_mask, mask in zip(seam_masks, warped_final_masks)
        ]
        seam_masks_plots = [
            SeamFinder.draw_seam_mask(img, seam_mask)
            for img, seam_mask in zip(warped_final_imgs, seam_masks)
        ]

        compensator = ExposureErrorCompensator()
        compensator.feed(low_corners, warped_low_imgs, warped_low_masks)
        compensated_imgs = [
            compensator.apply(idx, corner, img, mask)
            for idx, (img, mask, corner) in enumerate(
                zip(warped_final_imgs, warped_final_masks, final_corners)
            )
        ]

        blender = Blender(blender_type="no")
        blender.prepare(final_corners, final_sizes)
        for img, mask, corner in zip(compensated_imgs, seam_masks, final_corners):
            blender.feed(img, mask, corner)
        panorama, _ = blender.blend()
        print(time.time() - starttime)
        print("1.4 Stitching done")
        return panorama, indices, confmatrix

    except:
        print("Stitching Failed")
        return None, indices, confmatrix


def camera_corrector(src):
    width = src.shape[1]
    height = src.shape[0]
    distCoeff = np.zeros((4, 1), np.float64)
    # TODO: add your coefficients here!
    k1 = -8.0e-7
    # negative to remove barrel distortion
    k2 = 0.0
    p1 = 0.0
    p2 = 0.0
    distCoeff[0, 0] = k1
    distCoeff[1, 0] = k2
    distCoeff[2, 0] = p1
    distCoeff[3, 0] = p2
    # assume unit matrix for camera
    cam = np.eye(3, dtype=np.float32)
    cam[0, 2] = width / 2.0  # define center x
    cam[1, 2] = height / 2.0  # define center y
    cam[0, 0] = 10.0  # define focal length x
    cam[1, 1] = 10.0  # define focal length y
    # here the undistortion will be computed
    dst = cv2.undistort(src, cam, distCoeff)

    return dst


def create_panorama_image(filepaths):
    print(filepaths)
    os.makedirs("./temp", exist_ok=True)
    newfilepaths = []
    for i, filename in enumerate(filepaths):
        img = cv2.imread(filename)
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        img = camera_corrector(img)

        savename = "./temp/" + str(i) + ".jpg"
        cv2.imwrite(savename, img)
        newfilepaths.append(savename)

    finalimg = None
    indices = []
    cnt = 0
    while finalimg is None or len(indices) != len(newfilepaths):
        finalimg, indices, confmatrix = stitch(newfilepaths)
        cnt = cnt + 1
        if cnt >= 3:
            break

    if finalimg is None or len(indices) != len(newfilepaths):
        finalimg = None
        for impath in newfilepaths:
            img = cv2.imread(impath)
            if finalimg is None:
                finalimg = img
            else:
                h = finalimg.shape[0]
                w_buffer = int(img.shape[1] / 20)
                ratio = finalimg.shape[0] / img.shape[0]
                img = cv2.resize(img, (int(img.shape[1] * ratio), int(h)))
                buffer = np.zeros((h, w_buffer, 3)).astype("uint8")
                finalimg = np.concatenate((finalimg, buffer, img), axis=1)

    shutil.rmtree("./temp")
    return finalimg
