# `quantumDUO` od podstaw

## Po co jest ten projekt
Ten projekt ma pokazać jeden spójny scenariusz:
- najpierw sprawdzamy, czy kanał komunikacyjny jest bezpieczny,
- potem wykonujemy obliczenia kwantowe dla cząsteczki wodoru `H2`,
- na końcu szyfrujemy wynik i przygotowujemy go do przekazania.

Najkrócej:

> `BB84` sprawdza bezpieczeństwo, `VQE` liczy energię `H2`, a warstwa `Security` chroni wynik.

## Jakie są etapy projektu

### 1. Etap `BB84`
To etap kryptograficzny.

Program:
- losuje bity Alice,
- losuje bazy Alice,
- losuje bazy Boba,
- sprawdza, czy pojawia się Eve,
- liczy `QBER`.

Cel tego etapu:
- wykryć podsłuch lub zbyt duży szum,
- zbudować materiał kluczowy do szyfrowania.

### 2. Etap `VQE`
To etap obliczeniowy.

Program:
- bierze model cząsteczki `H2`,
- buduje uproszczony Hamiltonian 2-kubitowy,
- szuka najniższej energii dla kolejnych długości wiązania `R`.

Cel tego etapu:
- pokazać działanie algorytmu `VQE`,
- narysować krzywą energii cząsteczki.

### 3. Etap `Security`
To etap zabezpieczenia wyniku.

Program:
- bierze bity z `BB84`,
- robi z nich klucz,
- szyfruje wyniki `VQE`,
- daje użytkownikowi pliki do pobrania.

Cel tego etapu:
- domknąć cały pipeline,
- pokazać, że wynik obliczeń nie jest tylko wyświetlany, ale też bezpiecznie pakowany.

## Jak to się składa w jedną historię
Projekt nie składa się z trzech przypadkowych tematów.

To jedna zależność:

1. `BB84` odpowiada na pytanie: czy kanał jest wystarczająco bezpieczny?
2. Jeśli tak, uruchamiamy `VQE`.
3. Wynik `VQE` szyfrujemy kluczem pochodzącym z pierwszego etapu.

To oznacza, że wynik jednego etapu wpływa na następny.

## Jak uruchomić program

```bash
streamlit run app.py
```

Po uruchomieniu otwiera się aplikacja z panelem bocznym i trzema zakładkami:
- `BB84`,
- `VQE H2`,
- `Security`.

## Jak operować w Streamlit

## Panel boczny
To tutaj ustawiasz wszystko, co wpływa na wynik.

### Sekcja `BB84`

#### `n (raw rounds)`
Liczba rund BB84.

Jak rozumieć:
- mała liczba daje bardziej losowe i niestabilne wyniki,
- większa liczba daje lepszą statystykę.

Dobra intuicja:
- do prezentacji można używać `512` lub `1024`.

#### `Eve intercept probability`
Jak często Eve przechwytuje kubit.

Jak rozumieć:
- `0.0` oznacza brak podsłuchu,
- `1.0` oznacza, że Eve przechwytuje wszystko,
- większa wartość zwykle zwiększa `QBER`.

#### `Channel noise probability`
Jak bardzo kanał sam z siebie psuje dane.

Jak rozumieć:
- nawet bez Eve mogą pojawić się błędy,
- to pomaga pokazać, że wysoki `QBER` nie zawsze oznacza wyłącznie podsłuch.

#### `QBER sweep steps`
Liczba punktów na wykresie `QBER vs Eve`.

Jak rozumieć:
- im więcej punktów, tym gładszy wykres,
- ale obliczenia mogą być trochę wolniejsze.

#### `Seed`
Ziarno losowości.

Jak rozumieć:
- to pozwala powtórzyć te same wyniki,
- dobre do prezentacji, bo nie wszystko zmienia się przy każdym odświeżeniu.

### Sekcja `VQE`

#### `R grid (Å, comma-separated)`
Lista długości wiązania `H2`.

