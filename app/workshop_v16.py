from __future__ import annotations

from .workshop import analyze_pair as analyze_pair_v15
from .workshop import root_info as root_info_v15
from .workshop import workshop as workshop_v15

CONTEXTS = {"neutral", "software", "creative", "photography", "product", "service"}

FAMILY_META = {
    "semantic-context": {
        "label": "Kierunki dla kontekstu",
        "description": "Słowa dobrane do tego, co nazywasz — znaczenie przed dostępnością domeny.",
        "order": 10,
    },
    "brand-frame": {
        "label": "Forma marki",
        "description": "Krótkie ramy marki typu The / One / New.",
        "order": 20,
    },
    "relation": {
        "label": "Relacja / przyimek",
        "description": "Konstrukcje typu By / With / From — tylko tam, gdzie relacja ma jasny sens.",
        "order": 30,
    },
    "action": {
        "label": "Akcja / produkt",
        "description": "Konstrukcje produktowe i CTA, np. Get / Use / Ask.",
        "order": 40,
    },
    "contact": {
        "label": "Kontakt / komunikacja",
        "description": "Formy konwersacyjne, np. Hello / Hey / Ask.",
        "order": 50,
    },
    "possessive": {
        "label": "Przynależność",
        "description": "My / Our / Your — tylko gdy model marki faktycznie to uzasadnia.",
        "order": 60,
    },
    "descriptor": {
        "label": "Deskryptor po rdzeniu",
        "description": "Lab / Studio / Works / App itd. — opisują typ marki lub produktu.",
        "order": 70,
    },
}


def _scores(default: int, **kwargs: int) -> dict[str, int]:
    return {"default": default, **kwargs}


