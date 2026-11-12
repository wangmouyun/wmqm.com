#!/usr/bin/env python3
"""Build the complete static site. No third-party dependencies required."""
import argparse
import json
import shutil
from html import escape
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--origin', default='https://www.wmqm.com')
parser.add_argument('--out', default=str(ROOT))
args = parser.parse_args()
OUT = Path(args.out)
OUT.mkdir(parents=True, exist_ok=True)
ORIGIN = args.origin.rstrip('/')
ASSET_BASE = 'https://wmqm.wmou.com/assets/'
if OUT.resolve() != ROOT.resolve():
    shutil.copytree(ROOT / 'assets', OUT / 'assets', dirs_exist_ok=True)

ADDRESS = '上海市奉贤区奉城镇川南奉公路9650号'
INQUIRY_ENDPOINT = 'https://tongzhi.wangxiansheng.com/api/notify.php'
AREA_CITIES = ['上海','南京','苏州','无锡','常州','镇江','杭州','嘉兴','湖州','绍兴','合肥','滁州','马鞍山']
AREA_PROVINCES = ['上海市','江苏省','浙江省','安徽省']
AREA_GROUPS = [('上海市','上海'),('江苏省','南京、苏州、无锡、常州、镇江'),('浙江省','杭州、嘉兴、湖州、绍兴'),('安徽省','合肥、滁州、马鞍山')]
NAV = [('https://www.wmqm.com','首页'),('about.html','关于我们'),('services.html','业务服务'),('selection.html','选型参考'),('faq.html','常见问题'),('contact.html','联系我们')]
ARROW = '<span class="arrow" aria-hidden="true">↗</span>'
ICONS = {
 'phone':'<path d="M7 3H4a1 1 0 0 0-1 1c0 9.4 7.6 17 17 17a1 1 0 0 0 1-1v-3l-5-2-2 2a14 14 0 0 1-7-7l2-2-2-5Z"/>',
 'pin':'<path d="M19 10c0 5-7 11-7 11S5 15 5 10a7 7 0 1 1 14 0Z"/><circle cx="12" cy="10" r="2.5"/>',
 'menu':'<path d="M4 6h16M4 12h16M4 18h16"/>',
 'search':'<circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 5 5"/>',
 'mail':'<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 6 9 7 9-7"/>',
 'rental':'<path d="M3 6h13v11H3zM16 10h3l3 4v3h-6M6 3h7M6 10h7M6 13h4"/><circle cx="7" cy="18" r="2"/><circle cx="18" cy="18" r="2"/>',
 'sales':'<path d="M3 8h18v12H3zM3 8l5-5h8l5 5M8 8V4M16 8V4M8 12v5M12 12v5M16 12v5"/>',
 'custom':'<path d="M3 5h18v14H3zM7 5v4M11 5v3M15 5v4M19 5v3M3 15h4M3 11h3M13 13l3 3M12 17l6-6"/>',
 'recycling':'<path d="m17 3 4 5-6 1M21 8a9 9 0 0 0-16-3M7 21l-4-5 6-1M3 16a9 9 0 0 0 16 3"/><path d="M9 9h6v6H9z"/>',
 'check':'<path d="m5 12 4 4L19 6"/>',
 'range':'<path d="M3 5v14M21 5v14M3 12h18M7 8l-4 4 4 4M17 8l4 4-4 4"/>',
}
def icon(name):
    return f'<svg class="icon" viewBox="0 0 24 24" aria-hidden="true">{ICONS[name]}</svg>'

FAQ = [
 ('产品与规格','电动双飞翼车厢主要适合哪些装卸场景？','两侧翼板开启后，可为具备作业条件的场地提供侧向装卸空间。选型时需结合货物类型、托盘与叉车作业方式、上方净空、侧面通道以及车辆安装条件，判断是否匹配实际运输任务。'),
 ('产品与规格','可以咨询哪些长度的双飞翼车厢？','网谋汽贸提供12.5米至18米电动双飞翼车厢的租赁与买卖服务。具体长度、宽高、配置和可供情况，可带着使用需求与业务人员进一步核对。'),
 ('产品与规格','除了长度，还需要关注哪些配置？','建议同时核对宽高、车辆安装尺寸、翼板开合结构、厢体实际状态，以及货物装载与场地条件。如需更换现有车厢，可提前准备车辆和原厢体的资料。'),
 ('产品与规格','车厢询价需要提供哪些信息？','请说明所需长度、租赁或购买方式、使用城市、计划时间及车辆适配要求。业务人员可据此进一步对接车厢配置、报价与交付安排。'),
 ('租赁与购买','阶段性运输任务可以租赁车厢吗？','可以咨询电动双飞翼车厢租赁。建议说明所需长度、使用城市、预计起止日期和装卸方式，便于对应具体车厢，并进一步沟通租期、交接与维护安排。'),
 ('租赁与购买','购买车厢前，建议核对哪些信息？','可先核对尺寸、车辆适配条件、翼板与电动开合部件、厢体实际状态，再沟通数量、预算、验看方式及交付地点，明确具体交易范围。'),
 ('租赁与购买','租赁与购买应该如何比较？','可以把预计使用周期、任务稳定性、租赁费用或采购预算、维护责任与后续使用计划放在一起比较。阶段性任务与长期配置的关注点不同，具体方案应结合实际产品和需求确定。'),
 ('定制与置换','物流快递厢和挂板可以按尺寸定制吗？','可以向网谋汽贸咨询物流快递厢及各类尺寸挂板的定制需求。提供用途、目标尺寸、数量和安装条件，有助于进一步沟通适配方案。'),
 ('定制与置换','咨询挂板定制需要准备什么？','建议准备关键尺寸、使用用途、安装位置和数量。如有现有设备照片、尺寸草图或参考图纸，可在后续沟通中一并提供，便于核对结构与配套条件。'),
 ('定制与置换','旧车厢回收或置换，需要哪些资料？','可以先提供旧厢尺寸、所在地、使用情况和已知损坏，并准备整体、侧翼、底部等部位的清晰照片。网谋汽贸可据此进一步沟通评估和回收置换安排。'),
 ('咨询与交付','网谋汽贸的地址在哪里？',f'业务地址为{ADDRESS}。如计划到访或查看产品，建议提前电话联系，确认接待与验看安排。'),
 ('咨询与交付','上海、江苏、浙江及安徽的城市可以咨询吗？','可以。网谋汽贸立足上海奉贤，业务联系范围覆盖上海市、江苏省、浙江省及安徽省相关城市，包括南京、苏州、无锡、常州、镇江、杭州、嘉兴、湖州、绍兴、合肥、滁州和马鞍山。跨区域咨询时，建议说明所在城市、目标规格和期望交付地点，具体可供情况与交付安排以实际沟通确认为准。'),
 ('咨询与交付','车厢需求联系谁？','可联系王先生159-0083-3031，或吴先生175-2108-3572；业务邮箱为kf@wmqm.com。也可在联系我们页面填写具体需求。'),
 ('咨询与交付','可以预约到访或查看车厢吗？','可先联系王先生或吴先生，说明希望了解的车厢类型、规格与到访时间，便于提前安排业务沟通和产品验看。'),
]

