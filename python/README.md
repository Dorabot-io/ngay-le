# dorabot-ngay-le

Ngày nghỉ lễ, Tết **Việt Nam** 2026–2040 cho chấm công, tính lương, hạn giao hàng: có **nghỉ bù**, **hoán đổi ngày làm việc** theo thông báo Bộ Nội vụ (thứ Bảy đi làm bù), Tết theo âm lịch, **Ngày Văn hóa Việt Nam 24/11** (nghỉ hưởng lương từ 2026). Năm chưa có thông báo đánh dấu `du_kien`.

```bash
pip install dorabot-ngay-le
```

```python
from dorabot_ngay_le import lich_nghi_le, kiem_ngay, dem_ngay_lam_viec, cong_ngay_lam_viec

kiem_ngay("2026-01-10")            # {'nghi': False, 'ly_do': 'lam_bu', ...}  thứ Bảy đi làm bù
kiem_ngay("2026-11-24")            # {'nghi': True, 'ly_do': 'le', 'ten': 'Ngày Văn hóa Việt Nam (24/11)'}
dem_ngay_lam_viec("2026-02-01", "2026-02-28")   # 15 — công chuẩn tháng 2/2026
cong_ngay_lam_viec("2026-02-13", 3)              # '2026-02-25'
kiem_ngay("2026-01-02", doi_tuong="doanh_nghiep_cn")  # doanh nghiệp không hoán đổi
```

`doi_tuong`: `nha_nuoc` (mặc định), `doanh_nghiep_t7cn`, `doanh_nghiep_cn`.

Còn có: npm `@dorabot-io/ngay-le`, REST `GET https://dorabot.io/lich-am/api/ngay-le.php?nam=2026`, MCP `https://dorabot.io/lich-am/mcp`.
Giấy phép: code MIT, dữ liệu CC BY 4.0 (ghi nguồn "Dorabot (dorabot.io)"). Thấy sai: support@dorabot.io.
