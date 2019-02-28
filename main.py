import time

import numpy as np
import math
import random

filename = 'data/{}.txt'.format('b')

with open(filename) as f_in:
    content = f_in.read().split("\n")[:-1]


def eval_single_transition(prev_slide_tags, slide_tags):
    common = len(slide_tags.intersection(prev_slide_tags))
    in_previous_only = len([t for t in prev_slide_tags if t not in slide_tags])
    in_current_only = len([t for t in slide_tags if t not in prev_slide_tags])
    minimum = min(common, in_current_only, in_previous_only)
    # print("Common:", common)
    # print("In previous only:", in_previous_only)
    # print("In current only:", in_current_only)
    # print("Min:", minimum)
    return minimum


def eval_output(output_data):
    """
    ex. output_data
    [
        [
            [1, ["a", "b"]]
        ],
        [
            [2, ["c", "b"]]
        ],
        [
            [3, ["a", "c"]],
            [4, ["b", "d"]]
        ],
        [
            [5, ["c", "d"]]
        ],
        [
            [6, ["a", "c"]],
            [7, ["c", "d"]]
        ]
    ]
    """
    score = 0
    prev_slide_tags = []
    for slide in output_data:
        slide_tags = []
        for image in slide:
            slide_tags += image[1]
        slide_tags = set(slide_tags)

        score += eval_single_transition(prev_slide_tags, slide_tags)
        prev_slide_tags = slide_tags
    return score


# print("Score:", eval_output([[[1, ["a", "b"]]], [[2, ["c", "b"]]], [[3, ["a", "c"]], [4, ["b", "d"]]], [[5, ["c", "d"]]], [[6, ["a", "c"]], [7, ["c", "d"]]]]))


def create_output_file(output_data):
    # ex. output_data = [[1], [2], [3, 4], [5], [6, 7]]
    with open(filename.replace('data', 'out'), "w") as f_out:
        f_out.write(str(len(output_data)) + '\n')
        [f_out.write(' '.join([str(x) for x in slide]) + '\n') for slide in output_data]


class Image:
    def __init__(self, image_id, orientation, tags):
        self.id = image_id
        self.orientation = orientation
        self.tags = sorted(tags)

    def __str__(self):
        return "<Image {}: Orientation: {}, Tags: {}>".format(self.id, self.orientation, self.tags)

    def get(self):
        return [self.id, self.tags]


# noinspection PyShadowingNames
class Slide:
    def __init__(self, *images):
        self.images = images

    def __str__(self):
        slide_tags = []
        for image in self.images:
            slide_tags += image.tags
        slide_tags = set(slide_tags)
        return "<Slide: {}>".format(slide_tags)

    def get_tags(self):
        slide_tags = []
        for image in self.images:
            slide_tags += image.tags
        slide_tags = set(slide_tags)
        return list(slide_tags)

    def get(self):
        return [*[i.get() for i in self.images]]


if __name__ == '__main__':
    print("HASHCODE 2019!\n")
    t0 = time.time()
    aujsgdi = 0
    images = []
    for c in content[1:]:
        images.append(Image(content.index(c) - 1, c.split(" ")[0], c.split(" ")[2:]))
        aujsgdi += 1
        print(aujsgdi)
    print(len(images), "images loaded")

    vertical_images = []
    horizontal_images = []

    for img in images:
        if img.orientation == "V":
            vertical_images.append(img)
        else:
            horizontal_images.append(img)

    slides = []
    for img in horizontal_images:
        slides.append(Slide(img))

    # TODO Make it smart
    while True:
        if len(vertical_images) > 0:
            c1 = random.choice(vertical_images)
            vertical_images.remove(c1)
            if len(vertical_images) > 0:
                c2 = random.choice(vertical_images)
                vertical_images.remove(c2)
                slides.append(Slide(c1, c2))
            else:
                slides.append(Slide(c1))
                break
        else:
            break
    slide_tags = [x.get_tags() for x in slides]
    # print(Slide(images[0], images[1]).get_tags())
    # create_output_file([[1], [2], [3, 4], [5], [6, 7]])
    # print(eval_output([Slide(images[0], images[1]).get(), Slide(images[2], images[3]).get()]))
    print("Finished in {}s".format(time.time() - t0))
