export type DoiTuong = 'nha_nuoc' | 'doanh_nghiep_t7cn' | 'doanh_nghiep_cn';
export interface TuyChon { doiTuong?: DoiTuong }
export interface Nguon { so: string; url: string }
export interface KyNghi {
  ma: 'tet_duong' | 'tet_am' | 'gio_to' | 'le_30_4_1_5' | 'quoc_khanh' | 'van_hoa';
  ten: string; tu: string; den: string; soNgay: number;
  ngayLe: string[]; nghiBu: string[]; hoanDoi: Array<{ nghi: string; lamBu: string }>;
  duKien: boolean; nguon: Nguon;
}
export interface KetQuaNgay {
  ngay: string; nghi: boolean;
  lyDo: 'le' | 'nghi_bu' | 'hoan_doi' | 'cuoi_tuan' | 'lam_bu' | 'lam_viec';
  ten?: string; duKien?: boolean; ngoaiPhamVi?: boolean;
}
export declare const PHIEN_BAN_DU_LIEU: string;
export declare const TU_NAM: number;
export declare const DEN_NAM: number;
export declare function lichNghiLe(nam: number, opt?: TuyChon): KyNghi[];
export declare function kiemNgay(ngay: string | Date, opt?: TuyChon): KetQuaNgay;
export declare function demNgayLamViec(tu: string | Date, den: string | Date, opt?: TuyChon): number;
export declare function congNgayLamViec(tu: string | Date, soNgay: number, opt?: TuyChon): string;
export declare function ngayNghi(nam: number, opt?: TuyChon): {
  nghi: Array<{ ngay: string; lyDo: string; ten: string; duKien: boolean }>;
  lamBu: Array<{ ngay: string; lyDo: string; ten: string; duKien: boolean }>;
};
