#!/usr/bin/env python3
"""Snapshots the game content the site shows into data/game.json, from a checkout of the game repository.

    python3 tools/export_content.py ../kilkule

The site never invents a game number: names, rules, counts and accents come from the game's own content files
(Packages/KilkuleContent/.../Data/*.json, English from l10n/en.json). Run it again when the game content changes,
then `python3 build.py`. The art under assets/art is copied from kule-savunma/svg-varliklar/kutuphane in the same
repository; this script checks that every unit it names has its drawing there.
"""
import json, pathlib, sys, unicodedata

SITE = pathlib.Path(__file__).resolve().parent.parent
ART = SITE / "assets" / "art"

def slug(name):
    """'Kaya Yuvarlayıcı' → 'kaya-yuvarlayici', the file naming of the game's SVG library."""
    s = name.lower().replace("ı", "i").replace("ş", "s").replace("ğ", "g").replace("ç", "c").replace("ö", "o").replace("ü", "u")
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return "-".join("".join(c if c.isalnum() else " " for c in s).split())

def main(repo):
    data = repo / "Packages/KilkuleContent/Sources/KilkuleContent/Data"
    load = lambda name: json.loads((data / name).read_text())
    en = load("l10n/en.json")
    skills = {s["id"]: s for s in load("towerSkills.json")}
    bosses = {b["packId"]: b for b in load("bosses.json")}
    rules = {r["id"]: r for r in load("rules.json")}
    defenses = load("defenses.json")
    missing = []

    def art(pack, kind, name):
        rel = f"{pack}/{kind}-{slug(name)}.svg"
        if not (ART / rel).exists():
            missing.append(rel)
        return rel

    def skill(pack):
        s = skills[f"{pack}.skill"]
        return {"tr": {"name": s["name"], "text": s["text"]},
                "en": {"name": en[f"towerSkills.{pack}.skill.name"], "text": en[f"towerSkills.{pack}.skill.text"]},
                "seconds": s["chargeTicks"] // 30}

    def units(pack, group, kind, names):
        return [{"tr": n, "en": en[f"{group}.{pack}.{kind}.{i}"], "art": art(pack, "savunma" if kind == "defenses" else "dusman", n)}
                for i, n in enumerate(names)]

    def boss(pack, group, name):
        b = bosses[pack]
        return {"tr": {"name": name, "text": b["ruleText"]},
                "en": {"name": en[f"bosses.{pack}.boss.name"], "text": en[f"bosses.{pack}.boss.ruleText"]},
                "art": art(pack, "boss", name)}

    ages = []
    for a in load("ages.json"):
        p = a["id"]
        ages.append({
            "id": p, "index": a["index"], "levels": a["levels"], "accent": a["accent"],
            "tr": {"name": a["name"], "short": a["shortName"], "rule": a["ruleIntro"], "stages": a["towerStages"]},
            "en": {"name": en[f"ages.{p}.name"], "short": en[f"ages.{p}.shortName"], "rule": en[f"ages.{p}.ruleIntro"],
                   "stages": [en[f"ages.{p}.towerStages.{i}"] for i in range(3)]},
            "towers": [art(p, "kule", f"asama {i}") for i in (1, 2, 3)],
            "defenses": units(p, "ages", "defenses", a["defenses"]),
            "enemies": units(p, "ages", "enemies", a["enemies"]),
            "boss": boss(p, "ages", a["boss"]),
            "skill": skill(p),
        })
    realms = []
    for r in load("realms.json"):
        p = r["id"]
        realms.append({
            "id": p, "index": r["index"], "levels": r["levels"], "accent": r["accent"],
            "tr": {"name": r["name"], "short": r["shortName"], "guardian": r["guardian"], "grace": r["grace"], "tower": r["tower"],
                   "rule": r["rule"], "ruleIntro": r["ruleIntro"]},
            "en": {k: en[f"realms.{p}.{f}"] for k, f in (("name", "name"), ("short", "shortName"), ("guardian", "guardian"),
                   ("grace", "grace"), ("tower", "tower"), ("rule", "rule"), ("ruleIntro", "ruleIntro"))},
            "guardianArt": art(p, "koruyucu", r["guardian"]),
            "towerArt": art(p, "kule", r["tower"]),
            "defenses": units(p, "realms", "defenses", r["defenses"]),
            "enemies": units(p, "realms", "enemies", r["enemies"]),
            "boss": boss(p, "realms", r["boss"]["name"]),
            "skill": skill(p),
        })
    meta = load("meta.json")
    league = meta["weeklyLeague"]
    levels = load("levels.json")
    level_list = levels if isinstance(levels, list) else next(v for v in levels.values() if isinstance(v, list))
    cosmetics = load("cosmetics.json")
    cosmetic_list = cosmetics if isinstance(cosmetics, list) else next(v for v in cosmetics.values() if isinstance(v, list))
    season = load("season.json")
    out = {
        "source": "kilkule · Packages/KilkuleContent/Sources/KilkuleContent/Data",
        "counts": {"levels": len(level_list), "ages": len(ages), "realms": len(realms), "defenses": len(defenses),
                   "bosses": len(bosses), "sectors": len(load("sectors.json")), "cosmetics": len(cosmetic_list),
                   "skills": len(skills)},
        "ages": ages, "realms": realms,
        "league": {"groupSize": league["groupSize"], "promote": league["promote"], "demote": league["demote"],
                   "tiers": [{"tr": t["name"], "en": en[f"meta.weeklyLeague.tiers.{i}.name"]} for i, t in enumerate(league["tiers"])]},
        "endless": {"waves": meta["endless"]["wavesPerSector"], "rootNodes": meta["endless"]["rootTree"]["nodes"],
                    "depthGroup": meta["depthLeague"]["groupSize"]},
        "season": {"tr": season["name"], "en": en["season.name"], "tiers": season["tiers"]},
        "damage": {"pierce": {"tr": "Delici", "en": "Piercing"}, "blast": {"tr": "Patlama", "en": "Blast"},
                   "energy": {"tr": "Enerji", "en": "Energy"}},
        "matrix": load("economy.json")["damageMatrix"],
    }
    if missing:
        raise SystemExit("art missing under assets/art: " + ", ".join(missing))
    (SITE / "data").mkdir(exist_ok=True)
    (SITE / "data" / "game.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
    print("data/game.json:", out["counts"])

if __name__ == "__main__":
    main(pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "../kilkule").resolve())