Jak rozumieć:
- każda liczba to jeden punkt, dla którego liczymy energię,
- z tych punktów powstaje wykres krzywej energii.

#### `Max optimizer iterations`
Liczba kroków optymalizatora klasycznego.

Jak rozumieć:
- większa liczba może poprawić wynik,
- ale wydłuża czas liczenia.

#### `Ansatz reps`
Głębokość ansatzu.

Jak rozumieć:
- większe `reps` daje bardziej złożony stan próbny,
- może poprawić dopasowanie, ale zwiększa liczbę parametrów.

### Sekcja `Encryption`

#### `Force XOR (no AES)`
Wymusza użycie prostego szyfrowania `XOR` zamiast `AES-CTR`.

Jak rozumieć:
- to nie jest tryb produkcyjny,
- służy raczej do demonstracji albo gdy biblioteka `cryptography` nie działa.

### Sekcja `Optional`

#### `Generate QBER heatmap`
Włącza heatmapę pokazującą wpływ ataku i szumu na `QBER`.

#### `Walkthrough bits (0 = off)`
Włącza tabelę pokazującą dokładnie, co stało się dla kolejnych bitów.

To jest najlepsza opcja, jeśli chcesz tłumaczyć projekt od podstaw.

## Co pokazuje zakładka `BB84`
To pierwszy i najważniejszy etap logiczny.

Tutaj zobaczysz:
- `QBER (no attack)`,
- `QBER (full attack)`,
- `Threshold`,
- wykres `QBER vs Eve`,
- opcjonalnie heatmapę,
- opcjonalnie walkthrough.

### Co znaczy `QBER (no attack)`
To błąd kanału bez podsłuchu.

Jak to rozumieć:
- jeśli jest niski, wszystko wygląda zdrowo,
- jeśli jest wysoki mimo braku Eve, problemem jest szum albo za mało rund.

### Co znaczy `QBER (full attack)`
To błąd kanału przy maksymalnym ataku Eve.

Jak to rozumieć:
- pokazuje, jak bardzo atak powinien psuć kanał,
- jest punktem odniesienia dla użytkownika.

### Co znaczy `Threshold`
To próg bezpieczeństwa.

W projekcie:
- jeśli `QBER <= 0.11`, kanał jest traktowany jako bezpieczny,
- jeśli `QBER > 0.11`, dalsze etapy są blokowane.

### Jak czytać wykres `QBER vs Eve`
Oś pozioma:
- prawdopodobieństwo przechwycenia przez Eve.

Oś pionowa:
- `QBER`.

Interpretacja:
- im bardziej rośnie udział Eve, tym bardziej zwykle rośnie `QBER`,
- to pokazuje sens fizyczny protokołu `BB84`.

### Jak czytać heatmapę
Heatmapa pokazuje:
- wpływ Eve,
- wpływ szumu,
- końcową jakość kanału.

Kolor oznacza poziom `QBER`.

Najprościej:
- chłodniejsze/niższe wartości są lepsze,
- cieplejsze/wyższe wartości oznaczają bardziej podejrzany lub uszkodzony kanał.

### Jak czytać walkthrough
To tabela edukacyjna.

Pokazuje dla każdej pozycji:
- bit Alice,
- bazę Alice,
- bazę Boba,
- bit Boba,
- czy pozycja została zachowana.

Po co to jest:
- żeby zobaczyć BB84 na poziomie pojedynczych przypadków,
- a nie tylko jako końcową statystykę.

## Co pokazuje zakładka `VQE H2`
To etap obliczeniowy.

Jeśli kanał był bezpieczny, program pokazuje:
- wykres energii,
- wykres błędu,
- tabelę wyników.

### Wykres energii
Pokazuje zależność energii od długości wiązania `R`.

Są tam zwykle dwie serie:
- `VQE`,
- `Exact`.

