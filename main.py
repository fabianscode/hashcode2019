import numpy as np
import math

filename = 'data/{}.txt'.format('a')

with open(filename) as f_in:
    content = f_in.read().split("\n")[:-1]


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
        common = len(slide_tags.intersection(prev_slide_tags))
        in_previous_only = len([t for t in prev_slide_tags if t not in slide_tags])
        in_current_only = len([t for t in slide_tags if t not in prev_slide_tags])
        minimum = min(common, in_current_only, in_previous_only)

        prev_slide_tags = slide_tags
        score += minimum
        # print("Common:", common)
        # print("In previous only:", in_previous_only)
        # print("In current only:", in_current_only)
        # print("Min:", minimum)

        print()
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


if __name__ == '__main__':
    print("HASHCODE 2019!\n")

    images = [Image(content.index(c)-1, c.split(" ")[0], c.split(" ")[2:]) for c in content[1:]]
    print(len(images), "images loaded")
    [print(i) for i in images]
    # create_output_file([[1], [2], [3, 4], [5], [6, 7]])
