import argparse
import cv2 as cv
from pathvalidate.argparse import sanitize_filepath_arg
from gbf_automata.schema.image import ImageModel
from gbf_automata.enums.template_match import TemplateMatch

parse = argparse.ArgumentParser(
    prog="Template matching",
    description="Find objects in an image using template matching method",
)
parse.add_argument("-i", "--image", type=sanitize_filepath_arg)
parse.add_argument("-t", "--template", type=sanitize_filepath_arg)

if __name__ == "__main__":
    args = parse.parse_args()

    template_rgb = cv.imread(args.template)

    template_gray = cv.cvtColor(template_rgb, cv.COLOR_BGR2GRAY)

    image = cv.imread(args.image, cv.IMREAD_UNCHANGED)

    image_souce = template_rgb.copy()

    w, h = image.shape[::-1]

    method = TemplateMatch.TM_CCORR_NORMED

    res = cv.matchTemplate(template_gray, image, method)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)

    image_area = ImageModel(
        method=method,
        image_width=w,
        image_height=h,
        min_val=min_val,
        max_val=max_val,
        min_loc=min_loc,
        max_loc=max_loc,
    )

    top_left, bottom_right = image_area.plot_area()

    cv.namedWindow("Souce", cv.WINDOW_KEEPRATIO)
    cv.rectangle(image_souce, top_left, bottom_right, (0, 0, 255), 4)
    cv.imshow("Souce", image_souce)
    cv.waitKey(0)
