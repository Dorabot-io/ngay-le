"""Sinh dữ liệu ngày nghỉ lễ, Tết Việt Nam 2026–2040 (nghỉ bù, hoán đổi) cho:
  - gói npm @dorabot-io/ngay-le, PyPI dorabot-ngay-le
  - API/MCP https://dorabot.io/lich-am/api/ngay-le.php, /lich-am/mcp

  python apps/lich-am/ngay-le/build.py

Căn cứ:
  - Bộ luật Lao động 2019, Điều 111 khoản 3 (trùng ngày nghỉ hằng tuần thì nghỉ bù ngày làm việc kế tiếp), Điều 112 (11 ngày lễ, Tết).
  - Nghị quyết 28/2026/QH16 (hiệu lực 01/7/2026): 24/11 hằng năm là Ngày Văn hóa Việt Nam, người lao động nghỉ, hưởng nguyên lương.
  - Thông báo hằng năm của Bộ Nội vụ (hoán đổi ngày làm việc, chọn ngày nghỉ Tết / Quốc khánh) → THONG_BAO bên dưới.
Năm/kỳ chưa có thông báo: tính theo luật + cách Bộ Nội vụ hay chọn, đánh dấu du_kien = true.

Ra: data/ngay-le.json (một file, chép vào 2 gói + web).
"""
import datetime as dt
import json
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
D = dt.date

# Mùng 1 Tết và Giỗ Tổ (10/3 âm) — tính bằng apps/lich-am/web/lich-am/includes/la-lunar.php (la_lunar2solar)
TET = {2026: D(2026, 2, 17), 2027: D(2027, 2, 6), 2028: D(2028, 1, 26), 2029: D(2029, 2, 13), 2030: D(2030, 2, 2),
       2031: D(2031, 1, 23), 2032: D(2032, 2, 11), 2033: D(2033, 1, 31), 2034: D(2034, 2, 19), 2035: D(2035, 2, 8),
       2036: D(2036, 1, 28), 2037: D(2037, 2, 15), 2038: D(2038, 2, 4), 2039: D(2039, 1, 24), 2040: D(2040, 2, 12)}
GIO_TO = {2026: D(2026, 4, 26), 2027: D(2027, 4, 16), 2028: D(2028, 4, 4), 2029: D(2029, 4, 23), 2030: D(2030, 4, 12),
          2031: D(2031, 4, 1), 2032: D(2032, 4, 19), 2033: D(2033, 4, 9), 2034: D(2034, 4, 28), 2035: D(2035, 4, 17),
          2036: D(2036, 4, 6), 2037: D(2037, 4, 24), 2038: D(2038, 4, 13), 2039: D(2039, 4, 3), 2040: D(2040, 4, 20)}

BLLD = {'so': 'Bộ luật Lao động 2019 (45/2019/QH14), Điều 111–112', 'url': 'https://vanban.chinhphu.vn/?pageid=27160&docid=198540'}
NQ28 = {'so': 'Nghị quyết 28/2026/QH16 (Ngày Văn hóa Việt Nam 24/11, hiệu lực 01/7/2026)', 'url': 'https://thuvienphapluat.vn/phap-luat/ngay-van-hoa-viet-nam-24-11-duoc-nghi-huong-nguyen-luong-bao-nhieu-ngay-theo-quy-dinh-hien-nay-110888-298186.html'}
TB9441 = {'so': 'Thông báo 9441/TB-BNV ngày 16/10/2025 (Tết Âm lịch, Quốc khánh 2026)', 'url': 'https://moha.gov.vn/tin-tuc/bo-noi-vu-thong-bao-ve-viec-nghi-tet-am-lich-nghi----oid57695'}
TB12590 = {'so': 'Thông báo 12590/TB-BNV (hoán đổi ngày làm việc dịp Tết Dương lịch 2026)', 'url': 'https://tuoitre.vn/bo-noi-vu-thong-tin-chinh-thuc-ve-lich-nghi-tet-duong-lich-2026-20251225113924484.htm'}
VH2026 = {'so': 'Chính phủ đồng ý phương án của Bộ Nội vụ: nghỉ thứ Ba 24/11/2026, không hoán đổi (09/2026)', 'url': 'https://dantri.com.vn/noi-vu/chinh-phu-chot-nghi-1-ngay-ngay-van-hoa-viet-nam-2026-20260919231056506.htm'}
TB11483 = {'so': 'Thông báo 11483/TB-BNV ngày 09/10/2026 (Tết Âm lịch, Quốc khánh 2027)', 'url': 'https://thuvienphapluat.vn/van-ban/Lao-dong-Tien-luong/Thong-bao-11483-TB-BNV-2026-nghi-tet-Am-lich-doi-voi-can-bo-cong-chuc-va-nguoi-lao-dong-728560.aspx'}

