from math import ceil
import pandas as pd


def chunk(lst, size):
    # 列表分组,传入列表对其进行分组
    return list(
        map(lambda x: lst[x * size:x * size + size],
            list(range(0, ceil(len(lst) / size)))))


def flexible_group_df(df: pd.DataFrame, primary_group: str, secondary_group: str, group_size: int = 10) -> list:
    """
    from tybase.tools.basetools import flexible_group_df
    :param df: pandas的数组
    :param primary_group:  第一分组
    :param secondary_group: 第二分组
    :param group_size:  分组的规模
    :return:
    [{'advertiser_id': xxxxx,
    '广告ID': [[xxxx, xxxx, xxxxx]]}]
    """


    # Group by primary_group
    grouped = df.groupby(primary_group)

    result = []
    for name, group in grouped:
        # Split the secondary_group column into sublists of length group_size
        ids = group[secondary_group].tolist()
        split_ids = [ids[i:i + group_size] for i in range(0, len(ids), group_size)]

        # Append the result to the final list
        result.append({primary_group: name, secondary_group: split_ids})

    return result
