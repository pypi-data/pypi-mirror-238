import os
import pandas as pd

root_path = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(root_path, "src")

pants_df = pd.read_csv(os.path.join(src_path, "nicknames_pants.csv"))
dress_df = pd.read_csv(os.path.join(src_path, "nicknames_dress.csv"))
outer_df = pd.read_csv(os.path.join(src_path, "nicknames_outer.csv"))
top_df = pd.read_csv(os.path.join(src_path, "nicknames_top.csv"))
skirt_df = pd.read_csv(os.path.join(src_path, "nicknames_skirt.csv"))

nick_name_dicts = {}
for df in [pants_df, dress_df, outer_df, top_df, skirt_df]:
    for i in df.index:
        l = df.loc[i].tolist()
        ins_cls = l[2]
        if nick_name_dicts.get(ins_cls, False):
            nick_name_dicts[ins_cls].append(
                {
                    "nick_eng": l[0],
                    "nick_kor": l[1],
                    "definition": [t for t in l[3:] if isinstance(t, str)]
                }
            )
        else:
            nick_name_dicts.update({
                ins_cls: [
                    {
                        "nick_eng": l[0],
                        "nick_kor": l[1],
                        "definition": [t for t in l[3:] if isinstance(t, str)]
                    }
                ]
            })

