// @dorabot-io/ngay-le — ngày nghỉ lễ, Tết Việt Nam có nghỉ bù và hoán đổi ngày làm việc (2026–2040).
// Dữ liệu: Dorabot (dorabot.io/lich-am), theo Bộ luật Lao động 2019, Nghị quyết 28/2026/QH16 và thông báo hằng năm
// của Bộ Nội vụ. Năm chưa có thông báo: tính theo luật, đánh dấu duKien. Code MIT, dữ liệu CC BY 4.0.
import DATA from './data/ngay-le.js';

export const PHIEN_BAN_DU_LIEU = DATA.phien_ban;
export const TU_NAM = DATA.tu_nam;
export const DEN_NAM = DATA.den_nam;
const DOI_TUONG = { nha_nuoc: [6, 0], doanh_nghiep_t7cn: [6, 0], doanh_nghiep_cn: [0] }; // getUTCDay: 0 = CN, 6 = T7

const iso = (d) => (typeof d === 'string' ? d.slice(0, 10) : new Date(d.getTime() - d.getTimezoneOffset() * 60000).toISOString().slice(0, 10));
const dow = (s) => new Date(`${s}T00:00:00Z`).getUTCDay();
const add = (s, n) => { const d = new Date(`${s}T00:00:00Z`); d.setUTCDate(d.getUTCDate() + n); return d.toISOString().slice(0, 10); };
const doiTuong = (o) => { const k = o?.doiTuong ?? 'nha_nuoc'; if (!DOI_TUONG[k]) throw new Error(`doiTuong phải là ${Object.keys(DOI_TUONG).join(' | ')}`); return k; };

const out = (k) => ({ ma: k.ma, ten: k.ten, tu: k.tu, den: k.den, soNgay: k.so_ngay, ngayLe: k.ngay_le, nghiBu: k.nghi_bu,
  hoanDoi: k.hoan_doi.map((h) => ({ nghi: h.nghi, lamBu: h.lam_bu })), duKien: k.du_kien, nguon: k.nguon });

/**
 * Các kỳ nghỉ lễ, Tết của một năm.
 * @param {number} nam 2026–2040
 * @param {{doiTuong?: 'nha_nuoc'|'doanh_nghiep_t7cn'|'doanh_nghiep_cn'}} [opt] mặc định nha_nuoc (công chức, viên chức)
 */
export function lichNghiLe(nam, opt) {
  const y = DATA.nam[String(nam)];
  if (!y) throw new Error(`Chỉ có dữ liệu năm ${TU_NAM}–${DEN_NAM}`);
  return y[doiTuong(opt)].map(out);
}

const CACHE = {};
function bang(nam, k) {
  const key = `${nam}|${k}`;
  if (CACHE[key]) return CACHE[key];
  const m = { nghi: new Map(), lamBu: new Map() };
  const y = DATA.nam[String(nam)];
  if (y) for (const ky of y[k]) {
    for (const d of ky.ngay_le) m.nghi.set(d, { lyDo: 'le', ten: ky.ten, duKien: ky.du_kien });
    for (const d of ky.nghi_bu) m.nghi.set(d, { lyDo: 'nghi_bu', ten: `Nghỉ bù ${ky.ten}`, duKien: ky.du_kien });
    for (const h of ky.hoan_doi) {
      m.nghi.set(h.nghi, { lyDo: 'hoan_doi', ten: `Nghỉ hoán đổi dịp ${ky.ten} (làm bù ${h.lam_bu})`, duKien: ky.du_kien });
      m.lamBu.set(h.lam_bu, { lyDo: 'lam_bu', ten: `Làm bù cho ngày ${h.nghi} (dịp ${ky.ten})`, duKien: ky.du_kien });
    }
  }
  return (CACHE[key] = m);
}

/**
 * Một ngày có phải ngày nghỉ không.
 * @param {string|Date} ngay "YYYY-MM-DD" hoặc Date
 * @returns {{ngay: string, nghi: boolean, lyDo: 'le'|'nghi_bu'|'hoan_doi'|'cuoi_tuan'|'lam_bu'|'lam_viec', ten?: string, duKien?: boolean, ngoaiPhamVi?: boolean}}
 */
export function kiemNgay(ngay, opt) {
  const k = doiTuong(opt); const s = iso(ngay); const nam = +s.slice(0, 4);
  const b = bang(nam, k);
  const ngoai = nam < TU_NAM || nam > DEN_NAM ? { ngoaiPhamVi: true } : {};
  if (b.nghi.has(s)) return { ngay: s, nghi: true, ...b.nghi.get(s), ...ngoai };
  if (b.lamBu.has(s)) return { ngay: s, nghi: false, ...b.lamBu.get(s), ...ngoai };
  if (DOI_TUONG[k].includes(dow(s))) return { ngay: s, nghi: true, lyDo: 'cuoi_tuan', ten: dow(s) === 0 ? 'Chủ nhật' : 'Thứ Bảy', ...ngoai };
  return { ngay: s, nghi: false, lyDo: 'lam_viec', ...ngoai };
}

/** Số ngày làm việc từ `tu` đến `den` (tính cả hai đầu). */
export function demNgayLamViec(tu, den, opt) {
  let a = iso(tu); const b = iso(den); let n = 0;
  if (a > b) throw new Error('tu phải ≤ den');
  for (; a <= b; a = add(a, 1)) if (!kiemNgay(a, opt).nghi) n++;
  return n;
}

/** Ngày làm việc thứ `soNgay` sau `tu` (không tính `tu`). soNgay âm = lùi lại. Dùng cho hạn giao hàng, hạn xử lý hồ sơ. */
export function congNgayLamViec(tu, soNgay, opt) {
  let s = iso(tu); const step = soNgay < 0 ? -1 : 1; let con = Math.abs(soNgay);
  while (con > 0) { s = add(s, step); if (!kiemNgay(s, opt).nghi) con--; }
  return s;
}

/** Danh sách mọi ngày nghỉ lễ/bù/hoán đổi (không gồm cuối tuần) và ngày làm bù của một năm. */
export function ngayNghi(nam, opt) {
  const b = bang(nam, doiTuong(opt));
  if (!DATA.nam[String(nam)]) throw new Error(`Chỉ có dữ liệu năm ${TU_NAM}–${DEN_NAM}`);
  return {
    nghi: [...b.nghi].map(([ngay, v]) => ({ ngay, ...v })).sort((x, y) => x.ngay.localeCompare(y.ngay)),
    lamBu: [...b.lamBu].map(([ngay, v]) => ({ ngay, ...v })).sort((x, y) => x.ngay.localeCompare(y.ngay)),
  };
}