# Thông báo đã có: (năm, mã kỳ) -> ngày lễ chính thức (khu vực nhà nước), hoán đổi [(ngày nghỉ, ngày làm bù)], nguồn
THONG_BAO = {
    (2026, 'tet_duong'): {'le': [D(2026, 1, 1)], 'hoan_doi': [(D(2026, 1, 2), D(2026, 1, 10))], 'nguon': TB12590},
    (2026, 'tet_am'): {'le': [D(2026, 2, 16) + dt.timedelta(i) for i in range(5)], 'hoan_doi': [], 'nguon': TB9441},
    (2026, 'quoc_khanh'): {'le': [D(2026, 9, 1), D(2026, 9, 2)], 'hoan_doi': [(D(2026, 8, 31), D(2026, 8, 22))], 'nguon': TB9441},
    (2026, 'van_hoa'): {'le': [D(2026, 11, 24)], 'hoan_doi': [], 'nguon': VH2026},
    (2027, 'tet_am'): {'le': [D(2027, 2, 4) + dt.timedelta(i) for i in range(5)], 'hoan_doi': [], 'nguon': TB11483},
    (2027, 'quoc_khanh'): {'le': [D(2027, 9, 2), D(2027, 9, 3)], 'hoan_doi': [], 'nguon': TB11483},
}

TEN = {'tet_duong': 'Tết Dương lịch', 'tet_am': 'Tết Âm lịch (Tết Nguyên đán)', 'gio_to': 'Giỗ Tổ Hùng Vương (10/3 âm lịch)',
       'le_30_4_1_5': 'Ngày Chiến thắng 30/4 và Quốc tế Lao động 1/5', 'quoc_khanh': 'Quốc khánh (2/9)',
       'van_hoa': 'Ngày Văn hóa Việt Nam (24/11)'}


def qk_mac_dinh(y):
    """2/9 + 1 ngày liền trước hoặc liền sau — chọn như các năm trước (ưu tiên nối với cuối tuần)."""
    q = D(y, 9, 2)
    wd = q.weekday()  # 0 = thứ Hai
    other = q + dt.timedelta(1) if wd in (0, 3, 6) else q - dt.timedelta(1)
    return sorted([q, other])


def ky_le(y):
    """Các kỳ nghỉ của năm y: [(mã, [ngày lễ], [(nghỉ, làm bù)], nguồn, dự kiến)]"""
    out = []
    t = TET[y]
    defaults = {
        'tet_duong': [D(y, 1, 1)],
        'tet_am': [t - dt.timedelta(1) + dt.timedelta(i) for i in range(5)],  # 1 ngày cuối năm + mùng 1–4
        'gio_to': [GIO_TO[y]],
        'le_30_4_1_5': [D(y, 4, 30), D(y, 5, 1)],
        'quoc_khanh': qk_mac_dinh(y),
        'van_hoa': [D(y, 11, 24)],
    }
    for k, le in defaults.items():
        tb = THONG_BAO.get((y, k))
        if tb:
            out.append((k, tb['le'], tb['hoan_doi'], tb['nguon'], False))
        else:
            co_dinh = k in ('gio_to', 'le_30_4_1_5', 'van_hoa', 'tet_duong')
            nguon = NQ28 if k == 'van_hoa' else BLLD
            # ngày lễ cố định theo luật là chắc chắn; chỉ nghỉ bù/hoán đổi còn chờ thông báo
            out.append((k, le, [], nguon, not co_dinh))
    return out


