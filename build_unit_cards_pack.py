#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
بسم الله الرحمن الرحيم
مولّد حزمة «بطاقات تعريف الوحدات بلا دروس» — قالب الليل الملكي (الأمام فقط)

تشمل:
  • الرزمة الأساسية للفرنسي: French 9 (DOSSIER 01–06) و French 12 (UNIT 01–06)
  • الكلمات المهمة للرزم الخمس: English 9 / English Lit 12 / English Sci 12 / French 12 بوحدات،
    و French 9 بطاقة واحدة شاملة (لأنه غير مقسّم)

الهيكل:
    تعريف الوحدات
      ├ الرزمة الأساسية ▸ French 9 ▸ DOSSIER 01…  |  French 12 ▸ UNIT 01…
      └ الكلمات المهمة  ▸ English 9 ▸ UNIT 01…  |  English Lit 12  |  English Sci 12  |  French 12  |  French 9 (بطاقة واحدة)

الخلف تصمّمه أنت: القالب يعرض الأمام نفسه عند «إظهار الإجابة» لحين استبداله.

التشغيل في Termux:
    python build_unit_cards_pack.py
الناتج:
    UnitCards_Lessonless.apkg
"""
import os
import html
import math

import genanki

OUTPUT_FILE = "UnitCards_Lessonless.apkg"
PARENT = "تعريف الوحدات"
BASMALA = "بسم الله الرحمن الرحيم"

# الرزمة الأساسية للفرنسي: (رقم الوحدة، عدد البطاقات)
BASE = [
    {"key": "F9", "title": "French 9", "label": "DOSSIER", "total": 1045,
     "units": [("01", 305), ("02", 149), ("03", 164), ("04", 125), ("05", 175), ("06", 127)]},
    {"key": "F12", "title": "French 12", "label": "UNIT", "total": 2055,
     "units": [("01", 544), ("02", 359), ("03", 320), ("04", 244), ("05", 255), ("06", 333)]},
]
# الكلمات المهمة: بوحدات، أو بطاقة واحدة شاملة عند غياب التقسيم (units=None)
IMPORTANT = [
    {"key": "E9", "title": "English 9", "label": "UNIT", "total": 709,
     "units": [("01", 79), ("02", 42), ("03", 62), ("04", 58), ("05", 54), ("06", 109), ("07", 46), ("08", 62), ("09", 48), ("10", 36), ("11", 47), ("12", 66)]},
    {"key": "EL12", "title": "English Lit 12", "label": "UNIT", "total": 1216,
     "units": [("01", 119), ("02", 106), ("03", 108), ("04", 104), ("05", 105), ("06", 104), ("07", 96), ("08", 90), ("09", 83), ("10", 101), ("11", 105), ("12", 95)]},
    {"key": "ES12", "title": "English Sci 12", "label": "UNIT", "total": 1237,
     "units": [("01", 119), ("02", 106), ("03", 113), ("04", 110), ("05", 102), ("06", 101), ("07", 99), ("08", 95), ("09", 83), ("10", 103), ("11", 105), ("12", 101)]},
    {"key": "F12", "title": "French 12", "label": "UNIT", "total": 1036,
     "units": [("01", 124), ("02", 224), ("03", 205), ("04", 127), ("05", 189), ("06", 167)]},
    {"key": "F9", "title": "French 9", "label": "", "total": 430, "units": None},
]


def verify():
    ok = True
    for grp in (BASE, IMPORTANT):
        for p in grp:
            if p["units"] and sum(c for _, c in p["units"]) != p["total"]:
                ok = False
                print(f"  ✗ {p['title']}: المجموع {sum(c for _, c in p['units'])} ≠ {p['total']}")
    print("  ✓ كل الأرقام متطابقة" if ok else "  ⚠ راجع الفروق أعلاه")


CSS = r'''
:root{
--orn:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 56 14'%3E%3Cdefs%3E%3ClinearGradient id='g' x1='0' y1='0' x2='1' y2='1'%3E%3Cstop offset='0' stop-color='%23fff1bf'/%3E%3Cstop offset='.55' stop-color='%23e0b84f'/%3E%3Cstop offset='1' stop-color='%23a67c1f'/%3E%3C/linearGradient%3E%3C/defs%3E%3Cg fill='url(%23g)'%3E%3Cpolygon points='28,1 35,7 28,13 21,7'/%3E%3Cpolygon points='13,4 17,7 13,10 9,7'/%3E%3Cpolygon points='43,4 47,7 43,10 39,7'/%3E%3C/g%3E%3C/svg%3E");
--ar:"Noto Naskh Arabic","Droid Arabic Naskh","Noto Sans Arabic","Geeza Pro","Segoe UI",Tahoma,serif;
--lat:"Noto Serif","DejaVu Serif","Times New Roman","Liberation Serif",serif;
--s8:polygon(50% 0,62% 19%,85% 15%,81% 38%,100% 50%,81% 62%,85% 85%,62% 81%,50% 100%,38% 81%,15% 85%,19% 62%,0 50%,19% 38%,15% 15%,38% 19%);
--ch:polygon(12px 0,calc(100% - 12px) 0,100% 12px,100% calc(100% - 12px),calc(100% - 12px) 100%,12px 100%,0 calc(100% - 12px),0 12px);
--ch2:polygon(11px 0,calc(100% - 11px) 0,100% 11px,100% calc(100% - 11px),calc(100% - 11px) 100%,11px 100%,0 calc(100% - 11px),0 11px);
--grain:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='140' height='140'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 .5 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}
::selection{background:rgba(232,196,107,.35)}
@keyframes sweep{0%{background-position:0% 0,0 0}40%,100%{background-position:100% 0,0 0}}
@keyframes draw{from{stroke-dasharray:0 600}}
@keyframes nudge{0%,100%{transform:translateY(0);opacity:.7}50%{transform:translateY(4px);opacity:1}}
@keyframes breathe{0%,100%{box-shadow:0 8px 24px rgba(244,190,90,.38),0 0 0 0 rgba(244,190,90,0)}50%{box-shadow:0 8px 24px rgba(244,190,90,.38),0 0 0 9px rgba(244,190,90,.13)}}
@keyframes drift{from{transform:translate(0,0)}to{transform:translate(34px,-22px)}}
@media (prefers-reduced-motion:reduce){.K *{animation:none !important;transition:none !important}}
.K{--pg2:#04070f;--pg3:#03050b;--lead:#ece6d4;--mut:#a99c75;--lab:#e2dcc8;--gtxt:#f4d98a;--brk:#e8c46b;--body:#d8d1bd;
--foil:linear-gradient(180deg,#fff7d6 0%,#f4d27a 30%,#c9962f 55%,#f9e29b 75%,#a87a1f 100%);
--pl1:#142058;--pl2:#080e2c;--hi:rgba(255,255,255,.13);--shadow:rgba(0,0,0,.55);
--sap:#7aa2ff;--saptxt:#a9c0ff;--sapfoil:linear-gradient(180deg,#f2f6ff 0%,#b9ccff 40%,#6f95f0 75%,#a9c0ff 100%);--ivory:#f1eadb;
--wb1:#2c1a17;--wb2:#1c100f;--wink:#ffe9cf;--wt:#ffd7a8}
.K{box-sizing:border-box;position:relative;max-width:520px;margin:0 auto;direction:rtl;text-align:right;font-family:var(--ar);font-size:17px;line-height:2;overflow:hidden;overflow:clip;min-height:100%;color:#e6dec9}
.K *{box-sizing:border-box;min-width:0}
.K p{margin:0 0 8px;text-wrap:pretty}
.K h1,.K h2{margin:0;text-wrap:balance}
.K a{text-decoration:none}
.K .l{direction:ltr;unicode-bidi:isolate;display:inline-block}
.K .num{font-family:var(--lat);font-variant-numeric:lining-nums tabular-nums}
.K .bg{position:absolute;top:0;right:0;bottom:0;left:0;z-index:0;pointer-events:none;overflow:hidden;
background:radial-gradient(ellipse 80% 22% at 50% -2%,rgba(60,90,190,.55),transparent 70%),linear-gradient(180deg,#07112c,#04070f 42%,#03050b)}
.K .bg i{position:absolute;border-radius:50%;filter:blur(44px);opacity:.5}
.K .bg .o1{top:7%;left:-22%;width:230px;height:230px;background:#c8963c}
.K .bg .o2{top:36%;right:-26%;width:270px;height:270px;background:#2f58d0}
.K .bg .o3{top:72%;left:-18%;width:230px;height:230px;background:#c8963c;opacity:.34}
.K .bg::after{content:"";position:absolute;top:0;right:0;bottom:0;left:0;background:var(--grain);opacity:.05;mix-blend-mode:overlay}
.K::before{content:"";position:absolute;top:12px;right:12px;bottom:12px;left:12px;z-index:1;pointer-events:none;border:1px solid rgba(214,174,84,.58);box-shadow:inset 0 0 0 5px rgba(4,7,15,.82),inset 0 0 0 6px rgba(214,174,84,.28),inset 0 1px 0 6px rgba(255,255,255,.05)}
.K::after{content:"";position:absolute;top:7px;right:7px;bottom:7px;left:7px;z-index:1;pointer-events:none;filter:drop-shadow(0 0 5px rgba(232,196,107,.45));
background:
linear-gradient(var(--brk),var(--brk)) top left/34px 3px no-repeat,linear-gradient(var(--brk),var(--brk)) top left/3px 34px no-repeat,
linear-gradient(var(--brk),var(--brk)) top right/34px 3px no-repeat,linear-gradient(var(--brk),var(--brk)) top right/3px 34px no-repeat,
linear-gradient(var(--brk),var(--brk)) bottom left/34px 3px no-repeat,linear-gradient(var(--brk),var(--brk)) bottom left/3px 34px no-repeat,
linear-gradient(var(--brk),var(--brk)) bottom right/34px 3px no-repeat,linear-gradient(var(--brk),var(--brk)) bottom right/3px 34px no-repeat,
radial-gradient(circle,var(--brk) 2.6px,transparent 3.3px) left 33px top -2.5px/8px 8px no-repeat,radial-gradient(circle,var(--brk) 2.6px,transparent 3.3px) left -2.5px top 33px/8px 8px no-repeat,
radial-gradient(circle,var(--brk) 2.6px,transparent 3.3px) right 33px top -2.5px/8px 8px no-repeat,radial-gradient(circle,var(--brk) 2.6px,transparent 3.3px) right -2.5px top 33px/8px 8px no-repeat,
radial-gradient(circle,var(--brk) 2.6px,transparent 3.3px) left 33px bottom -2.5px/8px 8px no-repeat,radial-gradient(circle,var(--brk) 2.6px,transparent 3.3px) left -2.5px bottom 33px/8px 8px no-repeat,
radial-gradient(circle,var(--brk) 2.6px,transparent 3.3px) right 33px bottom -2.5px/8px 8px no-repeat,radial-gradient(circle,var(--brk) 2.6px,transparent 3.3px) right -2.5px bottom 33px/8px 8px no-repeat}
.K .foil{color:var(--gtxt)}
@supports ((-webkit-background-clip:text) or (background-clip:text)){
.K .foil{background:var(--foil);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:transparent;filter:drop-shadow(0 3px 10px var(--shadow))}
.K .sapfoil{background:var(--sapfoil);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:transparent;filter:drop-shadow(0 3px 10px var(--shadow))}
.K .sheen{background:linear-gradient(100deg,transparent 40%,rgba(255,255,255,.95) 50%,transparent 60%) 0% 0/300% 100% no-repeat,var(--foil);-webkit-background-clip:text;background-clip:text;animation:sweep 6s ease-in-out infinite}
}
.K .sapfoil{color:var(--saptxt)}
.K .mh{position:sticky;top:0;z-index:6;height:46px;margin-bottom:-46px;display:flex;align-items:center;justify-content:center;opacity:0;pointer-events:none;transition:opacity .25s;background:linear-gradient(180deg,rgba(4,7,15,.96) 55%,rgba(4,7,15,0))}
.K .mh.on,.K.rep.rev .mh{opacity:1}
.K .mh span{font:700 16px var(--lat);letter-spacing:1.5px;padding-top:2px}
.K .body{position:relative;z-index:2;padding:calc(40px + env(safe-area-inset-top,0px)) 30px calc(96px + env(safe-area-inset-bottom,0px))}
.K.rep.rev .body{padding-top:calc(58px + env(safe-area-inset-top,0px))}
.K .back{display:none}
.K.rev .back{display:block}
.K.rep.rev .front{display:none}
.js .K .rv{opacity:0;transform:translateY(16px);transition:opacity .7s cubic-bezier(.2,.7,.2,1),transform .7s cubic-bezier(.2,.7,.2,1)}
.js .K .rv.in{opacity:1;transform:none}
.K .f1{position:relative;min-height:584px;display:flex;flex-direction:column;align-items:center;justify-content:center}
.K .f1::before{content:"";position:absolute;left:50%;top:50%;width:380px;height:230px;margin:-130px 0 0 -190px;background:radial-gradient(ellipse at center,rgba(255,200,100,.3),rgba(255,200,100,0) 68%);pointer-events:none}
.K .bsm1{position:relative;font-size:clamp(25px,8.3vw,33px);line-height:1.7;font-weight:700;text-align:center;white-space:nowrap;-webkit-box-reflect:below -4px linear-gradient(transparent 56%,rgba(255,255,255,.3))}
.K .f1 .dv{width:84%;margin:20px 0 0;position:relative}
.K .f1 .dv.top{margin:0 0 6px}
.K.rev .f1{min-height:0;padding:0 0 2px}
.K.rev .f1::before{display:none}
.K.rev .bsm1{font-size:24px;-webkit-box-reflect:none}
.K.rev .f1 .dv{margin-top:8px}
.K.rev .f1 .dv.top{display:none}
.K .hdr{position:relative;text-align:center}
.K .pre{display:block;font-size:19px;line-height:1.6;color:#b8ae94;font-weight:600}
.K .big{display:block;margin:0 auto;width:fit-content;font:700 52px/1.12 var(--lat);letter-spacing:2px;text-align:center}
.K .ttl{display:block;text-align:center;font-size:36px;line-height:1.45;font-weight:800}
.K .sub{color:var(--gtxt);font-size:19px;line-height:1.6;text-align:center;margin-top:4px}
.K .hdr.glow::before{content:"";position:absolute;left:6%;right:6%;top:40%;height:70px;background:radial-gradient(ellipse at center,rgba(232,196,107,.3),transparent 70%);filter:blur(10px);pointer-events:none}
.K .lead{text-align:center;color:var(--lead);font-size:17.5px;line-height:2;margin:16px 0 8px}
.K .glass{position:relative;z-index:2;margin:16px 0 8px;padding:14px 18px;border-radius:20px;background:linear-gradient(180deg,rgba(255,255,255,.075),rgba(255,255,255,.02));border:1px solid rgba(232,196,107,.34);
-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px);box-shadow:0 14px 28px var(--shadow),inset 0 1px 0 rgba(255,255,255,.14)}
.K .glass p{margin:0}
.K .hg{color:var(--gtxt);font-weight:700}
.K .hb{color:var(--saptxt);font-weight:700}
.K .dv{display:flex;align-items:center;gap:12px;margin:28px 0}
.K .dv::before{content:"";flex:1;height:1px;background:linear-gradient(90deg,rgba(232,196,107,0),rgba(232,196,107,.7))}
.K .dv::after{content:"";flex:1;height:1px;background:linear-gradient(270deg,rgba(232,196,107,0),rgba(232,196,107,.7))}
.K .dv i{width:56px;height:14px;background:var(--orn) center/contain no-repeat;filter:drop-shadow(0 0 4px rgba(232,196,107,.45))}
.K h2{display:flex;align-items:center;gap:10px;font-size:21px;line-height:1.6;color:#e8c46b;margin:0 0 8px;text-shadow:0 0 18px rgba(232,196,107,.22)}
.K h2::before{content:"";width:10px;height:10px;transform:rotate(45deg);flex:none;background:linear-gradient(135deg,#fff1bf,#c9962f);box-shadow:0 0 10px rgba(232,196,107,.7)}
.K .body p{color:var(--body)}
.K .steps{position:relative;padding-right:54px;margin-top:6px}
.K .stp{position:relative;margin:0 0 22px;min-height:40px}
.K .stp:last-child{margin-bottom:0}
.K .stp p{margin:0}
.K .stp:not(:last-child)::before{content:"";position:absolute;right:-35px;top:42px;bottom:-20px;width:2px;border-radius:2px;background:linear-gradient(#e8c46b,rgba(232,196,107,.25))}
.K .sic{position:absolute;right:-54px;top:0;width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#f4d98a;border:1px solid rgba(230,195,108,.75);background:radial-gradient(circle,#18266a,#080e2c);box-shadow:0 0 16px rgba(230,195,108,.28)}
.K .sic svg{width:20px;height:20px}
.K .note{margin:16px 0 4px;padding:1.5px;background:linear-gradient(135deg,#f9e29b,#8a5f18 45%,#f4d27a);clip-path:var(--ch);filter:drop-shadow(0 8px 14px var(--shadow))}
.K .note span{display:block;padding:14px 16px;text-align:center;color:#f3ecd7;background:linear-gradient(180deg,var(--hi),transparent 34%),linear-gradient(180deg,var(--pl1),var(--pl2));clip-path:var(--ch2)}
.K svg.ic{fill:none;stroke:currentColor;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.K svg.wa{fill:currentColor;stroke:none}
.K .ringbox{position:relative;width:212px;height:212px;margin:16px auto 0}
.K .ringbox svg{position:absolute;top:0;left:0;width:100%;height:100%;display:block;overflow:visible;filter:drop-shadow(0 8px 14px var(--shadow))}
.K .arc{filter:drop-shadow(0 0 7px rgba(122,162,255,.85));animation:draw 1.3s cubic-bezier(.2,.7,.2,1) .25s both}
.K .rc{position:absolute;top:0;right:0;bottom:0;left:0;display:flex;flex-direction:column;align-items:center;justify-content:center}
.K .rc .num{font-size:36px;font-weight:700;line-height:1}
.K .rc .un{font-size:14px;line-height:1.5;color:var(--mut);margin-top:2px}
.K .stats{position:relative;z-index:3;display:grid;gap:10px;margin:18px 0 20px}
.K .stat{padding:1.5px;background:linear-gradient(135deg,#f9e29b,#8a5f18 45%,#f4d27a);clip-path:var(--ch);filter:drop-shadow(0 12px 16px var(--shadow))}
.K .pl{display:grid;grid-template-columns:1fr auto;align-items:center;gap:12px;padding:10px 18px;background:linear-gradient(180deg,var(--hi),transparent 34%),linear-gradient(180deg,var(--pl1),var(--pl2));clip-path:var(--ch2)}
.K .lb{display:flex;align-items:center;gap:9px;font-size:16px;line-height:1.55;color:var(--lab)}
.K .dot{flex:none;width:10px;height:10px;transform:rotate(45deg)}
.K .dot.a,.K .dot.c1{background:#e8c46b;box-shadow:0 0 10px rgba(232,196,107,.9)}
.K .dot.b{background:var(--sap);box-shadow:0 0 10px rgba(122,162,255,.9)}
.K .dot.c2{background:var(--ivory);box-shadow:0 0 10px rgba(241,234,219,.8)}
.K .nv{display:flex;flex-direction:column;align-items:center}
.K .pl .num{font-size:32px;font-weight:700;line-height:1}
.K .un2{font-size:13.5px;line-height:1.4;color:var(--mut)}
.K .txt{margin:0 0 8px}
.K .warn{margin:16px 0 6px;padding:1.5px;background:linear-gradient(135deg,#ffd9a0,#a85a1c 45%,#ffbb70);clip-path:var(--ch);filter:drop-shadow(0 8px 12px var(--shadow))}
.K .wi{display:flex;gap:12px;align-items:flex-start;padding:12px 14px;color:var(--wink);background:linear-gradient(180deg,var(--hi),transparent 30%),linear-gradient(180deg,var(--wb1),var(--wb2));clip-path:var(--ch2)}
.K .wi .ic2{flex:none;width:38px;height:38px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#ffc98a;border:1px solid rgba(255,180,90,.8);background:radial-gradient(circle,rgba(255,150,60,.3),rgba(255,150,60,.06));box-shadow:0 0 14px rgba(255,150,60,.25)}
.K .wi .ic2 svg{width:20px;height:20px}
.K .wi b{display:block;color:var(--wt);font-size:17px;line-height:1.7}
.K .wi div{font-size:16px;line-height:1.85}
.K .yr{display:flex;align-items:center;justify-content:center;gap:10px;width:fit-content;max-width:100%;margin:24px auto 0;padding:5px 20px;border-radius:999px;border:1px solid transparent;color:var(--mut);font-size:15px;line-height:1.7;
background:linear-gradient(#142058,#080e2c) padding-box,linear-gradient(135deg,#fff1bf,#c9962f 50%,#f4d98a) border-box;box-shadow:0 10px 18px var(--shadow)}
.K .yr i{flex:none;width:9px;height:9px;transform:rotate(45deg);background:linear-gradient(135deg,#fff1bf,#c9962f)}
.K .yr b{font:700 16px var(--lat)}
.K .sh{display:flex;align-items:center;gap:12px;margin-bottom:10px}
.K .sh h2{margin:0}
.K .sh h2::before{display:none}
.K .ic3{flex:none;width:40px;height:40px;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#f4d98a;border:1px solid rgba(230,195,108,.7);background:radial-gradient(circle,rgba(230,195,108,.25),rgba(230,195,108,.05));box-shadow:0 0 16px rgba(230,195,108,.22)}
.K .ic3 svg{width:21px;height:21px}
.K .modes{margin:6px 0 10px}
.K .mode{display:flex;align-items:center;gap:14px;padding:10px 0;border-bottom:1px solid rgba(232,196,107,.18)}
.K .mode:last-child{border-bottom:0}
.K .mode .wv{flex:none;width:58px;height:28px}
.K .mode b{display:block;color:#f4d98a;font-size:17px;line-height:1.6}
.K .mode .d{display:block;color:var(--body);font-size:15px;line-height:1.75}
.K .btnrow{margin:14px 0 8px}
.K .cta{display:flex;align-items:center;justify-content:center;gap:10px;min-height:54px;padding:0 24px;border-radius:999px;background:linear-gradient(180deg,#fff0b8,#eec45c 50%,#b88a28);color:#2a1d05 !important;font-weight:700;font-size:17.5px;box-shadow:0 8px 24px rgba(244,190,90,.38),inset 0 1px 0 rgba(255,255,255,.7);animation:breathe 3.4s ease-in-out infinite;transition:transform .15s}
.K .cta:active,.K .btn2:active,.K .spine:active{transform:scale(.97)}
.K .cta svg{width:22px;height:22px;stroke:#2a1d05}
.K .small{font-size:14px;text-align:center;color:var(--mut)}
.K .btn2{display:flex;align-items:center;justify-content:center;gap:10px;min-height:52px;padding:0 20px;border-radius:999px;color:#f4d98a !important;font-weight:700;font-size:16.5px;border:1px solid transparent;transition:transform .15s;
background:linear-gradient(180deg,var(--hi),transparent 40%) padding-box,linear-gradient(#142058,#080e2c) padding-box,linear-gradient(135deg,#fff1bf,#c9962f 50%,#f4d98a) border-box;box-shadow:0 8px 16px var(--shadow)}
.K .btn2 svg{width:22px;height:22px}
.K .btn2+.btn2{margin-top:10px}
.K .spines{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:10px 0 4px}
.K .spine{display:flex;align-items:center;justify-content:center;min-height:52px;padding:6px 10px;border-radius:12px;border:1px solid rgba(232,196,107,.4);border-left:6px solid #e8c46b;background:linear-gradient(180deg,rgba(232,196,107,.1),rgba(232,196,107,.02));color:#f4d98a !important;font:600 14.5px/1.4 var(--lat);direction:ltr;transition:transform .15s}
.K .chart{position:relative;margin:44px 0 22px;padding:26px 8px 8px;border-radius:16px;border:1px solid rgba(232,196,107,.28);background:linear-gradient(180deg,rgba(232,196,107,.07),rgba(232,196,107,.01))}
.K .tot{position:absolute;top:-19px;right:50%;transform:translateX(50%);display:flex;align-items:center;gap:8px;white-space:nowrap;padding:3px 6px 3px 16px;border-radius:999px;color:var(--lab);font-size:15px;border:1px solid transparent;
background:linear-gradient(#142058,#080e2c) padding-box,linear-gradient(135deg,#fff1bf,#c9962f 50%,#f4d98a) border-box;box-shadow:0 10px 18px var(--shadow)}
.K .pill{display:inline-block;padding:0 14px;border-radius:999px;background:linear-gradient(180deg,#fff0b8,#eec45c 50%,#b88a28);color:#3a2a08;font-weight:700;line-height:1.9;white-space:nowrap;box-shadow:inset 0 1px 0 rgba(255,255,255,.6)}
.K .pill b{font:700 1.08em var(--lat);font-variant-numeric:lining-nums}
.K .chart svg{display:block;width:100%;height:auto;overflow:visible}
.K .legend{display:flex;justify-content:center;gap:16px;flex-wrap:wrap;margin-top:6px;font-size:13.5px;color:var(--mut)}
.K .legend span{display:flex;align-items:center;gap:7px}
.K .ub{padding:14px 0 6px;border-top:1px solid rgba(232,196,107,.22)}
.K .ub:first-child{border-top:0}
.K .hd2{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:4px}
.K .ub .un{font:700 18px/1.5 var(--lat);letter-spacing:2px;color:#e8c46b;direction:ltr}
.K .ub .tt{display:flex;align-items:center;gap:7px;font-size:14px;color:var(--mut)}
.K .ub .tt .pill{font-size:14px;padding:0 11px;line-height:1.75}
.K .rw{display:flex;align-items:center;gap:10px;padding:6px 0;direction:ltr}
.K .rw .nm{flex:1 1 auto;min-width:0;direction:ltr;text-align:left;font:400 16px/1.45 var(--lat);color:#f6ead8;overflow-wrap:anywhere}
.K .cn{flex:none;direction:rtl;white-space:nowrap;font-size:13.5px;line-height:1.7;color:#f4d98a;padding:0 10px;border:1px solid rgba(232,196,107,.55);border-radius:999px;background:rgba(232,196,107,.09)}
.K .cn b{font:700 14.5px var(--lat);font-variant-numeric:lining-nums;color:#fff3c8}
.K .ur{display:flex;align-items:center;gap:12px;padding:9px 0;border-bottom:1px solid rgba(122,162,255,.18)}
.K .ur:last-child{border-bottom:0}
.K .ur .un{flex:none;width:76px;font:700 15.5px/1.5 var(--lat);letter-spacing:1.5px;color:var(--saptxt);direction:ltr;text-align:left}
.K .ur .bar{flex:1;height:7px;border-radius:99px;background:rgba(255,255,255,.07);overflow:hidden}
.K .ur .bar i{transform-origin:right;animation:growx 1s cubic-bezier(.2,.7,.2,1) both;display:block;height:100%;border-radius:99px;background:linear-gradient(90deg,#cfe0ff,#4f78e6);box-shadow:0 0 8px rgba(122,162,255,.55)}
.K .ur .c{flex:none;min-width:72px;text-align:left;font-size:14px;color:#cfdcff}
.K .ur .c b{font:700 16px var(--lat);font-variant-numeric:lining-nums;color:#fff}
.K .intro{text-align:center;color:var(--lead);margin:12px 2px 18px;font-size:17px}
.K .pr{padding:14px 0 12px;border-top:1px solid rgba(232,196,107,.22)}
.K .pr:first-child{border-top:0}
.K .pn{display:flex;align-items:baseline;gap:8px}
.K .pn .num{font-size:38px;font-weight:700;line-height:1}
.K .pn span{color:var(--lab);font-size:15.5px}
.K .pn em{margin-right:auto;font-style:normal;color:#fff3c8;font-size:15px;font-weight:700}
.K .pn em b{font:700 21px var(--lat);font-variant-numeric:lining-nums}
.K .pbar{display:flex;gap:3px;height:11px;margin:10px 0 8px}
.K .pbar i{display:block;height:100%;border-radius:99px;transform-origin:right;animation:growx 1s cubic-bezier(.2,.7,.2,1) both}
.K .pbar .s2{animation-delay:.35s}
.K .pbar .s1{background:linear-gradient(90deg,#fff1bf,#c9962f)}
.K .pbar .s2{background:linear-gradient(90deg,#cfe0ff,#4f78e6);box-shadow:0 0 10px rgba(122,162,255,.6)}
.K .pd{display:flex;gap:14px;flex-wrap:wrap;font-size:14px;color:var(--mut)}
.K .pd span{display:flex;align-items:center;gap:6px}
.K .pd b{color:#f4ecd6;font-variant-numeric:lining-nums}
.K .tip{display:flex;gap:14px;align-items:flex-start;padding:12px 0;border-top:1px solid rgba(232,196,107,.2)}
.K .tip:first-of-type{border-top:0}
.K .tip b{display:block;color:#f4d98a;font-size:17px;line-height:1.6}
.K .tip em{display:block;font:italic 13.5px/1.4 var(--lat);color:var(--saptxt);direction:ltr;text-align:right;margin-bottom:2px}
.K .tip p{margin:0;font-size:15.5px;line-height:1.85}
.K .uin{display:flex;flex-direction:column;min-height:580px;text-align:center}
.K .ubsm{text-align:center;line-height:1.9;font-weight:700;white-space:nowrap;overflow:visible}
.K .bq{display:inline-block;font-size:30px;letter-spacing:.5px}
.K .ubsm::after{content:"";display:block;width:140px;height:2px;margin:6px auto 0;background:linear-gradient(90deg,transparent,var(--brk),transparent)}
.K .uring{position:relative;width:216px;height:216px;margin:16px auto 0;flex:none}
.K .uring svg{position:absolute;top:0;left:0;width:100%;height:100%;display:block;overflow:visible;filter:drop-shadow(0 8px 14px var(--shadow))}
.K .uring .core{position:absolute;top:0;right:0;bottom:0;left:0;display:flex;flex-direction:column;align-items:center;justify-content:center}
.K .uring .w1{display:block;direction:ltr;font:400 13px/1.2 var(--lat);letter-spacing:8px;padding-left:8px;color:#e8c46b}
.K .uring .w2{display:block;direction:ltr;font:700 60px/1.02 var(--lat)}
.K .gp{position:relative;z-index:3;display:block;width:fit-content;margin:16px auto 18px;padding:1px 32px;border-radius:999px;background:linear-gradient(180deg,#fff0b8,#eec45c 50%,#b88a28);color:#3a2a08;font-weight:700;font-size:20px;line-height:1.9;box-shadow:0 10px 22px rgba(244,190,90,.4),inset 0 1px 0 rgba(255,255,255,.7),0 0 0 4px #04070f}
.K .gp b{font:700 21px var(--lat);font-variant-numeric:lining-nums}
.K .les{list-style:none;margin:0;padding:0;direction:ltr;text-align:left}
.K .les li{display:flex;align-items:center;gap:12px;padding:12px 2px;border-top:1px solid rgba(232,196,107,.26)}
.K .les li:last-child{border-bottom:1px solid rgba(232,196,107,.26)}
.K .les .tx{flex:1 1 auto;min-width:0;font:400 19px/1.4 var(--lat);color:#f6ead8;overflow-wrap:anywhere}
.K .hint{position:sticky;bottom:0;z-index:4;height:68px;margin-top:-68px;pointer-events:none;display:flex;align-items:flex-end;justify-content:center;padding-bottom:10px;background:linear-gradient(transparent,var(--pg3) 82%)}
.K .hint svg{width:24px;height:24px;fill:none;stroke:var(--brk);stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round;animation:nudge 2.2s ease-in-out infinite;filter:drop-shadow(0 0 6px rgba(232,196,107,.6))}
@media (max-width:360px){
.K .body{padding-left:22px;padding-right:22px}.K .big{font-size:42px}.K .ttl{font-size:30px}.K .pl .num{font-size:27px}.K .ringbox{width:188px;height:188px}.K .rc .num{font-size:31px}
}
.K .art{display:block;font-family:"Noto Naskh Arabic","Noto Sans Arabic","Amiri","Scheherazade New","Traditional Arabic","Arial Unicode MS",serif;font-size:clamp(66px,21vw,96px);line-height:1.3;font-weight:400;white-space:nowrap}
.K.rev .bsm1 .art{font-size:46px}
.K .ubsm .art{font-size:clamp(46px,15vw,62px);line-height:1.35}
.K .prog{position:sticky;top:0;z-index:8;height:3px;margin-bottom:-3px;width:0;background:linear-gradient(90deg,#fff1bf,#c9962f);box-shadow:0 0 8px rgba(232,196,107,.7);transition:width .1s}
@keyframes grow{from{transform:scaleY(0)}}
@keyframes growx{from{transform:scaleX(0)}}
.K .chart svg .col{transform-box:fill-box;transform-origin:bottom;animation:grow 1s cubic-bezier(.2,.7,.2,1) both}
.K .chap{display:flex;align-items:center;gap:14px;margin:0 0 12px}
.K .cnum{flex:none;direction:ltr;font:700 40px/1 var(--lat);letter-spacing:1px;padding-left:14px;border-left:1px solid rgba(232,196,107,.45)}
.K .chap h2{margin:0}
.K .chap h2::before{display:none}
.K .sic b{font:700 18px/1 var(--lat);color:#f4d98a}
.K .hr{height:1px;margin:28px 0;background:linear-gradient(90deg,transparent,rgba(232,196,107,.42),transparent)}
.K#k0 .body p{text-align:justify;text-align-last:right}
.K#k0 .glass p{text-align:center;text-align-last:center}
.K#k0 .note span{text-align:center}
.K .hero{position:relative;text-align:center;padding:6px 0 2px}
.K .hero::before{content:"";position:absolute;left:4%;right:4%;top:34%;height:80px;background:radial-gradient(ellipse at center,rgba(232,196,107,.3),transparent 70%);filter:blur(12px);pointer-events:none}
.K .hrule{position:relative;height:1px;margin:14px 0;background:linear-gradient(90deg,transparent,rgba(232,196,107,.85),transparent)}
.K .hrule::after{content:"";position:absolute;left:50%;top:-4px;margin-left:-4px;width:8px;height:8px;transform:rotate(45deg);background:linear-gradient(135deg,#fff1bf,#c9962f);box-shadow:0 0 10px rgba(232,196,107,.75)}
.K .hero .ttl{position:relative;font-size:36px;line-height:1.4}
.K .lead2{text-align:center;color:#ece6d4;font-size:18.5px;line-height:2.05;margin:16px 2px 0;text-wrap:pretty}
.K .blk{margin:0 0 36px}
.K .h{display:block;width:fit-content;max-width:100%;font-size:23px;line-height:1.5;color:#f0d484;margin:0 0 16px;padding-bottom:8px;border-bottom:2px solid transparent;border-image:linear-gradient(270deg,#e8c46b,rgba(232,196,107,0)) 1;text-shadow:0 0 18px rgba(232,196,107,.22)}
.K .h::before{display:none}
.K#k0 .body p.pull{font-size:21px;line-height:1.95;font-weight:700;color:#f6efdc;text-align:right;text-align-last:right;padding:4px 18px 4px 0;margin:0 0 14px;border-right:3px solid #e8c46b}
.K .st2{position:relative;overflow:hidden;margin:0 0 12px;padding:16px 16px 16px 14px;border-radius:18px;background:linear-gradient(180deg,rgba(255,255,255,.065),rgba(255,255,255,.015));border:1px solid rgba(232,196,107,.28);box-shadow:0 12px 22px rgba(0,0,0,.35),inset 0 1px 0 rgba(255,255,255,.1)}
.K .st2 .gn{position:absolute;left:12px;top:-16px;direction:ltr;font:700 96px/1 var(--lat);color:rgba(232,196,107,.08);-webkit-text-stroke:1px rgba(232,196,107,.42);pointer-events:none}
.K .st2 p{position:relative;margin:0;padding-left:56px}
.K#k0 .body p.lead2{text-align:center;text-align-last:center}
.K .lead2{margin:18px 2px 8px}
.K .lead2+.blk{margin-top:36px}
.K .closing{margin:10px 0 0}
.K .closing .hrule{margin:16px 0}
.K#k0 .body .closing p{margin:0 6px;text-align:center;text-align-last:center;font-size:19.5px;line-height:2.05;font-weight:700;color:#f3ecd7}
.K{text-rendering:optimizeLegibility;-webkit-font-smoothing:antialiased;font-kerning:normal;hyphens:none}
.K .cta,.K .btn2,.K .spine{touch-action:manipulation}
html,body{margin:0;padding:0;background:#04070f}
.K{min-height:100vh}
/* ═════ بطاقة عنوان الوحدة (بلا دروس) ═════ */
.K .tc{display:flex;flex-direction:column;align-items:center;text-align:center;min-height:600px}
.K .ubsm{text-align:center;line-height:1.9;font-weight:700;white-space:nowrap}
.K .bq{display:inline-block;font-size:30px;letter-spacing:.5px}
.K .ubsm::after{content:"";display:block;width:150px;height:2px;margin:6px auto 0;background:linear-gradient(90deg,transparent,#e8c46b,transparent)}
.K .itag{margin:18px 0 0;padding:2px 26px;border-radius:999px;border:1px solid transparent;font-size:17px;line-height:1.8;font-weight:700;color:#cfe0ff;background:linear-gradient(#142058,#080e2c) padding-box,linear-gradient(135deg,#cfe0ff,#4f78e6 55%,#a9c0ff) border-box;box-shadow:0 8px 16px rgba(0,0,0,.5)}
.K .hero-n{position:relative;width:100%;margin-top:30px;display:flex;flex-direction:column;align-items:center}
.K .hero-n::before{content:"";position:absolute;left:50%;top:58%;width:320px;height:230px;margin:-115px 0 0 -160px;background:radial-gradient(ellipse at center,rgba(232,196,107,.3),rgba(232,196,107,0) 68%);pointer-events:none}
.K .lab{position:relative;display:flex;align-items:center;gap:14px;width:76%;direction:ltr;font:700 15px/1.6 var(--lat);letter-spacing:10px;color:#e8c46b}
.K .lab::before,.K .lab::after{content:"";flex:1;height:1px;background:linear-gradient(90deg,transparent,rgba(232,196,107,.75))}
.K .lab::after{background:linear-gradient(270deg,transparent,rgba(232,196,107,.75))}
.K .lab span{padding-left:10px}
.K .lab.ar{direction:rtl;font:700 25px/1.5 var(--ar);letter-spacing:0;color:#cfe0ff}
.K .lab.ar span{padding:0}
.K .nbig{position:relative;margin-top:2px;direction:ltr;font:700 clamp(112px,37vw,156px)/1.02 var(--lat);letter-spacing:-2px}
.K .kick{margin:12px 0 0;font:700 13px/1.6 var(--lat);letter-spacing:7px;padding-left:7px;color:#a99c75;direction:ltr}
.K .cplq{margin:26px 0 0;min-width:210px;padding:1.5px;background:linear-gradient(135deg,#f9e29b,#8a5f18 45%,#f4d27a);clip-path:var(--ch);filter:drop-shadow(0 12px 16px rgba(0,0,0,.5))}
.K .pl2{display:flex;align-items:baseline;justify-content:center;gap:10px;padding:10px 28px;background:linear-gradient(180deg,rgba(255,255,255,.13),transparent 34%),linear-gradient(180deg,#142058,#080e2c);clip-path:var(--ch2)}
.K .pl2 b{font-size:42px;font-weight:700;line-height:1.1}
.K .pl2 span{font-size:17px;color:#a99c75}
.K .cnt-lab{margin-top:4px;font-size:22px;color:#cfe0ff}
.K .of{margin-top:10px;font-size:14.5px;line-height:1.7;color:#a99c75}
.K .of b{font:700 16px var(--lat);font-variant-numeric:lining-nums;color:#f4ecd6}
.K .track{display:flex;align-items:center;gap:5px;width:86%;margin-top:26px}
.K .track i{flex:1;height:6px;border-radius:3px;background:rgba(232,196,107,.16)}
.K .track i.done{background:rgba(232,196,107,.5)}
.K .track i.on{height:9px;background:linear-gradient(90deg,#fff1bf,#c9962f);box-shadow:0 0 12px rgba(232,196,107,.85)}
/* لمسة ياقوتية للكلمات المهمة (تشمل شريط التقدّم العلوي) */
.K.imp{--brk:#9db8ff}
.K.imp::before{border-color:rgba(122,162,255,.55);box-shadow:inset 0 0 0 5px rgba(4,7,15,.82),inset 0 0 0 6px rgba(122,162,255,.28)}
.K.imp::after{filter:drop-shadow(0 0 5px rgba(122,162,255,.5))}
.K.imp .prog{background:linear-gradient(90deg,#e6efff,#4f78e6);box-shadow:0 0 8px rgba(122,162,255,.75)}
.K.imp .bg .o1,.K.imp .bg .o3{background:#3a5fd0}
.K.imp .hero-n::before{background:radial-gradient(ellipse at center,rgba(122,162,255,.34),rgba(122,162,255,0) 68%)}
.K.imp .lab{color:#9db8ff}
.K.imp .lab::before{background:linear-gradient(90deg,transparent,rgba(122,162,255,.8))}
.K.imp .lab::after{background:linear-gradient(270deg,transparent,rgba(122,162,255,.8))}
.K.imp .kick{color:#8fa8e8}
.K.imp .of b{color:#cfe0ff}
.K.imp .cplq{background:linear-gradient(135deg,#e6efff,#4f78e6 45%,#9db8ff)}
.K.imp .pl2{background:linear-gradient(180deg,rgba(255,255,255,.13),transparent 34%),linear-gradient(180deg,#14275e,#080e2c)}
.K.imp .pl2 span{color:#8fa8e8}
.K.imp .track i{background:rgba(122,162,255,.16)}
.K.imp .track i.done{background:rgba(122,162,255,.5)}
.K.imp .track i.on{background:linear-gradient(90deg,#e6efff,#4f78e6);box-shadow:0 0 12px rgba(122,162,255,.85)}
@supports ((-webkit-background-clip:text) or (background-clip:text)){
.K .sapsheen{background:linear-gradient(100deg,transparent 40%,rgba(255,255,255,.95) 50%,transparent 60%) 0% 0/300% 100% no-repeat,var(--sapfoil);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;color:transparent;animation:sweep 6s ease-in-out infinite;filter:drop-shadow(0 3px 10px rgba(0,0,0,.6))}
}
'''

SCRIPT = r'''<script>
(function(){
 var d=document,h=d.documentElement;
 if((" "+h.className+" ").indexOf(" js ")<0)h.className+=" js";
 var K=d.querySelector(".K");if(!K)return;
 Array.prototype.forEach.call(K.querySelectorAll(".l"),function(e){e.setAttribute("lang","en")});
 Array.prototype.forEach.call(K.querySelectorAll(".fit"),function(el){
  var w=el.parentNode.clientWidth-8;if(w<=0)return;var fs=parseFloat(getComputedStyle(el).fontSize)||30;
  while(el.scrollWidth>w&&fs>15){fs-=1;el.style.fontSize=fs+"px";}
 });
 var bar=d.createElement("div");bar.className="prog";K.insertBefore(bar,K.firstChild);
 var hint=K.querySelector(".hint");
 function upd(){var se=d.scrollingElement||h,m=se.scrollHeight-window.innerHeight,y=window.pageYOffset||se.scrollTop||0;
  bar.style.width=(m>0?Math.min(100,y/m*100):0)+"%";if(hint)hint.style.visibility=(m>40&&y<m-24)?"visible":"hidden";}
 window.addEventListener("scroll",upd,{passive:true});upd();
 var els=K.querySelectorAll(".rv");
 if(!("IntersectionObserver" in window)){Array.prototype.forEach.call(els,function(e){e.classList.add("in")});}
 else{var io=new IntersectionObserver(function(es){es.forEach(function(en){if(en.isIntersecting){en.target.classList.add("in");io.unobserve(en.target);}});},{threshold:.08});
  Array.prototype.forEach.call(els,function(e){io.observe(e)});}
 Array.prototype.forEach.call(K.querySelectorAll(".cu"),function(el){
  var v=parseInt(el.getAttribute("data-v"),10),t0=null;
  function st(ts){if(t0===null)t0=ts;var p=Math.min(1,(ts-t0)/1000),e=1-Math.pow(1-p,3);el.textContent=Math.round(v*e).toLocaleString("en-US");if(p<1)requestAnimationFrame(st);else el.textContent=v.toLocaleString("en-US");}
  requestAnimationFrame(st);
 });
})();
</script>'''
assert "{{" not in SCRIPT


def esc(t):
    return html.escape(t, quote=False)


def fmt(n):
    return f"{n:,}"


def wrap(inner, cls=""):
    return (f'<div class="K {cls}"><div class="bg"><i class="o1"></i><i class="o2"></i><i class="o3"></i></div>'
            f'<main class="body">{inner}</main></div>')


def title_card(p, n, count, idx, imp):
    total_units = len(p["units"])
    segs = "".join(f'<i class="{"on" if i == idx else ("done" if i < idx else "")}"></i>' for i in range(total_units))
    num_cls = "sapfoil sapsheen" if imp else "foil sheen"
    tag = '<div class="itag rv">الكلمات المهمة</div>' if imp else ""
    inner = f"""<section class="front tc">
   <div class="ubsm foil rv"><span class="bq fit">{BASMALA}</span></div>{tag}
   <div class="hero-n rv"><div class="lab"><span>{p["label"]}</span></div><div class="nbig {num_cls}">{n}</div></div>
   <div class="kick rv">{esc(p["title"].upper())}</div>
   <div class="cplq rv"><div class="pl2"><b class="num {"sapfoil" if imp else "foil"} cu" data-v="{count}">{count}</b><span>بطاقة</span></div></div>
   <div class="of rv">من أصل <b>{fmt(p["total"])}</b> بطاقة</div>
   <div class="track rv">{segs}</div>
  </section>"""
    return wrap(inner, "imp" if imp else "")


def overall_card(p):
    inner = f"""<section class="front tc">
   <div class="ubsm foil rv"><span class="bq fit">{BASMALA}</span></div>
   <div class="kick rv" style="margin-top:22px">{esc(p["title"].upper())}</div>
   <div class="hero-n rv"><div class="lab ar"><span>الكلمات المهمة</span></div><div class="nbig sapfoil sapsheen cu" data-v="{p["total"]}">{p["total"]}</div><div class="cnt-lab">بطاقة</div></div>
  </section>"""
    return wrap(inner, "imp")


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    print("التحقق من الأرقام:")
    verify()
    model = genanki.Model(
        1907393301, "Royal Unit Title",
        fields=[{"name": "Title"}, {"name": "Front"}],
        templates=[{"name": "Unit", "qfmt": "{{Front}}" + SCRIPT, "afmt": "{{FrontSide}}"}],
        css=CSS)
    decks, did, cards = [], 2759000000, 0

    def add(name, title, front, tags, guid):
        nonlocal did, cards
        did += 1
        d = genanki.Deck(did, name)
        d.add_note(genanki.Note(model=model, fields=[title, front.replace("{{", "{ {")], guid=genanki.guid_for(*guid), tags=tags))
        decks.append(d)
        cards += 1

    for p in BASE:
        for i, (n, c) in enumerate(p["units"]):
            add(f"{PARENT}::الرزمة الأساسية::{p['title']}::{p['label']} {n}", f"{p['title']} · {p['label']} {n}",
                title_card(p, n, c, i, False), ["unit", p["key"]], ("ucard", "base", p["key"], n))
    for p in IMPORTANT:
        if p["units"] is None:
            add(f"{PARENT}::الكلمات المهمة::{p['title']}", f"{p['title']} · الكلمات المهمة", overall_card(p),
                ["important", p["key"]], ("ucard", "imp", p["key"], "all"))
            continue
        for i, (n, c) in enumerate(p["units"]):
            add(f"{PARENT}::الكلمات المهمة::{p['title']}::{p['label']} {n}", f"{p['title']} · {p['label']} {n} · الكلمات المهمة",
                title_card(p, n, c, i, True), ["important", p["key"]], ("ucard", "imp", p["key"], n))
    out = os.path.join(here, OUTPUT_FILE)
    genanki.Package(decks).write_to_file(out)
    print(f"\n✓ تم إنشاء: {out}")
    print(f"  رزم: {len(decks)} · بطاقات: {cards}")
    print('\nلنسخه إلى التنزيلات:  cp "%s" ~/storage/downloads/' % out)


if __name__ == "__main__":
    main()
