import os


class ImageHandler:
    def __init__(self, img_dir)
        self.img_dir = img_dir

    def get(self, img_name, img_size='40', img_ext='png'):
        img_full_name = '%s%s.%s' % (img_name, img_size, img_ext)
        img_path = '%s%s%s' % (self.img_dir,  os.sep, img_full_name)
        return img_path