# Curated naming constructions. Scores express linguistic/brand fit BEFORE domain availability.
CONSTRUCTIONS = [
    # Context-semantic directions. These help deepen a sparse shortlist without lowering quality.
    {"word":"signal","position":"after","family":"semantic-context","kind":"context-semantic","contexts":{"software","product"},"scores":_scores(84,software=93,product=88),"en":"{root} Signal suggests communication, detection or a live stream of information.","pl":"{root} Signal sugeruje komunikację, wykrywanie albo bieżący strumień informacji.","tone":"techniczny · komunikacyjny · dynamiczny","semantic_class":"brandable"},
    {"word":"pulse","position":"after","family":"semantic-context","kind":"context-semantic","contexts":{"software","product","service"},"scores":_scores(82,software=91,product=88,service=82),"en":"{root} Pulse suggests live status, rhythm, monitoring or a current signal.","pl":"{root} Pulse sugeruje bieżący status, rytm, monitoring albo aktualny sygnał.","tone":"żywy · aktualny · monitorujący","semantic_class":"brandable"},
    {"word":"flow","position":"after","family":"semantic-context","kind":"context-semantic","contexts":{"software","product","creative","service"},"scores":_scores(84,software=90,product=90,creative=86,service=88),"en":"{root} Flow suggests a smooth process, workflow or continuous movement.","pl":"{root} Flow sugeruje płynny proces, workflow albo ciągły przepływ.","tone":"płynny · procesowy · nowoczesny","semantic_class":"brandable"},
    {"word":"core","position":"after","family":"semantic-context","kind":"context-semantic","contexts":{"software","product"},"scores":_scores(82,software=90,product=87),"en":"{root} Core positions the root as the central or foundational part of a system.","pl":"{root} Core pozycjonuje rdzeń jako centralną albo podstawową część systemu.","tone":"techniczny · centralny · solidny","semantic_class":"brandable"},
    {"word":"loop","position":"after","family":"semantic-context","kind":"context-semantic","contexts":{"software","product"},"scores":_scores(80,software=88,product=86),"en":"{root} Loop suggests continuity, feedback or a repeating digital process.","pl":"{root} Loop sugeruje ciągłość, pętlę informacji zwrotnej albo powtarzalny proces cyfrowy.","tone":"cyfrowy · ciągły · systemowy","semantic_class":"brandable"},
    {"word":"spark","position":"after","family":"semantic-context","kind":"context-semantic","contexts":{"software","product","creative"},"scores":_scores(80,software=84,product=86,creative=91),"en":"{root} Spark suggests ignition, an idea, activation or a creative starting point.","pl":"{root} Spark sugeruje iskrę, pomysł, uruchomienie albo kreatywny punkt startu.","tone":"energetyczny · kreatywny · inicjujący","semantic_class":"brandable"},
    {"word":"echo","position":"after","family":"semantic-context","kind":"context-semantic","contexts":{"software","creative","service"},"scores":_scores(80,software=85,creative=88,service=83),"en":"{root} Echo suggests response, feedback, resonance or something that carries further.","pl":"{root} Echo sugeruje odpowiedź, feedback, rezonans albo coś, co niesie się dalej.","tone":"komunikacyjny · rezonujący · lekki","semantic_class":"brandable"},
    {"word":"cloud","position":"after","family":"semantic-context","kind":"context-semantic","contexts":{"software","product"},"scores":_scores(78,software=87,product=84),"en":"{root} Cloud clearly suggests an online or cloud-based software service.","pl":"{root} Cloud jasno sugeruje usługę online albo oprogramowanie działające w chmurze.","tone":"techniczny · usługowy · cyfrowy","semantic_class":"brandable"},
    {"word":"node","position":"after","family":"semantic-context","kind":"context-semantic","contexts":{"software","product"},"scores":_scores(78,software=86,product=82),"en":"{root} Node suggests a connected technical unit inside a network or system.","pl":"{root} Node sugeruje połączony element techniczny w sieci albo systemie.","tone":"techniczny · sieciowy · modularny","semantic_class":"brandable"},
    {"word":"frame","position":"after","family":"semantic-context","kind":"context-semantic","contexts":{"creative","photography"},"scores":_scores(84,creative=88,photography=94),"en":"{root} Frame suggests visual composition, a boundary or a photographic frame.","pl":"{root} Frame sugeruje kompozycję wizualną, ramę albo kadr fotograficzny.","tone":"wizualny · uporządkowany · fotograficzny","semantic_class":"brandable"},
    {"word":"form","position":"after","family":"semantic-context","kind":"context-semantic","contexts":{"creative","product"},"scores":_scores(82,creative=92,product=84),"en":"{root} Form suggests shape, structure and deliberate design.","pl":"{root} Form sugeruje kształt, strukturę i świadome projektowanie.","tone":"projektowy · strukturalny · czysty","semantic_class":"brandable"},
    {"word":"mark","position":"after","family":"semantic-context","kind":"context-semantic","contexts":{"creative","service"},"scores":_scores(80,creative=88,service=82),"en":"{root} Mark suggests a distinctive sign, identity or signature.","pl":"{root} Mark sugeruje charakterystyczny znak, identyfikację albo podpis.","tone":"brandowy · graficzny · wyrazisty","semantic_class":"brandable"},

    # Brand frames.
    {"word":"the","position":"before","family":"brand-frame","kind":"brand-frame","contexts":CONTEXTS,"scores":_scores(82,neutral=88,creative=86,photography=84),"en":"The {root} presents the root as a definite, named identity — the specific brand called {root}.","pl":"The {root} przedstawia rdzeń jako konkretną, nazwaną tożsamość — tę markę o nazwie {root}.","tone":"pewny · editorial · markowy","semantic_class":"brand-form"},
    {"word":"one","position":"before","family":"brand-frame","kind":"brand-frame","contexts":CONTEXTS,"scores":_scores(80,neutral=84,software=82,product=88),"en":"One {root} suggests one clear choice, singularity or a unified product/brand.","pl":"One {root} sugeruje jeden wyraźny wybór, wyjątkowość albo jedną spójną markę/produkt.","tone":"prosty · jednoznaczny · produktowy","semantic_class":"brand-form"},
    {"word":"new","position":"before","family":"brand-frame","kind":"brand-frame","contexts":CONTEXTS,"scores":_scores(72,creative=78,product=76),"en":"New {root} adds a sense of a fresh start, new chapter or renewed version of the root.","pl":"New {root} dodaje skojarzenie z nowym początkiem, nowym rozdziałem albo odświeżoną wersją rdzenia.","tone":"świeży · nowy · otwierający","semantic_class":"brand-form"},

    # Relation/preposition constructions.
    {"word":"by","position":"before","family":"relation","kind":"relation","contexts":{"neutral","creative","photography","service"},"scores":_scores(78,creative=95,photography=94,service=88,neutral=84),"en":"By {root} means work, a product or a brand created by / authored by {root}.","pl":"By {root} znaczy „autorstwa {root}” — praca, produkt albo marka stworzona przez {root}.","tone":"autorski · osobisty · twórczy","semantic_class":"brand-form"},
    {"word":"with","position":"before","family":"relation","kind":"relation","contexts":{"neutral","software","product","service","creative"},"scores":_scores(78,software=91,product=90,service=93,creative=84),"en":"With {root} suggests doing something together with, through or using {root}.","pl":"With {root} sugeruje działanie razem z {root}, za pośrednictwem {root} albo przy użyciu {root}.","tone":"partnerski · wspierający · usługowy","semantic_class":"brand-form"},
    {"word":"from","position":"before","family":"relation","kind":"relation","contexts":{"neutral","creative","photography","product"},"scores":_scores(72,creative=80,photography=79,product=76),"en":"From {root} suggests something originating from the brand, studio or source called {root}.","pl":"From {root} sugeruje coś pochodzącego od marki, studia albo źródła o nazwie {root}.","tone":"źródłowy · autorski · spokojny","semantic_class":"brand-form"},
    {"word":"for","position":"before","family":"relation","kind":"relation","contexts":{"service","product"},"scores":_scores(68,service=82,product=74),"en":"For {root} reads as something made for {root}; it is useful only when {root} clearly represents the audience or beneficiary.","pl":"For {root} znaczy „dla {root}”; ma sens tylko wtedy, gdy {root} jasno oznacza odbiorcę albo beneficjenta.","tone":"celowy · usługowy","semantic_class":"brand-form"},

    # Actions and conversational forms.
    {"word":"get","position":"before","family":"action","kind":"action","contexts":{"software","product","service"},"scores":_scores(80,software=94,product=95,service=84),"en":"Get {root} is a direct acquisition/activation call-to-action: get the product or service called {root}.","pl":"Get {root} to bezpośrednie CTA: „zdobądź / uruchom / pobierz {root}”.","tone":"bezpośredni · produktowy · CTA","semantic_class":"brand-form"},
    {"word":"use","position":"before","family":"action","kind":"action","contexts":{"software","product"},"scores":_scores(82,software=93,product=91),"en":"Use {root} directly tells the user to use the product or tool called {root}.","pl":"Use {root} bezpośrednio mówi użytkownikowi: „użyj produktu / narzędzia {root}”.","tone":"użytkowy · produktowy · jasny","semantic_class":"brand-form"},
    {"word":"try","position":"before","family":"action","kind":"action","contexts":{"software","product","service"},"scores":_scores(78,software=90,product=91,service=84),"en":"Try {root} invites the user to test or experience the product/service called {root}.","pl":"Try {root} zaprasza użytkownika do wypróbowania produktu lub usługi {root}.","tone":"lekki · zachęcający · produktowy","semantic_class":"brand-form"},
    {"word":"ask","position":"before","family":"action","kind":"action","contexts":{"software","product","service"},"scores":_scores(76,software=90,product=87,service=84),"en":"Ask {root} suggests an assistant, expert or service that can answer questions or perform requests.","pl":"Ask {root} sugeruje asystenta, eksperta albo usługę, której można zadawać pytania lub zlecać działania.","tone":"konwersacyjny · pomocny · AI-friendly","semantic_class":"brand-form"},
    {"word":"join","position":"before","family":"action","kind":"action","contexts":{"service","product"},"scores":_scores(72,service=82,product=78),"en":"Join {root} invites the user to become part of a service, community or product ecosystem.","pl":"Join {root} zaprasza użytkownika do dołączenia do usługi, społeczności albo ekosystemu produktu.","tone":"społecznościowy · zapraszający","semantic_class":"brand-form"},

    {"word":"hello","position":"before","family":"contact","kind":"contact","contexts":{"software","service","creative"},"scores":_scores(74,software=82,service=80,creative=79),"en":"Hello {root} feels conversational and approachable, like opening a direct interaction with the brand.","pl":"Hello {root} brzmi konwersacyjnie i przystępnie — jak rozpoczęcie bezpośredniego kontaktu z marką.","tone":"przyjazny · konwersacyjny","semantic_class":"brand-form"},
    {"word":"hey","position":"before","family":"contact","kind":"contact","contexts":{"software","service","creative"},"scores":_scores(70,software=78,service=76,creative=77),"en":"Hey {root} is a casual conversational opening; it works only for intentionally informal brands.","pl":"Hey {root} to luźne, konwersacyjne otwarcie; pasuje tylko do świadomie nieformalnej marki.","tone":"luźny · nieformalny · konwersacyjny","semantic_class":"brand-form"},

    # Possessive forms.
    {"word":"my","position":"before","family":"possessive","kind":"possessive","contexts":{"software","product","service"},"scores":_scores(72,software=83,product=86,service=80),"en":"My {root} makes the product feel personal: the user's own instance, space or version of {root}.","pl":"My {root} personalizuje produkt: „moje {root}”, czyli własna instancja, przestrzeń albo wersja użytkownika.","tone":"osobisty · konsumencki · produktowy","semantic_class":"brand-form"},
    {"word":"our","position":"before","family":"possessive","kind":"possessive","contexts":{"service","creative","product"},"scores":_scores(70,service=80,creative=78,product=75),"en":"Our {root} suggests a shared identity, collective product or community-owned perspective.","pl":"Our {root} sugeruje wspólną tożsamość, produkt zespołowy albo perspektywę społeczności.","tone":"wspólnotowy · zespołowy","semantic_class":"brand-form"},
    {"word":"your","position":"before","family":"possessive","kind":"possessive","contexts":{"software","product","service"},"scores":_scores(68,software=78,product=82,service=80),"en":"Your {root} addresses the user directly and frames {root} as something tailored to them.","pl":"Your {root} zwraca się bezpośrednio do użytkownika i przedstawia {root} jako coś dopasowanego do niego.","tone":"bezpośredni · personalizowany","semantic_class":"brand-form"},

    # Descriptors after the root.
    {"word":"studio","position":"after","family":"descriptor","kind":"descriptor","contexts":{"neutral","creative","photography","service"},"scores":_scores(82,creative=96,photography=97,service=86,neutral=86),"en":"{root} Studio clearly positions {root} as a creative studio or professional practice.","pl":"{root} Studio jasno pozycjonuje {root} jako studio kreatywne albo profesjonalną pracownię.","tone":"profesjonalny · kreatywny · czytelny","semantic_class":"brand-form"},
    {"word":"lab","position":"after","family":"descriptor","kind":"descriptor","contexts":{"neutral","software","creative","product"},"scores":_scores(84,software=94,creative=88,product=90,neutral=86),"en":"{root} Lab positions {root} as an experimental, research-led or innovation-focused brand.","pl":"{root} Lab pozycjonuje {root} jako markę eksperymentalną, badawczą albo nastawioną na innowacje.","tone":"eksperymentalny · techniczny · innowacyjny","semantic_class":"brand-form"},
    {"word":"works","position":"after","family":"descriptor","kind":"descriptor","contexts":{"neutral","creative","photography","product","service"},"scores":_scores(80,creative=92,photography=87,product=82,service=84),"en":"{root} Works suggests a maker, creative practice or body of work produced under the {root} name.","pl":"{root} Works sugeruje twórcę, pracownię albo zbiór realizacji powstających pod nazwą {root}.","tone":"rzemieślniczy · twórczy · szeroki","semantic_class":"brand-form"},
    {"word":"house","position":"after","family":"descriptor","kind":"descriptor","contexts":{"neutral","creative","photography","service"},"scores":_scores(76,creative=88,photography=85,service=82),"en":"{root} House suggests an independent creative, production or brand house.","pl":"{root} House sugeruje niezależny dom kreatywny, produkcyjny albo markę typu house.","tone":"editorial · kreatywny · premium","semantic_class":"brand-form"},
    {"word":"co","position":"after","family":"descriptor","kind":"descriptor","contexts":CONTEXTS,"scores":_scores(74,service=80,product=78),"en":"{root} Co gives the root a compact company-style identity without adding a specific product meaning.","pl":"{root} Co nadaje rdzeniowi zwięzły charakter firmowy bez dopisywania konkretnego znaczenia produktu.","tone":"firmowy · neutralny · prosty","semantic_class":"brand-form"},
    {"word":"app","position":"after","family":"descriptor","kind":"descriptor","contexts":{"software","product"},"scores":_scores(82,software=90,product=92),"en":"{root} App explicitly tells the user that {root} is an application.","pl":"{root} App wprost informuje użytkownika, że {root} jest aplikacją.","tone":"dosłowny · produktowy · cyfrowy","semantic_class":"brand-form"},
    {"word":"ai","position":"after","family":"descriptor","kind":"descriptor","contexts":{"software","product"},"scores":_scores(80,software=88,product=86),"en":"{root} AI explicitly frames {root} as an artificial-intelligence product or service.","pl":"{root} AI wprost pozycjonuje {root} jako produkt albo usługę wykorzystującą sztuczną inteligencję.","tone":"techniczny · AI · bezpośredni","semantic_class":"brand-form"},
]


