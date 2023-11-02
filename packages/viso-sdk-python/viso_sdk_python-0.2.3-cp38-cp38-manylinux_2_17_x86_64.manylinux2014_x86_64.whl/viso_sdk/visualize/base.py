import cv2
import numpy as np
from PIL import ImageDraw, Image

from viso_sdk.visualize.viz_roi import VizPolygonDraw
from viso_sdk.visualize.viz_object import VizObjectDraw
from viso_sdk.visualize.palette import get_rgba_color_with_palette_id
from viso_sdk.visualize import utils


class BaseVisualization:
    def __init__(self,
                 text_vis_params,
                 object_vis_params,
                 roi_vis_params
                 ):
        self.default_font = utils.init_font(font_size=text_vis_params.get('text_size', utils.DEFAULT_FONT_SIZE))

        self.object_drawer = VizObjectDraw(
            bbox_color=object_vis_params.get('bbox_color', utils.DEFAULT_ROI_OUTLINE_COLOR),
            bbox_thickness=object_vis_params.get('bbox_thickness', utils.DEFAULT_ROI_OUTLINE_THICKNESS),
            text_size=object_vis_params.get('text_size', utils.DEFAULT_FONT_SIZE),
            text_color=object_vis_params.get('text_color', utils.DEFAULT_TXT_COLOR)
        )

        self.roi_drawer = VizPolygonDraw(
            show_roi=roi_vis_params.get('show_roi', None),
            roi_color=roi_vis_params.get('roi_color', utils.DEFAULT_ROI_COLOR),
            outline_color=roi_vis_params.get('outline_color', utils.DEFAULT_ROI_OUTLINE_COLOR),
            outline_thickness=roi_vis_params.get('outline_thickness', utils.DEFAULT_ROI_OUTLINE_THICKNESS),
            show_label=roi_vis_params.get('show_label', True),
            label_size=roi_vis_params.get('label_size', utils.DEFAULT_LABEL_SIZE),
            label_color=roi_vis_params.get('label_color', utils.DEFAULT_LABEL_COLOR)
        )

    @staticmethod
    def __get_adjust_bbox_thick__(img_sz):
        img_h, img_w = img_sz
        bbox_thick = int(0.5 * (img_h + img_w) / 1000)
        if bbox_thick < 2:
            bbox_thick = 2

        return bbox_thick

    @staticmethod
    def get_rgba_color_with_palette_id(palette_id):
        return get_rgba_color_with_palette_id(palette_id)

    def draw_detections(self, img, detections, show_label, show_confidence):
        show = self.object_drawer.draw_detections(
            img=img,
            detections=detections,
            show_label=show_label,
            show_confidence=show_confidence
        )
        return show

    def draw_polygons(self, img, rois):
        show = self.roi_drawer.draw_polygon_rois(
            img=img,
            rois=rois
        )
        return show

    def draw_lines(self, img, lines, labels):
        show = self.roi_drawer.draw_line_rois(
            img=img,
            lines=lines,
            labels=labels)
        return show

    def put_text(self,
                 img,
                 font=None,
                 text="",
                 text_color=None,
                 align="left",
                 pos=(0, 0),
                 bbox_color=None,
                 bbox_thickness=-1,
                 large_padding=False,
                 show_shadow=True,
                 shadow_color=utils.DEFAULT_SHADOW_COLOR):
        cv_im_rgba = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2RGBA)

        # Pass the image to PIL
        pil_base_im = Image.fromarray(cv_im_rgba, "RGBA")

        pil_viz_im = Image.new("RGBA", pil_base_im.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(pil_viz_im, "RGBA")

        utils.put_text(
            draw=draw,
            font=self.default_font if font is None else font,
            bbox=pos,
            text=str(text),
            text_color=utils.DEFAULT_TXT_COLOR if text_color is None else text_color,
            align=align,
            large_padding=large_padding,
            bbox_color=utils.DEFAULT_ROI_COLOR if bbox_color is None else bbox_color,
            bbox_thickness=bbox_thickness,
            show_shadow=show_shadow,
            shadow_color=utils.DEFAULT_SHADOW_COLOR if shadow_color is None else shadow_color
        )

        pil_out = Image.alpha_composite(pil_base_im, pil_viz_im)
        cv_im_processed = cv2.cvtColor(np.array(pil_out), cv2.COLOR_RGBA2BGR)
        return cv_im_processed
