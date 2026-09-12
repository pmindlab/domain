from __future__ import annotations

"""v1.7.1 deep-pool extension for the legacy-named v1.7 curator module.

The main curator intentionally keeps a compact primary vocabulary. This module adds a
second, still-curated context pool so availability filtering does not collapse a good
Workshop session to one result when common combinations are already registered.
Every entry keeps a concrete whole-name EN/PL interpretation and a quality score that
is decided before any domain lookup.
"""

from . import workshop_v16 as workshop


def _row(word: str, score: int, en: str, pl: str, tone: str, *, product: int | None = None) -> dict:
    scores = {"default": 78, "software": score}
    if product is not None:
        scores["product"] = product
    return {
        "word": word,
        "position": "after",
        "family": "semantic-context",
        "kind": "context-semantic",
        "contexts": {"software", "product"} if product is not None else {"software"},
        "scores": scores,
        "en": en,
        "pl": pl,
        "tone": tone,
        "semantic_class": "brandable",
        "depth": 2,
    }


EXTRA_CONSTRUCTIONS = [
    _row("agent", 95, "{root} Agent suggests an intelligent software agent that acts, assists or completes tasks.", "{root} Agent sugeruje inteligentnego agenta programowego, który działa, pomaga albo wykonuje zadania.", "AI · autonomiczny · pomocny", product=91),
    _row("query", 93, "{root} Query suggests search, asking questions or retrieving structured information.", "{root} Query sugeruje wyszukiwanie, zadawanie pytań albo pobieranie uporządkowanych informacji.", "wyszukiwawczy · informacyjny · techniczny", product=88),
    _row("logic", 92, "{root} Logic suggests rules, reasoning and the decision layer of a software system.", "{root} Logic sugeruje reguły, rozumowanie i warstwę decyzyjną systemu programowego.", "logiczny · systemowy · techniczny", product=87),
    _row("sync", 92, "{root} Sync suggests synchronization, keeping data or work aligned across systems.", "{root} Sync sugeruje synchronizację i utrzymywanie danych albo pracy w zgodzie między systemami.", "zsynchronizowany · bieżący · produktowy", product=90),
    _row("code", 91, "{root} Code clearly positions the brand around software, programming or developer tooling.", "{root} Code jasno pozycjonuje markę wokół oprogramowania, programowania albo narzędzi developerskich.", "developerski · techniczny · bezpośredni", product=86),
    _row("data", 90, "{root} Data positions the product around collecting, processing or understanding data.", "{root} Data pozycjonuje produkt wokół zbierania, przetwarzania albo rozumienia danych.", "dane · analityczny · techniczny", product=88),
    _row("bridge", 90, "{root} Bridge suggests connecting tools, systems, teams or data that otherwise stay separate.", "{root} Bridge sugeruje łączenie narzędzi, systemów, zespołów albo danych, które inaczej pozostają rozdzielone.", "łączący · integracyjny · systemowy", product=88),
    _row("beacon", 89, "{root} Beacon suggests guidance, a visible signal or a system that helps users find what matters.", "{root} Beacon sugeruje prowadzenie, wyraźny sygnał albo system pomagający znaleźć to, co ważne.", "prowadzący · sygnałowy · czytelny", product=86),
    _row("scope", 89, "{root} Scope suggests visibility, inspection and a focused view into a system or problem.", "{root} Scope sugeruje widoczność, inspekcję i skupiony wgląd w system albo problem.", "analityczny · obserwacyjny · precyzyjny", product=86),
    _row("model", 88, "{root} Model suggests a structured representation, AI model or reusable system abstraction.", "{root} Model sugeruje uporządkowaną reprezentację, model AI albo wielokrotnie używaną abstrakcję systemu.", "modelowy · AI · strukturalny", product=88),
    _row("stack", 88, "{root} Stack suggests a complete technology stack or a set of software layers working together.", "{root} Stack sugeruje kompletny stos technologiczny albo zestaw współpracujących warstw oprogramowania.", "technologiczny · warstwowy · developerski", product=86),
    _row("relay", 87, "{root} Relay suggests passing messages, events or tasks reliably between parts of a system.", "{root} Relay sugeruje niezawodne przekazywanie komunikatów, zdarzeń albo zadań między częściami systemu.", "przekaźnikowy · komunikacyjny · systemowy", product=84),
    _row("mesh", 87, "{root} Mesh suggests a connected network of services, devices or cooperating components.", "{root} Mesh sugeruje połączoną sieć usług, urządzeń albo współpracujących komponentów.", "sieciowy · połączony · modularny", product=84),
    _row("grid", 87, "{root} Grid suggests an organized network, matrix or structured computational workspace.", "{root} Grid sugeruje uporządkowaną sieć, macierz albo strukturalną przestrzeń obliczeniową.", "strukturalny · sieciowy · techniczny", product=84),
    _row("link", 86, "{root} Link suggests a direct connection between people, data, tools or services.", "{root} Link sugeruje bezpośrednie połączenie między ludźmi, danymi, narzędziami albo usługami.", "łączący · prosty · cyfrowy", product=85),
    _row("stream", 86, "{root} Stream suggests continuous data, events or work moving through the product in real time.", "{root} Stream sugeruje ciągły strumień danych, zdarzeń albo pracy przepływający przez produkt w czasie rzeczywistym.", "bieżący · strumieniowy · dynamiczny", product=85),
    _row("layer", 85, "{root} Layer suggests a distinct software layer that adds capability without replacing the underlying system.", "{root} Layer sugeruje odrębną warstwę oprogramowania, która dodaje możliwości bez zastępowania systemu bazowego.", "warstwowy · modularny · techniczny", product=84),
    _row("engine", 85, "{root} Engine suggests the working core that powers processing, automation or generation.", "{root} Engine sugeruje działający rdzeń napędzający przetwarzanie, automatyzację albo generowanie.", "napędowy · systemowy · techniczny", product=86),
    _row("pilot", 85, "{root} Pilot suggests guided operation, assistance or a product that helps steer a task or workflow.", "{root} Pilot sugeruje prowadzenie, asystę albo produkt pomagający sterować zadaniem czy workflow.", "prowadzący · pomocny · produktowy", product=87),
    _row("lens", 84, "{root} Lens suggests a clearer analytical view or a focused way to inspect information.", "{root} Lens sugeruje wyraźniejszy analityczny widok albo skupiony sposób oglądania informacji.", "analityczny · klarowny · obserwacyjny", product=84),
    _row("trace", 84, "{root} Trace suggests tracking events, history, provenance or the path of activity through a system.", "{root} Trace sugeruje śledzenie zdarzeń, historii, pochodzenia albo przebiegu aktywności w systemie.", "śledzący · audytowy · techniczny", product=82),
    _row("route", 84, "{root} Route suggests directing requests, work or information toward the right destination.", "{root} Route sugeruje kierowanie żądań, pracy albo informacji do właściwego miejsca.", "kierunkowy · systemowy · operacyjny", product=83),
    _row("scan", 83, "{root} Scan suggests inspecting data, code or systems to find relevant signals or issues.", "{root} Scan sugeruje przeglądanie danych, kodu albo systemów w poszukiwaniu ważnych sygnałów lub problemów.", "inspekcyjny · analityczny · techniczny", product=82),
    _row("orbit", 83, "{root} Orbit suggests a product ecosystem with a clear center and connected surrounding tools or activity.", "{root} Orbit sugeruje ekosystem produktu z wyraźnym centrum i połączonymi wokół niego narzędziami lub aktywnością.", "ekosystemowy · przestrzenny · nowoczesny", product=83),
    _row("forge", 83, "{root} Forge suggests building, shaping or producing software and digital artifacts deliberately.", "{root} Forge sugeruje świadome budowanie, kształtowanie albo wytwarzanie oprogramowania i cyfrowych artefaktów.", "twórczy · developerski · konstrukcyjny", product=84),
    _row("hub", 82, "{root} Hub positions the product as a central place where tools, work or information come together.", "{root} Hub pozycjonuje produkt jako centralne miejsce, w którym spotykają się narzędzia, praca albo informacje.", "centralny · integracyjny · użytkowy", product=84),
    _row("kit", 82, "{root} Kit suggests a practical set of tools or reusable building blocks for a specific job.", "{root} Kit sugeruje praktyczny zestaw narzędzi albo wielokrotnie używanych elementów do konkretnego zadania.", "narzędziowy · modularny · praktyczny", product=86),
    _row("base", 82, "{root} Base suggests a stable foundation, shared source or starting layer for further work.", "{root} Base sugeruje stabilną podstawę, wspólne źródło albo warstwę startową do dalszej pracy.", "bazowy · stabilny · systemowy", product=82),
    _row("map", 82, "{root} Map suggests orientation, structure and a clearer way to navigate complex information.", "{root} Map sugeruje orientację, strukturę i czytelniejszy sposób poruszania się po złożonych informacjach.", "nawigacyjny · klarowny · strukturalny", product=82),
    _row("wire", 82, "{root} Wire suggests a direct technical connection or a channel carrying information between components.", "{root} Wire sugeruje bezpośrednie połączenie techniczne albo kanał przenoszący informacje między komponentami.", "połączeniowy · techniczny · lekki", product=80),
    _row("vault", 82, "{root} Vault suggests secure storage, protected knowledge or controlled access to valuable data.", "{root} Vault sugeruje bezpieczne przechowywanie, chronioną wiedzę albo kontrolowany dostęp do wartościowych danych.", "bezpieczny · zasobowy · kontrolowany", product=83),
    _row("path", 81, "{root} Path suggests a guided route through a process, workflow or technical decision.", "{root} Path sugeruje prowadzoną ścieżkę przez proces, workflow albo decyzję techniczną.", "kierunkowy · procesowy · czytelny", product=82),
    _row("wave", 81, "{root} Wave suggests a moving signal, new cycle or continuous digital activity.", "{root} Wave sugeruje poruszający się sygnał, nowy cykl albo ciągłą aktywność cyfrową.", "dynamiczny · sygnałowy · nowoczesny", product=81),
    _row("shift", 81, "{root} Shift suggests change, transition or moving work into a better operating state.", "{root} Shift sugeruje zmianę, przejście albo przesunięcie pracy do lepszego sposobu działania.", "zmiana · operacyjny · nowoczesny", product=82),
    _row("mode", 80, "{root} Mode suggests a distinct way of working or an operating state of the product.", "{root} Mode sugeruje określony sposób pracy albo stan działania produktu.", "operacyjny · prosty · produktowy", product=81),
    _row("port", 80, "{root} Port suggests an access point, interface or place where systems connect.", "{root} Port sugeruje punkt dostępu, interfejs albo miejsce, w którym łączą się systemy.", "interfejsowy · techniczny · łączący", product=80),
    _row("gate", 80, "{root} Gate suggests controlled entry, routing or a clear point of access into a system.", "{root} Gate sugeruje kontrolowane wejście, routing albo wyraźny punkt dostępu do systemu.", "dostępowy · kontrolowany · systemowy", product=80),
    _row("dock", 80, "{root} Dock suggests a practical place where tools, files or workflows connect and become ready to use.", "{root} Dock sugeruje praktyczne miejsce, w którym narzędzia, pliki albo workflow łączą się i są gotowe do użycia.", "użytkowy · integracyjny · produktowy", product=82),
]


def install() -> None:
    existing = {(x.get("word"), x.get("position"), x.get("family")) for x in workshop.CONSTRUCTIONS}
    for item in EXTRA_CONSTRUCTIONS:
        key = (item.get("word"), item.get("position"), item.get("family"))
        if key not in existing:
            workshop.CONSTRUCTIONS.append(item)
            existing.add(key)


install()