SERVICES = [
 dict(slug='rental',title='电动双飞翼车厢租赁',short='车厢租赁',en='RENTAL',ic='rental',num='01',subject='电动双飞翼车厢租赁',intro='围绕阶段性运输与项目用厢需求，沟通使用周期、厢体规格和交接安排。',heading='按运输计划，安排车厢使用',description='阶段性业务、项目运输或运力调整，都可以从实际使用期限出发，了解电动双飞翼车厢租赁方案。网谋汽贸提供12.5米至18米电动双飞翼车厢租赁服务，结合用途、配置与租期对接用厢需求。',checks=['使用城市、预计起止日期与租期','所需长度、宽高与车辆匹配条件','货物类型、装卸方式及场地空间','费用构成、交接地点与维护安排'],paras=['租赁车厢，先把使用计划说明白。运输任务持续多久、装卸地点在哪里、是否配合现有车辆使用，都会影响后续方案。您可以先提供已掌握的规格和时间安排，再与网谋汽贸核对可供厢体。','在确认具体车厢后，进一步了解实际状态、开合结构与配置资料，并将交付、归还、维护及续租等事项放在同一份需求中沟通，有助于让租赁安排与日常业务衔接。'],detailheading='从期限到交接，逐项沟通',detail='需求沟通可按“长度与用途—城市与时间—车辆及场地—合作条件”的顺序展开。如使用期限暂未确定，也可先描述运输任务的阶段和预期安排，方便后续比较。'),
 dict(slug='sales',title='电动双飞翼车厢买卖',short='车厢买卖',en='SALES',ic='sales',num='02',subject='电动双飞翼车厢购买',intro='面向长期配置与车厢更新，结合实际车况、尺寸和使用条件沟通采购。',heading='为长期运输，匹配合适厢体',description='准备配置或更新电动双飞翼车厢时，尺寸、开合结构、实际状态和车辆适配都值得同步考虑。网谋汽贸围绕12.5米至18米车厢买卖需求，提供具体产品与合作事项的沟通。',checks=['长度、宽度、高度及安装条件','翼板结构与电动开合部件状态','采购数量、预算和计划使用时间','产品验看、交易范围与交付地点'],paras=['长期配置车厢，需要让厢体与运输任务匹配。除了长度，还应结合所运货物、装卸频率、侧向通道与现有车辆条件，明确目标尺寸和结构。网谋汽贸可根据这些信息，与您进一步核对具体产品。','购买沟通中，可围绕整体外观、主要结构、开合部件和已有使用状态准备验看要点。在核对产品资料后，再明确交易范围、交接方式与费用事项，让采购计划更具体。'],detailheading='把配置与使用计划一起确认',detail='如涉及现有车辆更换厢体，可提前准备原厢体尺寸、车辆资料与安装位置照片。具体适配要求和可供产品在沟通中逐项确认，便于推进后续验看与交接。'),
 dict(slug='customization',title='物流快递厢与挂板定制',short='厢体与挂板定制',en='CUSTOMIZATION',ic='custom',num='03',subject='物流快递厢定制',intro='结合用途、关键尺寸和安装环境，沟通物流快递厢与各类挂板需求。',heading='从实际尺寸出发，沟通配套方案',description='物流快递厢与挂板定制，需要兼顾装载用途、结构尺寸和安装条件。网谋汽贸可接洽物流快递厢及各类尺寸挂板需求，结合图纸、照片或尺寸资料进一步沟通。',checks=['目标尺寸、数量和实际用途','货物与装卸方式、作业环境','车辆或既有设备的安装位置','尺寸草图、参考图纸或现场照片'],paras=['定制需求不一定要从完整图纸开始。先说明用于哪类运输、配合什么设备、希望解决哪些装载或安装问题，再提供关键尺寸，就可以开启有针对性的沟通。','对于物流快递厢，重点是用途、尺寸与实际装卸条件；对于挂板，建议进一步描述安装位置、现有结构和尺寸边界。网谋汽贸可围绕这些资料核对需求，逐步明确配套方案。'],detailheading='参考资料越清楚，沟通越直接',detail='可准备正面、侧面、连接位置等不同角度的照片，并标注关键尺寸。材料、结构、具体实现方式和交付安排在方案核对后确认。'),
 dict(slug='recycling',title='旧飞翼车厢回收与置换',short='旧厢回收置换',en='RECYCLE & REPLACE',ic='recycling',num='04',subject='旧飞翼车厢回收与置换',intro='围绕闲置处置和厢体更新，结合实物照片与使用情况沟通回收、置换。',heading='让旧厢处置，与更新计划衔接',description='车厢闲置、业务调整或准备更新设备时，可向网谋汽贸咨询旧飞翼车厢回收与置换。先提供尺寸、所在地与实物状态，便于开展后续评估和安排沟通。',checks=['旧厢尺寸、结构和使用情况','整体、翼板与底部的清晰照片','已知损坏、所在地和处理时间','回收意向或计划置换的目标规格'],paras=['旧厢回收与置换，首先需要了解实物。整体是否完整、翼板与开合部件的状态、底部结构和已知损坏，都可以通过清晰照片与文字说明先行沟通。','如同时计划更换车厢，可一并提供目标长度、使用城市和期望时间。网谋汽贸可将旧厢处理与新需求放在一起了解，进一步讨论适用的评估与合作方式。'],detailheading='先了解状态，再沟通具体安排',detail='建议准备整厢全景、左右侧面、翼板、底部与需要重点说明部位的照片。回收评估与置换安排结合实物状态、处理时间和更新需求展开。'),
]

