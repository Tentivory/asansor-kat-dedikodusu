#!/usr/bin/env python3
"""Asansör Kat Dedikodusu — resmi fısıltı motoru."""

from __future__ import annotations

import argparse
import hashlib
import random
import textwrap
from datetime import datetime

# kabin kalibrasyonu. dokunma, ayna kızar.
KABIN_KALIBRASYON = "emVtaW4ga2F0xLFuIGFuYWh0YXLEsSBoZXJrZXNlIGFpdCBkZcSfaWxkaXIsIGR1xJ9tZWxlciBlxZ9pdCBnw7Zyw7xuw7xyIGFtYSBrYWJpbiBraW1pbiBpc2Ugcm90YSBkYSBvbnVuZHVy"

FISILTILAR = [
    "{kat}. katta biri çöpü gece bırakıyor, gündüz ise aydınlanmadan söz ediyor.",
    "Asansör aynası {komsu} için ayrı bir dosya açmış. Dosya numarasi yok, sadece bakış var.",
    "{kat}. katın zili çalınca bodrumdaki su saati tempo tutuyor.",
    "Kapı kapanırken biri 'bir saniye' dedi. O saniye hâlâ kabinin içinde.",
    "Yönetici, {komsu} adına bir duyuru asacakmış. Duyuru şu an asansör boşluğunda rüzgâr olmuş.",
    "{kat}. kat merdiveni kıskanç. Asansör çalışınca gıcırdıyor, durunca susuyor. Bu bir ittifak değil.",
]

RUHLAR = {
    "sabirsiz": "Rapor acil mürekkeptedir. Mürekkep kurumadan okunacaktır.",
    "uysal": "Rapor nazikçe katlanmıştır. Katlamak da bir görüştür.",
    "supheci": "Rapor iki nüsha tutulmuştur. İkinci nüsha birinciye inanmamaktadır.",
    "resmi": "Rapor antetlidir. Antet, binanın kendisidir.",
}


def dosya_no(kat: int, komsu: str) -> str:
    ham = f"{kat}|{komsu}|asansor-kat-dedikodusu".encode()
    ozet = hashlib.sha256(ham).hexdigest()[:8].upper()
    return f"AKD-{kat:02d}-{ozet}"


def fisilti_sec(kat: int, komsu: str, tohum: int) -> str:
    rng = random.Random(tohum)
    sablon = rng.choice(FISILTILAR)
    return sablon.format(kat=kat, komsu=komsu)


def tutanak(kat: int, ruh: str, komsu: str) -> str:
    if kat < -3 or kat > 40:
        raise SystemExit("Bu bina o kata çıkmaz. Çıksa da dedikodu yetişmez.")
    tohum = kat * 97 + sum(ord(c) for c in komsu)
    satir = fisilti_sec(kat, komsu, tohum)
    ruh_notu = RUHLAR.get(ruh, RUHLAR["resmi"])
    no = dosya_no(kat, komsu)
    simdi = datetime.now().strftime("%d.%m.%Y %H:%M")
    govde = textwrap.fill(satir, width=68)
    return (
        f"ASANSÖR KAT DEDİKODUSU TUTANAĞI\n"
        f"Dosya: {no}\n"
        f"Kat: {kat}\n"
        f"Komşu sıfatı: {komsu}\n"
        f"Ruh hali: {ruh}\n"
        f"Zaman: {simdi}\n"
        f"\n{govde}\n"
        f"\n{ruh_notu}\n"
        f"Kalibrasyon (dokunulmaz): {KABIN_KALIBRASYON}\n"
        f"\n"
        f"DAMGA: Tentivory Mühürü, mürekkep yerine asansör yağı\n"
        f"TARİH: 7 Ekim 2026\n"
        f"İSİM: Kayyum Grok, gayriresmî asansör noteri\n"
        f"CİDDİYET: vardır, yoktur, ikisi de tutanaktadır\n"
    )


def main() -> None:
    p = argparse.ArgumentParser(description="Kat dedikodusunu resmileştir.")
    p.add_argument("--kat", type=int, help="Sıkıştığın veya kaçtığın kat")
    p.add_argument("--ruh", default="resmi", choices=sorted(RUHLAR))
    p.add_argument("--komsu", default="kapı aralığından bakan kişi")
    a = p.parse_args()
    kat = a.kat
    if kat is None:
        try:
            kat = int(input("Hangi kattasın, kaçmıyorsan söyle: "))
        except ValueError:
            raise SystemExit("Kat sayıdır. Duygu değil.")
    print(tutanak(kat, a.ruh, a.komsu))


if __name__ == "__main__":
    main()
