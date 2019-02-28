import os
import time
import random

filename = 'data/{}.txt'.format('c')

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


# noinspection PyShadowingNames
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


# noinspection PyShadowingNames
def create_output_file(output_data, fname=""):
    # ex. output_data = [[1], [2], [3, 4], [5], [6, 7]]
    if fname == "":
        with open(filename.replace('data/', 'out/' + fname), "w") as f_out:
            f_out.write(str(len(output_data)) + '\n')
            [f_out.write(' '.join([str(x) for x in slide]) + '\n') for slide in output_data]
    else:
        with open(filename.replace('data/', 'out_random/' + fname), "w") as f_out:
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

    # loading
    loading_counter = 0
    images = []
    used_cs = []
    for c in content[1:]:
        if c in used_cs:
            continue
        used_cs.append(c)
        images.append(Image(content.index(c) - 1, c.split(" ")[0], c.split(" ")[2:]))
        loading_counter += 1
        if loading_counter % 1000 == 0:
            print(loading_counter, "images loaded.")
    print(len(images), "images loaded. finished loading.")

    vertical_images = []
    horizontal_images = []

    slides = []
    for img in images:
        if img.orientation == "V":
            vertical_images.append(img)
        else:
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

    # matching slides
    # TODO Make it smart
    output_data = []
    for slide in slides:
        app = []
        for img in slide.images:
            app.append([img.id, img.tags])
        output_data.append(app)
    print(output_data)
    print("Score data:", eval_output(output_data))
    create_output_file([[y[0] for y in x] for x in output_data])
    scores = []
    for ctr in range(0, 20000):
        if ctr % 1000 == 0:
            print(ctr)
        output_dict = {}
        available_locations = [x for x in range(0, len(slides))]
        for slide in slides:
            loc = random.choice(available_locations)
            output_dict[loc] = slide
            available_locations.remove(loc)
        output_data = [output_dict[x].get() for x in sorted(output_dict)]
        scr = eval_output(output_data)
        scores.append(scr)
        if not os.path.exists('/out_random/' + str(scr) + '_c.txt'):
            create_output_file([[y[0] for y in x] for x in output_data], str(scr) + "_")
    print(max(scores))
    ex = [
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
    out = [
        [
            [0, ['beach', 'cat', 'sun']]
        ],
        [
            [3, ['cat', 'garden']]
        ],
        [
            [2, ['garden', 'selfie']],
            [1, ['selfie', 'smile']]
        ]
    ]
    # print(Slide(images[0], images[1]).get_tags())
    # create_output_file([[1], [2], [3, 4], [5], [6, 7]])
    # print(eval_output([Slide(images[0], images[1]).get(), Slide(images[2], images[3]).get()]))
    print("Finished in {}s".format(time.time() - t0))
