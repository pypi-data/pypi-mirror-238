from pandas import DataFrame

from tybase.adtools.toutiaoBase import TouTiaoAdvertiser

# 头条广告的信息配置
BASE_TOKEN = "UHP3GEvPBh6L2ujOniTwhFgtuyJ7ULdv"  # 用于查询广告数据的基本token
ADV_TOKEN = "9pDitb06b3NysTFtwc3Ym2x5zmefluy9"  # 用于获取账户数据的token,顶层的Token
AcEmail = "tayun2023@163.com"
base_token_url = "https://api.bi.tayun365.com/ext/oe/token?account={email}"


class MyTouTiaoAdvertiser(TouTiaoAdvertiser):
    def __init__(self):
        super().__init__(AcEmail, ADV_TOKEN, base_token_url)

    @staticmethod
    def parse_df(df_my_as):
        """
        处理DataFrame，将advertiser_name列进行分割，并添加新的列。

        :param df_my_as: 需要处理的DataFrame
        :return: 处理后的DataFrame
        """
        df_split = df_my_as.advertiser_name.str.split("-", expand=True)
        columns = ['运营方式', 'APP', '终端', '渠道', '代理', '投手', "返点"]
        col_len = len(columns)
        for i, col_name in enumerate(columns):
            df_my_as.loc[:, col_name] = df_split.iloc[:, i]
        df_my_as.loc[:, '其他'] = df_split.iloc[:, col_len:].apply(lambda row: '-'.join(row.dropna().astype(str)),
                                                                   axis=1)
        return df_my_as

    def get_as_df(self):
        """
        获取广告商的DataFrame。会用到`parse_df`的方法来解析最新的账户的数据
        :return: 广告商的DataFrame
        """
        print("正在获取所有的授权账户...")
        as_data = self.get_all_advertisers_threading()
        df_as = DataFrame(as_data)
        print("正在解析账户...")
        df_my_as = df_as[df_as['advertiser_name'].str.startswith(('Z-', 'D-', "S-"))]
        df = self.parse_df(df_my_as)
        replacement_dict = {"Z": "自运营", "D": "代运营", "S": "暂停"}
        df['运营方式'] = df['运营方式'].replace(replacement_dict)
        # 如果返点为空，则填充为0
        df['返点'] = df['返点'].fillna(0)
        df["返点"] = df['返点'].astype(float) / 100 + 1
        return df


if __name__ == '__main__':
    import time
    start = time.time()
    print(MyTouTiaoAdvertiser().get_as_df())
    print(time.time() - start)
