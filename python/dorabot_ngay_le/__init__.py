"""dorabot-ngay-le — ngày nghỉ lễ, Tết Việt Nam 2026–2040 có nghỉ bù, hoán đổi ngày làm việc.

Dữ liệu: Dorabot (dorabot.io/lich-am) theo Bộ luật Lao động 2019, Nghị quyết 28/2026/QH16 và thông báo hằng năm
của Bộ Nội vụ. Năm chưa có thông báo: tính theo luật, du_kien = True. Code MIT, dữ liệu CC BY 4.0.

    from dorabot_ngay_le import lich_nghi_le, kiem_ngay, dem_ngay_lam_viec, cong_ngay_lam_viec
"""
import datetime as _dt
import json
import os

__version__ = '1.0.0'
with open(os.path.join(os.path.dirname(__file__), 'data', 'ngay-le.json'), encoding='utf-8') as _f:
    _DATA = json.load(_f)
PHIEN_BAN_DU_LIEU = _DATA['phien_ban']
TU_NAM, DEN_NAM = _DATA['tu_nam'], _DATA['den_nam']
_NGHI_TUAN = {'nha_nuoc': {5, 6}, 'doanh_nghiep_t7cn': {5, 6}, 'doanh_nghiep_cn': {6}}  # date.weekday(): 5 = T7, 6 = CN
__all__ = ['lich_nghi_le', 'kiem_ngay', 'dem_ngay_lam_viec', 'cong_ngay_lam_viec', 'ngay_nghi', 'PHIEN_BAN_DU_LIEU', 'TU_NAM', 'DEN_NAM']


def _d(x):
    if isinstance(x, _dt.datetime):
        return x.date()
    if isinstance(x, _dt.date):
        return x
    return _dt.date.fromisoformat(str(x)[:10])


def _dt_check(doi_tuong):
    if doi_tuong not in _NGHI_TUAN:
        raise ValueError('doi_tuong phải là ' + ' | '.join(_NGHI_TUAN))
    return doi_tuong


def lich_nghi_le(nam, doi_tuong='nha_nuoc'):
    """Các kỳ nghỉ lễ, Tết của một năm (tu, den, ngay_le, nghi_bu, hoan_doi, du_kien, nguon)."""
    y = _DATA['nam'].get(str(nam))
    if not y:
        raise ValueError(f'Chỉ có dữ liệu năm {TU_NAM}–{DEN_NAM}')
    return [dict(k) for k in y[_dt_check(doi_tuong)]]


_CACHE = {}


def _bang(nam, doi_tuong):
    key = (nam, doi_tuong)
    if key in _CACHE:
        return _CACHE[key]
    nghi, lam_bu = {}, {}
    for ky in (_DATA['nam'].get(str(nam)) or {}).get(doi_tuong, []):
        for d in ky['ngay_le']:
            nghi[d] = {'ly_do': 'le', 'ten': ky['ten'], 'du_kien': ky['du_kien']}
        for d in ky['nghi_bu']:
            nghi[d] = {'ly_do': 'nghi_bu', 'ten': 'Nghỉ bù ' + ky['ten'], 'du_kien': ky['du_kien']}
        for h in ky['hoan_doi']:
            nghi[h['nghi']] = {'ly_do': 'hoan_doi', 'ten': f"Nghỉ hoán đổi dịp {ky['ten']} (làm bù {h['lam_bu']})", 'du_kien': ky['du_kien']}
            lam_bu[h['lam_bu']] = {'ly_do': 'lam_bu', 'ten': f"Làm bù cho ngày {h['nghi']} (dịp {ky['ten']})", 'du_kien': ky['du_kien']}
    _CACHE[key] = (nghi, lam_bu)
    return _CACHE[key]


def kiem_ngay(ngay, doi_tuong='nha_nuoc'):
    """Một ngày có nghỉ không. ly_do: le | nghi_bu | hoan_doi | cuoi_tuan | lam_bu | lam_viec."""
    d = _d(ngay)
    s = d.isoformat()
    nghi, lam_bu = _bang(d.year, _dt_check(doi_tuong))
    extra = {'ngoai_pham_vi': True} if not (TU_NAM <= d.year <= DEN_NAM) else {}
    if s in nghi:
        return dict(ngay=s, nghi=True, **nghi[s], **extra)
    if s in lam_bu:
        return dict(ngay=s, nghi=False, **lam_bu[s], **extra)
    if d.weekday() in _NGHI_TUAN[doi_tuong]:
        return dict(ngay=s, nghi=True, ly_do='cuoi_tuan', ten='Chủ nhật' if d.weekday() == 6 else 'Thứ Bảy', **extra)
    return dict(ngay=s, nghi=False, ly_do='lam_viec', **extra)


def dem_ngay_lam_viec(tu, den, doi_tuong='nha_nuoc'):
    """Số ngày làm việc từ tu đến den (tính cả hai đầu)."""
    a, b = _d(tu), _d(den)
    if a > b:
        raise ValueError('tu phải ≤ den')
    n = 0
    while a <= b:
        if not kiem_ngay(a, doi_tuong)['nghi']:
            n += 1
        a += _dt.timedelta(1)
    return n


def cong_ngay_lam_viec(tu, so_ngay, doi_tuong='nha_nuoc'):
    """Ngày làm việc thứ so_ngay sau tu (không tính tu); âm = lùi lại. Trả 'YYYY-MM-DD'."""
    d = _d(tu)
    step = -1 if so_ngay < 0 else 1
    con = abs(so_ngay)
    while con > 0:
        d += _dt.timedelta(step)
        if not kiem_ngay(d, doi_tuong)['nghi']:
            con -= 1
    return d.isoformat()


def ngay_nghi(nam, doi_tuong='nha_nuoc'):
    """{'nghi': [...], 'lam_bu': [...]} — mọi ngày nghỉ lễ/bù/hoán đổi và ngày làm bù của năm."""
    if str(nam) not in _DATA['nam']:
        raise ValueError(f'Chỉ có dữ liệu năm {TU_NAM}–{DEN_NAM}')
    nghi, lam_bu = _bang(int(nam), _dt_check(doi_tuong))
    return {'nghi': [dict(ngay=k, **v) for k, v in sorted(nghi.items())],
            'lam_bu': [dict(ngay=k, **v) for k, v in sorted(lam_bu.items())]}
