
# -*- coding: utf-8 -*-
import itertools
from functools import reduce

import numpy as np
import cv2
import math
import collections
from PIL import Image
from typing import List
from matplotlib import pyplot as plt
from sklearn.cluster import DBSCAN, KMeans, MeanShift, OPTICS, Birch


# (n, 2) poly -> box_dict
def trans_poly_to_rec(poly):
    # poly = np.array(poly).reshape(-1, 2)
    poly = poly.tolist()
    l = min([i[0] for i in poly])
    r = max([i[0] for i in poly])
    u = min([i[1] for i in poly])
    d = max([i[1] for i in poly])
    Rec = collections.namedtuple('Rec', 'l r u d')
    rec = Rec(l, r, u, d)
    return rec


def cluster_recs(recs, type='DBSCAN'):
    switch = {
        'DBSCAN': DBSCAN(min_samples=1, eps=7),
        'MeanShift': MeanShift(bandwidth=0.3),
        'OPTICS': OPTICS(min_samples=1, eps=20),
        'Birch': Birch(n_clusters=None)
    }
    try:
        cluster = switch[type]
    except ValueError as e:
        raise ValueError('type should be DBSCAN, MeanShift, OPTICS or Birch')
    boxes_data = [[rec.l, rec.r] for rec in recs]
    boxes_data = np.array(boxes_data)
    labels = cluster.fit_predict(boxes_data)
    '''
    plt.scatter(boxes_data[:, 0], boxes_data[:, 1], s=1, c=labels)
    plt.show()
    '''
    classified_box_ids = collections.defaultdict(list)
    for idx, label in enumerate(labels):
        classified_box_ids[label].append(idx)
    return classified_box_ids


def check_one_over_two(cur, nxt, recs, cover_threshold):
    cur_l = np.mean([recs[idx].l for idx in cur])
    cur_r = np.mean([recs[idx].r for idx in cur])
    nxt_l = np.mean([recs[idx].l for idx in nxt])
    nxt_r = np.mean([recs[idx].r for idx in nxt])
    cur_len = cur_r - cur_l
    nxt_len = nxt_r - nxt_l
    cover = min(cur_r, nxt_r) - max(cur_l, nxt_l)
    if nxt_len * 1.5 <= cur_len <= nxt_len * 2.5 and cover > cover_threshold * nxt_len:
        return True


def read_out(classified_recs, recs, cover_threshold=0.2):
    output_idx = []
    total_clusters = len(classified_recs)
    for i in range(total_clusters):
        # i - 1 can't be one-column.
        if i == total_clusters - 1:
            while classified_recs[i]:
                output_idx.append(classified_recs[i].pop(0))
        elif classified_recs[i]:
            # check if cur cluster is one-column and nxt cluster is two-column
            cur = classified_recs[i]
            nxt = classified_recs[i + 1]
            if check_one_over_two(cur, nxt, recs, cover_threshold):
                if i < total_clusters - 2:
                    nxt2 = classified_recs[i + 2]
                    # check another two-column cluster
                    if not check_one_over_two(cur, nxt2, recs, cover_threshold):
                        nxt2 = None
                else:
                    nxt2 = None

                while cur or nxt or nxt2:
                    if not cur:
                        while nxt:
                            output_idx.append(nxt.pop(0))
                        while nxt2:
                            output_idx.append(nxt2.pop(0))
                    cur_u = recs[cur[0]].u
                    while nxt and recs[nxt[0]].u < cur_u:
                        output_idx.append(nxt.pop(0))
                    while nxt2 and recs[nxt2[0]].u < cur_u:
                        output_idx.append(nxt2.pop(0))
                    output_idx.append(cur.pop(0))
            else:
                while classified_recs[i]:
                    output_idx.append(classified_recs[i].pop(0))
        else:
            continue
    return output_idx





def list_sort(box_list):
    r = np.mean([b.r for b in box_list])
    length = np.mean([b.r - b.l for b in box_list])
    return r + length


def box_sort(box):
    return (box.u + box.d) / 2