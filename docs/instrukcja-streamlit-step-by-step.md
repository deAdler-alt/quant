# Instrukcja step-by-step: jak korzystać ze Streamlit w `quantumDUO`

## 1. Po co jest ta aplikacja
Ta aplikacja prowadzi użytkownika przez trzy kolejne etapy:
- sprawdzenie bezpieczeństwa kanału przez `BB84`,
- obliczenie energii cząsteczki `H2` przez `VQE`,
- zaszyfrowanie wyniku.

Najważniejsza zasada:

> Jeśli kanał nie wygląda na bezpieczny, aplikacja nie przechodzi dalej do `VQE` i szyfrowania.

## 2. Jak uruchomić aplikację

```bash
streamlit run app.py
```

Po uruchomieniu zobaczysz:
- panel boczny po lewej,
- trzy zakładki: `BB84`, `VQE H2`, `Security`.

## 3. Co ustawiasz w panelu bocznym

## Sekcja `BB84`

### `n (raw rounds)`
To liczba prób BB84.

Jak używać:
- `64-256` do szybkiego eksperymentu,
- `512-1024` do sensownej prezentacji,
- więcej, jeśli chcesz stabilniejsze wyniki.

Jak interpretować:
- małe `n` oznacza większy wpływ losowości,
- duże `n` daje bardziej wiarygodne statystyki.

### `Eve intercept probability`
To siła ataku Eve.

Jak używać:
- `0.0` jeśli chcesz pokazać czysty kanał,
- `0.25` dla lekkiego ataku,
- `0.5` dla mocniejszego wpływu,
- `1.0` dla pełnego przechwycenia.

Jak interpretować:
- im większe `p_eve`, tym zwykle większy `QBER`.

### `Channel noise probability`
To poziom szumu kanału.

Jak używać:
- `0.0` dla idealnych warunków,
- `0.01-0.05` dla lekkiego zakłócenia,
- większe wartości do pokazania, że sam szum też może zepsuć kanał.

Jak interpretować:
- wysoki `QBER` nie musi oznaczać tylko ataku,
- może wynikać również z niedoskonałości kanału.

### `QBER sweep steps`
To liczba punktów wykresu `QBER vs Eve`.

Jak używać:
- `6-8` do typowej prezentacji,
- więcej, jeśli chcesz gładszy wykres.

### `Seed`
To ziarno losowości.

Jak używać:
- zostaw stałe, jeśli chcesz mieć powtarzalny pokaz,
- zmień, jeśli chcesz zobaczyć inny losowy przebieg.

## Sekcja `VQE`

### `R grid (Å, comma-separated)`
To lista długości wiązania `H2`.

Przykład:

```text
0.3,0.5,0.7,0.9,1.1,1.3
```

Jak interpretować:
- każda liczba daje jeden punkt na wykresie energii,
- zbyt mało punktów daje ubogi wykres,
- zbyt dużo punktów wydłuża obliczenia.

### `Max optimizer iterations`
To liczba kroków optymalizacji w `VQE`.

Jak używać:
- `100-200` zwykle wystarcza do prezentacji,
- wyższe wartości mogą poprawić wynik kosztem czasu.

### `Ansatz reps`
To złożoność stanu próbnego w `VQE`.

Jak używać:
- `1-2` do szybkiej demonstracji,
- `2-3` dla lepszego dopasowania,
- większe wartości zwiększają koszt obliczeń.

## Sekcja `Encryption`

### `Force XOR (no AES)`
To ręczne wymuszenie prostszego szyfrowania.

Jak używać:
- wyłączone dla normalnego pokazu,
- włączone tylko jeśli chcesz pokazać tryb awaryjny.

Jak interpretować:
- `AES-CTR` to sensowny tryb demonstracyjny,
- `XOR` to tylko awaryjny fallback.

## Sekcja `Optional`

### `Generate QBER heatmap`
Włącza dodatkową heatmapę.

Jak używać:
- włącz, jeśli chcesz porównać jednocześnie wpływ Eve i szumu,
- wyłącz, jeśli chcesz prostszy i szybszy pokaz.

