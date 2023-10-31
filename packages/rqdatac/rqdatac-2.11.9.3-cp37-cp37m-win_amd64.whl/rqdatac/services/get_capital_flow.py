# -*- coding: utf-8 -*-
import datetime

import pandas as pd
import numpy as np

from rqdatac.services.basic import instruments
from rqdatac.services.calendar import current_trading_date, get_next_trading_date
from rqdatac.validators import (
    ensure_string_in,
    ensure_order_book_ids,
    ensure_date_range,
    check_items_in_container,
    ensure_list_of_string,
    ensure_instruments,
)
from rqdatac.utils import (
    int8_to_datetime_v,
    int14_to_datetime_v,
    int17_to_datetime_v,
    int17_to_datetime,
    date_to_int8,
    get_tick_value,
)
from rqdatac.client import get_client
from rqdatac.decorators import export_as_api
from rqdatac.share.errors import PermissionDenied, MarketNotSupportError


DAYBAR_FIELDS = MINBAR_FIELDS = ["buy_volume", "buy_value", "sell_volume", "sell_value"]
TICKBAR_FIELDS = ["datetime", "direction", "volume", "value"]


def convert_bar_to_multi_df(data, dt_name, fields, convert_dt, default=0.0):
    line_no = 0
    dt_set = set()
    obid_level = []
    obid_slice_map = {}
    for obid, d in data:
        dts = d[dt_name]
        dts_len = len(dts)
        if dts_len == 0:
            continue
        obid_slice_map[obid] = slice(line_no, line_no + dts_len, None)
        dt_set.update(dts)
        line_no += dts_len

        obid_level.append(obid)

    if line_no == 0:
        return

    obid_idx_map = {o: i for i, o in enumerate(obid_level)}
    obid_label = np.empty(line_no, dtype=object)
    dt_label = np.empty(line_no, dtype=object)
    arr = np.full((line_no, len(fields)), default)
    r_map_fields = {f: i for i, f in enumerate(fields)}

    dt_arr_sorted = np.array(sorted(dt_set))
    dt_level = convert_dt(dt_arr_sorted)

    for obid, d in data:
        dts = d[dt_name]
        if len(dts) == 0:
            continue
        slice_ = obid_slice_map[obid]
        for f, value in d.items():
            if f == dt_name:
                dt_label[slice_] = dt_arr_sorted.searchsorted(dts, side='left')
            else:
                arr[slice_, r_map_fields[f]] = value
        obid_label[slice_] = [obid_idx_map[obid]] * len(dts)
    try:
        # func 'is_datetime_with_singletz_array'  is the most time consuming part in multi_index constructing
        # it is useless for our situation. skip it.
        func_is_singletz = getattr(pd._libs.lib, 'is_datetime_with_singletz_array')
        setattr(pd._libs.lib, 'is_datetime_with_singletz_array', lambda *args: True)
    except AttributeError:
        func_is_singletz = None

    multi_idx = pd.MultiIndex([obid_level, dt_level], [obid_label, dt_label],
                              names=('order_book_id', dt_name))

    if func_is_singletz is not None:
        # recovery
        setattr(pd._libs.lib, 'is_datetime_with_singletz_array', func_is_singletz)

    df = pd.DataFrame(data=arr, index=multi_idx, columns=fields)
    return df


def get_capital_flow_daybar(order_book_ids, start_date, end_date, fields, duration=1, market="cn"):
    data = get_client().execute(
        "get_capital_flow_daybar", order_book_ids, start_date, end_date, fields, duration, market=market
    )
    data = [(obid, {k: np.frombuffer(*v) for k, v in d.items()}) for obid, d in data]
    res = convert_bar_to_multi_df(data, 'date', fields, int8_to_datetime_v)
    return res


