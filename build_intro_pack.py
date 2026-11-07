#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
بسم الله الرحمن الرحيم
مولّد حزمة «البطاقات التمهيدية» للرزم الخمس — قالب الليل الملكي

في الحزمة الواحدة: خمس رزم فرعية (English 9 · English Lit 12 · English Sci 12 · French 9 · French 12)
وفي كل رزمة فرعية أربع بطاقات تمهيدية (بلا تعريف الوحدات) = 20 بطاقة:
  1) الترحيب  (الأمام: بسملة مؤقتة تستبدلها أنت — الخلف: بطاقة الترحيب)
  2) المعلومات (الأمام: الأرقام والحلقة — الخلف: الصوت والمعرض والرزم الأخرى والتواصل والنشر)
  3) الفهرس   (الأمام: مخطط الوحدات والدروس — الخلف: الكلمات المهمة)
  4) خطة الدراسة (الأمام: خمس وتائر — الخلف: ضبط Anki)

التشغيل في Termux:
    python build_intro_pack.py
الناتج:
    Intro_5Packs.apkg   (بجانب السكربت)

ما تعدّله أنت: الروابط والرسائل في قسم «الإعدادات» أدناه، وواجهة البطاقة الأولى (البسملة).
"""
import os
import html
import math
from urllib.parse import quote

import genanki

# ════════════════════════════════════════════════════════════════
#  الإعدادات
# ════════════════════════════════════════════════════════════════
OUTPUT_FILE = "Intro_5Packs.apkg"
PARENT_DECK = "البطاقات التمهيدية"
YEAR = "2026–2027"

WHATSAPP_CONTACT = "https://wa.me/963937175489"
TELEGRAM_GROUP = "https://t.me/Ankiarabic_QA"

# روابط المعارض: وهمية مؤقتاً — استبدلها بالروابط الحقيقية
GALLERY_URL = {
    "E9": "https://example.com/gallery/english-9",
    "EL12": "https://example.com/gallery/english-lit-12",
    "ES12": "https://example.com/gallery/english-sci-12",
    "F9": "https://example.com/gallery/french-9",
    "F12": "https://example.com/gallery/french-12",
}
# رسالة النشر لكل رزمة (اكتبها أنت). إن تُركت فارغة تُستعمل رسالة مؤقتة قصيرة.
SHARE_MESSAGE = {"E9": "", "EL12": "", "ES12": "", "F9": "", "F12": ""}

# ════════════════════════════════════════════════════════════════
#  البيانات (من النص المعتمد)
# ════════════════════════════════════════════════════════════════
def U(n, total, imp, *lessons):
    return {"n": n, "total": total, "imp": imp, "lessons": list(lessons)}

PACKS = [
    {"key": "E9", "title": "English 9", "lead": "اللغة الإنجليزية للصف التاسع", "sub": "مفردات اللغة الإنجليزية للصف التاسع",
     "adj": "الإنجليزي", "adj_f": "الإنجليزية", "label": "UNIT", "base": 1634, "imp": 709,
     "units": [
         U("01", 178, 79, ("A Different Class", 110), ("From Microsoft to Tomatoes", 68)),
         U("02", 118, 42, ("Light Initiative", 78), ("Pay It Forward", 40)),
         U("03", 117, 62, ("Life in the Future", 76), ("Living in Space", 41)),
         U("04", 186, 58, ("Autonomous Vehicles", 146), ("Ecological Cities", 40)),
         U("05", 104, 54, ("Late to Go Back", 46), ("Learn a Skill", 58)),
         U("06", 242, 109, ("All are Involved", 48), ("Mother's Decisions", 194)),
         U("07", 102, 46, ("Back to Life", 35), ("No One Had Believed", 67)),
         U("08", 152, 62, ("On the Edge of Innocence", 36), ("Sky Walkers", 116)),
         U("09", 96, 48, ("An Active Citizen", 37), ("Who Deserves the Award", 59)),
         U("10", 102, 36, ("Hurry Up", 30), ("Time Waits for No One", 72)),
         U("11", 73, 47, ("Messages from Space", 34), ("Touch People's Hearts", 39)),
         U("12", 164, 66, ("Do Animals Have Language", 40), ("Let's Communicate", 124)),
     ]},
    {"key": "EL12", "title": "English Lit 12", "lead": "اللغة الإنجليزية للبكالوريا الأدبي", "sub": "مفردات اللغة الإنجليزية للبكالوريا الأدبي",
     "adj": "الإنجليزي", "adj_f": "الإنجليزية", "label": "UNIT", "base": 2755, "imp": 1216,
     "units": [
         U("01", 387, 119, ("Future Careers", 177), ("Life Choice", 210)),
         U("02", 243, 106, ("Success — Part 1", 71), ("Success — Part 2", 172)),
         U("03", 279, 108, ("A Prominent Figure in English Literature", 85), ("History of Poetry", 194)),
         U("04", 377, 104, ("History of Drama", 238), ("William Shakespeare", 139)),
         U("05", 196, 105, ("Civil Rights", 80), ("The Right to Education", 116)),
         U("06", 220, 104, ("History of the United Nations", 117), ("United Nations / UNICEF", 103)),
         U("07", 152, 96, ("Charles Dickens", 75), ("Prose", 77)),
         U("08", 159, 90, ("Essay / Imru' al-Qais", 40), ("What is an Essay", 119)),
         U("09", 248, 83, ("Citizenship", 100), ("Racial discrimination / Civil disobedience", 148)),
         U("10", 173, 101, ("Culture Shock", 102), ("Montreal Diary / Sugar time", 71)),
         U("11", 165, 105, ("Epic of Gilgamesh", 112), ("The 1001 Nights", 53)),
         U("12", 156, 95, ("A Tale of Two Cities", 60), ("Mona Lisa", 96)),
     ]},
    {"key": "ES12", "title": "English Sci 12", "lead": "اللغة الإنجليزية للبكالوريا", "sub": "مفردات اللغة الإنجليزية للبكالوريا العلمي",
     "adj": "الإنجليزي", "adj_f": "الإنجليزية", "label": "UNIT", "base": 2834, "imp": 1237,
     "units": [
         U("01", 232, 119, ("A Learned Lesson is a Good Lesson", 116), ("Life Choices", 116)),
         U("02", 325, 106, ("Famous Failures Who Refused to Give up", 227), ("Success", 98)),
         U("03", 468, 113, ("History of Medicine", 198), ("Medical Inventions", 270)),
         U("04", 308, 110, ("History of Engineering", 125), ("Medical Technology Engineering", 183)),
         U("05", 210, 102, ("Civil Rights & Law", 128), ("The Right to Education", 82)),
         U("06", 311, 101, ("History of the United Nations", 156), ("UNICEF", 155)),
         U("07", 31, 99, ("Antibiotics", 11), ("Microorganisms", 20)),
         U("08", 251, 95, ("Facts about Human Body", 110), ("How does the Immune System Work?", 141)),
         U("09", 148, 83, ("Citizenship", 89), ("Our Duties and Responsibilities in Society", 59)),
         U("10", 139, 103, ("Culture Shock — Part 1", 67), ("Culture Shock — Part 2", 72)),
         U("11", 205, 105, ("Artificial Intelligence", 137), ("Robots", 68)),
         U("12", 206, 101, ("Digital Literacy — Part 1", 84), ("Digital Literacy — Part 2", 122)),
     ]},
    {"key": "F9", "title": "French 9", "lead": "اللغة الفرنسية", "sub": "مفردات اللغة الفرنسية للصف التاسع",
     "adj": "الفرنسي", "adj_f": "الفرنسية", "label": "DOSSIER", "base": 1045, "imp": 430,
     "units": [U("01", 305, None), U("02", 149, None), U("03", 164, None), U("04", 125, None), U("05", 175, None), U("06", 127, None)]},
    {"key": "F12", "title": "French 12", "lead": "اللغة الفرنسية للبكالوريا", "sub": "مفردات اللغة الفرنسية للبكالوريا",
     "adj": "الفرنسي", "adj_f": "الفرنسية", "label": "UNIT", "base": 2055, "imp": 1036,
     "units": [U("01", 544, 124), U("02", 359, 224), U("03", 320, 205), U("04", 244, 127), U("05", 255, 189), U("06", 333, 167)]},
]


def verify():
    ok = True
    for p in PACKS:
        tb = sum(u["total"] for u in p["units"])
        if tb != p["base"]:
            ok = False
            print(f"  ✗ {p['title']}: مجموع الوحدات {tb} ≠ {p['base']}")
        for u in p["units"]:
            if u["lessons"]:
                s = sum(c for _, c in u["lessons"])
                if s != u["total"]:
                    ok = False
                    print(f"  ✗ {p['title']} {p['label']} {u['n']}: مجموع الدروس {s} ≠ {u['total']}")
            if u["imp"] is not None and u["imp"] > u["total"]:
                print(f"  ⚠ {p['title']} {p['label']} {u['n']}: الكلمات المهمة {u['imp']} أكبر من الأساسية {u['total']} — راجع النص المصدر")
        if p["units"][0]["imp"] is not None:
            ti = sum(u["imp"] for u in p["units"])
            if ti != p["imp"]:
                ok = False
                print(f"  ✗ {p['title']}: مجموع الكلمات المهمة {ti} ≠ {p['imp']}")
    print("  ✓ كل الأرقام متطابقة" if ok else "  ⚠ راجع الفروق أعلاه")
    return ok


# ════════════════════════════════════════════════════════════════
#  التصميم (CSS + رموز SVG + سكربت اختياري)
# ════════════════════════════════════════════════════════════════
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

.K .hero{padding:16px 0 6px}
.K .closing{position:relative;margin:22px 0 0;padding:20px 22px;border-radius:16px;border:1px solid transparent;
background:linear-gradient(180deg,rgba(255,255,255,.09),transparent 42%) padding-box,linear-gradient(180deg,#16255a,#080e2c) padding-box,linear-gradient(135deg,#fff1bf,#c9962f 50%,#f4d98a) border-box;
box-shadow:inset 0 0 0 4px #04070f,inset 0 0 0 5px rgba(232,196,107,.3),0 18px 30px rgba(0,0,0,.55)}
.K .lc{display:flex;flex-direction:column;align-items:center;text-align:center;min-height:590px}
.K .bsm2{font-size:30px;line-height:1.7;font-weight:700;white-space:nowrap;text-align:center}
.K .bsm2::after{content:"";display:block;width:160px;height:2px;margin:6px auto 0;background:linear-gradient(90deg,transparent,#e8c46b,transparent)}
.K .tagu{display:inline-flex;align-items:center;gap:10px;margin:24px 0 10px;padding:3px 18px 3px 12px;border-radius:999px;border:1px solid transparent;direction:ltr;font:700 14px/1.7 var(--lat);letter-spacing:6px;color:#f4d98a;
background:linear-gradient(#142058,#080e2c) padding-box,linear-gradient(135deg,#fff1bf,#c9962f 50%,#f4d98a) border-box;box-shadow:0 8px 16px rgba(0,0,0,.5)}
.K .tagu i{width:8px;height:8px;transform:rotate(45deg);background:linear-gradient(135deg,#fff1bf,#c9962f);box-shadow:0 0 8px rgba(232,196,107,.7)}
.K .lname{direction:ltr;font:700 clamp(30px,9.8vw,40px)/1.22 var(--lat);letter-spacing:.5px;margin:6px 4px 0;text-wrap:balance}
.K .lring{position:relative;width:208px;height:208px;margin:28px auto 6px;flex:none}
.K .lring svg{position:absolute;top:0;left:0;width:100%;height:100%;display:block;overflow:visible;filter:drop-shadow(0 8px 14px rgba(0,0,0,.55))}
.K .of{font-size:14.5px;line-height:1.7;color:#a99c75;margin-top:6px}
.K .of b{font:700 16px var(--lat);font-variant-numeric:lining-nums;color:#f4ecd6}
.K .pos{display:flex;gap:12px;margin-top:16px}
.K .pos i{width:10px;height:10px;transform:rotate(45deg);border:1.5px solid rgba(232,196,107,.55);background:transparent}
.K .pos i.on{border-color:transparent;background:linear-gradient(135deg,#fff1bf,#c9962f);box-shadow:0 0 12px rgba(232,196,107,.8)}

.K .chart{margin-top:52px;padding-top:52px}
html,body{margin:0;padding:0;background:#04070f}
.K{min-height:100vh}
.K .f1{min-height:calc(100vh - 140px)}
'''

SPRITE = r'''<svg style="position:absolute;width:0;height:0" aria-hidden="true"><defs>
<linearGradient id="gG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff1bf"/><stop offset=".35" stop-color="#e8c46b"/><stop offset=".7" stop-color="#a87a1f"/><stop offset="1" stop-color="#f4d98a"/></linearGradient>
<linearGradient id="gB" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#cfe0ff"/><stop offset=".5" stop-color="#6f95f0"/><stop offset="1" stop-color="#3659c9"/></linearGradient>
<linearGradient id="gI" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".6" stop-color="#e8dfc8"/><stop offset="1" stop-color="#bfb391"/></linearGradient>
<radialGradient id="gF" cx="50%" cy="50%" r="50%"><stop offset="0" stop-color="#e8c46b" stop-opacity=".16"/><stop offset="1" stop-color="#e8c46b" stop-opacity="0"/></radialGradient>
<symbol id="i-cards" viewBox="0 0 24 24"><rect x="4" y="8" width="12" height="12" rx="2"/><path d="M8 4h10a2 2 0 0 1 2 2v10"/></symbol>
<symbol id="i-warn" viewBox="0 0 24 24"><path d="M12 4l9 16H3L12 4z"/><path d="M12 10v4M12 17v.5"/></symbol>
<symbol id="i-spk" viewBox="0 0 24 24"><path d="M4 9v6h4l5 4V5L8 9H4z"/><path d="M16 9a4 4 0 0 1 0 6M18.5 6.5a8 8 0 0 1 0 11"/></symbol>
<symbol id="i-grid" viewBox="0 0 24 24"><rect x="4" y="4" width="7" height="7" rx="1.5"/><rect x="13" y="4" width="7" height="7" rx="1.5"/><rect x="4" y="13" width="7" height="7" rx="1.5"/><rect x="13" y="13" width="7" height="7" rx="1.5"/></symbol>
<symbol id="i-globe" viewBox="0 0 24 24"><circle cx="12" cy="12" r="8"/><path d="M4 12h16M12 4c3 3 3 13 0 16M12 4c-3 3-3 13 0 16"/></symbol>
<symbol id="i-chat" viewBox="0 0 24 24"><path d="M4 5h16v11H9l-5 4V5z"/><path d="M8 9.5h8M8 12.5h5"/></symbol>
<symbol id="i-plane" viewBox="0 0 24 24"><path d="M21 4L3 11l6 2 2 6 3-4 5 3L21 4z"/><path d="M9 13l12-9"/></symbol>
<symbol id="i-spark" viewBox="0 0 24 24"><path d="M11 3l1.6 4.6L17 9.2l-4.4 1.6L11 15.4 9.4 10.8 5 9.2l4.4-1.6z"/><path d="M18.5 14l.8 2.2 2.2.8-2.2.8-.8 2.2-.8-2.2-2.2-.8 2.2-.8z"/><path d="M5.5 15.5l.6 1.6 1.6.6-1.6.6-.6 1.6-.6-1.6-1.6-.6 1.6-.6z"/></symbol>
<symbol id="i-cal" viewBox="0 0 24 24"><rect x="4" y="5" width="16" height="15" rx="2"/><path d="M8 3v4M16 3v4M4 10h16"/></symbol>
<symbol id="i-gear" viewBox="0 0 24 24"><circle cx="12" cy="12" r="3"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.6 5.6l2.1 2.1M16.3 16.3l2.1 2.1M18.4 5.6l-2.1 2.1M7.7 16.3l-2.1 2.1"/></symbol>
<symbol id="i-loop" viewBox="0 0 24 24"><path d="M20 12a8 8 0 0 0-14-5.3L4 9"/><path d="M4 4v5h5"/><path d="M4 12a8 8 0 0 0 14 5.3L20 15"/><path d="M20 20v-5h-5"/></symbol>
<symbol id="i-hourglass" viewBox="0 0 24 24"><path d="M7 3h10M7 21h10M8 3v4l4 5-4 5v4M16 3v4l-4 5 4 5v4"/></symbol>
<symbol id="i-bulb" viewBox="0 0 24 24"><path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.5 1 2.5h6c0-1 .2-1.7 1-2.5A6 6 0 0 0 12 3z"/></symbol>
<symbol id="i-eye" viewBox="0 0 24 24"><path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></symbol>
<symbol id="i-sprout" viewBox="0 0 24 24"><path d="M12 21v-9"/><path d="M12 13c0-4.5-3-7-8-7 0 4.5 3 7 8 7z"/><path d="M12 10.5c0-3.5 2.4-6 7-6 0 3.5-2.4 6-7 6z"/></symbol>
<symbol id="i-wa" viewBox="0 0 24 24"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.3-.15-1.263-.465-2.403-1.485-.888-.795-1.484-1.77-1.66-2.07-.174-.3-.019-.465.13-.615.136-.135.301-.345.451-.52.146-.181.194-.301.297-.497.1-.21.05-.375-.025-.524-.075-.15-.672-1.62-.922-2.206-.24-.584-.487-.51-.672-.51-.172-.015-.371-.015-.571-.015-.2 0-.523.074-.797.359-.273.3-1.045 1.02-1.045 2.475s1.07 2.865 1.219 3.075c.149.18 2.095 3.195 5.076 4.483.709.3 1.263.489 1.694.626.712.226 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></symbol>
</defs></svg>'''.replace('<symbol id="i-wa"','<symbol id="i-info" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><path d="M12 11v5M12 8v.5"/></symbol>\n<symbol id="i-wa"')

HINT = '<div class="hint"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></div>'

SCRIPT = r'''<script>
(function(){
 var d=document,h=d.documentElement;
 if((" "+h.className+" ").indexOf(" js ")<0)h.className+=" js";
 var K=d.querySelector(".K");if(!K)return;
 Array.prototype.forEach.call(K.querySelectorAll(".l"),function(e){e.setAttribute("lang","en")});
 var bar=d.createElement("div");bar.className="prog";K.insertBefore(bar,K.firstChild);
 var hint=K.querySelector(".hint"),mh=K.querySelector(".mh"),rep=K.classList.contains("rep");
 function upd(){
  var se=d.scrollingElement||h,m=se.scrollHeight-window.innerHeight,y=window.pageYOffset||se.scrollTop||0;
  bar.style.width=(m>0?Math.min(100,y/m*100):0)+"%";
  if(hint)hint.style.visibility=(m>40&&y<m-24)?"visible":"hidden";
  if(mh&&!rep)mh.className="mh"+(y>150?" on":"");
 }
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

WAVE = ('<svg class="wv" viewBox="0 0 56 28" aria-hidden="true">{}</svg>')
BARS = [(2, 10, 8), (10, 6, 16), (18, 2, 24), (26, 8, 12), (34, 4, 20), (42, 9, 10), (50, 6, 16)]


def wave(kind):
    ice, gold = "#e8eefc", "#e8c46b"
    cols = {"en": [ice] * 7, "ar": [gold] * 7, "both": [ice] * 3 + [gold] * 4}[kind]
    g = "".join(f'<rect x="{x}" y="{y}" width="4" height="{h}" rx="2" fill="{c}"/>' for (x, y, h), c in zip(BARS, cols))
    return WAVE.format(g)


# ════════════════════════════════════════════════════════════════
#  بناة الوجوه
# ════════════════════════════════════════════════════════════════
def fmt(n):
    return f"{n:,}"


def esc(t):
    return html.escape(t, quote=False)


A = '<span class="l">Anki</span>'


def wrap(inner, cls="", mh=None, hint=True):
    mh_html = f'<div class="mh"><span class="foil l">{esc(mh)}</span></div>' if mh else ""
    return (SPRITE + f'<div class="K {cls}"><div class="bg"><i class="o1"></i><i class="o2"></i><i class="o3"></i></div>{mh_html}'
            f'<main class="body">{inner}</main>{HINT if hint else ""}</div>')


# ── 1) الترحيب ──
def card1_front(p):
    # مكان واجهتك: استبدل هذا بتصميم بسملتك
    return wrap('<section class="front f1"><div class="bsm1 foil">بسم الله الرحمن الرحيم</div></section>', hint=False)


def card1_back(p):
    inner = f'''<section class="back">
   <header class="hero rv"><h1 class="ttl"><span class="pre">أهلًا بك في</span> <span class="l big foil sheen">{esc(p["title"])}</span></h1></header>
   <p class="lead2 rv">أُعدّت هذه الرزمة لتساعدك على دراسة مفردات {p["lead"]} ومراجعتها بطريقة منظّمة باستخدام {A}.</p>
   <section class="blk rv">
    <h2 class="h">ما هو {A}؟</h2>
    <p class="pull">برنامج يساعدك على تثبيت المعلومات في الذاكرة من خلال الاسترجاع النشط والتكرار المتباعد.</p>
    <p>فبدلًا من مراجعة جميع الكلمات بالوتيرة نفسها، يساعدك البرنامج على تحديد مواعيد المراجعة بحسب مدى سهولة تذكّرك لكل معلومة.</p>
   </section>
   <section class="blk rv">
    <h2 class="h">كيف تستفيد منه؟</h2>
    <div class="st2"><span class="gn">1</span><p>عندما تظهر الكلمة {p["adj_f"]}، حاول تذكّر معناها قبل كشف الإجابة. بعد ذلك، اكشف الإجابة وقارنها بما تذكرته، ثم قيّم مدى سهولة استرجاعك للمعلومة.</p></div>
    <div class="st2"><span class="gn">2</span><p>بناءً على تقييمك، يحدد {A} موعد ظهور البطاقة مجددًا. فالكلمة التي يصعب تذكّرها تحتاج إلى مراجعة أقرب، أما التي تتذكرها بسهولة فيمكن مراجعتها على فترات أبعد.</p></div>
   </section>
   <section class="blk rv">
    <h2 class="h">لماذا يناسب المفردات؟</h2>
    <p>لأن تعلّم المفردات لا يقتصر على قراءة الكلمة ومعناها، بل يحتاج إلى القدرة على استرجاعهما عند الحاجة. وهنا تأتي فائدة الجمع بين محاولة التذكّر قبل كشف الإجابة والمراجعة على فترات متباعدة.</p>
    <div class="closing"><p>التكرار المتباعد والاسترجاع النشط من طرق الدراسة المدعومة بأبحاث علم الذاكرة والتعلّم.</p></div>
   </section>
  </section>'''
    return wrap(inner, cls="rev")


# ── 2) المعلومات ──
def card2_front(p):
    B, I = p["base"], p["imp"]
    C = 2 * math.pi * 80
    arc = C * I / B
    inner = f'''<section class="front">
   <div class="hdr glow rv"><h1 class="big l foil sheen">{esc(p["title"])}</h1><div class="sub">{p["sub"]}</div></div>
   <p class="lead rv">رزمة أُعدّت لتنظيم دراسة المفردات ومراجعتها، مع الفصل بين <span class="hg">المفردات الأساسية</span> والمجموعة المخصّصة <span class="hb">للكلمات المهمة</span>.</p>
   <div class="ringbox rv">
    <svg viewBox="0 0 220 220" aria-hidden="true">
     <circle cx="110" cy="110" r="72" fill="url(#gF)"/>
     <circle cx="110" cy="110" r="106" fill="none" stroke="url(#gG)" stroke-width="1.2"/>
     <circle cx="110" cy="110" r="100" fill="none" stroke="url(#gG)" stroke-width="5" stroke-dasharray="1 5.98" opacity=".75"/>
     <circle cx="110" cy="110" r="80" fill="none" stroke="url(#gG)" stroke-width="18"/>
     <circle class="arc" cx="110" cy="110" r="80" fill="none" stroke="url(#gB)" stroke-width="18" stroke-linecap="round" stroke-dasharray="{arc:.1f} {C - arc:.1f}" transform="rotate(-90 110 110)"/>
     <circle cx="110" cy="110" r="62" fill="none" stroke="url(#gG)" stroke-width="1" opacity=".6"/>
    </svg>
    <div class="rc"><b class="num foil cu" data-v="{B}">{fmt(B)}</b><span class="un">بطاقة</span></div>
   </div>
   <div class="stats rv">
    <div class="stat"><div class="pl"><div class="lb"><i class="dot a"></i><span>الرزمة الأساسية الشاملة</span></div><div class="nv"><b class="num foil cu" data-v="{B}">{fmt(B)}</b><span class="un2">بطاقة</span></div></div></div>
    <div class="stat"><div class="pl"><div class="lb"><i class="dot b"></i><span>رزمة الكلمات المهمة</span></div><div class="nv"><b class="num sapfoil cu" data-v="{I}">{fmt(I)}</b><span class="un2">بطاقة</span></div></div></div>
   </div>
   <p class="txt rv"><span class="hb">الكلمات المهمة</span> مجموعة مختارة من مفردات <span class="hg">الرزمة الأساسية</span> للتركيز على الكلمات ذات الأهمية في المراجعة؛ أما <span class="hg">الرزمة الأساسية</span> فهي المرجع الأشمل لدراسة المفردات.</p>
   <div class="warn rv"><div class="wi"><span class="ic2"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-warn"/></svg></span><div><b>تنبيه مهم</b>تساعدك الرزمة على حفظ المفردات ومراجعتها، لكنها لا تغني عن الدراسة من الكتاب.</div></div></div>
   <div class="yr rv"><i></i><span>أُعدّت للعام الدراسي <b class="l foil">{YEAR}</b>.</span><i></i></div>
  </section>'''
    return wrap(inner, cls="rep")


def share_links(p):
    url = GALLERY_URL[p["key"]]
    msg = SHARE_MESSAGE.get(p["key"]) or f"رزمة {p['title']} لـ Anki: {url}"
    if url not in msg:
        msg = msg + "\n" + url
    return "https://wa.me/?text=" + quote(msg), "https://t.me/share/url?url=" + quote(url) + "&text=" + quote(msg.replace(url, "").strip())


def card2_back(p):
    adj, adjf = p["adj"], p["adj_f"]
    others = [q for q in PACKS if q["key"] != p["key"]]
    spines = "".join(f'<a class="spine" href="{GALLERY_URL[q["key"]]}">{esc(q["title"])}</a>' for q in others)
    wa, tg = share_links(p)
    inner = f'''<section class="back">
   <section class="rv"><div class="sh"><span class="ic3"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-spk"/></svg></span><h2>الصوت والنطق</h2></div>
    <p>عند ظهور البطاقة، يبدأ الصوت {adj} تلقائيًا. وبعد كشف الإجابة، يُشغَّل الصوت {adj} أولًا، يليه الصوت العربي مباشرةً.</p>
    <p>وتتيح لك أزرار الصوت اختيار طريقة الاستماع المناسبة:</p>
    <div class="modes">
     <div class="mode">{wave("en")}<div><b>{adjf} فقط</b><span class="d">للاستماع إلى نطق الكلمة {adjf}.</span></div></div>
     <div class="mode">{wave("ar")}<div><b>العربية فقط</b><span class="d">للاستماع إلى نطق المقابل العربي.</span></div></div>
     <div class="mode">{wave("both")}<div><b>الصوتان معًا</b><span class="d">للاستماع إلى الكلمة {adjf} أولًا، ثم المقابل العربي.</span></div></div>
    </div>
    <p>يمكنك إعادة تشغيل أيٍّ من الخيارات كلما احتجت إلى ذلك.</p>
    <div class="warn rv" style="margin-top:16px"><div class="wi"><span class="ic2"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-info"/></svg></span><div><b>ملاحظة</b>الصوت مُولَّد آليًا، وقد توجد فيه بعض الأخطاء في اللفظ، كما قد تقع أخطاء في التشكيل العربي. إن لاحظت شيئًا من ذلك فراسلنا لنصحّحه في التحديثات القادمة.</div></div></div></section>
   <div class="dv rv"><i></i></div>
   <section class="rv"><div class="sh"><span class="ic3"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-grid"/></svg></span><h2>معرض الرزمة</h2></div>
    <p>من خلال المعرض، يمكنك تخصيص الرزمة بحسب الخيارات المتاحة، ومنها اختيار القالب والصوت أو اللهجة، وضبط النطق التلقائي، وتعطيل الصوت بالكامل لتقليل حجم الرزمة.</p>
    <div class="btnrow"><a class="cta" href="{GALLERY_URL[p["key"]]}"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-grid"/></svg><span>فتح معرض <span class="l">{esc(p["title"])}</span></span></a></div>
    <p class="small">قد يستغرق فتح المعرض لحظات؛ يُرجى الانتظار قليلًا.</p>
    <p>بعد اختيار الإعدادات المناسبة، يمكنك تنزيل النسخة التي تريدها.</p></section>
   <div class="dv rv"><i></i></div>
   <section class="rv"><div class="sh"><span class="ic3"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-globe"/></svg></span><h2>رزم أخرى</h2></div>
    <p>يمكنك زيارة معارض الرزم الأخرى من خلال الروابط التالية:</p>
    <div class="spines">{spines}</div></section>
   <div class="dv rv"><i></i></div>
   <section class="rv"><div class="sh"><span class="ic3"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-chat"/></svg></span><h2>التواصل والمساعدة</h2></div>
    <p>للاستفسارات المتعلقة بالرزم أو لإرسال ملاحظة بشأن محتواها:</p>
    <a class="btn2" href="{WHATSAPP_CONTACT}"><svg class="ic wa" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-wa"/></svg><span>التواصل عبر <span class="l">WhatsApp</span></span></a>
    <p style="margin-top:14px">وللحصول على المساعدة في استخدام {A} وحل مشكلاته، يمكنك الانضمام إلى مجموعة {A} على <span class="l">Telegram</span>:</p>
    <a class="btn2" href="{TELEGRAM_GROUP}"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-plane"/></svg><span>مجموعة {A} على <span class="l">Telegram</span></span></a></section>
   <div class="dv rv"><i></i></div>
   <section class="rv"><div class="sh"><span class="ic3"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-sprout"/></svg></span><h2>ساهم في نشر الخير</h2></div>
    <div class="note" style="margin-top:4px"><span>انشر الرزمة؛ فالدال على الخير كفاعله.</span></div>
    <a class="btn2" style="margin-top:14px" href="{wa}"><svg class="ic wa" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-wa"/></svg><span>مشاركة عبر <span class="l">WhatsApp</span></span></a>
    <a class="btn2" href="{tg}"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-plane"/></svg><span>مشاركة عبر <span class="l">Telegram</span></span></a></section>
  </section>'''
    return wrap(inner, cls="rep rev", mh=p["title"])


# ── 3) الفهرس ──
def chart_svg(p):
    units = p["units"]
    n = len(units)
    W, H = 324, 170
    bw = 20 if n > 8 else 38
    gap = (W - n * bw) / (n - 1)
    mx = max(u["total"] for u in units)
    base, top = H - 22, 38
    mh = base - top
    s = [f'<svg viewBox="0 0 {W} {H}" aria-hidden="true">',
         f'<line x1="0" y1="{base}" x2="{W}" y2="{base}" stroke="rgba(232,196,107,.4)" stroke-width="1"/>']
    fs_n, fs_t = (10, 8.5) if n > 8 else (12, 11)
    for i, u in enumerate(units):
        x = i * (bw + gap)
        h = u["total"] / mx * mh
        s.append(f'<rect x="{x:.1f}" y="{base - h:.1f}" width="{bw}" height="{h:.1f}" rx="3" fill="url(#gG)" class="col" style="animation-delay:{i * 0.07:.2f}s"/>')
        if u["imp"] is not None:
            hi = min(u["imp"], u["total"]) / u["total"] * h
            s.append(f'<rect x="{x:.1f}" y="{base - hi:.1f}" width="{bw}" height="{hi:.1f}" rx="3" fill="url(#gB)" class="col" style="animation-delay:{i * 0.07 + 0.18:.2f}s"/>')
        s.append(f'<text x="{x + bw / 2:.1f}" y="{H - 6}" text-anchor="middle" font-family="\'Noto Serif\',serif" font-size="{fs_n}" font-weight="700" fill="#a99c75">{u["n"]}</text>')
        s.append(f'<text x="{x + bw / 2:.1f}" y="{base - h - 4:.1f}" text-anchor="middle" font-family="\'Noto Serif\',serif" font-size="{fs_t}" fill="#d8d1bd">{u["total"]}</text>')
    s.append("</svg>")
    return "".join(s)


def card3_front(p):
    has_imp = p["units"][0]["imp"] is not None
    blocks = []
    for u in p["units"]:
        rows = "".join(f'<div class="rw"><i class="dot a"></i><span class="nm" dir="ltr">{esc(nm)}</span><span class="cn"><b>{c}</b> بطاقة</span></div>' for nm, c in u["lessons"])
        blocks.append(f'<div class="ub rv"><div class="hd2"><span class="un">{p["label"]} {u["n"]}</span><span class="tt">إجمالي الوحدة <span class="pill"><b>{u["total"]}</b> بطاقة</span></span></div>{rows}</div>')
    legend = '<span><i class="dot a"></i>الرزمة الأساسية الشاملة</span>' + ('<span><i class="dot b"></i>رزمة الكلمات المهمة</span>' if has_imp else "")
    inner = f'''<section class="front">
   <div class="hdr glow rv"><h1 class="ttl foil sheen">فهرس الرزمة</h1><div class="sub">المفردات الأساسية الشاملة</div></div>
   <div class="chart rv">
    <div class="tot"><span>إجمالي البطاقات</span><span class="pill"><b class="cu" data-v="{p["base"]}">{fmt(p["base"])}</b> بطاقة</span></div>
    {chart_svg(p)}
    <div class="legend">{legend}</div>
   </div>
   {"".join(blocks)}
  </section>'''
    return wrap(inner, cls="rep")


def card3_back(p):
    units = p["units"]
    if units[0]["imp"] is not None:
        mx = max(u["imp"] for u in units)
        rows = "".join(f'<div class="ur"><span class="un">{p["label"]} {u["n"]}</span><div class="bar"><i style="width:{u["imp"] / mx * 100:.1f}%"></i></div><span class="c"><b>{u["imp"]}</b> بطاقة</span></div>' for u in units)
        body = f'<div class="chart rv" style="margin-top:52px;padding-top:52px"><div class="tot"><span>إجمالي البطاقات</span><span class="pill"><b>{fmt(p["imp"])}</b> بطاقة</span></div>{rows}</div>'
    else:
        body = f'<div class="stats rv" style="margin-top:26px"><div class="stat"><div class="pl"><div class="lb"><i class="dot b"></i><span>إجمالي البطاقات</span></div><div class="nv"><b class="num sapfoil cu" data-v="{p["imp"]}">{fmt(p["imp"])}</b><span class="un2">بطاقة</span></div></div></div></div>'
    inner = f'''<section class="back">
   <div class="hdr glow rv"><h1 class="ttl sapfoil">الكلمات المهمة</h1></div>
   {body}
   <div class="note rv"><span>الكلمات المهمة مجموعة منتقاة من مفردات الرزمة الأساسية للتركيز عليها في المراجعة، وليست بديلًا عن الرزمة الأساسية الشاملة.</span></div>
  </section>'''
    return wrap(inner, cls="rep rev", mh=p["title"])


# ── 4) خطة الدراسة ──
def card4_front(p):
    B, I = p["base"], p["imp"]
    paces = [10, 20, 30, 40, 50]
    mx = math.ceil(B / 10) + math.ceil(I / 10)
    rows = []
    for n in paces:
        d1, d2 = math.ceil(B / n), math.ceil(I / n)
        t = d1 + d2
        rows.append(f'<div class="pr"><div class="pn"><b class="num foil">{n}</b><span>بطاقات جديدة يوميًا</span><em><b>{t}</b> يومًا ≈ {t / 30.4:.1f} شهر</em></div>'
                    f'<div class="pbar"><i class="s1" style="width:{d1 / mx * 100:.1f}%"></i><i class="s2" style="width:{d2 / mx * 100:.1f}%"></i></div>'
                    f'<div class="pd"><span><i class="dot a"></i>الأساسية <b>{d1}</b> يومًا</span><span><i class="dot b"></i>المهمة <b>{d2}</b> يومًا</span></div></div>')
    inner = f'''<section class="front">
   <div class="hdr glow rv"><h1 class="ttl foil sheen">خطة الدراسة</h1></div>
   <p class="intro rv">اختر وتيرتك: عدد البطاقات الجديدة يوميًا. ستنتهي من <span class="hg">الرزمة الأساسية</span> ثم من رزمة <span class="hb">الكلمات المهمة</span> في المدة المقابلة.</p>
   <div class="rv">{"".join(rows)}</div>
   <p class="small rv" style="margin-top:14px">الأرقام تقديرية: تفترض الدراسة كل يوم دون انقطاع، وتُضاف المراجعات اليومية فوقها.</p>
  </section>'''
    return wrap(inner, cls="rep")


def card4_back(p):
    inner = f'''<section class="back">
   <div class="hdr glow rv"><h1 class="ttl foil">اضبط {A}</h1></div>
   <p class="intro rv">بعد اختيار وتيرتك، اضبط هذه الخيارات في إعدادات المجموعة (<span class="l">Deck options</span>):</p>
   <div class="rv">
    <div class="tip"><span class="ic3"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-cal"/></svg></span><div><em>New cards/day</em><b>البطاقات الجديدة يوميًا</b><p>اجعلها مساوية للوتيرة التي اخترتها.</p></div></div>
    <div class="tip"><span class="ic3"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-loop"/></svg></span><div><em>Maximum reviews/day</em><b>الحد الأقصى للمراجعات يوميًا</b><p>اجعله كبيرًا (مثل 9999) كي لا تتراكم عليك المراجعات.</p></div></div>
    <div class="tip"><span class="ic3"><svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><use href="#i-hourglass"/></svg></span><div><em>Maximum interval</em><b>الحد الأقصى للفاصل</b><p>اجعله أقل من عدد الأيام المتبقية للامتحان، لتعود إليك البطاقات قبل موعده.</p></div></div>
   </div>
  </section>'''
    return wrap(inner, cls="rep rev", mh=p["title"])


CARDS = [("c1", card1_front, card1_back), ("c2", card2_front, card2_back), ("c3", card3_front, card3_back), ("c4", card4_front, card4_back)]


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    print("التحقق من الأرقام:")
    verify()
    model = genanki.Model(
        1907393001, "Royal Intro",
        fields=[{"name": "Front"}, {"name": "Back"}],
        templates=[{"name": "Card", "qfmt": "{{Front}}" + SCRIPT, "afmt": "{{Back}}" + SCRIPT}],
        css=CSS,
    )
    decks, total = [], 0
    for i, p in enumerate(PACKS):
        deck = genanki.Deck(2459400101 + i, f"{PARENT_DECK}::{p['title']}")
        for cid, ff, bf in CARDS:
            deck.add_note(genanki.Note(model=model, fields=[ff(p), bf(p)],
                                       guid=genanki.guid_for("royal-intro", p["key"], cid), tags=["intro", p["key"]]))
            total += 1
        decks.append(deck)
    out = os.path.join(here, OUTPUT_FILE)
    genanki.Package(decks).write_to_file(out)
    print(f"\n✓ تم إنشاء: {out}")
    print(f"  رزم فرعية: {len(decks)} · بطاقات: {total}")
    print('\nلنسخه إلى التنزيلات:  cp "%s" ~/storage/downloads/' % out)


if __name__ == "__main__":
    main()