def contact_link(subject='',label='咨询具体需求',classes='button'):
    q='?subject='+quote(subject) if subject else ''
    return f'<a class="{classes}" href="contact.html{q}#inquiry">{label}{ARROW}</a>'

def brand_lockup(kind='header'):
    if kind == 'footer':
        return f'<span class="brand-lockup brand-lockup--footer" aria-hidden="true"><img class="brand-footer-image" src="{ASSET_BASE}logo-footer.png" alt="" width="1074" height="925" loading="lazy"></span>'
    return f'<span class="brand-lockup brand-lockup--header" aria-hidden="true"><img class="brand-symbol" src="{ASSET_BASE}logo-symbol.png" alt="" width="1074" height="489"><img class="brand-wordmark" src="{ASSET_BASE}logo-wordmark.png" alt="" width="1031" height="277"></span>'

def header(page):
    active='https://www.wmqm.com' if page=='index.html' else ('services.html' if page in [s['slug']+'.html' for s in SERVICES] else page)
    links=''.join(f'<a href="{url}"'+(' class="active" aria-current="page"' if url==active else '')+f'>{label}</a>' for url,label in NAV)
    return f'''<a class="skip" href="#main">跳转到主要内容</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="https://www.wmqm.com" aria-label="网谋汽贸首页">{brand_lockup()}</a><nav class="nav" id="site-nav" aria-label="主导航">{links}</nav><a class="header-phone" href="tel:+8615900833031">{icon('phone')}<span><small>王先生</small><strong>159-0083-3031</strong></span></a><button class="menu-button" type="button" aria-label="打开导航" aria-expanded="false" aria-controls="site-nav">{icon('menu')}</button></div></header>'''

def qr_frame():
    return f'<div class="qr-frame"><img src="{ASSET_BASE}wechat.jpg" alt="网谋汽贸微信公众号二维码" width="258" height="258" loading="lazy"></div>'

def contact_band():
    return f'''<section class="contact-band" aria-label="业务联系与微信公众号"><div class="wrap contact-band-inner"><div><span class="eyebrow">CONTACT WMQM</span><h2>车厢租售与定制，欢迎联系。</h2><p>租赁、买卖、定制或旧厢置换，从您的实际用途开始。</p><div class="contact-band-phones"><a class="phone-block" href="tel:+8615900833031"><small>王先生</small><strong>159-0083-3031</strong></a><a class="phone-block" href="tel:+8617521083572"><small>吴先生</small><strong>175-2108-3572</strong></a></div></div><div class="contact-qr">{qr_frame()}<div><h3>微信扫码，关注我们</h3><p>了解网谋汽贸业务与厢体信息，方便后续联系。</p><button class="qr-button" type="button" data-open-qr>查看大图 <span aria-hidden="true">↗</span></button></div></div></div></section>'''

def footer():
    links=''.join(f'<a href="{u}">{n}</a>' for u,n in NAV)
    return f'''<footer class="site-footer" id="site-footer"><div class="wrap"><div class="footer-main"><div><a class="footer-brand" href="https://www.wmqm.com" aria-label="网谋汽贸首页">{brand_lockup('footer')}</a><p class="footer-about">电动双飞翼车厢租赁与买卖、物流快递厢与挂板定制、旧厢回收与置换。业务联系覆盖上海、江苏、浙江及安徽等长三角城市。</p></div><div><h3 class="footer-title">网站导航</h3><nav class="footer-nav" aria-label="页脚导航">{links}</nav></div><div><h3 class="footer-title">联系网谋汽贸</h3><ul class="footer-contacts"><li><span>电话</span><span><a href="tel:+8615900833031">王先生 159-0083-3031</a><br><a href="tel:+8617521083572">吴先生 175-2108-3572</a></span></li><li><span>邮箱</span><a href="mailto:kf@wmqm.com">kf@wmqm.com</a></li><li><span>地址</span><span>{ADDRESS}</span></li></ul></div></div><div class="footer-bottom"><span>© <span data-year>2026</span> 网谋汽贸 版权所有</span></div></div></footer><div class="mobile-callbar" aria-label="快捷电话咨询"><a href="tel:+8615900833031">{icon('phone')}<span><small>王先生 · 点击拨打</small><strong>159-0083-3031</strong></span></a><a href="tel:+8617521083572">{icon('phone')}<span><small>吴先生 · 点击拨打</small><strong>175-2108-3572</strong></span></a></div><dialog class="qr-dialog" aria-labelledby="qr-title"><button type="button" class="dialog-close" aria-label="关闭二维码">×</button><h2 id="qr-title">网谋汽贸微信公众号</h2><img src="{ASSET_BASE}wechat.jpg" alt="微信扫描此二维码关注网谋汽贸" width="258" height="258"><p>微信扫一扫，关注我们<br>手机端可保存图片后，在微信中识别二维码。</p><a class="qr-download" href="{ASSET_BASE}wechat.jpg" download="网谋汽贸微信公众号.jpg">保存二维码</a></dialog>'''

def faq_details(items, first_open=False):
    return ''.join(f'<details class="faq-item" data-category="{escape(cat)}"'+(' open' if first_open and i==0 else '')+f'><summary>{escape(q)}</summary><p>{escape(a)}</p></details>' for i,(cat,q,a) in enumerate(items))

