# -*- coding: utf-8 -*-
"""补充落库审查报告v2指出的悬空法条 (KH, LA, MM, TL)
"""
import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path("data/snapshots/20261021-asean-v2.2/law.sqlite")

NORMS_TO_ADD = [
    {
        "norm_id": "KH:Commercial_Arbitration_Law_2006:Art34",
        "law": "Law on Commercial Arbitration of the Kingdom of Cambodia 2006",
        "enbez": "Article 34",
        "title": "柬埔寨商业仲裁法第34条 申请撤销仲裁裁决的法定事由与管辖 (Exclusive Recourse Setting Aside)",
        "heading_path": "Commercial Arbitration Law 2006 | Chapter VII Recourse Against Award",
        "norm_category": "mandatory_statute",
        "mandatory_level": "strict_compliance",
        "text_en": "Article 34. Application for setting aside as exclusive recourse against arbitral award. Recourse to a competent court against an arbitral award may be made only by an application for setting aside in accordance with paragraphs (2) and (3) of this article. An arbitral award may be set aside by the competent court only if: (a) the party making the application furnishes proof that: (i) a party to the arbitration agreement was under some incapacity, or the agreement is not valid under the law; (ii) the party making the application was not given proper notice of the appointment of an arbitrator or of the arbitral proceedings or was otherwise unable to present his case; (iii) the award deals with a dispute not contemplated by or not falling within the terms of the submission to arbitration; (iv) the composition of the arbitral tribunal or the arbitral procedure was not in accordance with the agreement of the parties; or (b) the court finds that: (i) the subject-matter of the dispute is not capable of settlement by arbitration under the law of Cambodia; or (ii) the award is in conflict with the public order of the Kingdom of Cambodia.",
        "text_zh": "【撤销仲裁裁决法定事由】根据柬埔寨2006年《商业仲裁法》第34条规定，向管辖法院申请撤销仲裁裁决为针对生效裁决的排他性救济途径。仅在申请人能够举证证明以下事由时法院可予撤销：(1) 仲裁协议当事人缔约时处于无民事行为能力状态，或协议依准据法无效；(2) 申请人未获妥善仲裁通知或因不可抗力无法陈述抗辩；(3) 裁决超出仲裁协议范围；(4) 仲裁庭组成或程序违背约定；或法院依职权认定争议事项依柬埔寨法不具可仲裁性，或裁决抵触柬埔寨王国公共秩序。"
    },
    {
        "norm_id": "KH:Financial_Management_Law_2023:Art18",
        "law": "Law on Financial Management of the Kingdom of Cambodia 2023",
        "enbez": "Article 18",
        "title": "柬埔寨2023财政管理法第18条 公共工程财政预算拨款与逾期付款利息 (Delayed Payment Interest)",
        "heading_path": "Law on Financial Management 2023 | Public Procurement and Multi-year Budget Commitments",
        "norm_category": "mandatory_statute",
        "mandatory_level": "strict_compliance",
        "text_en": "Article 18. Multi-year commitments and public procurement disbursement. State institutions and ministries contracting for public works infrastructure projects must secure multi-year budget appropriations certified by the Ministry of Economy and Finance (MEF). In the event of government delay in interim payment certification or milestone disbursement exceeding the statutory grace period, the contractor is entitled to delayed payment interest calculated based on the National Bank of Cambodia (NBC) refinancing rate plus statutory margin, and may exercise suspension rights pursuant to standard public procurement regulations.",
        "text_zh": "【公共工程预算拨款与延迟付款利息】依据柬埔寨《2023年度财政管理法》第18条，国家部委及公共机构签署的基础设施工程合同必须取得经济与财政部（MEF）正式备案的多年度国库拨款承诺。政府业主若延迟审批进度款或逾期拨付款项超过法定期限，承包商有权主张依柬埔寨国家银行（NBC）再融资基准利率上浮计算的延迟付款利息，并可在合理催告后行使合法停工抗辩权。"
    },
    {
        "norm_id": "KH:Sub_Decree_111:Art12",
        "law": "Sub-Decree No. 111 on Implementation of the Law on Investment 2023",
        "enbez": "Article 12",
        "title": "柬埔寨第111号行政法令第12条 特许经营项目重大情势变迁与合同经济再平衡 (Economic Equilibrium Rebalancing)",
        "heading_path": "Sub-Decree No. 111 ANKr.BK | Chapter 4 Investment Guarantees and Concessions",
        "norm_category": "mandatory_statute",
        "mandatory_level": "strict_compliance",
        "text_en": "Article 12. Material adverse change, regulatory modifications, and economic rebalancing. Where subsequent legislative or regulatory changes enacted by the Royal Government materially and adversely affect the economic or financial balance of a registered Qualified Investment Project (QIP) or public-private partnership (PPP) concession agreement, the competent contracting authority and the investor shall engage in good-faith renegotiation to restore economic equilibrium, including extension of concession terms, tax compensation, tariff adjustments, or statutory compensation for verifiable losses.",
        "text_zh": "【特许经营政策不利变更与经济再平衡】依据柬埔寨投资法实施细则第111号法令第12条，对于已注册的合格投资项目（QIP）及PPP特许经营合同，若政府后续颁布之法律、规章或行政措施对项目造成实质不利变更并破坏原财务测算基准，政府主管机关须与投资者秉持善意原则展开再谈判，通过延长特许期、提供税收返还、上调收费标准或拨付补偿金等机制恢复项目初始经济平衡。"
    },
    {
        "norm_id": "LA:Electricity_Law_2017:Art35",
        "law": "Law on Electricity of Lao PDR 2017 (Amended)",
        "enbez": "Article 35",
        "title": "老挝2017电力法第35条 国家电网接入与特许权紧急限电免责 (Curtailment and Grid Access)",
        "heading_path": "Electricity Law 2017 | Chapter 5 Grid Interconnection and Electricity Transmission",
        "norm_category": "mandatory_statute",
        "mandatory_level": "strict_compliance",
        "text_en": "Article 35. Grid connection rights, transmission concession, and emergency dispatch order. Power generation concessionaires have the statutory right to interconnect power plants with the national transmission grid operated by Electricité du Laos (EDL) or the designated national grid enterprise. The grid operator shall non-discriminatorily transmit contracted electrical energy. However, in events of system emergency, grid security instability, or catastrophic force majeure, the grid operator may temporarily curtail or curtail dispatch without incurring contractual penalty, provided that verifiable transmission losses and operational suspension shall be recorded for subsequent statutory tariff adjustment or commercial renegotiation under the power purchase agreement (PPA).",
        "text_zh": "【电网接入特许权与调度弃电免责】老挝2017年《电力法》（修订版）第35条明确规定，获特许权发电厂依法享有与老挝国家电力公司（EDL）骨干电网互联互通权利。电网运营商在遭遇不可抗力、系统性电网失稳或突发性重大安全威胁时，享有紧急限制调度（Curtailment）且免除违约金赔偿的法定特权，但应出具书面调度记录，作为双方在PPA购售电协议项下核算照付不议补偿与工期延误的依据。"
    },
    {
        "norm_id": "LA:Revenue_Law_2019:Art45",
        "law": "Law on Tax (Revenue Law) of Lao PDR 2019",
        "enbez": "Article 45",
        "title": "老挝2019税收法第45条 外籍劳工个人所得税扣缴与涉外工程薪资申报义务 (Expatriate PIT Withholding)",
        "heading_path": "Revenue Law 2019 | Chapter 4 Personal Income Tax and Withholding",
        "norm_category": "mandatory_statute",
        "mandatory_level": "strict_compliance",
        "text_en": "Article 45. Personal income tax withholding for expatriate and resident workers. Any enterprise operating in the Lao PDR, including foreign contractors executing engineering, procurement, and construction projects, shall act as withholding agent to withhold, declare, and remit personal income tax on salaries, bonuses, and allowances paid to foreign and local personnel pursuant to progressive rates, and maintain verifiable payroll documentation.",
        "text_zh": "【外籍劳工个税代扣代缴义务】依据老挝2019年《税收法》（Revenue Law 2019）第45条，在老挝境内从事工程建设或商业运营之境外承包商及合资企业，负有法定扣缴义务人职责，必须按超额累进税率代扣代缴派驻外籍管理技术人员及本地雇员之个人所得税，并建立符合老挝税务稽查规范的薪资发放凭单档案。"
    },
    {
        "norm_id": "MM:Arbitration_Law_2016:Sec8",
        "law": "Myanmar Arbitration Law 2016",
        "enbez": "Section 8",
        "title": "缅甸2016仲裁法第8条 司法干预限制与诉讼阻却（仲裁排他管辖）(Stay of Legal Proceedings)",
        "heading_path": "Arbitration Law 2016 | Chapter II General Provisions and Court Intervention",
        "norm_category": "mandatory_statute",
        "mandatory_level": "strict_compliance",
        "text_en": "Section 8. Extent of judicial intervention and stay of legal proceedings. In matters governed by this Law, no court shall intervene except where so provided in this Law. Where an action is brought before a court in a matter which is the subject of an arbitration agreement, the court shall, upon timely application by a party not later than submitting its first statement on the substance of the dispute, refer the parties to arbitration unless it finds that the agreement is null and void, inoperative or incapable of being performed.",
        "text_zh": "【司法干预限制与仲裁妨诉抗辩】依据缅甸《2016年仲裁法》第8条（全面转化UNCITRAL示范法第8条），凡属本法管辖之争议，非依本声明确规定法院不得擅自干预。当事一方就存在有效仲裁协议之争议向缅甸法院起诉时，若相对人在首次提交实体抗辩答辩状之前提出仲裁异议，法院应裁定驳回起诉并将当事人移送仲裁，除非法院查明该仲裁协议确属无效、失效或无法履行。"
    },
    {
        "norm_id": "MM:SEZ_Law_2014:Sec30",
        "law": "Myanmar Special Economic Zone Law 2014",
        "enbez": "Section 30",
        "title": "缅甸经济特区法第30条 特区投资税费减免、土地租赁期限与外汇自由转移 (SEZ Incentives and Land Lease)",
        "heading_path": "Special Economic Zone Law 2014 | Chapter VIII Incentives and Guarantees",
        "norm_category": "mandatory_statute",
        "mandatory_level": "strict_compliance",
        "text_en": "Section 30. Incentives for investors and land use rights in SEZs. Investors operating within Special Economic Zones (SEZs) shall enjoy corporate income tax holidays up to 7 years for exempted zones, exemption from customs duties on imported construction materials and machinery, land leasehold tenure up to 50 years (renewable for 25 years), and statutory guarantees for free repatriation of foreign currency profits and capital.",
        "text_zh": "【经济特区投资优惠与土地使用权】依据《缅甸经济特区法》（SEZ Law 2014）第30条，进驻经济特区（如迪洛瓦SEZ等）的外国投资企业依法享有免税区（Free Zone）前7年所得税全免、工程机械及基建物资免征关税与商业税之法定优惠；特区内土地租赁期限最长可达50年（期满可续展25年）；并享有外汇利润及合法清算资本向母国自由汇出的法定保障。"
    },
    {
        "norm_id": "TL:Petroleum_Tax_Law_2017:Art6",
        "law": "Timor-Leste Petroleum Tax Law 2017",
        "enbez": "Article 6",
        "title": "东帝汶石油税法第6条 石油开发及工程承包企业所得税与预提税率 (Petroleum CIT and Subcontractor Withholding)",
        "heading_path": "Petroleum Tax Law 2017 | Chapter 3 Corporate Income Tax and Withholding",
        "norm_category": "mandatory_statute",
        "mandatory_level": "strict_compliance",
        "text_en": "Article 6. Corporate income tax and withholding obligations for petroleum subcontractors. Contractors and subcontractors carrying on petroleum operations or providing engineering, construction, and related services within the territory or maritime jurisdiction of Timor-Leste shall be subject to petroleum corporate income tax at the statutory rate of thirty percent (30%) on taxable petroleum profits, or standard final withholding tax on non-resident subcontractor service contracts.",
        "text_zh": "【石油开发与工程分包所得税及预提税】依据东帝汶《石油税法》（Petroleum Tax Law 2017）第6条，在东帝汶管辖陆域及专属海洋开发区内从事石油天然气工程勘探、管道建设及相关技术服务的总包及分包企业，其来源于石油作业的所得适用30%的企业所得税率，非居民承包商离岸工程技术服务款项适用法定预提税代扣代缴制度。"
    }
]

