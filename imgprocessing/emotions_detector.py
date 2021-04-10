import paz.processors as pr
from paz.applications import HaarCascadeFrontalFace, MiniXceptionFER


class EmotionDetector(pr.Processor):

    def __init__(self):
        super(EmotionDetector, self).__init__()
        self.detect = HaarCascadeFrontalFace(draw=False)
        self.corp = pr.CropBoxes2D()
        self.classify = MiniXceptionFER()
        self.draw = pr.DrawBoxes2D(self.classify.class_names)

    def call(self, image: np.ndarray):
        boxes2D = self.detect(image)["boxes2D"]
        cropped_images = self.corp(image, boxes2D)
        classes = []
        for img, box in zip(cropped_images, boxes2D):
            result = self.classify(img)
            box.class_name = result["class_name"]
            classes.append(result["class_name"])
        return classes
