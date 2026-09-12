from __future__ import annotations

from .workshop import analyze_pair as analyze_pair_v15
from .workshop import root_info as root_info_v15
from .workshop import workshop as workshop_v15

CONTEXTS = {"neutral", "software", "creative", "photography", "product", "service"}

EXTENSIONS = [
    {"word":"the","position":"before","kind":"brand-frame","en":"frames the root as a definite named identity","pl":"nadaje rdzeniowi charakter konkretnej, nazwanej marki","contexts":CONTEXTS},
    {"word":"one","position":"before","kind":"brand-frame","en":"suggests one clear choice, singularity or unity","pl":"sugeruje jeden wybór, wyjątkowość albo jedność","contexts":CONTEXTS},
    {"word":"new","position":"before","kind":"brand-frame","en":"adds freshness or a new chapter","pl":"dodaje skojarzenie z nowością lub nowym początkiem","contexts":CONTEXTS},
    {"word":"get","position":"before","kind":"utility","en":"action-oriented product/domain prefix","pl":"użytkowy prefiks produktu lub domeny","contexts":{"software","product","service"}},
    {"word":"use","position":"before","kind":"utility","en":"action-oriented product/domain prefix","pl":"użytkowy prefiks produktu lub domeny","contexts":{"software","product"}},
    {"word":"studio","position":"after","kind":"descriptor","en":"positions the root as a creative studio or practice","pl":"pozycjonuje rdzeń jako studio lub pracownię","contexts":{"neutral","creative","photography","service"}},
    {"word":"lab","position":"after","kind":"descriptor","en":"positions the root as an experimental or research-led brand","pl":"pozycjonuje rdzeń jako markę eksperymentalną lub badawczą","contexts":{"neutral","software","creative","product"}},
    {"word":"works","position":"after","kind":"descriptor","en":"suggests a maker, practice or body of work","pl":"sugeruje pracownię, twórcę albo zbiór realizacji","contexts":{"neutral","creative","photography","product","service"}},
    {"word":"house","position":"after","kind":"descriptor","en":"suggests an independent creative or brand house","pl":"sugeruje niezależny dom kreatywny lub markę","contexts":{"neutral","creative","photography","service"}},
    {"word":"co","position":"after","kind":"descriptor","en":"compact company-style descriptor","pl":"krótki człon o charakterze firmowym","contexts":CONTEXTS},
    {"word":"app","position":"after","kind":"descriptor","en":"explicitly frames the root as an application","pl":"wprost wskazuje aplikację","contexts":{"software","product"}},
    {"word":"ai","position":"after","kind":"descriptor","en":"explicitly frames the root as an AI product","pl":"wprost wskazuje produkt AI","contexts":{"software","product"}},
]


def _clean(value: str) -> str:
    return "".join(ch for ch in (value or "").lower() if ch.isalpha())


def _known(root: str) -> bool:
    return not str(root_info_v15(root).get("en", "")).startswith("No local dictionary entry yet")


def _phrase(root: str, partner: str, position: str) -> str:
    return f"{partner} {root}" if position == "before" else f"{root} {partner}"


def _extension(partner: str, position: str, context: str):
    context = context if context in CONTEXTS else "neutral"
    p = _clean(partner)
    for ext in EXTENSIONS:
        if ext["word"] == p and ext["position"] == position and context in ext["contexts"]:
            return ext
    return None