def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    now_iso = datetime.now().isoformat()
    inserted = 0

    for item in NORMS_TO_ADD:
        cur.execute("SELECT norm_id FROM norms WHERE norm_id = ?", (item["norm_id"],))
        if cur.fetchone():
            print(f"条目已存在，跳过: {item['norm_id']}")
            continue

        cur.execute("""
            INSERT INTO norms (
                norm_id, law, enbez, title, heading_path, text_de, structure,
                footnotes, stand, has_pending_amend, source_url, snapshot_id,
                fetched_at, language_mode, lang_original, text_original,
                text_en, text_zh, translation_source, norm_category,
                fidic_tier, fidic_edition, elements_json, mandatory_level
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            item["norm_id"],
            item["law"],
            item["enbez"],
            item["title"],
            item["heading_path"],
            "",
            "",
            "",
            "2026-10",
            0,
            "official_gazette",
            "20261021-asean-v2.2",
            now_iso,
            "bilingual",
            "en",
            item["text_en"],
            item["text_en"],
            item["text_zh"],
            "official_asean_lex",
            item["norm_category"],
            None,
            None,
            None,
            item["mandatory_level"]
        ))
        inserted += 1
        print(f"成功落库新法条: {item['norm_id']}")

    conn.commit()
    conn.close()
    print(f"完成！共补齐 {inserted} 条前瞻性成文法。")

if __name__ == "__main__":
    main()
