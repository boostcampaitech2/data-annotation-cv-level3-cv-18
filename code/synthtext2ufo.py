from scipy import io
from functools import reduce
import json

import numpy as np

def split_gt_txt(gt_txt):
    tmp = []
    for txt in gt_txt:
        txt = txt.strip()
        txt = txt.split("\n")
        txt = [t.strip().split(" ") for t in txt]
        txt = reduce(lambda x, y: x+y, txt)
        tmp += txt
    return tmp


def get_words_from_points(gt_word_bbox, txt, gt_imname):
    gt_word_bbox = gt_word_bbox.astype(dtype=float)
    if gt_word_bbox.shape == (2, 4):
        words = {}
        words_points = [[float(x), float(y)] for idx, (x, y) in enumerate(zip(*gt_word_bbox))]
        words["0"] = {
            "points":words_points,
            "orientation":"Horizontal",
            "transcription":txt[0],
            "word_tag":None,
            "language":["EN"],
            "illegibility":False
        }
        return words
    
    points_x, points_y = gt_word_bbox
    
    points_x1, points_x2, points_x3, points_x4 = points_x
    points_y1, points_y2, points_y3, points_y4 = points_y

    points_x1y1 = zip(points_x1, points_y1)
    points_x2y2 = zip(points_x2, points_y2)
    points_x3y3 = zip(points_x3, points_y3)
    points_x4y4 = zip(points_x4, points_y4)
        
    points = zip(points_x1y1, points_x2y2, points_x3y3, points_x4y4)

    words = {}
    
    for idx, four_points in enumerate(points):
        words_points = [[float(x), float(y)] for idx, (x, y) in enumerate(four_points)]

        words[f"{idx}"] = {
            "points":words_points,
            "orientation":"Horizontal",
            "transcription":txt[idx],
            "word_tag":"null",
            "language":["EN"],
            "illegibility":False
        }
        
    return words


def main():
    gt = io.loadmat("./SynthText/gt.mat")
    
    gt_word_bboxes = gt['wordBB'][0]
    gt_imnames = gt['imnames'][0]
    gt_txts = gt['txt'][0]

    ufo = {
        "images":{}
    }
    
    license_tag = {
        "usability":True,
        "public":True,
        "commercial":True,
        "type":"null",
        "holder":"null",
    }
    
    for gt_word_bbox, gt_imname, gt_txt in zip(gt_word_bboxes, gt_imnames, gt_txts):
        gt_imname = gt_imname[0]
        gt_txt = split_gt_txt(gt_txt)

        words = get_words_from_points(gt_word_bbox, gt_txt, gt_imname)

        ufo["images"][gt_imname] = {
            "paragraphs":{},
            "words":words,
            "chars":{},
            "tags":{},
            "relations":{},
            "license_tag": license_tag
        }
    
    with open("./ufo.json", "w") as f:
        json.dump(ufo, f)
        print("done.")
        
if __name__ == "__main__":
    main()


