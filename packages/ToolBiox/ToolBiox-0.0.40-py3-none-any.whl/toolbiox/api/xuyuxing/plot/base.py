from matplotlib.path import Path
from toolbiox.lib.xuyuxing.base.console import green, dark
import matplotlib.cbook as cbook
import matplotlib.patches as Patches
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import numpy as np
import sys


class STICK_PLOT():
    def get_patch(self, start_point, end_point, ax, thickness=2, linewidth=2, alpha=1, facecolor='b', edgecolor='k', bulge=0.67):

        x1, y1 = start_point
        x2, y2 = end_point

        l = np.sqrt(np.square(x1-x2) + np.square(y1-y2))

        # 0-base
        p1 = 0, thickness/2
        p2 = l, thickness/2
        p3 = l+thickness*bulge, thickness/2
        p4 = l+thickness*bulge, -thickness/2
        p5 = l, -thickness/2
        p6 = 0, -thickness/2
        p7 = 0-thickness*bulge, -thickness/2
        p8 = 0-thickness*bulge, thickness/2

        # transforms
        deg = self.get_rotate_deg(y2-y1, x2-x1)
        trans = (x1, y1)

        tp1 = self.get_transforms_point(p1, deg, trans, ax)
        tp2 = self.get_transforms_point(p2, deg, trans, ax)
        tp3 = self.get_transforms_point(p3, deg, trans, ax)
        tp4 = self.get_transforms_point(p4, deg, trans, ax)
        tp5 = self.get_transforms_point(p5, deg, trans, ax)
        tp6 = self.get_transforms_point(p6, deg, trans, ax)
        tp7 = self.get_transforms_point(p7, deg, trans, ax)
        tp8 = self.get_transforms_point(p8, deg, trans, ax)

        patch = self.stick_base(tp1, tp2, tp3, tp4, tp5, tp6, tp7, tp8, linewidth=linewidth,
                                alpha=alpha, facecolor=facecolor, edgecolor=edgecolor)

        return patch

    def get_rotate_deg(self, o, a):
        """
        opposite:对边
        adjacent:临边
        """
        if a == 0 and o > 0:
            return 90
        elif a == 0 and o < 0:
            return -90
        elif o == 0 and a > 0:
            return 0
        elif o == 0 and a < 0:
            return 180
        else:
            return np.arctan(o/a)/np.pi*180

    def reget_ax_point(self, point, transData, ax):
        inv = ax.transData.inverted()
        return inv.transform(transData.transform(point))

    def get_transforms_point(self, x, deg, trans, ax):
        affline = mtransforms.Affine2D().rotate_deg_around(0, 0, deg).translate(*trans)
        transData = affline + ax.transData
        return self.reget_ax_point(x, transData, ax)

    def stick_base(self, p1, p2, p3, p4, p5, p6, p7, p8, linewidth=2, alpha=0.5, facecolor='b', edgecolor='k'):
        path_data = [
            # up line
            (Path.MOVETO, p1),
            (Path.LINETO, p2),
            # right CURVE4
            (Path.CURVE4, p3),
            (Path.CURVE4, p4),
            (Path.CURVE4, p5),
            # down line
            (Path.LINETO, p6),
            # left CURVE4
            (Path.CURVE4, p7),
            (Path.CURVE4, p8),
            (Path.CURVE4, p1),
        ]

        codes, verts = zip(*path_data)
        path = Path(verts, codes)

        patch = Patches.PathPatch(
            path, alpha=alpha, facecolor=facecolor, edgecolor=edgecolor, linewidth=linewidth)

        return patch


def save_figure(fig_object, output_file, format='svg'):
    fig_object.savefig(output_file, format=format,
                       facecolor='none', edgecolor='none', bbox_inches='tight')


# def savefig(figname, dpi=150, iopts=None, cleanup=True):
#     try:
#         format = figname.rsplit(".", 1)[-1].lower()
#     except:
#         format = "pdf"
#     try:
#         plt.savefig(figname, dpi=dpi, format=format)
#     except Exception as e:
#         message = "savefig failed. Reset usetex to False."
#         message += "\n{0}".format(str(e))
#         rc("text", usetex=False)
#         plt.savefig(figname, dpi=dpi)

#     msg = "Figure saved to `{0}`".format(figname)
#     if iopts:
#         msg += " {0}".format(iopts)

#     if cleanup:
#         plt.rcdefaults()


def load_image(input_file):
    with cbook.get_sample_data(input_file) as image_file:
        image = plt.imread(image_file)
    return image