def get_today_capital_flow_minbar(order_book_ids, date, fields, duration, market="cn"):
    data = get_client().execute("get_today_capital_flow_minbar", order_book_ids, date, fields, duration, market=market)
    return convert_bar_to_multi_df(data, "datetime", fields, int14_to_datetime_v)


def get_capital_flow_minbar(order_book_ids, start_date, end_date, fields, duration, market):
    history_permission_denied = realtime_permission_denied = False
    try:
        data = get_client().execute(
            "get_capital_flow_minbar", order_book_ids, start_date, end_date, fields, duration, market=market
        )
    except PermissionDenied:
        history_permission_denied = True
        data = []

    if data:
        data = [(obid, {k: np.frombuffer(*v) for k, v in d.items()}) for obid, d in data]
        df = convert_bar_to_multi_df(data, 'datetime', fields, int14_to_datetime_v)
    else:
        df = None

    live_date = current_trading_date()
    if start_date > live_date or end_date < live_date:
        return df

    live_date_str = '%d-%02d-%02d' % (live_date // 10000, live_date % 10000 // 100, live_date % 100)
    live_obs = set(
        ins.order_book_id for ins in instruments(order_book_ids)
        if ins.de_listed_date == '0000-00-00' or ins.de_listed_date >= live_date_str
    )

    if df is not None:
        idx = df.index
        for ob in idx.levels[0]:
            if ob not in live_obs:
                continue
            loc = idx.get_loc(ob)
            if date_to_int8(idx[loc.stop - 1][-1]) == live_date:
                live_obs.remove(ob)

    if not live_obs:
        return df

    try:
        live_df = get_today_capital_flow_minbar(list(live_obs), live_date, fields, duration, market)
    except PermissionDenied:
        live_df = None
        realtime_permission_denied = True
    except MarketNotSupportError:
        live_df = None

    if history_permission_denied and realtime_permission_denied:
        raise PermissionDenied("get_capital_flow_minbar")

    if live_df is None:
        return df

    live_df = live_df[
        live_df.index.get_level_values(1).date ==
        datetime.date(live_date // 10000, live_date % 10000 // 100, live_date % 100)
    ]

    if df is None:
        return live_df
    df = pd.concat([df, live_df])
    df.sort_index(inplace=True)
    return df


def get_today_capital_flow_tick(order_book_id, date, market="cn"):
    data = get_client().execute("get_today_capital_flow_tick", order_book_id, date, market=market)
    df = pd.DataFrame(data[0])
    if df.empty:
        return None
    df.datetime = df.datetime.apply(int17_to_datetime)
    df = df.astype({"direction": "i1", "volume": "u8", "value": "u8"})
    df.set_index(['order_book_id', 'datetime'], inplace=True)
    return df


def get_capital_flow_tickbar(order_book_ids, start_date, end_date, fields,  market):
    ins_list = ensure_instruments(order_book_ids)
    order_book_ids = [ins.order_book_id for ins in ins_list]

    start_date, end_date = ensure_date_range(start_date, end_date, datetime.timedelta(days=3))

    history_permission_denied = realtime_permission_denied = False
    try:
        data = get_client().execute(
            "get_capital_flow_tickbar", order_book_ids, start_date, end_date, fields, market=market
        )
    except PermissionDenied:
        data = []
        history_permission_denied = True

    if data:
        data = [(obid, {k: np.frombuffer(*v) for k, v in d.items()}) for obid, d in data]
        df_list = []
        for obid, d in data:
            df = pd.DataFrame(d)
            df['order_book_id'] = obid
            df_list.append(df)

        df = pd.concat(df_list)  # type: pd.DataFrame
        df["datetime"] = int17_to_datetime_v(df["datetime"].values)
        df.set_index(['order_book_id', 'datetime'], inplace=True)
    else:
        df = None

    live_date = current_trading_date()
    if start_date > live_date or end_date < live_date:
        if history_permission_denied:
            raise PermissionDenied("get_capital_flow_tick")
        return df

    live_date_str = '%d-%02d-%02d' % (live_date // 10000, live_date % 10000 // 100, live_date % 100)
    live_dfs = []

    def _to_trading_date(dt):
        if 7 <= dt.hour < 18:
            return datetime.datetime(year=dt.year, month=dt.month, day=dt.day)
        return get_next_trading_date(dt - datetime.timedelta(hours=4))

    for ins in ins_list:
        if ins.de_listed_date != '0000-00-00' and ins.de_listed_date < live_date_str:
            continue
        try:
            if df is not None and date_to_int8(_to_trading_date(
                    df.loc[ins.order_book_id].index.max())) == live_date:
                continue
        except KeyError:
            pass
        try:
            live_df = get_today_capital_flow_tick(ins.order_book_id, live_date, market=market)
            if live_df is None:
                continue
            live_dfs.append(live_df)
        except PermissionDenied:
            realtime_permission_denied = True
            break
        except MarketNotSupportError:
            pass

    if history_permission_denied and realtime_permission_denied:
        raise PermissionDenied("get_capital_flow_tick")

    if not live_dfs:
        return df

    live_df = pd.concat(live_dfs)
    return pd.concat([df, live_df])


@export_as_api
def get_capital_flow(order_book_ids, start_date=None, end_date=None, frequency="1d", market="cn"):
    """获取资金流入流出数据
    :param order_book_ids: 股票代码or股票代码列表, 如'000001.XSHE'
    :param start_date: 开始日期
    :param end_date: 结束日期
    :param frequency: 默认为日线。日线使用 '1d', 分钟线 '1m'  快照 'tick' (Default value = "1d"),
    :param market:  (Default value = "cn")
    :returns: pandas.DataFrame or None
    """
    ensure_string_in(frequency, ("1d", "1m", "tick"), "frequency")
    if frequency == "tick":
        df = get_capital_flow_tickbar(order_book_ids, start_date, end_date, TICKBAR_FIELDS, market)
        if isinstance(order_book_ids, str):
            return df.droplevel(0)
        return df

    order_book_ids = ensure_order_book_ids(order_book_ids)
    start_date, end_date = ensure_date_range(start_date, end_date)
    if frequency == "1d":
        return get_capital_flow_daybar(order_book_ids, start_date, end_date, DAYBAR_FIELDS, 1, market)

    return get_capital_flow_minbar(order_book_ids, start_date, end_date, MINBAR_FIELDS, 1, market)


def _auction_field_type(field_name):
    return (np.object_ if field_name == "order_book_id"
            else np.uint64 if field_name == "datetime"
            else np.float64)


AUCTION_FIELDS = [
    "open",
    "last",
    "high",
    "low",
    "limit_up",
    "limit_down",
    "prev_close",
    "volume",
    "total_turnover",
    "a1",
    "a2",
    "a3",
    "a4",
    "a5",
    "b1",
    "b2",
    "b3",
    "b4",
    "b5",
    "a1_v",
    "a2_v",
    "a3_v",
    "a4_v",
    "a5_v",
    "b1_v",
    "b2_v",
    "b3_v",
    "b4_v",
    "b5_v",
]


def get_auction_info(order_book_ids, start_date=None, end_date=None, auction_type='close', fields=None, market="cn"):
    assert auction_type in ('open', 'close'), "auction_type must be 'open' or 'close'"

    order_book_ids = ensure_order_book_ids(order_book_ids)
    if not order_book_ids:
        return None

    start_date, end_date = ensure_date_range(start_date, end_date, datetime.timedelta(days=0))
    if fields is None:
        fields = AUCTION_FIELDS
    else:
        fields = ensure_list_of_string(fields, "fields")
        check_items_in_container(fields, set(AUCTION_FIELDS), "fields")

    history_permission_denied = realtime_permission_denied = False
    try:
        data = get_client().execute("get_{}_auction_info_daybar".format(auction_type), order_book_ids,
                                    start_date, end_date, fields + ["datetime", "date"], market=market)
    except PermissionDenied:
        data = []
        history_permission_denied = True

    live_date = current_trading_date()
    live_date_str = '%d-%02d-%02d' % (live_date // 10000, live_date % 10000 // 100, live_date % 100)

    live_obs = set(
        ins.order_book_id for ins in instruments(order_book_ids)
        if ins.de_listed_date == '0000-00-00' or ins.de_listed_date > live_date_str
    )
    if data:
        data = [(obid, {k: np.frombuffer(*v) for k, v in d.items()}) for obid, d in data]

        extra_fields = ['open_interest', 'prev_settlement', 'date'] if any(
            ['prev_settlement' in d for _, d in data]
        ) else ['date']

        df = convert_bar_to_multi_df(data, 'datetime', fields + extra_fields, int17_to_datetime_v, default=0.0)
        if df is not None:
            del df["date"]
    else:
        df = None

    if start_date > live_date or end_date < live_date:
        return df

    if df is not None:
        idx = df.index
        for ob in idx.levels[0]:
            if ob not in live_obs:
                continue
            loc = idx.get_loc(ob)
            if date_to_int8(idx[loc.stop - 1][-1]) == live_date:
                live_obs.remove(ob)

    if not live_obs:
        return df

    try:
        live_df = get_today_auction(list(live_obs), auction_type, live_date, market=market)
    except PermissionDenied:
        live_df = None
        realtime_permission_denied = True
    except MarketNotSupportError:
        live_df = None

    if history_permission_denied and realtime_permission_denied:
        raise PermissionDenied("get_open_auction_info")

    if live_df is None:
        return df
    if 'prev_settlement' in live_df.columns:
        fields = fields + ['open_interest', 'prev_settlement']
    if df is None:
        return live_df[fields]
    df = pd.concat([df, live_df[fields]])
    df.sort_index(inplace=True)
    return df


def get_today_auction(order_book_ids, auction_type='close', today=None,  market="cn"):
    if auction_type == 'close':
        return
        # ticks = get_client().execute('get_today_close_auction', order_book_ids, market=market)
    else:
        ticks = get_client().execute('get_today_open_auction', order_book_ids, today, market=market)
    if not ticks:
        return

    fields = ["order_book_id", "datetime"] + AUCTION_FIELDS

    if any(['prev_settlement' in tick for tick in ticks]):
        fields += ['open_interest', 'prev_settlement']

    dtype = np.dtype([(f, _auction_field_type(f)) for f in fields])
    bars = np.array([tuple([get_tick_value(t, f) for f in fields]) for t in ticks], dtype=dtype)

    df = pd.DataFrame(bars)
    df.datetime = df.datetime.apply(int17_to_datetime)
    df.set_index(["order_book_id", "datetime"], inplace=True)
    return df


@export_as_api
def get_open_auction_info(order_book_ids, start_date=None, end_date=None, fields=None, market="cn"):
    """获取盘前集合竞价数据
    :param order_book_ids: 股票代码
    :param start_date: 起始日期，默认为今天
    :param end_date: 截止日期，默认为今天
    :param fields: 需要获取的字段, 默认为所有字段
    :param market:  (Default value = "cn")
    :returns: pd.DataFrame or None
    """
    return get_auction_info(order_book_ids, start_date, end_date, 'open', fields, market)


@export_as_api
def get_close_auction_info(order_book_ids, start_date=None, end_date=None, fields=None, market="cn"):
    """获取尾盘集合竞价数据
    :param order_book_ids: 股票代码
    :param start_date: 起始日期，默认为今天
    :param end_date: 截止日期，默认为今天
    :param fields: 需要获取的字段, 默认为所有字段
    :param market:  (Default value = "cn")
    :returns: pd.DataFrame or None
    """
    return get_auction_info(order_book_ids, start_date, end_date, 'close', fields, market)