def tinh(y, nghi_tuan):
    """nghi_tuan: tập weekday nghỉ hằng tuần (5 = thứ Bảy, 6 = Chủ nhật). Hoán đổi chỉ áp dụng khu vực nhà nước (nghi_tuan T7+CN)."""
    nha_nuoc = nghi_tuan == {5, 6}
    ky = []
    tat_ca_le = set()
    for k, le, hd, nguon, du_kien in ky_le(y):
        tat_ca_le.update(le)
    da_dung = set()
    for k, le, hd, nguon, du_kien in ky_le(y):
        nghi = set(le)
        bu = []
        # nghỉ bù: mỗi ngày lễ trùng ngày nghỉ hằng tuần -> ngày làm việc kế tiếp (không trùng lễ, chưa dùng)
        so_bu = sum(1 for d in le if d.weekday() in nghi_tuan)
        d = max(le)
        while len(bu) < so_bu:
            d += dt.timedelta(1)
            if d.weekday() in nghi_tuan or d in tat_ca_le or d in da_dung:
                continue
            bu.append(d)
            da_dung.add(d)
        nghi.update(bu)
        hoan = [(a, b) for a, b in hd] if nha_nuoc else []
        nghi.update(a for a, _ in hoan)
        # cả kỳ: mở rộng ra cuối tuần liền kề
        tu, den = min(nghi), max(nghi)
        while (tu - dt.timedelta(1)).weekday() in nghi_tuan:
            tu -= dt.timedelta(1)
        while (den + dt.timedelta(1)).weekday() in nghi_tuan:
            den += dt.timedelta(1)
        ky.append({'ma': k, 'ten': TEN[k], 'tu': tu.isoformat(), 'den': den.isoformat(), 'so_ngay': (den - tu).days + 1,
                   'ngay_le': [x.isoformat() for x in sorted(le)], 'nghi_bu': [x.isoformat() for x in bu],
                   'hoan_doi': [{'nghi': a.isoformat(), 'lam_bu': b.isoformat()} for a, b in hoan],
                   'du_kien': du_kien, 'nguon': nguon})
    return ky


def main():
    out = {'phien_ban': dt.date.today().isoformat(), 'tu_nam': min(TET), 'den_nam': max(TET),
           'ghi_chu': 'nha_nuoc = cán bộ, công chức, viên chức (nghỉ thứ Bảy, Chủ nhật; có hoán đổi theo thông báo Bộ Nội vụ). '
                      'doanh_nghiep_t7cn / doanh_nghiep_cn = người lao động doanh nghiệp nghỉ hằng tuần thứ Bảy + Chủ nhật / chỉ Chủ nhật '
                      '(không tự hoán đổi; Tết Âm lịch doanh nghiệp tự chọn 5 ngày, ở đây theo phương án của khu vực nhà nước). '
                      'du_kien = chưa có thông báo của Bộ Nội vụ, tính theo Bộ luật Lao động.',
           'can_cu': [BLLD, NQ28], 'nam': {}}
    for y in sorted(TET):
        out['nam'][str(y)] = {'nha_nuoc': tinh(y, {5, 6}), 'doanh_nghiep_t7cn': tinh(y, {5, 6}), 'doanh_nghiep_cn': tinh(y, {6})}
        # doanh nghiệp không có hoán đổi
        for kk in out['nam'][str(y)]['doanh_nghiep_t7cn']:
            kk['hoan_doi'] = []
    os.makedirs(os.path.join(ROOT, 'data'), exist_ok=True)
    p = os.path.join(ROOT, 'data', 'ngay-le.json')
    json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
    for dst in ['../packages/ngay-le-js/data', '../packages/ngay-le-py/dorabot_ngay_le/data', '../web/lich-am/api/data']:
        d = os.path.normpath(os.path.join(ROOT, dst))
        os.makedirs(d, exist_ok=True)
        shutil.copy(p, os.path.join(d, 'ngay-le.json'))
    js = os.path.normpath(os.path.join(ROOT, '../packages/ngay-le-js/data/ngay-le.js'))
    open(js, 'w', encoding='utf-8').write('export default ' + open(p, encoding='utf-8').read() + ';\n')
    os.remove(os.path.join(os.path.dirname(js), 'ngay-le.json'))
    print(f'{len(TET)} năm, {os.path.getsize(p) // 1024} KB')
    for k in out['nam']['2026']['nha_nuoc'] + out['nam']['2027']['nha_nuoc']:
        print(k['tu'], '→', k['den'], k['so_ngay'], 'ngày', k['ten'], 'bù', k['nghi_bu'], 'đổi', k['hoan_doi'], '(dự kiến)' if k['du_kien'] else '')


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