def _clean(value: str) -> str:
    return "".join(ch for ch in (value or "").lower() if ch.isalpha())


def _known(root: str) -> bool:
    return not str(root_info_v15(root).get("en", "")).startswith("No local dictionary entry yet")


def _phrase(root: str, partner: str, position: str) -> str:
    return f"{partner} {root}" if position == "before" else f"{root} {partner}"


def _construction(partner: str, position: str, context: str):
    context = context if context in CONTEXTS else "neutral"
    p = _clean(partner)
    for item in CONSTRUCTIONS:
        if item["word"] == p and item["position"] == position and context in item["contexts"]:
            return item
    return None


def _construction_score(item: dict, context: str) -> int:
    scores = item.get("scores", {})
    return int(scores.get(context, scores.get("default", 70)))


def _tier(score: int) -> str:
    if score >= 88:
        return "recommended"
    if score >= 78:
        return "good"
    return "experimental"


def _tier_label(tier: str) -> str:
    return {
        "recommended": "mocno rekomendowane",
        "good": "dobra alternatywa",
        "experimental": "eksperymentalne",
    }.get(tier, tier)


def _format_meaning(template: str, root: str) -> str:
    return str(template or "").format(root=root.title())


def _construction_row(root: str, item: dict, context: str) -> dict:
    r = _clean(root)
    partner = item["word"]
    position = item["position"]
    joined = partner + r if position == "before" else r + partner
    score = _construction_score(item, context)
    tier = _tier(score)
    return {
        "word": partner,
        "position": position,
        "phrase": _phrase(r, partner, position),
        "domain": f"{joined}.com",
        "joined": joined,
        "score": score,
        "semantic_class": item.get("semantic_class", "brand-form"),
        "semantic_alert": "Mocna rekomendacja z konkretnym znaczeniem całej konstrukcji." if tier == "recommended" else "Konstrukcja ma sens, ale jest słabsza od rekomendowanych kierunków." if tier == "good" else "Kierunek eksperymentalny — pokazuj dopiero po rozwinięciu dalszych opcji.",
        "interpretation_en": _format_meaning(item.get("en", ""), r),
        "interpretation_pl": _format_meaning(item.get("pl", ""), r),
        "tone": item.get("tone", ""),
        "kind": item.get("kind", "construction"),
        "family": item.get("family", "descriptor"),
        "recommendation_tier": tier,
        "recommendation_label": _tier_label(tier),
        "context": context,
    }


