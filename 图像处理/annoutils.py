
import os


def cut_value_normal(val):
    val = max(val, 0.0)
    val = min(val, 1.0)
    return val*1.0




def center_d2center_f(center_x_d,center_y_d,w_d,h_d,height, width):
    center_x = cut_value_normal(1.0*center_x_d/width)
    center_y = cut_value_normal(1.0*center_y_d/height)
    rect_w =cut_value_normal(1.0*w_d/width)
    rect_h =cut_value_normal(1.0*h_d/height)
    return center_x,center_y,rect_w,rect_h

def rectify_center_f(center_x, center_y, rect_w, rect_h):
    xmin_f, ymin_f, xmax_f, ymax_f = center_f2xyxy_f(
        center_x, center_y, rect_w, rect_h)
    center_x, center_y, rect_w, rect_h = xyxy_f2center_f(
        xmin_f, ymin_f, xmax_f, ymax_f)
    return center_x, center_y, rect_w, rect_h


def xyxy2xyxy_f(xyxy, height, width):
    xmin, ymin, xmax, ymax = xyxy
    xmin_f = 1.0*xmin/width
    ymin_f = 1.0*ymin/height
    xmax_f = 1.0*xmax/width
    ymax_f = 1.0*ymax/height
    return xmin_f, ymin_f, xmax_f, ymax_f


def xyxy_f2center_f(xmin_f, ymin_f, xmax_f, ymax_f):
    center_x = cut_value_normal((xmax_f+xmin_f)/2)
    center_y = cut_value_normal((ymax_f+ymin_f)/2)
    rect_w = cut_value_normal(xmax_f-xmin_f)
    rect_h = cut_value_normal(ymax_f-ymin_f)
    return center_x, center_y, rect_w, rect_h


def xyxy2center_f(xyxy, height, width):
    xmin_f, ymin_f, xmax_f, ymax_f = xyxy2xyxy_f(xyxy, height, width)
    center_x, center_y, rect_w, rect_h = xyxy_f2center_f(
        xmin_f, ymin_f, xmax_f, ymax_f)
    return center_x, center_y, rect_w, rect_h


def center_f2xyxy_f(center_x, center_y, rect_w, rect_h):

    xmin_f = cut_value_normal(center_x - rect_w/2)
    ymin_f = cut_value_normal(center_y - rect_h/2)
    xmax_f = cut_value_normal(center_x + rect_w/2)
    ymax_f = cut_value_normal(center_y + rect_h/2)

    return xmin_f, ymin_f, xmax_f, ymax_f


def xyxy_f2xyxy(xmin_f, ymin_f, xmax_f, ymax_f, height, width):
    xmin = int(xmin_f*width)
    ymin = int(ymin_f*height)
    xmax = int(xmax_f*width)
    ymax = int(ymax_f*height)
    return xmin, ymin, xmax, ymax


def center_f2xyxy(center_x, center_y, rect_w, rect_h, height, width):
    xmin_f, ymin_f, xmax_f, ymax_f = center_f2xyxy_f(
        center_x, center_y, rect_w, rect_h)
    xmin, ymin, xmax, ymax = xyxy_f2xyxy(
        xmin_f, ymin_f, xmax_f, ymax_f, height, width)

    return xmin, ymin, xmax, ymax


def center_f2center_int(center_x, center_y, rect_w, rect_h, height, width):
    rect_w_int = int(rect_w*width)
    rect_h_int = int(rect_h*height)
    center_x_int = int(center_x*width)
    center_y_int = int(center_y*height)

    return center_x_int, center_y_int, rect_w_int, rect_h_int


def expand_center_normal(center_x, center_y, rect_w, rect_h):

    center_x, center_y, rect_w, rect_h = rectify_center_f(
        center_x, center_y, rect_w, rect_h)

    return center_x, center_y, rect_w, rect_h





def expand_center(center_x, center_y, rect_w, rect_h, expand_method, expand_rate, height, width):

    if expand_method == "normal":
        print("+++++normal++++++")
        center_x, center_y, rect_w, rect_h = expand_center_normal(
            center_x, center_y, rect_w, rect_h)

    elif expand_method == "bigger_rect":
        print("+++++bigger_rect,rate=",expand_rate)
        # xmin, ymin, xmax, ymax = center_f2xyxy(center_x,center_y,rect_w,rect_h,height, width)
        rect_w_int = int(rect_w*width)
        rect_h_int = int(rect_h*height)

        bigger_side = max(rect_w_int, rect_h_int)
        # bigger_side=512
        # if bigger_side<20:
        #     bigger_size=20



        rect_w = 1.0*bigger_side/width
        rect_h = 1.0*bigger_side/height
        rect_w = rect_w*(expand_rate)
        rect_h = rect_h*(expand_rate)
        center_x, center_y, rect_w, rect_h = expand_center_normal(
            center_x, center_y, rect_w, rect_h)


    xmin, ymin, xmax, ymax = center_f2xyxy(
        center_x, center_y, rect_w, rect_h, height, width)
    return xmin, ymin, xmax, ymax



