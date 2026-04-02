# Skrypt prezentacji `quantumDUO` w formie drzewa

## Jak korzystać z tego pliku

To nie jest zwykły linearny tekst do czytania od góry do dołu.

To jest drzewo prezentacji:

- sekcje główne to główny tok wypowiedzi,
- odnośniki prowadzą do rozwinięć pojęć,
- możesz iść krótką ścieżką albo schodzić głębiej, jeśli padnie pytanie.

## Szybka nawigacja

- [1. Start prezentacji](#1-start-prezentacji)
- [2. Problem i pomysł projektu](#2-problem-i-pomysł-projektu)
- [3. Jak działa aplikacja](#3-jak-działa-aplikacja)
- [4. Etap BB84](#4-etap-bb84)
- [5. Etap VQE](#5-etap-vqe)
- [6. Etap Security](#6-etap-security)
- [7. Co pokazują wyniki](#7-co-pokazują-wyniki)
- [8. Ograniczenia projektu](#8-ograniczenia-projektu)
- [9. Zakończenie](#9-zakończenie)

### Rozwinięcia pojęć

- [A. Czym jest `QBER`](#a-czym-jest-qber)
- [B. Czym jest `BB84`](#b-czym-jest-bb84)
- [C. Czym jest `VQE`](#c-czym-jest-vqe)
- [D. Czym jest Hamiltonian `H2`](#d-czym-jest-hamiltonian-h2)
- [E. Czym jest `AES-CTR`](#e-czym-jest-aes-ctr)
- [F. Czym jest `SHA-256`](#f-czym-jest-sha-256)
- [G. Co oznacza `Exact`](#g-co-oznacza-exact)
- [H. Jak policzony jest `QBER` w projekcie](#h-jak-policzony-jest-qber-w-projekcie)

## 1. Start prezentacji

### Wersja krótka

`quantumDUO` to projekt, który łączy bezpieczną komunikację kwantową z obliczeniami kwantowymi. Najpierw sprawdzamy kanał przez `BB84`, potem liczymy energię `H2` przez `VQE`, a na końcu szyfrujemy wynik.

### Jeśli chcesz dodać jedno zdanie więcej

To jest projekt demonstracyjny pokazujący kompletny pipeline: bezpieczeństwo komunikacji wpływa na to, czy w ogóle pozwalamy na wykonanie dalszych obliczeń i przekazanie wyniku.

### Jeśli ktoś zapyta o skróty

- Zobacz: [B. Czym jest `BB84`](#b-czym-jest-bb84)
- Zobacz: [A. Czym jest `QBER`](#a-czym-jest-qber)
- Zobacz: [C. Czym jest `VQE`](#c-czym-jest-vqe)

## 2. Problem i pomysł projektu

### Co mówisz

Chcieliśmy połączyć dwa ważne zastosowania informatyki kwantowej:

- bezpieczną wymianę klucza,
- obliczenia chemiczne.

Zamiast pokazywać je osobno, zrobiliśmy jedną aplikację, w której pierwszy etap decyduje, czy drugi etap w ogóle się uruchomi.

### Główna teza

Projekt pokazuje, że technologie kwantowe mogą tworzyć jeden proces, a nie tylko dwa niezależne dema.

### Jeśli padnie pytanie „co jest wynikiem końcowym?”

Wynikiem końcowym są:

- wykresy i tabela energii `H2`,
- zaszyfrowany plik z wynikami,
- możliwość sprawdzenia, czy kanał był wystarczająco bezpieczny.

## 3. Jak działa aplikacja

### Co mówisz

Aplikacja ma trzy zakładki:

- `BB84`,
- `VQE H2`,
- `Security`.

Użytkownik ustawia parametry z lewej strony, a potem widzi kolejne etapy całego pipeline'u.

### Główna logika

1. Liczymy `QBER`.
2. Sprawdzamy, czy jest poniżej progu `0.11`.
3. Jeśli tak, uruchamiamy `VQE`.
4. Następnie szyfrujemy wyniki.

### Jeśli chcesz pokazać to jednym zdaniem

Najpierw oceniamy jakość kanału, potem wykonujemy obliczenie, a na końcu zabezpieczamy rezultat.

### Jeśli padnie pytanie o próg

- Zobacz: [A. Czym jest `QBER`](#a-czym-jest-qber)
- Zobacz: [H. Jak policzony jest `QBER` w projekcie](#h-jak-policzony-jest-qber-w-projekcie)

## 4. Etap `BB84`

### Co mówisz

W pierwszym etapie symulujemy protokół `BB84`.

Alice:

- losuje bity,
- losuje bazy,
- wysyła zakodowane stany.

Bob:

- losuje własne bazy,
- mierzy otrzymane kubity.

Potem porównują tylko bazy i zachowują te pozycje, gdzie bazy były zgodne.

### Najważniejsza intuicja

Jeśli Eve podsłuchuje, musi mierzyć stan kwantowy. Jeżeli wybierze złą bazę, wprowadza błąd. Ten błąd widzimy jako wzrost `QBER`.

### Co pokazujesz w aplikacji

- metryki `QBER (no attack)` i `QBER (full attack)`,
- wykres `QBER vs Eve`,
- opcjonalnie heatmapę,
- opcjonalnie walkthrough.

### Jeśli padnie pytanie „co to dokładnie jest BB84?”

- Zobacz: [B. Czym jest `BB84`](#b-czym-jest-bb84)

### Jeśli padnie pytanie „co to jest QBER?”

- Zobacz: [A. Czym jest `QBER`](#a-czym-jest-qber)
- Zobacz: [H. Jak policzony jest `QBER` w projekcie](#h-jak-policzony-jest-qber-w-projekcie)

## 5. Etap `VQE`

### Co mówisz

Jeśli kanał jest bezpieczny, przechodzimy do `VQE`, czyli algorytmu, który szuka najniższej energii układu kwantowego.

W naszym przypadku tym układem jest uproszczona cząsteczka wodoru `H2`.

### Co dzieje się technicznie

- dla kolejnych odległości wiązania `R` budujemy Hamiltonian,
- uruchamiamy `VQE`,
- porównujemy wynik z rozwiązaniem dokładnym `Exact`.

### Co pokazujesz w aplikacji

- wykres energii,
- wykres błędu,
- tabelę z wartościami.

### Główna intuicja

`VQE` próbuje znaleźć taki stan próbny, który daje jak najniższą energię. Im bliżej wyniku dokładnego, tym lepiej działa przybliżenie.

### Jeśli padnie pytanie „co to jest VQE?”

- Zobacz: [C. Czym jest `VQE`](#c-czym-jest-vqe)

### Jeśli padnie pytanie „co to jest Hamiltonian?”

- Zobacz: [D. Czym jest Hamiltonian `H2`](#d-czym-jest-hamiltonian-h2)

### Jeśli padnie pytanie „co oznacza Exact?”

- Zobacz: [G. Co oznacza `Exact`](#g-co-oznacza-exact)

## 6. Etap `Security`

### Co mówisz

Po obliczeniu energii zabezpieczamy wynik.

Do tego używamy bitów z fazy `BB84`, przekształcamy je do postaci klucza i szyfrujemy wynik `VQE`.

### Główna intuicja

Wartość tego projektu polega na tym, że klucz nie jest wymyślony osobno. On wynika z fazy kwantowej i domyka cały scenariusz.

### Co pokazujesz w aplikacji

- jaki tryb szyfrowania został użyty,
- ile mamy bajtów klucza surowego,
- ile ma klucz końcowy,
- że round-trip działa poprawnie,
- że można pobrać zaszyfrowany plik.

### Jeśli padnie pytanie o `AES-CTR`

- Zobacz: [E. Czym jest `AES-CTR`](#e-czym-jest-aes-ctr)

### Jeśli padnie pytanie o `SHA-256`

- Zobacz: [F. Czym jest `SHA-256`](#f-czym-jest-sha-256)

## 7. Co pokazują wyniki

### Wykres `QBER vs Eve`

Co mówisz:
ten wykres pokazuje, że wzrost intensywności podsłuchu podnosi poziom błędów w kanale.

Wniosek:
protokół ma sens, bo ingerencja Eve zostawia ślad w statystyce.

### Heatmapa

Co mówisz:
heatmapa pokazuje wspólny wpływ ataku i szumu na `QBER`.

Wniosek:
nie każdy błąd oznacza podsłuch, ale oba zjawiska pogarszają jakość kanału.

### Krzywa energii `H2`

Co mówisz:
ten wykres pokazuje energię cząsteczki w funkcji długości wiązania.

Wniosek:
minimum krzywej odpowiada najbardziej stabilnej konfiguracji.

### Wykres błędu

Co mówisz:
to jest różnica między wynikiem przybliżonym i dokładnym.

Wniosek:
pokazuje, jak dobrze działa `VQE`.

## 8. Ograniczenia projektu

### Co mówisz

Projekt jest demonstracyjny, więc świadomie upraszcza kilka rzeczy:

- `BB84` jest uproszczoną symulacją,
- nie ma pełnego toru `QKD`,
- model `H2` jest mały i edukacyjny,
- `VQE` działa na symulatorze,
- `AES-CTR` daje poufność, ale nie integralność.

### Jeśli chcesz dodać uczciwy komentarz

To nie jest system produkcyjny, tylko dobrze zbudowany model edukacyjno-techniczny.

## 9. Zakończenie

### Co mówisz

Projekt pokazuje pełny łańcuch działania:

- najpierw bezpieczny kanał,
- potem obliczenia kwantowe,
- na końcu zabezpieczenie wyniku.

Dzięki temu `quantumDUO` nie jest tylko zbiorem trzech modułów, ale jedną spójną demonstracją.

## A. Czym jest `QBER`

### Rozwinięcie skrótu

`QBER` to `Quantum Bit Error Rate`.

### Co to znaczy po ludzku

To procent błędnych bitów po odsianiu tych przypadków, gdzie Alice i Bob użyli różnych baz.

### Za co odpowiada u nas

W projekcie `QBER` jest głównym wskaźnikiem jakości kanału.

To od niego zależy, czy:

- uznamy kanał za bezpieczny,
- przejdziemy do `VQE`,
- przejdziemy do szyfrowania.

### Jak interpretować

- mały `QBER` oznacza dobry kanał,
- duży `QBER` oznacza problem: podsłuch albo szum.

### Gdzie jest używany

W logice warunkowej aplikacji.

### Jeśli chcesz zejść jeszcze głębiej

- Zobacz: [H. Jak policzony jest `QBER` w projekcie](#h-jak-policzony-jest-qber-w-projekcie)

## B. Czym jest `BB84`

### Rozwinięcie nazwy

`BB84` pochodzi od nazwisk Bennett i Brassard oraz roku 1984.

### Co to jest

To protokół kwantowej dystrybucji klucza.

### Idea

Alice koduje bity w dwóch bazach kwantowych, Bob mierzy je w losowych bazach, a później obie strony porównują tylko bazy.

### Dlaczego to działa

Bo pomiar w złej bazie zaburza stan kwantowy, więc podsłuch zostawia ślad.

### Za co odpowiada u nas

- generuje materiał kluczowy,
- wykrywa problemy z kanałem,
- decyduje, czy dalszy pipeline ma sens.

## C. Czym jest `VQE`

### Rozwinięcie skrótu

`VQE` to `Variational Quantum Eigensolver`.

### Co to jest

To hybrydowy algorytm kwantowo-klasyczny do szukania najniższej energii danego układu.

### Jak działa ogólnie

- część kwantowa przygotowuje stan próbny,
- część klasyczna zmienia parametry tego stanu,
- celem jest minimalizacja energii.

### Za co odpowiada u nas

Liczy energię cząsteczki `H2` dla różnych długości wiązania.

### Dlaczego działa

Bo opiera się na zasadzie wariacyjnej: dobry stan próbny daje energię bliską energii stanu podstawowego.

## D. Czym jest Hamiltonian `H2`

### Co to jest

Hamiltonian to matematyczny opis energii układu.

### Co oznacza u nas

To operator opisujący uproszczony model cząsteczki `H2`.

### Po co jest potrzebny

Bez Hamiltonianu nie wiemy, jaką energię ma dany stan kwantowy.

### Dlaczego jest uproszczony

Bo projekt ma być szybki, demonstracyjny i możliwy do uruchomienia lokalnie.

## E. Czym jest `AES-CTR`

### Co to jest

To tryb pracy szyfru `AES`.

### Co daje

Poufność danych.

### Co to znaczy w praktyce

Osoba bez klucza nie powinna móc odczytać zaszyfrowanego wyniku.

### Ograniczenie

`AES-CTR` sam z siebie nie zapewnia integralności. To znaczy, że chroni treść, ale nie mówi automatycznie, czy ktoś jej nie zmienił.

## F. Czym jest `SHA-256`

### Co to jest

To funkcja skrótu kryptograficznego.

### Po co jest używana u nas

Zamienia materiał kluczowy z `BB84` w 32-bajtowy klucz pasujący do `AES-256`.

### Co daje

- stałą długość klucza,
- dobre wymieszanie danych wejściowych.

## G. Co oznacza `Exact`

### Co to jest

To wynik dokładny policzony klasycznie przez diagonalizację Hamiltonianu.

### Po co jest potrzebny

Stanowi punkt odniesienia dla `VQE`.

### Co nam mówi

Jeśli `VQE` jest blisko `Exact`, to znaczy, że algorytm działa sensownie.

## H. Jak policzony jest `QBER` w projekcie

### Idea

Bierzemy tylko te pozycje, gdzie Alice i Bob użyli tej samej bazy.

Potem liczymy, jaki procent tych bitów jest różny.

### Wzór

`QBER = liczba niezgodnych bitów / liczba zachowanych bitów`

### Co to znaczy u nas

Jeżeli Alice i Bob mają wiele niezgodności, kanał wygląda źle.

### Dlaczego to ma sens

Bo po odsianiu różnych baz powinniśmy porównywać tylko te przypadki, które teoretycznie miały szansę dać zgodny wynik.

### Co psuje `QBER`

- podsłuch Eve,
- szum kanału,
- zbyt mała liczba prób, jeśli statystyka jest słaba.