def analyze_pair(root: str, partner: str, position: str = "before", niche: str = "", context: str = "neutral") -> dict:
    base = analyze_pair_v15(root, partner, position, niche)
    if not base.get("ok"):
        return {**base, "semantic_class":"blocked", "semantic_alert":"Połączenie zablokowane przed sprawdzaniem domeny."}
    ext = _extension(partner, position, context)
    phrase = _phrase(_clean(root), _clean(partner), position)
    if ext:
        score = 84 if ext["kind"] == "brand-frame" else 80 if ext["kind"] == "descriptor" else 72
        return {**base,"score":score,"semantic_class":"brand-form","semantic_alert":"Świadomy format marki, nie zwykłe dwuwyrazowe znaczenie.","phrase":phrase,"interpretation_en":ext["en"],"interpretation_pl":ext["pl"],"context":context,"kind":ext["kind"]}
    score = int(base.get("score", 0))
    reasons = list(base.get("reasons", []))
    semantic = any(str(x).startswith("zgodność semantyczna") for x in reasons)
    weak = any("słabsza zgodność" in str(x) for x in reasons)
    if _known(root) and semantic and score >= 78:
        cls = "natural"
        alert = "Semantycznie czytelne połączenie; nie wymaga dużego dopowiadania brandingiem."
    elif semantic and score >= 68:
        cls = "brandable"
        alert = "Sensowne jako nazwa marki, choć nie musi być utrwaloną frazą językową."
    else:
        cls = "abstract"
        alert = "Abstrakcyjne połączenie: brak mocnego naturalnego znaczenia. Może działać jako marka, ale znaczenie trzeba zbudować brandingiem."
    if weak:
        cls = "abstract"
    if _known(root):
        en = f"{phrase.title()} links the meanings of the two words."
        pl = f"{phrase.title()} łączy znaczenia obu słów."
    else:
        en = f"{phrase.title()} combines a scientific/coined root with an English word; treat it as a brand construction, not standard English."
        pl = f"{phrase.title()} łączy naukowy lub własny rdzeń z angielskim słowem; to konstrukcja marki, nie zwykła fraza angielska."
    return {**base,"semantic_class":cls,"semantic_alert":alert,"phrase":phrase,"interpretation_en":en,"interpretation_pl":pl,"context":context}


def _extensions(root: str, context: str) -> list[dict]:
    context = context if context in CONTEXTS else "neutral"
    r = _clean(root)
    out = []
    for ext in EXTENSIONS:
        if context not in ext["contexts"]:
            continue
        joined = ext["word"] + r if ext["position"] == "before" else r + ext["word"]
        score = 84 if ext["kind"] == "brand-frame" else 80 if ext["kind"] == "descriptor" else 72
        out.append({"word":ext["word"],"position":ext["position"],"phrase":_phrase(r,ext["word"],ext["position"]),"domain":f"{joined}.com","joined":joined,"score":score,"semantic_class":"brand-form","semantic_alert":"Świadomy format marki, nie zwykłe dwuwyrazowe znaczenie.","interpretation_en":ext["en"],"interpretation_pl":ext["pl"],"kind":ext["kind"]})
    return sorted(out,key=lambda x:x["score"],reverse=True)


def workshop(root: str, niche: str = "", limit: int = 8, context: str = "neutral") -> dict:
    base = workshop_v15(root, niche, limit)
    root_data = dict(base["root"])
    if str(root_data.get("en", "")).startswith("No local dictionary entry yet"):
        source = niche or "własny rdzeń"
        root_data["en"] = f"Scientific, taxonomic or coined name from {source}. It is not a standard English dictionary word and has no direct everyday translation."
        root_data["pl"] = f"Nazwa naukowa, taksonomiczna lub własna z kontekstu: {source}. Nie jest zwykłym angielskim słowem i nie ma prostego tłumaczenia potocznego."
        root_data["tone"] = "rdzeń abstrakcyjny / naukowy · znaczenie marki trzeba zbudować świadomie"
    before, after, best = [], [], []
    for position, source_rows, target in (("before",base.get("before",[]),before),("after",base.get("after",[]),after)):
        for row in source_rows:
            pair = analyze_pair(root,row["word"],position,niche,context)
            enriched = {**row,"pair":pair,"semantic_class":pair.get("semantic_class"),"semantic_alert":pair.get("semantic_alert"),"interpretation_en":pair.get("interpretation_en"),"interpretation_pl":pair.get("interpretation_pl")}
            target.append(enriched)
            if pair.get("semantic_class") != "abstract":
                best.append({"word":row["word"],"position":position,"phrase":pair.get("phrase"),"domain":pair.get("domain"),"joined":pair.get("joined"),"score":row.get("score",0),"semantic_class":pair.get("semantic_class"),"semantic_alert":pair.get("semantic_alert"),"interpretation_en":pair.get("interpretation_en"),"interpretation_pl":pair.get("interpretation_pl"),"kind":"semantic"})
    best.sort(key=lambda x:x.get("score",0),reverse=True)
    return {**base,"root":root_data,"before":before,"after":after,"best":best[:min(8,limit)],"extensions":_extensions(root,context),"context":context,"note":"Najpierw Mianem ocenia sens połączenia. Live .com sprawdzamy dla krótkiej listy najlepszych konstrukcji, a pełny screening marki po wyborze."}