def analyze_pair(root: str, partner: str, position: str = "before", niche: str = "", context: str = "neutral") -> dict:
    base = analyze_pair_v15(root, partner, position, niche)
    if not base.get("ok"):
        return {**base, "semantic_class":"blocked", "semantic_alert":"Połączenie zablokowane przed sprawdzaniem domeny."}
    context = context if context in CONTEXTS else "neutral"
    item = _construction(partner, position, context)
    phrase = _phrase(_clean(root), _clean(partner), position)
    if item:
        row = _construction_row(root, item, context)
        return {
            **base,
            **row,
            "score": row["score"],
            "phrase": phrase,
            "reasons": [
                f"rodzina konstrukcji: {FAMILY_META[row['family']]['label']}",
                f"rekomendacja: {row['recommendation_label']}",
                "znaczenie ocenione przed dostępnością .com",
            ],
        }

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
    tier = "recommended" if cls == "natural" and score >= 84 else "good" if cls in {"natural", "brandable"} else "experimental"
    return {
        **base,
        "semantic_class": cls,
        "semantic_alert": alert,
        "phrase": phrase,
        "interpretation_en": en,
        "interpretation_pl": pl,
        "context": context,
        "family": "semantic",
        "recommendation_tier": tier,
        "recommendation_label": _tier_label(tier),
    }


