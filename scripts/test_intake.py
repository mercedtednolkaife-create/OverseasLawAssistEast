import urllib.request
import json

raw_text = """关于马来西亚巴林基安燃煤电站二期 EPC 总承包合同工期顺延与 CIPAA 法定裁决预警通告函

致：马来西亚国家能源公司 (TNB) 沙捞越项目管理部
发件方：中国电力建设集团海外工程联营体 (SinoHydro - PowerChina Consortium)
日期：2024年4月10日

一、合同基本信息与背景
双方于2023年8月15日正式签署《马来西亚巴林基安燃煤电站二期 2×300MW 机组 EPC 总承包合同》（采用 FIDIC 银皮书范本），约定适用马来西亚联邦实体法律，争议管辖约定为亚洲国际仲裁中心 (AIAC) 及马来西亚法定裁决。合同约定工程本地化率采购指标 (TKDN / Local Content) 须达到 35.0%。

二、受阻事实与工期延误
自2024年1月起，因东道国属地原住民土地征收诉讼及当地环境保护局临时停工调查令，导致关键路径主厂房与输水隧洞施工全面受阻，累计造成关键工期滞后达 120 天。总承包商依据 FIDIC 第 8.4 条及合同专用条件，在知悉现场阻碍事件发生后第 14 天向工程师签发索赔通知 (Claim Notice)，请求顺延工期 120 天并补偿窝工窝料损失 2,800 万令吉。

三、争议焦点与法律诉求
业主于2024年4月以“索赔通知超出合理审查期”及分包合同中订有“以总业主给付为前提的背靠背付款条款”为由，全面冻结核发第 6 期工程进度款，并威胁向吉隆坡开证行没收 10% 履约保函 (Performance Bond)。
总承包商依法主张：
1. 依据马来西亚《建设工程付款与快速裁决法》(CIPAA 2012) 第 35 条强行法规定，建设工程分包中任何背靠背付款条款自始绝对无效，业主不得据此抗辩拒付；
2. 索赔通知在 14 天内发出，完全符合 FIDIC 28 天失权前置时效要求，受阻属于不可归责于承包商的业主交地风险；
3. 若业主在 7 日内未纠正违约并解除保函扣划威胁，承包商将依法向 AIAC 提起 CIPAA 极速法定裁决并申请合法停工。"""

req = urllib.request.Request(
    'http://127.0.0.1:8000/api/cases/extract-intake',
    data=json.dumps({'raw_text': raw_text, 'hint_jurisdiction': 'asean_my'}).encode('utf-8'),
    headers={'Content-Type': 'application/json'},
    method='POST'
)
with urllib.request.urlopen(req) as resp:
    res = json.loads(resp.read().decode('utf-8'))
    print("=== EXTRACT INTAKE RESULT ===")
    print("Title:", res.get('title'))
    print("Jurisdiction:", res.get('jurisdiction'))
    print("Governing Law:", res.get('governing_law'))
    print("Lifecycle Stage:", res.get('lifecycle_stage'))
    print("Project Archetype:", res.get('project_archetype'))
    print("Contract Date:", res.get('contract_date'))
    print("Event Date:", res.get('event_date'))
    print("Dispute Resolution:", res.get('dispute_resolution'))
    print("Extracted Params:", res.get('extracted_params'))
