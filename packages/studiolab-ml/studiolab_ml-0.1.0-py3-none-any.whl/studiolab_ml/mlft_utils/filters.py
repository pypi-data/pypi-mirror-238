import numpy as np

from .meta import attr_dict, minor_ins_keys, major_ins_keys, classes_of_seller_category
from .nick_name import nick_name_dicts
from .bbox import bbox_inter, nms

def get_class_list(instance_keys, return_keys=False):
    det_classes = []
    det_keys = []
    for k in instance_keys:
        for v in attr_dict[k]:
            if v == "None": continue
            det_classes.append(v)
            det_keys.append(k)
    if return_keys:
        return det_classes, det_keys
    return det_classes

def major_inst_filter(pred_cls, det_conf, xyxy, instance_list):
    pred_ins_name = [instance_list[int(p)] for p in pred_cls]
    major_cls = get_class_list(major_ins_keys)
    idx = [i for i, pin in enumerate(pred_ins_name) if pin in major_cls]
    idx = np.array(idx)
    if len(idx) < 2:
        return pred_cls
    keep = nms(xyxy[idx], det_conf[idx], 0.5, return_bool=True)
    pred_cls[idx[~keep]] = -1

    return pred_cls

def seller_major_filer(pred_cls, det_conf, xyxy, instance_list, category_id):
    if category_id is None:
        return pred_cls
    cat_cls = classes_of_seller_category[category_id]
    pred_ins_name = [instance_list[int(p)] for p in pred_cls]
    # if category_id == 7: #Can not filtering set-up
    #     cat_cls = pred_ins_name
    major_cls = get_class_list(major_ins_keys)
    idx = []
    for i, pin in enumerate(pred_ins_name):
        if pin in major_cls:
            if pin in cat_cls:
                idx.append(i)
            else:
                pred_cls[i] = -1
    idx = np.array(idx)
    if len(idx) < 2:
        return pred_cls
    keep = nms(xyxy[idx], det_conf[idx], 0.5, return_bool=True)
    pred_cls[idx[~keep]] = -1

    return pred_cls

def neck_filter(pred_cls, det_conf, xyxy, instance_list):
    pred_ins_name = [instance_list[int(p)] for p in pred_cls]
    neck_cls = get_class_list(['collar', 'neckline', "hood"])
    idx = [i for i, pin in enumerate(pred_ins_name) if pin in neck_cls]
    if len(idx) < 2:
        return pred_cls
    idx = np.array(idx)
    keep = nms(xyxy[idx], det_conf[idx], 0.2, return_bool=True)
    pred_cls[idx[~keep]] = -1
    return pred_cls

def sleeve_filter(res):
    upper = get_class_list(['top', 'outer', 'dress'])
    sleeve_instance = get_class_list(['sleeve length'])
    remove_list = []
    for r in res:
        if r['cls'] in upper:
            s_cls = []
            s_score = []
            s_idx = []
            for c_idx in r['children_ids']:
                c = res[c_idx]
                if c['cls'] in sleeve_instance:
                    s_cls.append(c['cls'])
                    s_score.append(c['conf'])
                    s_idx.append(c_idx)
            if len(s_cls) == 0: continue
            s_idx = np.array(s_idx)

            # find redundant sleeve length instances
            if len(s_cls) > 2:
                sorted_sleeve = np.argsort(s_score)[::-1]
                remove_list += s_idx[sorted_sleeve[2:]].tolist()
                r['children_ids'] = list(set(r['children_ids']).difference(set(remove_list)))
                s_idx = s_idx[sorted_sleeve[:2]]

            # sync sleeve length classes
            maxi_cls = s_cls[np.argmax(s_score)]
            for s_ in s_idx:
                res[s_]['cls'] = maxi_cls
    
    remove_list = sorted(remove_list, reverse=True)
    for r in remove_list:
        res.pop(r)

    
def instance_heirarchy(res):
    minor_ins_list = get_class_list(
        minor_ins_keys
    )
    major_bbox = []
    major_idx = []
    minor_bbox = []
    minor_idx = []
    for idx, r in enumerate(res):
        if r["cls"] in minor_ins_list:
            minor_bbox.append(r["bbox"])
            minor_idx.append(idx)
            r.update({"parents_id": None, "is_major": False})
        else:
            r.update({"children_ids": [], "is_major": True})
            major_bbox.append(r["bbox"])
            major_idx.append(idx)
    if len(minor_bbox) == 0 or len(major_bbox) == 0:
        return res
    ratio = bbox_inter(np.array(major_bbox), np.array(minor_bbox))
    hei = np.argmax(ratio, axis=0)
    max_r = np.max(ratio, axis=0)
    sum_r = np.sum(ratio, axis=0)
    for mi, h, r, s in zip(minor_idx, hei, max_r, sum_r):
        if s > 1.5: continue
        if r < 0.8: continue
        res[mi]["parents_id"] = major_idx[h]
        res[major_idx[h]]["children_ids"].append(mi)    
    return res

#TODO
# def get_loc_desc(res):
#     # Describe location of minor instances
#     target_classes = get_class_list(['fastening', 'pocket', 'detail'])

#     for r in res:
#         if r.get("children_ids", False):
#             major_bbox = r["bbox"] #xyxy
#             center = [(major_bbox[0] + major_bbox[2])/2, (major_bbox[1] + major_bbox[3])/2]
#             width = major_bbox[2] - major_bbox[0]
#             height = major_bbox[3] - major_bbox[1]
#             w_margin = width * 0.3
#             h_margin = height * 0.3
#             for ch in r["children_ids"]:
#                 if res[ch]['cls'] not in target_classes: continue
#                 ch_bbox = res[ch]['bbox'] #xyxy
#                 ch_center = [(ch_bbox[0] + ch_bbox[2])/2, (ch_bbox[1] + ch_bbox[3])/2]

def get_nick_name(res):
    for r in res:
        nicks = nick_name_dicts.get(r['cls'], False)
        selected = "None"
        if nicks:
            vals = list(r['attributes'].values())
            for c in r['children_ids']:
                vals += [res[c]['cls']]
            vals = list(set(vals))
            cand_nicks = []
            l_defi = []
            for nick in nicks:
                defi = nick["definition"]
                inter = set(defi).intersection(set(vals))
                if len(inter) == len(defi):
                    cand_nicks.append(nick['nick_kor'])
                    l_defi.append(len(defi))
            if len(l_defi) > 1:
                max = np.max(l_defi)
                unique, counts = np.unique(l_defi, return_counts=True)
                tmp = dict(zip(unique, counts))
                if tmp[max] > 1:
                    selected = cand_nicks[-1]
                else:
                    idx = np.argmax(l_defi)
                    selected = cand_nicks[idx]
            elif len(l_defi)==1:
                selected = cand_nicks[0]

        r.update({"nick_name": selected})