def quick_show_image_from_file(input_file):

    fig, ax = plt.subplots()

    im = load_image(input_file)

    ax.imshow(im)
    ax.axis('off')

    plt.show()


# def load_image(filename):
#     img = plt.imread(filename)
#     if len(img.shape) == 2:  # Gray-scale image, convert to RGB
#         # http://www.socouldanyone.com/2013/03/converting-grayscale-to-rgb-with-numpy.html
#         h, w = img.shape
#         ret = np.empty((h, w, 3), dtype=np.uint8)
#         ret[:, :, 2] = ret[:, :, 1] = ret[:, :, 0] = img
#         img = ret
#     else:
#         h, w, c = img.shape
#     print("Image `{0}` loaded ({1}px x {2}px).".format(filename, w, h))
#     return img

# ascii


def asciiaxis(x, digit=1):
    if isinstance(x, int):
        x = str(x)
    elif isinstance(x, float):
        x = "{0:.{1}f}".format(x, digit)
    elif isinstance(x, np.int64):
        x = str(x)
    elif isinstance(x, np.ndarray):
        assert len(x) == 2
        x = str(x).replace("]", ")")  # upper bound not inclusive

    return x


def asciiplot(x, y, digit=1, width=50, title=None, char="="):
    """
    Print out a horizontal plot using ASCII chars.
    width is the textwidth (height) of the plot.
    """
    ax = np.array(x)
    ay = np.array(y)

    if title:
        print(dark(title), file=sys.stderr)

    az = ay * width // ay.max()
    tx = [asciiaxis(x, digit=digit) for x in ax]
    rjust = max([len(x) for x in tx]) + 1

    for x, y, z in zip(tx, ay, az):
        x = x.rjust(rjust)
        y = y or ""
        z = green(char * z)
        print("{0} |{1} {2}".format(x, z, y), file=sys.stderr)


# little plot
def add_stick_box_plot(start, end, high=5, x_y_lim=None, thickness=2, linewidth=2, alpha=0.5, facecolor='b', edgecolor='k', bulge=2):
    if not x_y_lim:
        circle_radius = thickness/bulge
    else:
        x_lim, y_lim = x_y_lim
        x_y_ratio = (max(x_lim) - min(x_lim)) / (max(y_lim) - min(y_lim))
        circle_radius = (thickness/bulge) * x_y_ratio

    if end - start > 2 * circle_radius:

        start = start + circle_radius
        end = end - circle_radius

        path_data = [
            # up line
            (Path.MOVETO, [start, high+thickness/2]),
            (Path.LINETO, [end, high+thickness/2]),
            # right CURVE4
            (Path.CURVE4, [end+circle_radius, high+thickness/2]),
            (Path.CURVE4, [end+circle_radius, high-thickness/2]),
            (Path.CURVE4, [end, high-thickness/2]),
            # down line
            (Path.LINETO, [start, high-thickness/2]),
            # left CURVE4
            (Path.CURVE4, [start-circle_radius, high-thickness/2]),
            (Path.CURVE4, [start-circle_radius, high+thickness/2]),
            (Path.CURVE4, [start, high+thickness/2]),
        ]

        codes, verts = zip(*path_data)
        path = Path(verts, codes)

        patch = Patches.PathPatch(
            path, alpha=alpha, facecolor=facecolor, edgecolor=edgecolor, linewidth=linewidth)

    else:
        patch = Patches.Circle(((end + start)/2, high), radius=circle_radius,
                               alpha=alpha, facecolor=facecolor, edgecolor=edgecolor, linewidth=linewidth)

    return patch


def add_small_axes_on_other(main_ax, figure, left_bottom_xy, right_top_xy):
    """
    add a new axes on a main axes by left_bottom_xy and right_top_xy

    left_bottom_xy = (2,2)
    right_top_xy = (3,4)
    """

    # print(ax.transData.transform((0, 4)))
    lb_xy = figure.transFigure.inverted().transform(
        main_ax.transData.transform(left_bottom_xy))
    rt_xy = figure.transFigure.inverted().transform(
        main_ax.transData.transform(right_top_xy))

    return figure.add_axes([lb_xy[0], lb_xy[1], rt_xy[0]-lb_xy[0], rt_xy[1]-lb_xy[1]])


if __name__ == "__main__":
    # stick plot
    fig, ax = plt.subplots(figsize=(10, 10))
    stick_plot = STICK_PLOT()

    patch = stick_plot.get_patch(
        (0, 1.5), (1, 1.5), ax, thickness=0.1, linewidth=0, facecolor='b')
    ax.add_patch(patch)

    plt.show()