def _families(root: str, context: str) -> list[dict]:
    context = context if context in CONTEXTS else "neutral"
    grouped: dict[str, list[dict]] = {}
    for item in CONSTRUCTIONS:
        if context not in item["contexts"]:
            continue
        row = _construction_row(root, item, context)
        grouped.setdefault(row["family"], []).append(row)
    out = []
    for key, rows in grouped.items():
        meta = FAMILY_META[key]
        rows.sort(key=lambda x: (-x["score"], x["word"]))
        out.append({"key": key, **meta, "items": rows})
    out.sort(key=lambda x: x["order"])
    return out


def workshop(root: str, niche: str = "", limit: int = 8, context: str = "neutral") -> dict:
    # Deepen the semantic pool substantially; the UI can then fill 6–8 genuinely available names.
    semantic_limit = max(8, min(int(limit), 32))
    base = workshop_v15(root, niche, semantic_limit)
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
            enriched = {
                **row,
                "pair": pair,
                "semantic_class": pair.get("semantic_class"),
                "semantic_alert": pair.get("semantic_alert"),
                "interpretation_en": pair.get("interpretation_en"),
                "interpretation_pl": pair.get("interpretation_pl"),
                "recommendation_tier": pair.get("recommendation_tier"),
                "recommendation_label": pair.get("recommendation_label"),
                "family": pair.get("family", "semantic"),
            }
            target.append(enriched)
            if pair.get("semantic_class") != "abstract":
                best.append({
                    "word":row["word"],
                    "position":position,
                    "phrase":pair.get("phrase"),
                    "domain":pair.get("domain"),
                    "joined":pair.get("joined"),
                    "score":row.get("score",0),
                    "semantic_class":pair.get("semantic_class"),
                    "semantic_alert":pair.get("semantic_alert"),
                    "interpretation_en":pair.get("interpretation_en"),
                    "interpretation_pl":pair.get("interpretation_pl"),
                    "recommendation_tier":pair.get("recommendation_tier"),
                    "recommendation_label":pair.get("recommendation_label"),
                    "family":"semantic",
                    "kind":"semantic",
                })
    best.sort(key=lambda x:x.get("score",0),reverse=True)
    families = _families(root, context)
    extensions = [item for family in families for item in family["items"]]
    return {
        **base,
        "root":root_data,
        "before":before,
        "after":after,
        "best":best[:min(12, semantic_limit)],
        "families":families,
        "extensions":extensions,
        "context":context,
        "shortlist_target":8,
        "shortlist_minimum":6,
        "note":"Mianem ocenia znaczenie i naturalność przed dostępnością domeny. Potem sprawdza szerszą pulę .com, aby wypełnić shortlistę 6–8 mocnych wolnych kierunków bez promowania bełkotu.",
    }
