import { test } from 'node:test';
import assert from 'node:assert/strict';
import { lichNghiLe, kiemNgay, demNgayLamViec, congNgayLamViec, ngayNghi } from './index.js';

test('2026 khu vực nhà nước theo thông báo Bộ Nội vụ', () => {
  const k = Object.fromEntries(lichNghiLe(2026).map((x) => [x.ma, x]));
  assert.deepEqual([k.tet_duong.tu, k.tet_duong.den], ['2026-01-01', '2026-01-04']);
  assert.deepEqual([k.tet_am.tu, k.tet_am.den, k.tet_am.soNgay], ['2026-02-14', '2026-02-22', 9]);
  assert.deepEqual([k.quoc_khanh.tu, k.quoc_khanh.den], ['2026-08-29', '2026-09-02']);
  assert.equal(k.van_hoa.tu, '2026-11-24');
  assert.equal(kiemNgay('2026-01-10').lyDo, 'lam_bu');       // thứ Bảy đi làm bù
  assert.equal(kiemNgay('2026-01-10').nghi, false);
  assert.equal(kiemNgay('2026-04-27').lyDo, 'nghi_bu');      // Giỗ Tổ trùng Chủ nhật
  assert.equal(kiemNgay('2026-08-31').lyDo, 'hoan_doi');
});

test('2027 Tết 7 ngày, Quốc khánh 4 ngày', () => {
  const k = Object.fromEntries(lichNghiLe(2027).map((x) => [x.ma, x]));
  assert.deepEqual([k.tet_am.tu, k.tet_am.den], ['2027-02-04', '2027-02-10']);
  assert.deepEqual(k.tet_am.nghiBu, ['2027-02-09', '2027-02-10']);
  assert.deepEqual([k.quoc_khanh.tu, k.quoc_khanh.den], ['2027-09-02', '2027-09-05']);
  assert.equal(kiemNgay('2027-05-03').lyDo, 'nghi_bu');
});

test('doanh nghiệp: không hoán đổi, nghỉ tuần chỉ Chủ nhật', () => {
  const o = { doiTuong: 'doanh_nghiep_cn' };
  assert.equal(kiemNgay('2026-01-02', o).nghi, false);
  assert.equal(kiemNgay('2026-01-10', o).lyDo, 'lam_viec');
  assert.equal(kiemNgay('2026-01-03', o).lyDo, 'lam_viec');  // thứ Bảy
  assert.equal(ngayNghi(2026, o).lamBu.length, 0);
});

test('đếm, cộng ngày làm việc', () => {
  assert.equal(demNgayLamViec('2026-02-01', '2026-02-28'), 15);   // 20 ngày thường − 5 ngày Tết
  assert.equal(congNgayLamViec('2026-02-13', 1), '2026-02-23');    // qua kỳ nghỉ Tết
  assert.equal(congNgayLamViec('2026-01-09', 1), '2026-01-10');    // thứ Bảy làm bù là ngày làm việc
  assert.equal(congNgayLamViec('2026-02-23', -1), '2026-02-13');
});
