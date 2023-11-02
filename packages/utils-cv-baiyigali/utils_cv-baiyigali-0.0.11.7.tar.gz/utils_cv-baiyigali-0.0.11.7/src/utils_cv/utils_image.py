import cv2
import numpy as np


def binarize(im, show=False):
    if len(im.shape) == 3 and im.shape[2] == 3:
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    ret, dst = cv2.threshold(im, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    if show:
        cv2.imshow('bin', dst)
        cv2.waitKey(0)
    return dst


def binarize_small(im, height_persentage=1, show=False):
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    width = im_gray.shape[1]
    height = im_gray.shape[0]
    if show:
        print(im_gray.shape)
    dh = int(height * height_persentage)
    dw = dh
    nw = int(width // dw)
    nh = int(height // dh)
    ret, dst = cv2.threshold(im_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    dst_block = np.copy(dst)
    for w in range(nw):
        for h in range(nh):
            ret, dst_block[dh * h:dh * (h + 1), dw * w:dw * (w + 1)] = cv2.threshold(
                im_gray[dh * h:dh * (h + 1), dw * w:dw * (w + 1)], 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    ret, dst_block[:, -dh:] = cv2.threshold(im_gray[:, -dh:], 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    if show:
        cv2.imshow('bin', dst)
        cv2.imshow('bin_block', dst_block)
        cv2.waitKey(0)
    return dst_block


def image_dilate(im, width, height, show=False):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (width, height))
    dilate = cv2.dilate(im, kernel)
    if show:
        cv2.imshow('dilate', dilate)
        cv2.waitKey(0)
    return dilate


def image_close(im, width, height, show=False):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (width, height))
    closed = cv2.morphologyEx(im, cv2.MORPH_CLOSE, kernel)
    if show:
        cv2.imshow('closed', closed)
        cv2.waitKey(0)
    return closed


def image_open(im, width, height, show=False):
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (width, height))
    opened = cv2.morphologyEx(im, cv2.MORPH_OPEN, kernel)
    if show:
        cv2.imshow('opened', opened)
        cv2.waitKey(0)
    return opened


def get_boundray(histogram, space):
    space = int(space)
    max_density = 0
    max_index = 0
    for i in range(len(histogram) - space):
        density_tmp = sum(histogram[i:i + space])
        if density_tmp > max_density:
            max_density = density_tmp
            max_index = i
    return max_index


def cc_analyze(im_bin, show=False):
    connectivity = 4
    # Perform the operation
    output = cv2.connectedComponentsWithStats(im_bin, connectivity, cv2.CV_16U)
    # Get the results
    # The first cell is the number of labels
    num_labels = output[0]
    # The second cell is the label matrix
    labels = output[1]
    # The third cell is the stat matrix
    stats = output[2]
    # The fourth cell is the centroid matrix
    centroids = output[3]
    if show:
        cv2.imshow('cc', np.array(labels, dtype=np.uint8))
        cv2.waitKey(0)


def get_roi_with_perspective(im_path, target, border=0.1):
    target = np.float32(target).reshape([4, 2])
    target_left_top = target[0]
    target_right_top = target[1]
    target_right_bottom = target[2]
    target_left_bottom = target[3]
    target_top = (target_right_top - target_left_top)[0]
    target_bottom = (target_right_bottom - target_left_bottom)[0]
    target_left = (target_left_bottom - target_left_top)[1]
    target_right = (target_right_bottom - target_right_top)[1]
    border = border
    new_target_left_top = target[0] + np.array([-target_top * border, -target_left * border])
    new_target_right_top = target[1] + np.array([target_top * border, -target_right * border])
    new_target_right_bottom = target[2] + np.array([target_bottom * border, target_right * border])
    new_target_left_bottom = target[3] + np.array([-target_bottom * border, target_left * border])

    new_target_top = target_top + target_top * border * 2
    new_target_bottom = target_bottom + target_bottom * border * 2
    new_target_left = target_left + target_left * border * 2
    new_target_right = target_right + target_right * border * 2

    # new_width=(new_target_top+new_target_bottom)/2
    # new_height=(new_target_left+new_target_right)/2
    new_width = 560
    new_height = 400
    src = np.float32([new_target_left_top, new_target_right_top, new_target_right_bottom, new_target_left_bottom])

    dst = np.float32([0, 0, new_width, 0, new_width, new_height, 0, new_height]).reshape([4, 2])

    im = cv2.imread(im_path)
    perspective_mat = cv2.getPerspectiveTransform(src, dst)
    im_perspective = cv2.warpPerspective(im, perspective_mat, (int(new_width), int(new_height)))

    in_point = target.reshape([1, 4, 2])
    out_point = cv2.perspectiveTransform(in_point, perspective_mat)
    out_point = np.array(out_point, dtype=np.float32).reshape([-1])
    return im_perspective, out_point


def get_roi_with_border(im, target, border=0.5):
    log = False
    if log:
        print(target)
    width = im.shape[1]
    height = im.shape[0]

    points = np.array(target, dtype=int).reshape([4, 2])
    p_x_min = points.min(0)[0]
    p_y_min = points.min(0)[1]
    p_x_max = points.max(0)[0]
    p_y_max = points.max(0)[1]

    left = p_x_min
    right = p_x_max
    top = p_y_min
    bottom = p_y_max
    target_width = right - left
    target_height = bottom - top

    x_border = int(target_width * border)
    y_border = int(target_height * border)

    new_left = left - x_border
    if new_left < 0:
        new_left = 0
    new_top = top - y_border
    if new_top < 0:
        new_top = 0
    new_right = right + x_border
    if new_right > width:
        new_right = width
    new_bottom = bottom + y_border
    if new_bottom > height:
        new_bottom = height

    im = im[:, new_left:new_right]
    im = im[new_top:new_bottom, :]

    shift = np.array([new_left, new_top], dtype=int)
    for i in range(len(points)):
        points[i] = points[i] - np.array(shift)

    new_target_points = np.array(points, dtype=np.float32).reshape([-1])

    return im, new_target_points, shift


def get_clear_sample(im, target):
    target = np.float32(target).reshape([4, 2])
    target_left_top = target[0]
    target_right_top = target[1]
    target_right_bottom = target[2]
    target_left_bottom = target[3]
    target_top = (target_right_top - target_left_top)[0]
    target_bottom = (target_right_bottom - target_left_bottom)[0]
    target_left = (target_left_bottom - target_left_top)[1]
    target_right = (target_right_bottom - target_right_top)[1]
    border = 0.2
    new_target_left_top = target[0] + np.array([-target_top * border, -target_left * border])
    new_target_right_top = target[1] + np.array([target_top * border, -target_right * border])
    new_target_right_bottom = target[2] + np.array([target_bottom * border, target_right * border])
    new_target_left_bottom = target[3] + np.array([-target_bottom * border, target_left * border])

    new_target_top = target_top + target_top * border * 2
    new_target_bottom = target_bottom + target_bottom * border * 2
    new_target_left = target_left + target_left * border * 2
    new_target_right = target_right + target_right * border * 2

    new_width = (new_target_top + new_target_bottom) / 2
    new_height = (new_target_left + new_target_right) / 2
    # new_width=560
    # new_height=400
    src = np.float32([new_target_left_top, new_target_right_top, new_target_right_bottom, new_target_left_bottom])

    dst = np.float32([0, 0, new_width, 0, new_width, new_height, 0, new_height]).reshape([4, 2])

    perspective_mat = cv2.getPerspectiveTransform(src, dst)
    im_perspective = cv2.warpPerspective(im, perspective_mat, (int(new_width), int(new_height)))

    in_point = target.reshape([1, 4, 2])
    out_point = cv2.perspectiveTransform(in_point, perspective_mat)
    out_point = np.array(out_point, dtype=np.float32).reshape([-1])
    return im_perspective, out_point


def get_original_coordinate(target, shift, scale):
    target = np.array(target, dtype=np.float32).reshape([-1, 2])
    for i in range(len(target)):
        target[i] = target[i] / scale
        target[i] = target[i] - shift
    return target


def shift_image_point(im, target):
    log = False
    width = im.shape[1]
    height = im.shape[0]

    points = np.array(target, dtype=int).reshape([4, 2])
    p_x_min = points.min(0)[0]
    p_y_min = points.min(0)[1]
    p_x_max = points.max(0)[0]
    p_y_max = points.max(0)[1]

    left_border = p_x_min
    right_border = width - p_x_max
    top_border = p_y_min
    bottom_border = height - p_y_max

    x_shift = -left_border // 4
    y_shift = 0

    im_shift = im
    BLACK = [0, 0, 0]
    if y_shift < 0:
        im_shift = im_shift[-y_shift:, :]
        im_shift = cv2.copyMakeBorder(im_shift, 0, -y_shift, 0, 0, cv2.BORDER_CONSTANT, value=BLACK)
    else:
        im_shift = im_shift[:height - y_shift, :]
        im_shift = cv2.copyMakeBorder(im_shift, y_shift, 0, 0, 0, cv2.BORDER_CONSTANT, value=BLACK)
    if x_shift < 0:
        im_shift = im_shift[:, -x_shift:]
        im_shift = cv2.copyMakeBorder(im_shift, 0, 0, 0, -x_shift, cv2.BORDER_CONSTANT, value=BLACK)
    else:
        im_shift = im_shift[:, :width - x_shift]
        im_shift = cv2.copyMakeBorder(im_shift, 0, 0, x_shift, 0, cv2.BORDER_CONSTANT, value=BLACK)

    points_shift = points + np.array([[x_shift, y_shift]] * 4, dtype=int)

    if log:
        cv2.imshow('shift', im_shift)
        cv2.waitKey(0)
    return im_shift, points_shift.reshape([-1])


def get_roi(im, target, mode='4points', log=False):
    target = np.array(target, dtype=np.int32)
    if mode == '4points':
        width = im.shape[1]
        height = im.shape[0]

        points = np.array(target, dtype=int).reshape([4, 2])
        p_x_min, p_y_min = np.min(points, axis=0)
        p_x_max, p_y_max = np.max(points, axis=0)

        left = max(p_x_min, 0)
        top = max(p_y_min, 0)
        right = min(p_x_max, width)
        bottom = min(p_y_max, height)
        im_roi = im[top:bottom, left:right]
        return im_roi
    elif mode == 'rect':
        target = np.reshape(target, [4])
        left, top, right, bottom = target
    elif mode == 'box':
        target = np.reshape(target, [4])
        left, top, w, h = target
        bottom = top + h
        right = left + w
    else:
        raise Exception('mode error ', mode)
    top=max(0,top)
    left=max(0,left)
    bottom=min(im.shape[0],bottom)
    right=min(im.shape[1],right)
    im_roi = im[top:bottom, left:right]
    return im_roi


def resize(im, width, height):
    x_shift = 0
    y_shift = 0
    if im.shape[0] * im.shape[1] == 0:
        print('image width or height is zero...\n\n')
    if (im.shape[1] / im.shape[0] > width / height):
        border = int(im.shape[1] * height / width - im.shape[0])
        if border % 2 == 0:
            im = cv2.copyMakeBorder(im, border // 2, border // 2, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        else:
            im = cv2.copyMakeBorder(im, border // 2, border // 2 + 1, 0, 0, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        y_shift = border // 2
    else:
        border = int(im.shape[0] * width / height - im.shape[1])
        if border % 2 == 0:
            im = cv2.copyMakeBorder(im, 0, 0, border // 2, border // 2, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        else:
            im = cv2.copyMakeBorder(im, 0, 0, border // 2, border // 2 + 1, cv2.BORDER_CONSTANT, value=[0, 0, 0])
        x_shift = border // 2
    scale = width / im.shape[1]
    im = cv2.resize(im, (width, height))
    return (x_shift, y_shift), scale, im


def show_result(im_draw, original_points, predicted_points):
    original_points = np.array(original_points, dtype=int).reshape([-1, 2])
    predicted_points = np.array(predicted_points, dtype=int).reshape([-1, 2])
    for p in range(len(original_points)):
        cv2.circle(im_draw, (original_points[p][0], original_points[p][1]), 2, (0, 255, 0), 2)
        cv2.circle(im_draw, (predicted_points[p][0], predicted_points[p][1]), 2, (255, 0, 0), 2)
    cv2.imshow('result', im_draw)
    cv2.waitKey(0)


def show_conv(conv, title='conv', swap=None):
    conv = np.array(np.array(conv, dtype=np.float32) * 255, dtype=np.uint8)
    shape = conv.shape
    chanel = shape[-1]
    for i in range(chanel):
        im_draw = conv[0, :, :, i]
        if swap:
            im_draw = im_draw.swapaxes(0, 1)
        cv2.imshow(title + '{}'.format(i), im_draw)
        cv2.waitKey(0)


def show_conv_plot(conv, title='conv', swap=None, show=False):
    conv = np.array(np.array(conv, dtype=np.float32) * 255, dtype=np.uint8)
    shape = conv.shape
    chanel = shape[-1]
    raw = 6
    col = chanel // raw + 1
    fig = plt.figure(title)
    for i in range(chanel):
        im_draw = conv[0, :, :, i]
        if swap:
            im_draw = im_draw.swapaxes(0, 1)
        ax = fig.add_subplot(raw, col, i + 1)
        ax.imshow(im_draw, cmap="gray")
        # ax.imshow(im_draw)
        ax.set_title(i + 1)
        plt.axis("off")
    if show:
        # plt.show(block=True)
        plt.show()


def show_rect(im, rect):
    rect = np.array(rect, np.int16).reshape([-1, 2])
    cv2.rectangle(im, (rect[0][0], rect[0][1]), (rect[1][0], rect[1][1]), [255, 0, 0], 2)
    cv2.imshow('rect', im)
    cv2.waitKey(0)


def draw_rect(im, rect, color=None,thickness=2):
    if color is None:
        color = [255, 0, 0]
    rect = np.array(rect, np.int16).reshape([4])
    cv2.rectangle(im, (rect[0], rect[1]), (rect[2], rect[3]), color, thickness=thickness)
    return im

def draw_rects(im, rects, color=None,thickness=2):
    if color is None:
        color = [255, 0, 0]
    rects = np.array(rects, np.int16).reshape([-1,4])
    for rect in rects:
        cv2.rectangle(im, (rect[0], rect[1]), (rect[2], rect[3]), color, thickness=thickness)
    return im

def draw_box(im, box, color=None, thickness=2):
    if color is None:
        color = [255, 0, 0]
    box = np.array(box).reshape([4])
    rect = np.array([box[0], box[1], box[0] + box[2], box[1] + box[3]], dtype=np.int16)
    cv2.rectangle(im, (rect[0], rect[1]), (rect[2], rect[3]), color, thickness=thickness)
    return im


def draw_4point(im, points, color=None):
    if color is None:
        color = [255, 0, 0]
    points = np.array(points, dtype=np.int32).reshape([4, 1, 2])
    im = cv2.polylines(im, [points], True, color)

    return im


def show_points(im, points):
    points = np.array(points, np.int16).reshape([-1, 2])
    for i in points:
        cv2.circle(im, (points[i][0], points[i][1]), [255, 0, 0], 2)
    cv2.imshow('rect', im)
    cv2.waitKey(0)


def show_image(im, title='title', wait=0):
    if im is None:
        raise Exception("image is None")
    width = im.shape[1]
    height = im.shape[0]
    scale = 1
    while height > 700 or width > 1000:
        width *= 0.9
        height *= 0.9
        scale *= 0.9
    im = cv2.resize(im, None, fx=scale, fy=scale)
    cv2.imshow(title, im)
    cv2.waitKey(wait)


def four_point_to_mask(im, point, color=255, show=False):
    point = np.array(point, dtype=np.int32)
    points = point.reshape([4, 1, 2])
    im = cv2.fillPoly(im, [points], color)
    if show:
        cv2.imshow('im', im)
        cv2.waitKey(0)
    return im


def box_to_mask(im, box, color=255, show=False):
    box = np.array(box, dtype=np.int32).reshape([4])
    im = cv2.rectangle(im, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), color, cv2.FILLED)
    if show:
        cv2.imshow('im', im)
        cv2.waitKey(0)
    return im


def rect_to_mask(im, box, color=255, show=False):
    box = np.array(box, dtype=np.int32).reshape([4])
    im = cv2.rectangle(im, (box[0], box[1]), (box[2], box[3]), color, cv2.FILLED)
    if show:
        cv2.imshow('im', im)
        cv2.waitKey(0)
    return im


def rect_to_mask_border(im, box, thickness, show=False):
    box = np.array(box, dtype=np.int32).reshape([4])
    im = cv2.rectangle(im, (box[0], box[1]), (box[2], box[3]), 1, cv2.FILLED)
    im = cv2.rectangle(im, (box[0], box[1]), (box[2], box[3]), 2, thickness)
    return im


def poly_to_mask_border(im, poly, thickness, show=False):
    poly = np.array(poly, dtype=np.int32).reshape([1, -1, 2])
    im = cv2.fillPoly(im, poly, 1)
    im = cv2.polylines(im, poly, True, 2, thickness)
    if show:
        cv2.imshow('im', im)
        cv2.waitKey(0)
    return im


def rect_to_mask_no_corner(im, box, color=255, show=False):
    box = np.array(box, dtype=np.int32).reshape([4])
    w = box[2] - box[0]
    h = box[3] - box[1]
    dh = int(h / 2.0)
    dh = min(dh, int(w / 2.0))
    p1 = [box[0], box[1] + dh]
    p2 = [box[0] + dh, box[1]]
    p3 = [box[2] - dh, box[1]]
    p4 = [box[2], box[1] + dh]
    p5 = [box[2] - dh, box[3]]
    p6 = [box[0] + dh, box[3]]
    points = np.array([p1, p2, p3, p4]).reshape([1, -1, 2])
    im = cv2.fillPoly(im, points, color)
    points = np.array([p1, p4, p5, p6]).reshape([1, -1, 2])
    im = cv2.fillPoly(im, points, 128)

    if show:
        cv2.imshow('im', im)
    cv2.waitKey(0)
    return im


def rect_to_mask_no_corner_2chanel(im, box, color=255, show=False):
    assert im.shape[2] >= 2, 'image must be greater than 2 chanel'
    box = np.array(box, dtype=np.int32).reshape([4])
    w = box[2] - box[0]
    h = box[3] - box[1]
    dh = int(h / 2.0)
    dh = min(dh, int(w / 2.0))
    p1 = [box[0], box[1] + dh]
    p2 = [box[0] + dh, box[1]]
    p3 = [box[2] - dh, box[1]]
    p4 = [box[2], box[1] + dh]
    p5 = [box[2] - dh, box[3]]
    p6 = [box[0] + dh, box[3]]
    points = np.array([p1, p2, p3, p4]).reshape([1, -1, 2])
    im = cv2.fillPoly(im, points, [color, 0, 0])
    # show_image(m, 'm')
    # print(m)
    points = np.array([p1, p4, p5, p6]).reshape([1, -1, 2])
    im = cv2.fillPoly(im, points, [0, color, 0])

    if show:
        cv2.imshow('im', im)
    cv2.waitKey(0)
    return im


def rect_to_mask_up_below_se_3chanel(im, box, color=255, show=False):
    assert im.shape[2] >= 2, 'image must be greater than 2 chanel'
    box = np.array(box, dtype=np.int32).reshape([4])
    h = box[3] - box[1]
    dh = int(h / 2.0)
    im = cv2.rectangle(im, (box[0], box[1]), (box[2], box[3] - dh), [255, 0, 0], cv2.FILLED)
    im = cv2.rectangle(im, (box[0], box[1] + dh), (box[2], box[3]), [0, 255, 0], cv2.FILLED)
    im = cv2.rectangle(im, (box[0] - 5, box[1]), (box[0], box[3]), [0, 0, 255], cv2.FILLED)
    im = cv2.rectangle(im, (box[2], box[1]), (box[2] + 5, box[3]), [0, 0, 255], cv2.FILLED)

    if show:
        cv2.imshow('im', im)
    cv2.waitKey(0)
    return im


def rect_to_mask_linear(im, box, color=255, show=False):
    box = np.array(box, dtype=np.int32).reshape([4])
    w = box[2] - box[0]
    h = box[3] - box[1]
    kx = 255.0 / w
    ky = 255.0 / h

    row = np.zeros(w, dtype=np.uint8)
    for x in range(w):
        row[x] = int(x * kx)
    col = np.zeros(h, dtype=np.uint8)
    for y in range(h):
        col[y] = int(y * ky)

    mask = np.zeros([h, w, 3], dtype=np.uint8)
    for x in range(w):
        mask[:, x, 0] = col
    for y in range(h):
        mask[y, :, 1] = row

    im[box[1]:box[3], box[0]:box[2]] = mask

    if show:
        # im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        cv2.imshow('im', im)
        cv2.waitKey(0)
    return im


def rect_to_mask_log(im, box, color=255, show=False):
    box = np.array(box, dtype=np.int32).reshape([4])
    w = box[2] - box[0]
    h = box[3] - box[1]
    kx = 255.0 / w
    ky = 255.0 / h
    cx = (box[0] + box[2]) / 2.0
    cy = (box[1] + box[3]) / 2.0

    row = np.zeros(w, dtype=np.uint8)
    for x in range(w):
        row[x] = int(x * kx)
    col = np.zeros(h, dtype=np.uint8)
    for y in range(h):
        col[y] = int(y * ky)

    mask = np.zeros([h, w, 3], dtype=np.uint8)
    for x in range(w):
        mask[:, x, 0] = col
    for y in range(h):
        mask[y, :, 1] = row

    im[box[1]:box[3], box[0]:box[2]] = mask

    if show:
        im = cv2.cvtColor(im, cv2.COLOR_BAYER_BG2GRAY)
        cv2.imshow('im', im)
        cv2.waitKey(0)
    return im


def get_perspective(p_src, strength=0.2):
    p_src = np.array(p_src, dtype=np.float32)
    p_dst = np.array(p_src, dtype=np.float32)
    width, height = np.max(p_src, axis=0) - np.min(p_src, axis=0)

    def dx():
        return np.random.uniform(0, width * strength)

    def dy():
        return np.random.uniform(0, height * strength)

    r = np.random.randint(0, 100)
    if r < 25:
        p_dst[0] += np.array([-dx(), -dy()])
        p_dst[2] += np.array([dx(), dy()])
    elif r < 50:
        p_dst[1] += np.array([dx(), -dy()])
        p_dst[3] += np.array([-dx(), dy()])
    elif r < 75:
        p_dst[0] += np.array([-dx(), -dy()])
        p_dst[3] += np.array([-dx(), dy()])
    elif r <= 100:
        p_dst[1] += np.array([dx(), -dy()])
        p_dst[2] += np.array([dx(), dy()])

    p_dst -= np.min(p_dst, axis=0)
    p_dst = np.float32(p_dst)

    p_mat = cv2.getPerspectiveTransform(p_src, p_dst)
    return p_mat


def box_to_4point(box):
    point = [[box[0], box[1]],
             [box[0] + box[2], box[1]],
             [box[0] + box[2], box[1] + box[3]],
             [box[0], box[1] + box[3]]]
    return point


def rect_to_4point(rect):
    rect = np.array(rect).reshape([4])
    point = [[rect[0], rect[1]],
             [rect[2], rect[1]],
             [rect[2], rect[3]],
             [rect[0], rect[3]]]
    return point


def warp_perspective(im, perspective_mat, out_width, out_height, fix_out_size=True):
    if fix_out_size:
        # determine output shape
        im_box = [0, 0, im.shape[1], im.shape[0]]
        im_4point = np.float32(box_to_4point(im_box))
        in_point = im_4point.reshape([1, 4, 2])
        out_point = cv2.perspectiveTransform(in_point, perspective_mat)
        out_point = np.array(out_point, dtype=np.int16).reshape([4, 2])

        left, top = np.min(out_point, axis=0)
        if left < 0 or top < 0:
            raise Exception('perspective transform loss image at top left')

        right, bottom = np.max(out_point, axis=0)
        if right != out_width or bottom != out_height:
            out_width = right
            out_height = bottom

    im_perspective = cv2.warpPerspective(im, perspective_mat, (out_width, out_height))
    return im_perspective


def add_light(im, strength=0.1, show=False):
    size = 100
    center = (np.random.randint(0, size), np.random.randint(0, size))
    spread = ((np.random.uniform(size * 5, size * 10), 0), (0, np.random.uniform(size * 5, size * 10)))
    a = np.random.multivariate_normal(center, spread, size * size * 10)

    a = np.array(a, dtype=np.int64)

    light = np.zeros((size, size), np.float32)
    for pos in a:
        if 0 <= pos[0] < size and 0 <= pos[1] < size:
            light[pos[0], pos[1]] += strength

    light = (light / np.max(light) * 255).astype(np.uint8)
    light = cv2.resize(light, (im.shape[1], im.shape[0]))
    light = blur(light, kernel=np.random.randint(size // 20, size // 10) // 2 * 2 + 1,
                 sigma=np.random.randint(size // 20, size // 10) + 1)
    light = (light / np.max(light) * 255).astype(np.uint8)

    im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
    v = im[:, :, 2].astype(np.int32) + light.astype(np.int32)
    v = (v / np.max(v) * 255).astype(np.uint8)
    im[:, :, 2] = v

    im = cv2.cvtColor(im, cv2.COLOR_HSV2BGR)
    if show:
        show_image(light, 'light')
        show_image(im, 'im')
    return im


def blur(img, sigma=1, kernel=None):
    if kernel is None:
        kernel_list = [3, 5]
    else:
        kernel_list = [kernel]
    kernel = np.random.choice(kernel_list)
    return cv2.GaussianBlur(img, (kernel, kernel), sigma)


def expand_4point(point4, scale, side='all'):
    point4 = np.array(point4, dtype=np.int).reshape([4, 2])
    x_min, y_min = np.min(point4, axis=0)
    x_max, y_max = np.max(point4, axis=0)
    w = x_max - y_min
    h = y_max - y_min
    dw = int(w * scale)
    dh = int(h * scale)
    if side == 'all':
        point4[[0, 3], 0] -= dw
        point4[[1, 2], 0] += dw
        point4[[0, 1], 1] -= dh
        point4[[2, 3], 1] += dh
    elif side == 'left':
        point4[[0, 3], 0] -= dw
    elif side == 'right':
        point4[[1, 2], 0] += dw
    elif side == 'up':
        point4[[0, 1], 1] -= dh
    elif side == 'down':
        point4[[2, 3], 1] += dh
    else:
        raise Exception('side mode error: ' + side)
    return point4


def sort_4point(four_point, debug=False):
    four_point = np.array(four_point)
    four_point = np.reshape(four_point, [4, 2])

    four_point = sorted(four_point, key=lambda x: x[0])
    four_point[:2] = sorted(four_point[:2], key=lambda x: x[1])
    four_point[1:] = sorted(four_point[1:], key=lambda x: -x[0])
    four_point[1:3] = sorted(four_point[1:3], key=lambda x: x[1])

    four_point = np.reshape(four_point, [4, 2])
    return four_point


def get_roi_perspective(im, src, dst=None, show=False):
    src = np.array(src, dtype=np.int).reshape([4, 2])
    src = sort_4point(src, debug=True)
    if dst is None:
        mask = np.zeros(im.shape[:2], dtype=np.uint8)
        mask = four_point_to_mask(mask, src, color=1)
        area = np.sum(mask)
        width = np.max(src, axis=0)[0] - np.min(src, axis=0)[0]
        height = area // width
        dst = box_to_4point([0, 0, width, height])

    dst = np.array(dst, dtype=np.int).reshape([4, 2])
    width, height = np.max(dst, axis=0) - np.min(dst, axis=0)

    src = np.float32(src)
    dst = np.float32(dst)

    perspective_mat = cv2.getPerspectiveTransform(src, dst)
    roi = cv2.warpPerspective(im, perspective_mat, (width, height))

    return roi


def get_min_area_box(mask, log=False):
    vert = np.sum(mask, axis=1)
    hori = np.sum(mask, axis=0)
    y_min = 0
    x_min = 0
    y_max = mask.shape[0] - 1
    x_max = mask.shape[1] - 1
    for y in range(len(vert)):
        if vert[y] > 0:
            y_min = y
            break
    for y in range(len(vert)):
        if vert[-y] > 0:
            y_max = y_max - y
            break
    for x in range(len(hori)):
        if hori[x] > 0:
            x_min = x
            break
    for x in range(len(hori)):
        if hori[-x] > 0:
            x_max = x_max - x
            break
    return [x_min, y_min, x_max - x_min, y_max - y_min]


def get_cc(im_bin, area_thresh=3 * 3):
    im_bin = binarize(im_bin)
    connectivity = 8
    output = cv2.connectedComponentsWithStats(im_bin, connectivity, cv2.CV_32S)
    num_labels = output[0]
    labels = output[1]
    stats = output[2]
    centroids = output[3]
    cc_list = []
    for i in range(1, len(stats)):
        if stats[i][4] > area_thresh:
            cc_list.append(stats[i][:4])
    return cc_list


def get_cc_rrect(im_bin, area_thresh=3 * 3):
    im_bin = binarize(im_bin)
    connectivity = 8
    output = cv2.connectedComponentsWithStats(im_bin, connectivity, cv2.CV_32S)
    num_labels = output[0]
    labels = output[1]
    stats = output[2]
    centroids = output[3]
    rrect_list = []
    for i in range(1, len(stats)):
        if stats[i][4] > area_thresh:
            statsi = stats[i]
            maski = labels[statsi[1]:statsi[1] + statsi[3], statsi[0]:statsi[0] + statsi[2]]
            rrect = cv2.minAreaRect(np.stack(np.where(maski == i), axis=1))
            rrect = ((rrect[0][0] + statsi[1], rrect[0][1] + statsi[0]), (rrect[1][0], rrect[1][1]), rrect[2])
            rrect_list.append(rrect)
    return rrect_list


def contrast(image, alpha):
    mean = np.mean(image, axis=(0, 1), keepdims=True)
    image = (image - mean) * alpha + mean
    image = np.clip(image, 0, 255)
    image = image.astype(np.uint8)
    return image


def brightness(image, alpha):
    image = image + alpha
    image = np.clip(image, 0, 255)
    image = image.astype(np.uint8)
    return image


def hue(image, alpha):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    image[..., 0] = image[..., 0] * alpha
    image[..., 0] = np.clip(image[..., 0], 0, 180)
    image = image.astype(np.uint8)
    image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
    return image


def saturation(image, alpha):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    image[..., 1] = image[..., 1] * alpha
    image = np.clip(image, 0, 255)
    image = image.astype(np.uint8)
    image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
    return image


def value(image, alpha):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    v = image[..., 2].astype(np.float32)
    v = v * alpha
    v = np.clip(v, 0, 255)
    image[..., 2] = v.astype(np.uint8)
    image = cv2.cvtColor(image, cv2.COLOR_HSV2BGR)
    return image


def noise_gaussian(image, alpha, beta):
    # alpha [0,30]
    # beta [0,30]
    gauss = np.random.normal(alpha, beta, image.shape)
    image = image + gauss
    image = np.clip(image, 0, 255)
    image = image.astype(np.uint8)
    return image


def get_perspective_transform(src, dst):
    src = np.array(src, dtype=np.float32).reshape([4, 2])
    dst = np.array(dst, dtype=np.float32).reshape([4, 2])
    mat = cv2.getPerspectiveTransform(src, dst)
    return mat


def perspective_transform(src, mat):
    src = np.array(src, dtype=np.float32).reshape([1, -1, 2])
    dst = cv2.perspectiveTransform(src, mat)
    dst = np.array(dst, dtype=np.float32).reshape([-1, 2])
    return dst


def warp_perspective_simple(im, mat, width, height):
    im = cv2.warpPerspective(im, mat, (width, height))
    return im
def draw_poly(im, poly, color=None,thickness=2):
    poly = np.array(poly, dtype=np.int32).reshape([1, -1, 2])
    im = cv2.polylines(im, poly, True, color, thickness)
    return im

def draw_circles(im, pts, r=3, color=None,thickness=2):
    pts=np.array(pts,dtype=np.int32).reshape([-1,2])
    for pt in pts:
        im = cv2.circle(im, tuple(pt),r , color, thickness,-1)
    return im