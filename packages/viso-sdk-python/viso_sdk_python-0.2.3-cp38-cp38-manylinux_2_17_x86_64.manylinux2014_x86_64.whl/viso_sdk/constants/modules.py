
class Module:
    """
        modules container mqtt and redis ports as individual
    """
    class Region:
        type = 'region-of-interest'

        class RoiType:
            polygon = 'polygon'
            rectangle = 'rectangle'
            section = 'section'

    class MultipleObjectDetection:
        type = "multiple-object-detection"

    class VideoFeed:
        type = "video-feed"

    class ColorRecognition:
        type = 'color-recognition'

    class ReIdObjectTracking:
        type = 'reid-object-tracking'

    class ObjectCount:
        type = "object-count"

    """
        modules publish metadata in redis string together
    """
    class Roi:
        type = 'roi'

        class RoiType:
            polygon = 'polygon'
            rectangle = 'rectangle'
            section = 'section'

    class VideoSource:
        type = "video-source"

    class ObjectDetection:
        type = "object-detection"

    class ObjectTracking:
        type = 'object-tracking'

    class FrameViewer:
        type = "frame-viewer"