### `Walkthrough bits (0 = off)`
Pokazuje szczegółowy przebieg BB84.

Jak używać:
- ustaw `8` lub `16`, jeśli chcesz tłumaczyć projekt krok po kroku,
- ustaw `0`, jeśli chcesz tylko końcowe statystyki.

## 4. Jak przejść przez aplikację krok po kroku

## Wariant 1: najprostszy pokaz działania
Ustaw:
- `n = 1024`
- `p_eve = 0.0`
- `p_noise = 0.0`
- `steps = 8`
- `seed = 1`
- `R grid = 0.3,0.5,0.7,0.9,1.1,1.3`
- `maxiter = 200`
- `reps = 2`
- `Force XOR = off`
- `Generate QBER heatmap = off`
- `Walkthrough bits = 8`

### Co powinieneś zobaczyć
- niski `QBER`,
- komunikat, że kanał jest bezpieczny,
- aktywne wyniki `VQE`,
- działające szyfrowanie.

### Co to znaczy
To jest zdrowy, poprawny przebieg całego pipeline'u.

## Wariant 2: pokaż wpływ podsłuchu
Zostaw wszystko tak samo, ale ustaw:
- `p_eve = 0.5`

### Co powinieneś zobaczyć
- wzrost `QBER`,
- gorszą jakość kanału,
- możliwe zablokowanie dalszych etapów, jeśli wynik przekroczy próg.

### Co to znaczy
Projekt pokazuje, że ingerencja w kanał zostawia ślad statystyczny.

## Wariant 3: pokaż wpływ samego szumu
Ustaw:
- `p_eve = 0.0`
- `p_noise = 0.05` albo `0.1`

### Co powinieneś zobaczyć
- `QBER` wzrośnie nawet bez Eve.

### Co to znaczy
Wysoki błąd nie zawsze oznacza atak. Czasem problemem jest sam kanał.

## Wariant 4: pokaż heatmapę
Ustaw:
- `Generate QBER heatmap = on`

### Co powinieneś zobaczyć
- mapę kolorów zależną od `p_eve` i `p_noise`.

### Co to znaczy
Heatmapa pokazuje wszystkie kombinacje ataku i szumu, zamiast tylko jednego przebiegu.

## Wariant 5: pokaż walkthrough BB84
Ustaw:
- `Walkthrough bits = 8`

### Co powinieneś zobaczyć
- tabelę z kolejnymi bitami, bazami i wynikami.

### Co to znaczy
To najlepszy wariant do tłumaczenia projektu osobie początkującej.

## Wariant 6: pokaż kanał niebezpieczny
Ustaw:
- `p_eve = 1.0`
- albo `p_noise` na większą wartość

### Co powinieneś zobaczyć
- duży `QBER`,
- komunikat, że kanał jest niebezpieczny,
- brak przejścia do `VQE`,
- brak szyfrowania.

### Co to znaczy
To nie jest błąd programu. To poprawna logika bezpieczeństwa projektu.

## Wariant 7: pokaż tryb awaryjny szyfrowania
Ustaw:
- `Force XOR = on`

### Co powinieneś zobaczyć
- w zakładce `Security` tryb `XOR`.

### Co to znaczy
Projekt nadal działa, ale używa słabszego szyfrowania demonstracyjnego.

## 5. Jak czytać zakładkę `BB84`

## Metryka `QBER (no attack)`
To błąd kanału bez Eve.

Jak interpretować:
- niski wynik oznacza, że kanał sam z siebie jest w porządku,
- wysoki wynik oznacza szum albo zbyt mało prób.

## Metryka `QBER (full attack)`
To błąd przy pełnym przechwyceniu kanału.

Jak interpretować:
- pokazuje, jak bardzo idealny atak Eve psuje komunikację,
- służy jako punkt porównawczy.

## `Threshold`
To próg bezpieczeństwa.

Jak interpretować:
- poniżej progu system traktuje kanał jako bezpieczny,
- powyżej progu blokuje dalsze etapy.

## Wykres `QBER vs Eve`
Jak czytać:
- oś X: siła ataku Eve,
- oś Y: poziom błędu.

Co mówi:
- im większy atak, tym większy błąd.

