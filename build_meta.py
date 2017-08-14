import json
import os


def build_meta_dict(a_dict, u_dict):
    dict = {}
    dict["folder"] = "unknown"
    dict["language"] = "EN"
    dict["encoding"] = "UTF8"
    dict["candidate-authors"] = a_dict
    dict["unknown-texts"] = u_dict
    return(dict)


def build_ground_truth(truth_list):
    dict = {}
    dict["ground-truth"] = truth_list
    return(dict)


# candidates = ["candidate00001","candidate00002","candidate00003"]
# unknowns = ["unknown00001", "unknown00002", "unknown00003", "unknown00004"]
# gr_truths = [{"unknown-text": "unknown00001.txt", "true-author": "candidate00003"},
#             {"unknown-text": "unknown00002.txt", "true-author": "candidate00002"},
#             {"unknown-text": "unknown00003.txt", "true-author": "candidate00003"},
#             {"unknown-text": "unknown00004.txt", "true-author": "candidate00001"},
#             {"unknown-text": "unknown00005.txt", "true-author": "candidate00001"},
#             {"unknown-text": "unknown00006.txt", "true-author": "candidate00002"}]

# author_list = []
# unknown_list = []
# true_list = []
# for candidate in candidates:
#     c_list = {}
#     c_list["author-name"] = candidate
#     author_list.append(c_list)
# for unknown in unknowns:
#     u_list = {}
#     u_list["unknown-text"] = unknown
#     unknown_list.append(u_list)
#
# dict = build_meta_dict(author_list, unknown_list)
# print(dict)
# gt_dict = build_ground_truth(gr_truths)
# print(gt_dict)
#
# metafile = "meta.json"
# gtfile = "ground-truth.json"
# with open(metafile,'a',encoding="utf-8") as m_outfile:
#     json.dump(dict,m_outfile,indent=0)
# with open(gtfile,'a',encoding="utf-8") as gt_outfile:
#     json.dump(gt_dict,gt_outfile,indent=0)
