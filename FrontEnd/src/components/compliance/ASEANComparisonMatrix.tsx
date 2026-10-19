import React from 'react';

interface ComparisonRow {
  dimension: string;
  id: string;
  vn: string;
  my: string;
  sg: string;
  th: string;
  ph: string;
}

const COMPARISON_DATA: ComparisonRow[] = [
  {
    dimension: '法系与司法特征',
    id: '大陆法系 + 习惯法 (Adat) + 伊斯兰法',
    vn: '社会主义成文法系 (成文法典至上)',
    my: '普通法系 (遵循判例，判例法约束力强)',
    sg: '普通法系 (国际工程争议解决中心 SIAC)',
    th: '大陆法系 (民商法典编纂体例)',
    ph: '混合法系 (美式普通法 + 西班牙大陆法)',
  },
  {
    dimension: '法源语种与签署要求',
    id: '三语模式 (印尼语正本 + 权威英译 + 中文精译)；依据 SEMA 3/2023 无恶意不得机械判合同无效',
    vn: '三语模式 (越语正本 + 权威英译 + 中文精译)；政府备案强制越文，涉外合同可约定英文为主',
    my: '双语模式 (官方英文正本 + 中文精译)；商事与工程合同全面通行英文',
    sg: '双语模式 (官方英文正本 + 中文精译)；100% 通行英文',
    th: '三语模式 (泰语正本 + 权威英译 + 中文精译)；公共采购强制泰语，商事可约定英文',
    ph: '双语模式 (官方英文正本 + 中文精译)；100% 通行英文',
  },
  {
    dimension: '核心工程与投资法典 (2026现行有效)',
    id: '《建筑服务法》(UU 2/2017)；《综合创造就业法》(UU 6/2023)；能矿部 MEMR 11/2024 电力 TKDN 规程',
    vn: '《2025新建设法》(Law 135/2025/QH15)；《第210/2026/ND-CP号建设合同法令》；《PPP法》(Law 64/2020)',
    my: '《建设工程付款与快速裁决法》(CIPAA 2012)；《建筑业发展局法》(Act 520)；《1950合同法》',
    sg: '《建筑业付款保障法》(SOPA 2004)；《建筑管制法》(Building Control Act)；《国际仲裁法》(IAA)',
    th: '《民商法典》(CCC) 承揽编；《外商经营法》(FBA 1999)；《PPP法》(2019)',
    ph: '《菲律宾PPP法典》(RA 11966，已全面废止旧BOT法)；《新政府采购法》(RA 12009)；《承包商执照法》(RA 4566)',
  },
  {
    dimension: '外资施工准入与联营红线',
    id: '设立 BUJKA 代表处（强制与本土大型企业组建 KSO 联营体），或设立合资 PMA（受 KBLI 股比限制）',
    vn: '中标后逐项目申请“外国承包商许可证”(Contractor Permit)，强制与越南本土承包商联营或分包',
    my: '注册本地公司并取得 CIDB G7 级牌照（无投标金额上限），公建项目受土著 (Bumiputera) 配额制约',
    sg: '取得 BCA 承包商注册系统 (CRS) CW01/CW02 A1 级资质，市场化开放透明',
    th: '受 FBA 附件三限制（外资上限 49%），除非取得 BOI 投资促进优惠或申请外商经营许可证 (FBL)',
    ph: '最高院 Manila Water 案已废除常规施工牌照 60% 菲籍股权门槛，但公建采购与特许经营仍受审查',
  },
  {
    dimension: '工程款追索与背靠背条款效力',
    id: '无快速裁决法，通过 BANI 或境外 SIAC 仲裁',
    vn: '无快速裁决法；新建设法正式承认预定违约金 (LD)，打破 12% 封顶',
    my: 'CIPAA 2012 第 35 条宣布“背靠背付款 (Pay-when-paid)”一律无效，支持 45 天极速法定裁决',
    sg: 'SOPA 第 9 条宣布“背靠背付款”一律无效，7~14 天极速付款响应与裁决机制',
    th: '无快速裁决法；公共工程纠纷受最高行政法院管辖',
    ph: '由建设行业仲裁委员会 (CIAC) 专属法定管辖（合同约定其他机构仍不排除 CIAC 管辖权）',
  },
  {
    dimension: '见索即付独立保函止付司法标准',
    id: '极难止付，地方法院程序冗长，建议约定 SIAC 仲裁并申请紧急仲裁员 (EA) 禁令',
    vn: '法院对独立保函干预保守，需依托国际仲裁紧急财产保全联动',
    my: '适用 Sumatec 先例：承认“欺诈例外”与严格限定的“显失公平 (Unconscionability)”',
    sg: '适用 BS Mount Sophia 先例：确立“显失公平 (Unconscionability)”独立保函止付裁定标准',
    th: '严格遵循“欺诈例外”，需向泰国法院提供高额反担保金',
    ph: '适用“欺诈例外与滥用权利”标准，申请临时禁令 (TRO) 审限严苛',
  },
];

export const ASEANComparisonMatrix: React.FC = () => {
  return (
    <div className="bg-white rounded-2xl border border-zinc-200/80 p-6 shadow-xs space-y-4">
      <div className="border-b border-zinc-100 pb-4">
        <div className="flex items-center gap-2">
          <span className="w-2 h-2 rounded-full bg-blue-600" />
          <h3 className="text-base font-bold text-zinc-900">
            东盟核心六国涉外基建与并购实务横向对比矩阵 (2026 现行有效法源版)
          </h3>
        </div>
        <p className="text-xs text-zinc-500 mt-1">
          直观横向比对东盟六国法系、语种模式、2026最新法典、准入联营红线、工程款追索与保函止付标准
        </p>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse min-w-[900px]">
          <thead>
            <tr className="border-b border-zinc-200 bg-zinc-50/70">
              <th className="py-3 px-3 text-xs font-bold text-zinc-700 w-44">
                实务审查维度
              </th>
              <th className="py-3 px-3 text-xs font-bold text-zinc-900">
                🇮🇩 印度尼西亚
              </th>
              <th className="py-3 px-3 text-xs font-bold text-zinc-900">
                🇻🇳 越南
              </th>
              <th className="py-3 px-3 text-xs font-bold text-zinc-900">
                🇲🇾 马来西亚
              </th>
              <th className="py-3 px-3 text-xs font-bold text-zinc-900">
                🇸🇬 新加坡
              </th>
              <th className="py-3 px-3 text-xs font-bold text-zinc-900">
                🇹🇭 泰国
              </th>
              <th className="py-3 px-3 text-xs font-bold text-zinc-900">
                🇵🇭 菲律宾
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-zinc-100 text-xs text-zinc-700">
            {COMPARISON_DATA.map((row, idx) => (
              <tr key={idx} className="hover:bg-zinc-50/60 transition-colors">
                <td className="py-3.5 px-3 font-bold text-zinc-900 bg-zinc-50/40">
                  {row.dimension}
                </td>
                <td className="py-3.5 px-3 leading-relaxed">{row.id}</td>
                <td className="py-3.5 px-3 leading-relaxed">{row.vn}</td>
                <td className="py-3.5 px-3 leading-relaxed">{row.my}</td>
                <td className="py-3.5 px-3 leading-relaxed">{row.sg}</td>
                <td className="py-3.5 px-3 leading-relaxed">{row.th}</td>
                <td className="py-3.5 px-3 leading-relaxed">{row.ph}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