## Heatmapa
Jak czytać:
- oś X: `p_eve`,
- oś Y: `p_noise`,
- kolor: `QBER`.

Co mówi:
- gdzie kanał jest zdrowy,
- gdzie kanał robi się podejrzany,
- gdzie kanał jest wyraźnie zły.

## Walkthrough
Jak czytać:
- patrzysz na pojedyncze przypadki zamiast tylko na końcową statystykę.

Co mówi:
- jak Alice koduje bity,
- jak Bob mierzy,
- kiedy pozycja zostaje zachowana,
- skąd biorą się zgodności i niezgodności.

## 6. Jak czytać zakładkę `VQE H2`

## Wykres energii
Jak czytać:
- oś X to długość wiązania `R`,
- oś Y to energia.

Co oznaczają linie:
- `VQE` to wynik przybliżony,
- `Exact` to wynik dokładny.

Jak interpretować:
- jeśli linie są blisko, `VQE` działa dobrze,
- minimum energii odpowiada najbardziej stabilnej konfiguracji.

## Wykres błędu
Jak czytać:
- pokazuje `|E_vqe - E_exact|`.

Jak interpretować:
- mały błąd jest dobry,
- większy błąd znaczy, że przybliżenie było gorsze.

## Tabela wyników
Jak czytać:
- `R (Å)` to długość wiązania,
- `E_vqe` to wynik z algorytmu,
- `E_exact` to rozwiązanie dokładne,
- `|error|` to różnica między nimi.

## 7. Jak czytać zakładkę `Security`

## `Encryption`
Mówi, czy użyto `AES-CTR`, czy `XOR`.

## `Raw key bytes`
To długość klucza zbudowanego bezpośrednio z bitów `BB84`.

## `Derived key bytes`
To długość finalnego klucza użytego w szyfrowaniu.

## Komunikat o round-trip
Oznacza:
- zaszyfrowaliśmy dane,
- odszyfrowaliśmy je,
- odzyskaliśmy dokładnie to samo.

To jest potwierdzenie, że technicznie szyfrowanie działa poprawnie.

## 8. Co oznaczają wszystkie główne warianty programu

## Kanał dobry, brak Eve, brak szumu
Interpretacja:
- pełny, wzorcowy przebieg,
- cały projekt działa od początku do końca.

## Kanał dobry, lekki szum
Interpretacja:
- projekt pokazuje realizm,
- małe błędy są normalne.

## Kanał z wyraźnym podsłuchem
Interpretacja:
- `QBER` rośnie,
- protokół wykrywa ingerencję.

## Kanał z dużym szumem
Interpretacja:
- też może zostać odrzucony,
- nie każdy zły kanał oznacza atakującego.

## Kanał odrzucony
Interpretacja:
- program poprawnie zatrzymuje pipeline,
- bezpieczeństwo ma pierwszeństwo przed dalszym przetwarzaniem.

## Dobry kanał i słaby wynik `VQE`
Interpretacja:
- problem nie leży w BB84,
- trzeba patrzeć na `reps`, `maxiter` albo dobrane punkty `R`.

## Dobry kanał i dobry wynik `VQE`
Interpretacja:
- cały pipeline działa poprawnie,
- to najlepszy wariant do pokazu końcowego.

## 9. Najlepsza kolejność pokazywania projektu na żywo
1. Pokaż ustawienia domyślne i czysty kanał.
2. Pokaż walkthrough dla kilku bitów.
3. Pokaż wykres `QBER vs Eve`.
4. Pokaż krzywą energii `H2`.
5. Pokaż wykres błędu.
6. Pokaż zakładkę `Security`.
7. Na końcu zwiększ `p_eve` i pokaż, że projekt blokuje dalsze etapy.

## 10. Najkrótsze podsumowanie dla użytkownika
Jeśli masz zapamiętać tylko jedną rzecz, to tę:

> W Streamlit najpierw patrzysz, czy `QBER` jest niski. Jeśli tak, przechodzisz do wyników `VQE`. Jeśli nie, projekt celowo zatrzymuje się, bo kanał jest uznany za zbyt ryzykowny.
