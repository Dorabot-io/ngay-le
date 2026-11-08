# @dorabot-io/ngay-le

Ngày nghỉ lễ, Tết **Việt Nam** cho app chấm công, tính lương, hạn giao hàng, hạn xử lý hồ sơ — có đủ thứ mà thư viện ngày lễ quốc tế thiếu:

- **Nghỉ bù** khi ngày lễ trùng thứ Bảy/Chủ nhật (Điều 111 Bộ luật Lao động 2019).
- **Hoán đổi ngày làm việc** theo thông báo hằng năm của Bộ Nội vụ (vd 2026: nghỉ 02/01, đi làm bù thứ Bảy 10/01).
- **Tết Âm lịch** đúng ngày theo âm lịch, đúng phương án Bộ Nội vụ chọn.
- **Ngày Văn hóa Việt Nam 24/11** — ngày nghỉ hưởng lương mới từ 2026 (Nghị quyết 28/2026/QH16).
- Hai nhóm: cán bộ, công chức (`nha_nuoc`) và doanh nghiệp (nghỉ tuần T7+CN hoặc chỉ CN, không hoán đổi).

Dữ liệu 2026–2040. Năm đã có thông báo của Bộ Nội vụ: theo thông báo (có số văn bản + link). Năm chưa có: tính theo luật, đánh dấu `duKien: true`.

```bash
npm i @dorabot-io/ngay-le
```

```js
import { lichNghiLe, kiemNgay, demNgayLamViec, congNgayLamViec } from '@dorabot-io/ngay-le';

lichNghiLe(2026);
// [{ ten: 'Tết Dương lịch', tu: '2026-01-01', den: '2026-01-04', hoanDoi: [{ nghi: '2026-01-02', lamBu: '2026-01-10' }], nguon: {...} },
//  { ten: 'Tết Âm lịch (Tết Nguyên đán)', tu: '2026-02-14', den: '2026-02-22', soNgay: 9, ... }, ...]

kiemNgay('2026-01-10');   // { nghi: false, lyDo: 'lam_bu', ten: 'Làm bù cho ngày 2026-01-02 …' }   ← thứ Bảy vẫn đi làm
kiemNgay('2026-04-27');   // { nghi: true, lyDo: 'nghi_bu', ten: 'Nghỉ bù Giỗ Tổ Hùng Vương …' }
kiemNgay('2026-11-24');   // { nghi: true, lyDo: 'le', ten: 'Ngày Văn hóa Việt Nam (24/11)' }

demNgayLamViec('2026-02-01', '2026-02-28');           // 15 — công chuẩn tháng 2/2026
congNgayLamViec('2026-02-13', 3);                      // '2026-02-25' — hạn 3 ngày làm việc, qua Tết
kiemNgay('2026-01-02', { doiTuong: 'doanh_nghiep_cn' }); // { nghi: false } — doanh nghiệp không hoán đổi
```

`doiTuong`: `nha_nuoc` (mặc định), `doanh_nghiep_t7cn`, `doanh_nghiep_cn`. Doanh nghiệp tự chọn 5 ngày Tết Âm lịch; gói dùng phương án của khu vực nhà nước — app cho chỉnh nếu công ty chọn khác.

Còn có: Python `pip install dorabot-ngay-le`, REST `GET https://dorabot.io/lich-am/api/ngay-le.php?nam=2026`, MCP `https://dorabot.io/lich-am/mcp` (cho Claude, ChatGPT, Cursor). Lịch âm, ngày tốt, văn khấn: https://dorabot.io/lich-am/

Giấy phép: code MIT, dữ liệu CC BY 4.0 (ghi nguồn "Dorabot (dorabot.io)"). Thông báo mới của Bộ Nội vụ được cập nhật trong vài ngày (nâng version); thấy sai: support@dorabot.io.
*Dorabot (dorabot.io) là công cụ của Việt Nam, không liên quan tới dorabot.com.*

---

**English.** Vietnam public holidays 2026–2040 with compensatory days off, government-announced working-day swaps (e.g. work on Saturday 10 Jan 2026), lunar-calendar Tết, and the new 24 November Vietnamese Culture Day (from 2026). `kiemNgay(date)` = is it a day off, `demNgayLamViec(from, to)` = business days, `congNgayLamViec(date, n)` = add n business days. Public sector vs private companies (Sat+Sun or Sun-only weekly rest). Code MIT, data CC BY 4.0.
