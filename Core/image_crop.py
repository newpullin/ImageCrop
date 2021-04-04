from PIL import Image


def image_crop(infilename, target_path, save_path, left_top_right_bottom):
    """
    image file 와 crop한이미지를 저장할 path 을 입력받아 crop_img를 저장한다.
    :param infilename:
        crop할 대상 image file 입력으로 넣는다.
    :param save_path:
        crop_image file의 저장 경로를 넣는다.
    :return:
    """

    img = Image.open(target_path + "/" + infilename)
    (img_w, img_h) = img.size

    start_left = left_top_right_bottom[0]
    end_right = img_w - left_top_right_bottom[2]
    start_top = left_top_right_bottom[1]
    end_bottom = img_h - left_top_right_bottom[3]

    bbox = (start_left, start_top, end_right, end_bottom)

    crop_img = img.crop(bbox)
    save_name = save_path + "/" + infilename
    crop_img.save(save_name)

    return True