def schema(page,title,desc,faq=None,service=None):
    url=ORIGIN+('/' if page=='index.html' else '/'+page)
    business={'@type':'LocalBusiness','@id':ORIGIN+'/#business','name':'网谋汽贸','url':ORIGIN+'/','logo':ASSET_BASE+'logo-symbol.png','image':ASSET_BASE+'truck.png','description':'电动双飞翼车厢租赁与买卖、物流快递厢与挂板定制、旧厢回收与置换。','telephone':'+86-15900833031','email':'kf@wmqm.com','address':{'@type':'PostalAddress','streetAddress':'奉城镇川南奉公路9650号','addressLocality':'奉贤区','addressRegion':'上海市','addressCountry':'CN'},'areaServed':AREA_CITIES + AREA_PROVINCES, 'contactPoint':[{'@type':'ContactPoint','name':'王先生','telephone':'+86-15900833031','contactType':'客户服务'},{'@type':'ContactPoint','name':'吴先生','telephone':'+86-17521083572','contactType':'客户服务'}]}
    graph=[business,{'@type':'WebSite','@id':ORIGIN+'/#website','url':ORIGIN+'/','name':'网谋汽贸','inLanguage':'zh-CN','publisher':{'@id':ORIGIN+'/#business'}},{'@type':'WebPage','@id':url+'#webpage','url':url,'name':title,'description':desc,'inLanguage':'zh-CN','isPartOf':{'@id':ORIGIN+'/#website'},'about':{'@id':ORIGIN+'/#business'}}]
    if faq:graph.append({'@type':'FAQPage','@id':url+'#faq','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for _,q,a in faq]})
    if service:graph.append({'@type':'Service','name':service['title'],'description':service['description'],'provider':{'@id':ORIGIN+'/#business'},'areaServed':AREA_CITIES + AREA_PROVINCES, 'url':url})
    if page!='index.html':graph.append({'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'首页','item':ORIGIN+'/'},{'@type':'ListItem','position':2,'name':title.split('_')[0],'item':url}]})
    return json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('</','<\\/')

config_text = (ROOT / 'assets' / 'config.js').read_text(encoding='utf-8')
if INQUIRY_ENDPOINT not in config_text:
    raise SystemExit('询盘接口配置不一致：请同步检查 assets/config.js 与 scripts/build.py。')
region_markup = ''.join(f'<div class="region-group"><b>{group}</b><span>{cities}</span></div>' for group,cities in AREA_GROUPS)

def save(page,title,desc,body,faq=None,service=None,band=True,keywords=None):
    url=ORIGIN+('/' if page=='index.html' else '/'+page)
    preload=f'<link rel="preload" as="image" href="{ASSET_BASE}truck.png" fetchpriority="high"><link rel="preload" as="image" href="{ASSET_BASE}hero-road.webp">' if page=='index.html' else ''
    keywords_meta=f'<meta name="keywords" content="{escape(keywords)}">' if keywords else ''
    html=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{escape(title)}</title><meta name="description" content="{escape(desc)}">{keywords_meta}<meta name="theme-color" content="#061c44"><meta name="format-detection" content="telephone=no"><link rel="canonical" href="{url}"><link rel="icon" href="{ASSET_BASE}favicon.png" type="image/png" sizes="256x256"><meta property="og:type" content="website"><meta property="og:locale" content="zh_CN"><meta property="og:site_name" content="网谋汽贸"><meta property="og:title" content="{escape(title)}"><meta property="og:description" content="{escape(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{ASSET_BASE}og-logo.png"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{escape(title)}"><meta name="twitter:description" content="{escape(desc)}"><meta name="twitter:image" content="{ASSET_BASE}og-logo.png">{preload}<link rel="stylesheet" href="{ASSET_BASE}site.css"><link rel="stylesheet" href="{ASSET_BASE}brand.css?v=1.8"><script src="{ASSET_BASE}config.js" defer></script><script src="{ASSET_BASE}site.js" defer></script><script src="{ASSET_BASE}inquiry.js" defer></script><script type="application/ld+json">{schema(page,title,desc,faq,service)}</script></head><body>{header(page)}<main id="main">{body}</main>{contact_band() if band else ''}{footer()}</body></html>'''
    (OUT/page).write_text(html,encoding='utf-8')

def page_hero(label,en,title,desc,action=''):
    return f'<section class="page-hero"><div class="wrap"><nav class="breadcrumb" aria-label="面包屑"><a href="https://www.wmqm.com">首页</a><span aria-hidden="true">/</span><span>{label}</span></nav><span class="eyebrow">{en}</span><h1>{title}</h1><p>{desc}</p>{action}</div></section>'

def service_cards():
    return '<div class="business-grid">'+''.join(f'<a class="business-card" href="{s["slug"]}.html"><div class="card-top"><span class="card-number">{s["num"]} /</span>{icon(s["ic"])}</div><h3>{s["short"]}</h3><p>{s["intro"]}</p><div class="card-bottom"><span>了解服务</span>{ARROW}</div></a>' for s in SERVICES)+'</div>'

def process():
    data=[('01','说明需求','告知业务类型、使用城市、目标规格与时间安排。'),('02','核对产品','结合实际资料，确认尺寸、结构、配置和使用状态。'),('03','沟通方案','明确租期、价格、定制或回收置换的具体事项。'),('04','确认交接','双方核对合作内容，安排验看、交付与后续事项。')]
    return '<ol class="process">'+''.join(f'<li><b>{n}</b><h3>{h}</h3><p>{p}</p></li>' for n,h,p in data)+'</ol>'

home=f'''<section class="hero" aria-labelledby="hero-title"><div class="wrap hero-intro"><div class="hero-copy"><span class="eyebrow">网谋汽贸 · 厢体租售与配套服务</span><h1 id="hero-title">电动双飞翼车厢<span class="gradient-text">租售与定制服务</span></h1><p>提供12.5米至18米电动双飞翼车厢租赁与买卖，<br class="desktop-break">物流快递厢及各类尺寸挂板定制，旧厢回收与置换。</p><div class="actions">{contact_link(label='咨询厢体需求',classes='button white')}<a class="button outline-light" href="services.html">了解业务服务 <span aria-hidden="true">→</span></a></div></div><div class="hero-spec"><div class="number">12.5–18<span>m</span></div><p>电动双飞翼车厢 · 规格范围</p><div class="spec-rule"></div><small>租赁 / 买卖 / 定制 / 置换<br>上海 · 长三角</small></div></div><div class="hero-stage"><img class="hero-truck" src="{ASSET_BASE}truck.png" alt="网谋汽贸蓝色车厢运输车辆品牌形象" width="2048" height="682" fetchpriority="high"></div><div class="wrap hero-bottom"><div class="location">{icon('pin')}<span>上海市奉贤区 · 奉城镇川南奉公路9650号</span></div><a class="scroll-link" href="#business">探索网谋汽贸 <span aria-hidden="true">↓</span></a></div></section>
<section class="section" id="business"><div class="wrap"><div class="section-head"><div><span class="eyebrow">OUR SERVICES</span><h2>车厢租售与配套，<br>满足不同用厢需求。</h2></div><p>从阶段性用厢到长期采购，从配套定制到旧厢更新，按照实际用途与合作方式，找到适合您的业务服务。</p></div>{service_cards()}</div></section>
<section class="section pale"><div class="wrap feature-layout"><div class="feature-visual"><span class="range-label">ELECTRIC WING BODY · 电动双飞翼车厢</span><div class="range-number">12.5–18<span> 米</span></div><div class="range-track"></div><div class="range-markers"><span>12.5 m</span><span>电动双飞翼车厢</span><span>18 m</span></div><div class="range-caption">{icon('range')}<span>从长度到配置，匹配实际运输条件。</span></div></div><div class="feature-copy"><span class="eyebrow">FIND YOUR FIT</span><h2>让车厢规格，<br>与运输任务相匹配。</h2><p>长度是起点，货物、车辆与装卸空间同样重要。结合现有条件，沟通车厢尺寸、开合结构与合作方式。</p><table class="spec-table"><caption class="visually-hidden" hidden>电动双飞翼车厢业务范围</caption><tbody><tr><th scope="row">业务产品</th><td>电动双飞翼车厢</td></tr><tr><th scope="row">长度范围</th><td>12.5米—18米</td></tr><tr><th scope="row">合作方式</th><td>租赁 · 买卖 · 回收置换</td></tr><tr><th scope="row">配套业务</th><td>物流快递厢 · 各类尺寸挂板定制</td></tr></tbody></table><a class="text-link" href="selection.html">查看完整选型参考{ARROW}</a></div></div></section>
<section class="section"><div class="wrap"><div class="journey"><div class="journey-heading"><span class="eyebrow">START WITH YOUR NEEDS</span><h2>从您的使用计划，<br>找到合作方向。</h2><p>阶段性运输、长期配置与旧厢更新，对应不同的合作方式。结合使用计划，了解适合的业务方向。</p></div><div class="choice-widget"><div class="choice-tabs" role="tablist" aria-label="使用需求"><button type="button" role="tab" id="intent-tab-rent" aria-controls="intent-rent" aria-selected="true" data-choice="rent">阶段性运输</button><button type="button" role="tab" id="intent-tab-buy" aria-controls="intent-buy" aria-selected="false" tabindex="-1" data-choice="buy">长期配置</button><button type="button" role="tab" id="intent-tab-replace" aria-controls="intent-replace" aria-selected="false" tabindex="-1" data-choice="replace">旧厢更新</button></div><div class="choice-panel" id="intent-rent" role="tabpanel" aria-labelledby="intent-tab-rent"><h3>先明确租期，再沟通用厢安排。</h3><p>有明确的运输项目或阶段性需求时，可围绕使用时间、目标尺寸与交接城市，了解车厢租赁方案。</p><ul class="micro-list"><li>使用起止时间</li><li>尺寸与车辆条件</li><li>交接及维护安排</li></ul><a class="text-link" href="rental.html">了解车厢租赁{ARROW}</a></div><div class="choice-panel" id="intent-buy" role="tabpanel" aria-labelledby="intent-tab-buy" hidden><h3>结合实际车况，规划长期配置。</h3><p>计划长期使用或采购车厢时，可先确认车辆适配与配置要求，再进一步核对厢体状态、预算与交付条件。</p><ul class="micro-list"><li>尺寸与开合结构</li><li>产品验看与预算</li><li>使用及交付计划</li></ul><a class="text-link" href="sales.html">了解车厢买卖{ARROW}</a></div><div class="choice-panel" id="intent-replace" role="tabpanel" aria-labelledby="intent-tab-replace" hidden><h3>带上旧厢资料，衔接更新需求。</h3><p>有闲置车厢或置换计划时，可提供整厢、侧翼与底部照片，并说明尺寸、所在地及目标规格。</p><ul class="micro-list"><li>旧厢照片与尺寸</li><li>使用状态与所在地</li><li>回收或置换意向</li></ul><a class="text-link" href="recycling.html">了解回收置换{ARROW}</a></div></div></div><div class="home-about"><div><span class="eyebrow">ABOUT WMQM</span><h3>立足上海奉贤，<br>接洽长三角厢体需求。</h3><div class="region-label">{icon('pin')}<span><b>业务咨询区域</b>：上海；江苏（南京、苏州、无锡、常州、镇江）；浙江（杭州、嘉兴、湖州、绍兴）；安徽（合肥、滁州、马鞍山）</span></div></div><div><p>网谋汽贸围绕电动双飞翼车厢及厢体配套业务，面向物流企业、运输车队与采购人员，提供租赁、买卖、定制和回收置换需求对接。业务咨询范围覆盖上海市、江苏省、浙江省及安徽省相关城市，具体可供情况和交付安排以实际沟通确认为准。</p><a class="text-link" href="about.html">进一步了解网谋汽贸{ARROW}</a></div></div></div></section>
<section class="section pale"><div class="wrap home-faq"><div class="faq-intro"><span class="eyebrow">QUESTIONS & ANSWERS</span><h2>咨询前，<br>您可能想了解。</h2><p>关于长度规格、租买方式与业务沟通，先看这些常见问题。</p><a class="text-link" href="faq.html">查看全部问题{ARROW}</a></div><div>{faq_details([FAQ[1],FAQ[6],FAQ[9]],True)}</div></div></section>'''
save('index.html','上海双飞翼车厢租赁出售_物流快递厢与挂板定制_网谋汽贸','网谋汽贸位于上海市奉贤区奉城镇川南奉公路9650号，提供12.5米至18米电动双飞翼车厢租赁与买卖，以及物流快递厢、各类尺寸挂板定制、旧厢回收与置换服务。联系王先生：159-0083-3031，邮箱：kf@wmqm.com。',home,faq=[FAQ[1],FAQ[6],FAQ[9]],keywords='网谋汽贸,上海电动双飞翼车厢,上海飞翼车厢租赁,上海奉贤飞翼车厢,奉城飞翼车厢,电动双飞翼车厢买卖,物流快递厢,挂板定制,飞翼车厢回收,飞翼车厢置换')

about=page_hero('关于我们','ABOUT WMQM','专注电动双飞翼车厢<br>租售与配套服务。','网谋汽贸立足上海奉贤，面向物流企业、运输车队及采购人员，提供电动双飞翼车厢租售与相关配套业务。')
about+=f'''<section class="section"><div class="wrap intro-grid"><div><span class="eyebrow">BUSINESS PROFILE</span><h2>从实际用途出发，<br>让需求与厢体对应。</h2><div class="fact-panel"><h3>网谋汽贸</h3><dl><div><dt>业务地点</dt><dd>上海 · 奉贤</dd></div><div><dt>主营方向</dt><dd>电动双飞翼车厢与厢体配套</dd></div><div><dt>合作方式</dt><dd>租赁、买卖、定制、回收置换</dd></div></dl></div></div><div class="body-copy"><p>网谋汽贸主要提供12.5米至18米电动双飞翼车厢的租赁与买卖服务，同时可接洽物流快递厢、各类尺寸挂板的定制，以及旧厢回收与置换需求。</p><p>物流运输中的用厢需求各有不同。阶段性任务需要考虑租期与交接，长期配置需要关注车况与适配，定制配套则要明确尺寸和安装条件。网谋汽贸按照具体业务展开沟通，将使用场景、产品资料与合作方式联系起来。</p><p>无论您已明确所需规格，还是正准备比较不同合作方向，都可以先说明用途、所在城市与预计时间，再逐步核对尺寸、配置和安排。</p><div class="actions" style="margin-top:29px"><a class="button" href="services.html">了解业务服务{ARROW}</a><a class="button secondary" href="contact.html">联系网谋汽贸</a></div></div></div></section>
<section class="section pale"><div class="wrap"><div class="section-head"><div><span class="eyebrow">WHO WE SERVE</span><h2>对应不同的运输与采购需求。</h2></div></div><div class="audience-grid"><article class="audience-item"><span class="index">01 / 运输运营</span><h3>物流企业与运输车队</h3><p>围绕运输任务、装卸方式、车辆条件与使用周期，沟通车厢租赁或配置需求。</p><a class="text-link" href="rental.html">了解租赁业务{ARROW}</a></article><article class="audience-item"><span class="index">02 / 厢体采购</span><h3>采购与装备配置</h3><p>结合尺寸、结构、实际车况与交付地点，对接具体车厢与配套要求。</p><a class="text-link" href="sales.html">了解车厢买卖{ARROW}</a></article><article class="audience-item"><span class="index">03 / 更新处置</span><h3>旧厢更新与置换</h3><p>先了解实物状态，再沟通回收评估或置换方向，让旧厢处置与更新计划衔接。</p><a class="text-link" href="recycling.html">了解回收置换{ARROW}</a></article></div></div></section>
<section class="section"><div class="wrap about-region"><div><span class="eyebrow">SHANGHAI & THE YANGTZE RIVER DELTA</span><h2>以上海为起点，<br>拓展周边业务联系。</h2><div class="body-copy" style="margin-top:20px"><p>网谋汽贸的业务联系地点位于上海市奉贤区，咨询与需求对接范围覆盖上海市、江苏省、浙江省及安徽省相关城市，包括南京、苏州、无锡、常州、镇江、杭州、嘉兴、湖州、绍兴、合肥、滁州和马鞍山。跨区域需求可先说明产品规格、使用城市与期望交付地点，具体可供情况及交付安排以实际沟通确认为准。</p></div><a class="text-link" href="contact.html" style="margin-top:25px">查看地址与联系方式{ARROW}</a></div><div class="region-board"><div class="region-board-head"><span>BUSINESS CONTACT AREA</span><strong>长三角城市</strong></div><div class="region-groups">{region_markup}</div><p class="region-board-note">业务联系地点：上海市奉贤区。跨区域可供情况、具体规格与交付安排，以实际沟通确认为准。</p></div></div></section>'''
save('about.html','关于网谋汽贸_上海车厢租售与厢体配套服务','了解网谋汽贸的业务方向与合作方式：电动双飞翼车厢租售、物流快递厢和挂板定制、旧厢回收置换，立足上海奉贤。',about)

services=page_hero('业务服务','BUSINESS SERVICES','从租售到配套，<br>按需求选择服务。','电动双飞翼车厢租赁与买卖、物流快递厢和挂板定制、旧厢回收置换。每一种合作方式，都从实际用途和产品资料开始。')
services+='<section class="section"><div class="wrap service-list">'
for s in SERVICES:
    services+=f'''<article class="service-row" id="{s['slug']}"><div class="service-num">{s['num']}</div><div><span class="eyebrow">{s['en']}</span><h2>{s['title']}</h2><p>{s['description']}</p><a class="text-link" href="{s['slug']}.html">查看服务详情{ARROW}</a></div><div class="service-check"><h3>服务对接要点</h3><ul class="check-list">{''.join('<li>'+c+'</li>' for c in s['checks'])}</ul></div></article>'''
services+='</div></section>'
services+=f'''<section class="section pale"><div class="wrap"><div class="section-head"><div><span class="eyebrow">HOW WE WORK</span><h2>从需求对接，<br>到合作与交付。</h2></div><p>从咨询到交接，逐步确认产品与合作事项。已掌握的尺寸、照片或使用条件，都可以成为沟通的起点。</p></div>{process()}</div></section>'''
save('services.html','业务服务_车厢租赁买卖定制与回收置换_网谋汽贸','网谋汽贸四项业务服务：电动双飞翼车厢租赁、买卖、物流快递厢与挂板定制、旧厢回收置换，了解各项服务的沟通重点。',services)

for s in SERVICES:
    body=page_hero(s['short'],s['en'],s['title'],s['description'],f'<div class="actions">{contact_link(s["subject"],"咨询这项业务", "button white")}<a class="button outline-light" href="services.html">全部业务服务</a></div>')
    body+=f'''<section class="section"><div class="wrap detail-layout"><article class="detail-main"><span class="eyebrow">{s['num']} / SERVICE DETAILS</span><h2>{s['heading']}</h2>{''.join('<p>'+p+'</p>' for p in s['paras'])}<h3>{s['detailheading']}</h3><p>{s['detail']}</p><h3>需求资料</h3><ul class="check-list">{''.join('<li>'+c+'</li>' for c in s['checks'])}</ul><div class="related-links"><a href="selection.html">查看选型参考 ↗</a><a href="faq.html">了解常见问题 ↗</a><a href="services.html">全部业务服务 ↗</a></div></article><aside class="detail-aside"><span class="eyebrow">TALK TO US</span><h3>带着具体需求来聊。</h3><p>提供业务类型、使用城市和已知规格，方便进一步核对产品与合作方案。</p>{contact_link(s['subject'],'提交业务需求')}<a class="small-phone" href="tel:+8615900833031">王先生 159-0083-3031</a><a class="small-phone" href="tel:+8617521083572">吴先生 175-2108-3572</a></aside></div></section>'''
    body+=f'<section class="section pale"><div class="wrap"><div class="section-head"><div><span class="eyebrow">NEXT STEPS</span><h2>从需求对接，到合作确认。</h2></div></div>{process()}</div></section>'
    save(s['slug']+'.html',s['title']+'_上海及长三角厢体服务_网谋汽贸',s['description'],body,service=s)

selection=page_hero('选型参考','SELECTION GUIDE','选车厢，<br>先看实际使用条件。','从货物、装卸场地、车辆条件与使用周期出发，梳理租赁、购买或定制前需要沟通的关键事项。')
guide=[('货物与装卸方式','说明货物尺寸、装载方式、装卸频率，以及是否使用托盘、叉车等设备，判断侧向装卸是否适合当前作业。'),('尺寸与车辆匹配','除了目标长度，还需核对宽高、车辆安装条件及现有结构。更换旧厢时，可提供车辆和原厢体资料。'),('翼板开启与现场空间','考虑上方净空、侧面通道、门洞和叉车行走路线，核对翼板开启后是否具备实际作业空间。'),('周期与合作安排','说明预计使用时间、所在城市与交接地点，再分别沟通租期、采购、定制或置换的具体条件。')]
selection+='<section class="section"><div class="wrap"><span class="eyebrow">FOUR THINGS TO CONSIDER</span><h2>长度之外，这些同样重要。</h2><div class="guide-grid">'+''.join(f'<article class="guide-item"><span>0{i+1}</span><div><h3>{h}</h3><p>{p}</p></div></article>' for i,(h,p) in enumerate(guide))+'</div></div></section>'
selection+=f'''<section class="section pale"><div class="wrap"><div class="section-head"><div><span class="eyebrow">RENT OR BUY</span><h2>租赁与购买，<br>从使用计划来比较。</h2></div><p>将使用周期、预算、产品状态与交接安排放在一起考虑，选择更贴近当前业务的合作方向。</p></div><div class="compare-grid"><article class="compare-card"><span class="eyebrow">01 / RENTAL</span><h3>阶段性使用，了解租赁。</h3><p>适合围绕项目周期或特定时间安排，进一步沟通车厢使用需求。</p><ul class="check-list"><li>明确起止时间与续租事项</li><li>核对尺寸、实际状态与车辆条件</li><li>沟通费用、交接与维护安排</li></ul>{contact_link('电动双飞翼车厢租赁','咨询租赁方案','text-link')}</article><article class="compare-card warm"><span class="eyebrow">02 / PURCHASE</span><h3>长期配置，了解买卖。</h3><p>适合计划长期使用或更新厢体，结合产品状态与配置比较采购条件。</p><ul class="check-list"><li>明确目标尺寸与配置需求</li><li>核对预算、车况及验看方式</li><li>确认交易范围与交付安排</li></ul>{contact_link('电动双飞翼车厢购买','咨询购买方案','text-link')}</article></div></div></section>
<section class="section inquiry-section"><div class="wrap inquiry-info-layout" id="inquiry-information"><div class="inquiry-info-intro"><span class="eyebrow">INQUIRY INFORMATION</span><h2>需求沟通，<br>从这些信息开始。</h2><p>结合业务方向、尺寸和使用计划提供需求信息，便于安排产品与配套服务。</p></div><div class="inquiry-info-content"><dl class="inquiry-info-list">'''
checks=[('业务方向','租赁、购买、定制，或旧厢回收置换'),('所需规格','长度、宽高、结构或现有厢体尺寸'),('使用场景','货物、装卸方式、车辆与场地条件'),('时间与地点','预计使用时间、所在城市与交付地点'),('参考资料','现场照片、尺寸图或产品配置资料')]
selection+=''.join(f'<div><dt>{h}</dt><dd>{p}</dd></div>' for h,p in checks)
selection+=f'''</dl>{contact_link(label='联系业务人员')}</div></div></section>'''
save('selection.html','双飞翼车厢选型参考_租赁购买与尺寸匹配_网谋汽贸','双飞翼车厢如何选型？围绕货物、装卸空间、尺寸、车辆匹配与使用周期，了解租赁、购买和定制前需要沟通的事项。',selection)

faq=page_hero('常见问题','QUESTIONS & ANSWERS','把常见问题，<br>提前了解清楚。','按产品规格、租赁购买、定制置换与咨询交付查找问题。具体的车况、报价和交付需求，可直接联系业务人员。')
filters=['全部问题','产品与规格','租赁与购买','定制与置换','咨询与交付']
faq+=f'''<section class="section"><div class="wrap faq-layout"><aside class="faq-sidebar"><div class="search-field"><label for="faq-search" hidden>搜索常见问题</label><input id="faq-search" type="search" placeholder="搜索规格、租期、定制…" autocomplete="off">{icon('search')}</div><div class="faq-filters" aria-label="问题分类">{''.join(f'<button type="button" data-filter="{f}" aria-pressed="{str(i==0).lower()}">{f}</button>' for i,f in enumerate(filters))}</div><div class="faq-support"><p>没有找到想了解的问题？</p><a href="contact.html">联系网谋汽贸 ↗</a></div></aside><div class="faq-results">{faq_details(FAQ,True)}<div class="empty-state" hidden>暂未找到相关问题。可尝试其他关键词，或 <a href="contact.html">直接联系业务人员 ↗</a></div></div></div></section>'''
save('faq.html','常见问题_飞翼车厢租售定制与回收置换_网谋汽贸','查找网谋汽贸业务常见问题：车厢长度规格、租赁买卖、物流快递厢与挂板定制、旧厢回收置换，以及咨询和交付安排。',faq,faq=FAQ)

def form():
    subjects=['电动双飞翼车厢租赁','电动双飞翼车厢购买','物流快递厢定制','挂板尺寸定制','旧飞翼车厢回收与置换','其他业务需求']
    return f'''<form class="inquiry-card" id="inquiry" action="{INQUIRY_ENDPOINT}" method="post" enctype="multipart/form-data" aria-label="网谋汽贸业务需求"><span class="eyebrow">BUSINESS INQUIRY</span><h2>提交业务需求</h2><p>请填写联系方式及车厢需求，我们将与您进一步沟通。</p><div class="fields"><div class="field full"><label for="subject">咨询业务 <span class="required">*</span></label><select id="subject" name="subject" required><option value="">请选择业务类型</option>{''.join(f'<option>{s}</option>' for s in subjects)}</select></div><div class="field"><label for="name">联系人 <span class="required">*</span></label><input id="name" name="name" type="text" required maxlength="50" autocomplete="name" placeholder="您的姓名或称呼"></div><div class="field"><label for="phone">联系电话 <span class="required">*</span></label><input id="phone" name="phone" type="tel" inputmode="tel" required maxlength="32" autocomplete="tel" placeholder="手机或固定电话"></div><div class="field"><label for="company">公司名称 <small>选填</small></label><input id="company" name="company" type="text" maxlength="100" autocomplete="organization" placeholder="公司 / 车队 / 单位"></div><div class="field"><label for="email">电子邮箱 <small>选填</small></label><input id="email" name="email" type="email" maxlength="120" autocomplete="email" placeholder="接收业务资料的邮箱"></div><div class="field full"><label for="message">需求说明 <span class="required">*</span></label><textarea id="message" name="message" required minlength="10" maxlength="1500" rows="5" placeholder="请说明所需长度、租买方式、使用城市、预计时间，以及其他具体要求。"></textarea><div class="field-hint"><span>可填写尺寸、使用城市与计划时间。</span><span><span data-char-count>0</span> / 1500</span></div></div></div><div class="trap" aria-hidden="true"><label>请留空<input name="contact_guard_field" tabindex="-1" autocomplete="off"></label></div><div class="submit-actions"><button class="button" type="submit" disabled><span data-submit-label>提交业务需求</span>{ARROW}</button></div><p class="form-privacy" data-form-note>所填信息仅用于业务联系。</p><div class="form-status" role="status" aria-live="polite" hidden></div><noscript><p class="form-status">请开启 JavaScript 后使用表单，或直接拨打 159-0083-3031 联系王先生。</p></noscript></form>'''

contact=page_hero('联系我们','CONTACT WMQM','车厢租售与定制，<br>欢迎联系网谋汽贸。','电动双飞翼车厢租赁与买卖、物流快递厢与挂板定制、旧厢回收与置换，欢迎通过电话、邮件或在线表单联系。')
contact+=f'''<section class="section"><div class="wrap contact-layout"><div class="contact-info"><span class="eyebrow">GET IN TOUCH</span><h2>联系网谋汽贸</h2><p>关于租赁、买卖、定制与旧厢置换，欢迎沟通。</p><a class="contact-person" href="tel:+8615900833031">{icon('phone')}<span><small>王先生</small><strong>159-0083-3031</strong></span>{ARROW}</a><a class="contact-person" href="tel:+8617521083572">{icon('phone')}<span><small>吴先生</small><strong>175-2108-3572</strong></span>{ARROW}</a><a class="contact-person email" href="mailto:kf@wmqm.com">{icon('mail')}<span><small>业务邮箱</small><strong>kf@wmqm.com</strong></span>{ARROW}</a><div class="contact-address"><h3>联系地址</h3><p>上海市奉贤区<br>奉城镇川南奉公路9650号</p><small>到访或查看产品前，请先电话确认接待安排。</small></div><div class="contact-page-qr">{qr_frame()}<div><h3>微信扫码，关注我们</h3><p>了解业务与厢体信息<br>方便后续联系。</p><button type="button" class="qr-button" data-open-qr>查看二维码大图 ↗</button></div></div></div>{form()}</div></section>'''
save('contact.html','联系我们_电话地址与在线咨询_网谋汽贸',f'联系网谋汽贸：王先生159-0083-3031，吴先生175-2108-3572，邮箱kf@wmqm.com，地址{ADDRESS}。',contact,band=False)

thanks=f'<section class="section"><div class="wrap success-box"><div class="status-icon">{icon("check")}</div><h1 data-thanks-title>感谢您的咨询</h1><p data-thanks-message>如需确认厢体规格、租期或交付安排，可直接联系业务人员进一步沟通。</p><div class="actions"><a class="button" href="tel:+8615900833031">联系王先生{icon("phone")}</a><a class="button secondary" href="https://www.wmqm.com">返回首页</a></div></div></section>'
save('thanks.html','业务需求_网谋汽贸','感谢关注网谋汽贸，欢迎就车厢租赁买卖、定制与回收置换进行业务沟通。',thanks,band=False)
notfound='<section class="section"><div class="wrap success-box"><span class="eyebrow">404 / PAGE NOT FOUND</span><h1>这个页面暂时找不到了</h1><p>您可以返回首页，继续了解车厢业务，或直接联系网谋汽贸。</p><div class="actions"><a class="button" href="https://www.wmqm.com">返回首页 ↗</a><a class="button secondary" href="contact.html">联系我们</a></div></div></section>'
save('404.html','页面未找到_网谋汽贸','返回网谋汽贸首页，了解电动双飞翼车厢租售与配套业务。',notfound,band=False)
pages=['index.html','about.html','services.html','selection.html','faq.html','contact.html']+[s['slug']+'.html' for s in SERVICES]
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>{ORIGIN}/'+('' if p=='index.html' else p)+'</loc></url>' for p in pages)+'</urlset>',encoding='utf-8')
(OUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\nDisallow: /thanks.html\nSitemap: {ORIGIN}/sitemap.xml\n',encoding='utf-8')
print(json.dumps({'pages':len(pages)+2,'output':str(OUT),'origin':ORIGIN},ensure_ascii=False))