Jak to rozumieć:
- `Exact` to wynik dokładny,
- `VQE` to wynik przybliżony,
- jeśli linie są blisko siebie, to znaczy, że `VQE` działa dobrze.

### Wykres błędu
Pokazuje różnicę:

`|E_vqe - E_exact|`

Jak to rozumieć:
- mały błąd oznacza dobre dopasowanie,
- większy błąd oznacza słabszy punkt obliczeń.

### Tabela wyników
Pokazuje liczby stojące za wykresami:
- `R`,
- `E_vqe`,
- `E_exact`,
- `|error|`.

To przydaje się do omówienia konkretnych wartości na prezentacji.

## Co pokazuje zakładka `Security`
To etap końcowy.

Tutaj program:
- przygotowuje klucz,
- szyfruje wyniki,
- sprawdza, czy da się je poprawnie odszyfrować,
- udostępnia pliki do pobrania.

### Co oznacza `Encryption`
Pokazuje, czy użyto:
- `AES-CTR`,
- czy `XOR`.

### Co oznacza `Raw key bytes`
To liczba bajtów zbudowanych bezpośrednio z bitów `BB84`.

### Co oznacza `Derived key bytes`
To długość finalnego klucza użytego w szyfrowaniu.

Przy `AES` zwykle będzie to `32`, bo używany jest klucz 256-bitowy.

### Co oznacza komunikat o round-trip
To znaczy:
- zaszyfrowaliśmy dane,
- odszyfrowaliśmy je,
- dostaliśmy z powrotem to samo.

Czyli implementacja szyfrowania i odszyfrowania działa poprawnie.

## Co wyniki mówią o projekcie

### Jeśli `QBER` jest mały
To znaczy:
- kanał wygląda dobrze,
- aplikacja pozwala przejść do `VQE`,
- cały pipeline może zostać dokończony.

### Jeśli `QBER` jest duży
To znaczy:
- kanał jest podejrzany albo zbyt zaszumiony,
- projekt celowo wstrzymuje dalsze etapy,
- to jest ważna część logiki projektu, a nie błąd aplikacji.

### Jeśli `VQE` jest blisko `Exact`
To znaczy:
- algorytm wariacyjny dobrze przybliża wynik,
- model działa sensownie.

### Jeśli wykres błędu jest niski
To znaczy:
- ansatz i optymalizacja są wystarczające dla tego uproszczonego problemu.

## Jak najłatwiej tłumaczyć projekt na prezentacji
Najprostszy opis brzmi tak:

> Najpierw symulujemy bezpieczny kanał kwantowy przez `BB84`. Jeśli kanał przejdzie test jakości przez `QBER`, uruchamiamy `VQE` dla `H2`. Wynik tych obliczeń szyfrujemy kluczem pochodzącym z pierwszej fazy i udostępniamy użytkownikowi.

## Najważniejsze rzeczy do zapamiętania
- `BB84` odpowiada za bezpieczeństwo kanału.
- `QBER` jest wskaźnikiem jakości i bezpieczeństwa.
- `VQE` szuka najniższej energii `H2`.
- `Security` chroni wynik końcowy.
- `Streamlit` spina wszystko w jedną aplikację.

## Jak najlepiej pokazywać program na żywo

### Wariant prosty
Ustaw:
- `n = 1024`,
- `p_eve = 0.0`,
- `p_noise = 0.0`,
- `steps = 8`,
- `walkthrough bits = 8`.

Pokaż:
1. niski `QBER`,
2. tabelę walkthrough,
3. przejście do `VQE`,
4. wykres energii,
5. zakładkę `Security`.

### Wariant demonstracyjny
Potem zwiększ:
- `p_eve` do `0.5` albo `1.0`.

Pokaż:
1. że `QBER` rośnie,
2. że kanał może zostać uznany za niebezpieczny,
3. że logika projektu blokuje dalsze etapy.

To bardzo dobrze pokazuje, że projekt ma sens jako całość.
