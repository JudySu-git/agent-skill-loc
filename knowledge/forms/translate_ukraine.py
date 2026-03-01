#!/usr/bin/env python3
"""
Translate the 'en' column of formId_47192 (Ukraine) to Ukrainian.
All other columns are kept unchanged. Overwrites the original file.
"""

import csv
import io
import os

INPUT_FILE = os.path.join(os.path.dirname(__file__), "formId_47192_en_20260223_165924.csv")

# Map original English 'en' values -> Ukrainian translation
# Key: exact original string; Value: Ukrainian translation
TRANSLATIONS = {

    # ── Question group ──────────────────────────────────────────────────────
    "Avetta PQF - Ukraine Company Information":
        "Avetta PQF - Інформація про компанію в Україні",

    # ── Business entity type description ───────────────────────────────────
    "[Ukraine Civil Code Article 81. Types of Legal Entities  No. 3262-VI]"
    "(https://zakon.rada.gov.ua/laws/show/435-15#Text)":
        "[Цивільний кодекс України, стаття 81. Види юридичних осіб № 3262-VI]"
        "(https://zakon.rada.gov.ua/laws/show/435-15#Text)",

    # ── Business entity questionText ────────────────────────────────────────
    "Please indicate your company's business entity / form of business within Ukraine.":
        "Будь ласка, вкажіть організаційно-правову форму / форму ведення бізнесу вашої компанії в Україні.",

    # ── Business entity response options ───────────────────────────────────
    "Limited Liability Company (ТОВ/TOV/LLC)":
        "Товариство з обмеженою відповідальністю (ТОВ)",
    "Other":
        "Інше",
    "Representative Office":
        "Представництво",
    "Joint Stock Company (АT/JSC)":
        "Акціонерне товариство (АТ)",
    "Sole Proprietorship":
        "Фізична особа-підприємець (ФОП)",

    # ── "If Other" questionText ─────────────────────────────────────────────
    "If Other, please explain.":
        "Якщо інше, будь ласка, поясніть.",

    # ── EDRPOU / TIN / KVED / USR / VAT description ────────────────────────
    (
        "EDPROU is an 8-digit numeric code uniquely assigned to every legal entity registered in Ukraine. "
        "[Unified State Register of Enterprises and Organizations of Ukraine (USREOU/EDRPOU)]"
        "(https://www.lv.ukrstat.gov.ua/eng/edrpoy.php). You can find your EDPROU on the "
        "[Ukraine Ministry of Justice Portal](https://usr.minjust.gov.ua/ua/freesearch).\n<br/>\n\n"
        "The Ukraine Tax Identification Number (TIN/RNOKPP) is a unique code assigned for tax reporting. "
        "For most legal entities, the RNOKPP is identical to the EDRPOU. For sole proprietors, it's a distinct "
        "10- or 12-digit code assigned by the [State Tax Service]"
        "(https://www.oecd.org/content/dam/oecd/en/topics/policy-issue-focus/aeoi/ukraine-tin.pdf). "
        "It can be accessed on the [Unified State Register Portal](https://usr.minjust.gov.ua/ua/freesearch).\n\n"
        "<br/>\nKVED Industry Classification Code is the official business activity code under the "
        "\"Classifier of Types of Economic Activity (KVED)\" system. The codes are listed in the "
        "[Unified State Register](https://stat.gov.ua/en/codelists) and can be checked via the State Statistics "
        "Service KVED directory or company registration extract.\n<br/>\n"
        "The USR extract is an official certified statement from the Unified State Register, containing up-to-date "
        "data on a legal entity. The USR extract is obtained directly from the Ministry of Justice's Unified State "
        "Register portal or via the [\"Diia\"](https://diia.gov.ua/) government service portal.\n\n<br/>\n\n"
        "VAT Registration Number is a unique registration number confirming a company's VAT payer status. "
        "The company VAT number can be accessed at the "
        "[State Tax Service of Ukraine's public VAT register](https://cabinet.tax.gov.ua/registers).\n\n<br/>\n\n"
        "The [VAT Registration Certificate](https://tax.gov.ua/en/new-about-taxes--news-/858814.html) is the "
        "official document/certificate issued by the State Tax Service attesting that the company is registered "
        "as a VAT payer.\n\n\n"
    ): (
        "ЄДРПОУ — 8-значний числовий код, унікально присвоєний кожній юридичній особі, зареєстрованій в Україні. "
        "[Єдиний державний реєстр підприємств та організацій України (ЄДРПОУ)]"
        "(https://www.lv.ukrstat.gov.ua/eng/edrpoy.php). Ви можете знайти свій ЄДРПОУ на "
        "[Порталі Міністерства юстиції України](https://usr.minjust.gov.ua/ua/freesearch).\n<br/>\n\n"
        "РНОКПП (реєстраційний номер облікової картки платника податків) — унікальний код, присвоєний для цілей "
        "податкової звітності. Для більшості юридичних осіб РНОКПП збігається з ЄДРПОУ. Для ФОП це окремий "
        "10- або 12-значний код, присвоєний [Державною податковою службою]"
        "(https://www.oecd.org/content/dam/oecd/en/topics/policy-issue-focus/aeoi/ukraine-tin.pdf). "
        "Його можна перевірити на [Порталі Єдиного державного реєстру](https://usr.minjust.gov.ua/ua/freesearch).\n\n"
        "<br/>\nКод виду економічної діяльності (КВЕД) — офіційний код господарської діяльності відповідно до "
        "системи «Класифікатор видів економічної діяльності (КВЕД)». Коди наведені в "
        "[Єдиному державному реєстрі](https://stat.gov.ua/en/codelists) та можуть бути перевірені через довідник "
        "КВЕД Державної служби статистики або витяг з реєстру компанії.\n<br/>\n"
        "Витяг з ЄДР — офіційна завірена довідка з Єдиного державного реєстру, що містить актуальні дані про "
        "юридичну особу. Витяг з ЄДР отримується безпосередньо через портал Єдиного державного реєстру "
        "Міністерства юстиції або через державний сервіс [«Дія»](https://diia.gov.ua/).\n\n<br/>\n\n"
        "Номер реєстрації платника ПДВ — унікальний реєстраційний номер, що підтверджує статус компанії як "
        "платника ПДВ. Номер ПДВ компанії можна перевірити в "
        "[публічному реєстрі платників ПДВ Державної податкової служби України](https://cabinet.tax.gov.ua/registers).\n\n<br/>\n\n"
        "[Свідоцтво про реєстрацію платника ПДВ](https://tax.gov.ua/en/new-about-taxes--news-/858814.html) — "
        "офіційний документ/сертифікат, виданий Державною податковою службою, що засвідчує реєстрацію компанії "
        "як платника ПДВ.\n\n\n"
    ),

    # ── Proof checklist questionText ────────────────────────────────────────
    (
        "Check the box next to the item(s) that you will provide as proof of a business entity in Ukraine. \n\n"
        "For each item you check, you will be asked to provide a registration number and upload supporting "
        "documents in follow-up questions. \n\nIf you leave any items unchecked, please also select the option: "
        "\"The company is not required to provide proof for any of the unchecked items above and will submit an "
        "explanation for each,\" in addition to the items you did check."
    ): (
        "Позначте поле поряд із пунктом (пунктами), які ви надасте як підтвердження реєстрації юридичної особи "
        "в Україні. \n\nДля кожного позначеного пункту вас попросять надати реєстраційний номер та завантажити "
        "підтверджувальні документи у наступних питаннях. \n\nЯкщо ви залишите будь-які пункти непозначеними, "
        "будь ласка, також виберіть опцію: \"Компанія не зобов'язана надавати підтвердження для жодного з "
        "незазначених пунктів вище та надасть пояснення для кожного,\" на додаток до позначених вами пунктів."
    ),

    # ── Proof checklist response options ───────────────────────────────────
    "EDRPOU":                   "ЄДРПОУ",
    "VAT Registration Certificate": "Свідоцтво про реєстрацію платника ПДВ",
    "USR extract":              "Витяг з ЄДР",
    "KVED":                     "КВЕД",
    "RNOKPP/TIN":               "РНОКПП/ІПН",
    "VAT Registration Number":  "Номер реєстрації платника ПДВ",
    (
        "The company is not required to provide proof for any of the unchecked items above and will submit "
        "an explanation for each."
    ): (
        "Компанія не зобов'язана надавати підтвердження для жодного з незазначених пунктів вище та надасть "
        "пояснення для кожного."
    ),

    # ── Exemptions description ──────────────────────────────────────────────
    (
        "EDPROU code valid exemptions: The EDRPOU code is required for all resident legal entities and "
        "organizations in Ukraine. However, individuals (including sole proprietors/FOPs) do NOT receive an "
        "EDRPOU code. They are registered individually with the State Tax Service and identified by the RNOKPP "
        "(personal taxpayer number). [Order No. 499, Ukraine State Statistics Service]"
        "(https://zakon.rada.gov.ua/laws/show/499-95-%D0%BF) \n\n<br/>\n\n"
        "RNKOPPP/TIN valid exemptions- Legal entities use the EDRPOU as their official TIN; only individuals "
        "and sole proprietors need the RNOKPP. Foreign legal entities with no permanent establishment may not "
        "have RNOKPP unless required by specific operations. "
        "[Tax Code of Ukraine, Article 70](https://zakon.rada.gov.ua/laws/show/2755-17)\n\n<br/>\n\n"
        "KVED valid exemptions- Entities conducting business in Ukraine must be registered and assigned at least "
        "one KVED code, except for foreign representative offices that do not conduct business activities "
        "directly in Ukraine (such as purely liaison offices). "
        "[Cabinet of Ministers Resolution No. 1439 (2010), Article 4]"
        "(https://zakon.rada.gov.ua/laws/show/1439-2010-%D0%BF ), "
        "[Law on State Registration No. 755-IV.](https://zakon.rada.gov.ua/laws/show/755-15) \n\n<br/>\n\n"
        "USR Extract valid exemption: While almost all business activity requires state registration, foreign "
        "companies without permanent establishment and non-resident representative offices may be exempt from "
        "USR registration (and thus do not receive USR extracts). Registration in the USR is only required for "
        "entities carrying out economic activities on Ukrainian territory. "
        "[Law of Ukraine \"On State Registration of Legal Entities, Individual Entrepreneurs and Public "
        "Organizations,\" No. 755-IV, Article 2, 4.]"
        "(https://zakon.rada.gov.ua/laws/show/755-15)\n\n<br/>\n\n"
        "VAT Registration Number and Certificate valid exemptions- Not all companies are VAT payers: Companies "
        "and sole proprietors whose annual taxable supplies do NOT exceed UAH1,000,000 are not required to "
        "register for VAT and thus do not receive a VAT registration number or certificate. Certain entities "
        "(e.g., non-profits, public organizations, agricultural producers, and Unified tax regime payers) may "
        "also be exempt from VAT registration requirements as per Article 181 and 183 of the "
        "[Tax Code of Ukraine](https://tax.gov.ua/en/new-about-taxes--hotlines-/print-785260.html). "
        "During martial law, additional exemptions apply to public and charitable organizations. "
        "[Tax Code of Ukraine, Articles 181, 183, 197]"
        "(https://tax.gov.ua/en/new-about-taxes--news-/858814.html)."
    ): (
        "Дійсні винятки для коду ЄДРПОУ: Код ЄДРПОУ є обов'язковим для всіх резидентних юридичних осіб та "
        "організацій в Україні. Однак фізичні особи (включаючи ФОП) НЕ отримують код ЄДРПОУ. Вони "
        "реєструються індивідуально в Державній податковій службі та ідентифікуються за РНОКПП (особистий "
        "номер платника податків). [Наказ № 499, Державна служба статистики України]"
        "(https://zakon.rada.gov.ua/laws/show/499-95-%D0%BF) \n\n<br/>\n\n"
        "Дійсні винятки для РНОКПП/ІПН: Юридичні особи використовують ЄДРПОУ як свій офіційний "
        "ідентифікаційний номер платника податків; лише фізичні особи та ФОП потребують РНОКПП. Іноземні "
        "юридичні особи без постійного представництва можуть не мати РНОКПП, якщо це не вимагається "
        "конкретними операціями. "
        "[Податковий кодекс України, стаття 70](https://zakon.rada.gov.ua/laws/show/2755-17)\n\n<br/>\n\n"
        "Дійсні винятки для КВЕД: Суб'єкти господарювання в Україні повинні бути зареєстровані та мати "
        "принаймні один код КВЕД, за винятком іноземних представництв, що не здійснюють безпосередньо "
        "господарської діяльності в Україні (наприклад, суто представницькі офіси). "
        "[Постанова Кабінету Міністрів № 1439 (2010), стаття 4]"
        "(https://zakon.rada.gov.ua/laws/show/1439-2010-%D0%BF ), "
        "[Закон про державну реєстрацію № 755-IV.](https://zakon.rada.gov.ua/laws/show/755-15) \n\n<br/>\n\n"
        "Дійсний виняток для витягу з ЄДР: Хоча майже вся господарська діяльність потребує державної "
        "реєстрації, іноземні компанії без постійного представництва та нерезидентні представництва можуть "
        "бути звільнені від реєстрації в ЄДР (і, відповідно, не отримують витягів з ЄДР). Реєстрація в ЄДР "
        "є обов'язковою лише для суб'єктів, які провадять господарську діяльність на території України. "
        "[Закон України «Про державну реєстрацію юридичних осіб, фізичних осіб-підприємців та громадських "
        "формувань», № 755-IV, статті 2, 4.]"
        "(https://zakon.rada.gov.ua/laws/show/755-15)\n\n<br/>\n\n"
        "Дійсні винятки для номера та свідоцтва реєстрації платника ПДВ: Не всі компанії є платниками ПДВ: "
        "компанії та ФОП, річний обсяг оподатковуваних постачань яких НЕ перевищує 1 000 000 грн, не "
        "зобов'язані реєструватися платниками ПДВ і, відповідно, не отримують номера чи свідоцтва про "
        "реєстрацію платника ПДВ. Певні суб'єкти (наприклад, неприбуткові організації, громадські організації, "
        "сільськогосподарські виробники та платники єдиного податку) також можуть бути звільнені від вимог "
        "реєстрації платника ПДВ відповідно до статей 181 та 183 "
        "[Податкового кодексу України](https://tax.gov.ua/en/new-about-taxes--hotlines-/print-785260.html). "
        "Під час воєнного стану додаткові винятки застосовуються до громадських та благодійних організацій. "
        "[Податковий кодекс України, статті 181, 183, 197]"
        "(https://tax.gov.ua/en/new-about-taxes--news-/858814.html)."
    ),

    # ── Exemption reason questionText ───────────────────────────────────────
    "For those items unchecked, provide the reason(s) that you do not have this information.":
        "Для незазначених пунктів вкажіть причини, через які ця інформація відсутня.",

    # ── Follow-up questionTexts ─────────────────────────────────────────────
    "Please provide your company's EDRPOU.":
        "Будь ласка, надайте код ЄДРПОУ вашої компанії.",
    "Please provide your company's Tax Identification Number (RNOKPP).":
        "Будь ласка, надайте РНОКПП вашої компанії (реєстраційний номер облікової картки платника податків).",
    "Please provide your company's KVED Industry Classification Code.":
        "Будь ласка, надайте код КВЕД (вид економічної діяльності) вашої компанії.",
    "Please upload your company's USR extract.":
        "Будь ласка, завантажте виписку з ЄДР вашої компанії.",
    "Please provide your company's VAT Registration Number.":
        "Будь ласка, надайте номер реєстрації платника ПДВ вашої компанії.",
    "Please upload your company's VAT Registration Certificate.":
        "Будь ласка, завантажте свідоцтво про реєстрацію платника ПДВ вашої компанії.",
}


def translate(text):
    return TRANSLATIONS.get(text, text)  # return original if no translation found


def main():
    # Read
    with open(INPUT_FILE, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    # Translate 'en' column only
    for row in rows:
        row["en"] = translate(row["en"])

    # Write back (utf-8, no BOM)
    with open(INPUT_FILE, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(rows)

    translated = sum(1 for r in rows if r["en"] != rows[0]["en"])  # rough count
    print(f"Done. Translated {len(rows)} rows in {os.path.basename(INPUT_FILE)}")


if __name__ == "__main__":
    main()
