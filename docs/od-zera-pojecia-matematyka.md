# `quantumDUO` od zera: pojęcia, intuicja i matematyka

## 1. Dla kogo jest ten dokument
Ten dokument zakłada, że nie umiesz nic albo prawie nic z:
- kryptografii,
- informatyki kwantowej,
- chemii kwantowej,
- matematyki używanej w tym projekcie.

Czyli jeśli widzisz słowo `bit Alice`, `QBER`, `ansatz`, `Hamiltonian` albo `AES-CTR` i nie wiesz, co to jest, to właśnie od tego miejsca zaczynamy.

## 2. Najpierw najprościej: co robi projekt
Projekt robi trzy rzeczy:

1. Sprawdza, czy kanał komunikacji wygląda na bezpieczny.
2. Jeśli wygląda dobrze, liczy energię cząsteczki `H2`.
3. Na końcu szyfruje wynik.

To jest cała historia projektu.

## 3. Co to jest bit
Bit to najmniejsza porcja informacji.

Bit może mieć tylko jedną z dwóch wartości:
- `0`
- `1`

Przykład:
- odpowiedź tak/nie,
- włączone/wyłączone,
- prawda/fałsz.

W zwykłym komputerze wszystko ostatecznie opiera się na bitach.

## 4. Co to jest „bit Alice”
W tym projekcie Alice to jedna ze stron komunikacji.

`Bit Alice` to po prostu:

> wartość `0` albo `1`, którą Alice chce zakodować i wysłać.

Czyli jeśli w tabeli widzisz:
- `alice_bit = 0`, to znaczy, że Alice chciała wysłać `0`,
- `alice_bit = 1`, to znaczy, że Alice chciała wysłać `1`.

## 5. Skąd bierze się bit Alice
Bit Alice nie jest wpisywany ręcznie. Program go losuje.

Dlaczego?
- bo BB84 opiera się na losowości,
- dzięki temu nie da się łatwo przewidywać wysyłanych danych,
- losowy klucz jest podstawą bezpiecznej komunikacji.

## 6. Co to jest Bob
Bob to druga strona komunikacji.

Jego zadanie:
- odebrać to, co wysyła Alice,
- zmierzyć stan,
- spróbować odtworzyć wysłany bit.

## 7. Co to jest Eve
Eve to podsłuchiwacz.

Jej zadanie:
- przechwycić komunikację,
- odczytać informację,
- najlepiej zrobić to tak, żeby Alice i Bob się nie zorientowali.

W `BB84` cała idea polega na tym, że Eve nie da się ukryć idealnie, bo sam pomiar może psuć stan kwantowy.

## 8. Co to jest baza
W projekcie pojawia się pojęcie bazy `Z` i `X`.

Na poziomie intuicji:

> baza to sposób, w jaki kodujemy albo mierzymy informację.

W projekcie używamy dwóch baz:
- `Z`
- `X`

To są dwa różne „układy odniesienia” dla tej samej informacji.

## 9. Dlaczego baza jest ważna
W BB84 nie wystarczy znać sam bit.

Trzeba też wiedzieć:
- w jakiej bazie Alice go zakodowała,
- w jakiej bazie Bob go mierzył.

Jeśli Bob mierzy w tej samej bazie, ma dużą szansę dostać poprawny wynik.
Jeśli mierzy w innej bazie, wynik może być losowy.

To właśnie daje bezpieczeństwo.

## 10. Co to jest kubit
Kubit to kwantowy odpowiednik bitu.

Nie będziemy tu zaczynać od pełnej fizyki. Na potrzeby projektu wystarczy zapamiętać:

- bit klasyczny to `0` albo `1`,
- kubit to obiekt kwantowy, który można przygotować i zmierzyć.

W BB84 kubit przenosi informację od Alice do Boba.

## 11. Co oznaczają stany `|0>`, `|1>`, `|+>`, `|->`
To sposoby zapisania stanu kubitu.

W projekcie:
- `|0>` i `|1>` należą do bazy `Z`,
- `|+>` i `|->` należą do bazy `X`.

Najważniejsza intuicja:
- ten sam bit można zakodować na dwa różne sposoby,
- właśnie to utrudnia podsłuch.

## 12. Jak działa BB84 po ludzku

### Krok 1
Alice losuje:
- bit,
- bazę.

### Krok 2
Alice koduje bit do stanu kwantowego i wysyła go Bobowi.

### Krok 3
Bob losuje bazę pomiaru i mierzy to, co dostał.

### Krok 4
Alice i Bob ujawniają sobie tylko bazy, ale nie ujawniają samych bitów.

### Krok 5
Zostawiają tylko te przypadki, gdzie ich bazy były zgodne.

### Krok 6
Sprawdzają, ile mają błędów. Tym właśnie jest `QBER`.

## 13. Co to jest `QBER`
`QBER` to `Quantum Bit Error Rate`.

Po polsku:

> odsetek błędnych bitów po odsianiu pozycji z niezgodnymi bazami.

To jest jedna z najważniejszych rzeczy w całym projekcie.

## 14. Po co liczymy `QBER`
Liczymy `QBER`, bo chcemy wiedzieć:
- czy kanał wygląda normalnie,
- czy Eve mogła ingerować,
- czy poziom błędów nie jest zbyt duży.

Jeśli `QBER` jest niski, kanał wygląda dobrze.
Jeśli `QBER` jest wysoki, coś jest nie tak.

## 15. Jak policzony jest `QBER`
Załóżmy, że po odsianiu zostało 10 bitów.

Jeśli:
- 9 bitów jest zgodnych,
- 1 bit jest różny,

to:

`QBER = 1 / 10 = 0.1 = 10%`

Ogólny wzór:

`QBER = liczba niezgodnych bitów / liczba wszystkich zachowanych bitów`

## 16. Co oznacza próg `0.11`
W projekcie jest próg:

`QBER_SECURITY_THRESHOLD = 0.11`

Czyli 11%.

Znaczenie praktyczne:
- jeśli `QBER <= 0.11`, kanał uznajemy za wystarczająco bezpieczny,
- jeśli `QBER > 0.11`, uznajemy, że ryzyko jest za duże.

To jest bardzo ważne, bo od tego zależy, czy projekt przejdzie do następnych etapów.

## 17. Co to znaczy „kanał jest bezpieczny”
To nie znaczy, że jest magicznie idealny.

To znaczy:
- poziom błędów nie wygląda groźnie,
- nie widać silnych oznak podsłuchu albo zbyt dużego zakłócenia,
- można warunkowo przejść dalej.

## 18. Co to jest szum
Szum to każde zakłócenie, które psuje informację, nawet jeśli nie ma atakującego.

W tym projekcie szum jest modelowany prosto:
- czasem bit zmienia się przez zakłócenie kanału.

Czyli wysoki `QBER` może wynikać z:
- Eve,
- szumu,
- albo obu rzeczy naraz.

## 19. Co to jest wykres `QBER vs Eve`
To wykres pokazujący:
- jak zmienia się `QBER`,
- kiedy zmieniamy siłę ataku Eve.

Jeśli wszystko działa sensownie:
- mały atak daje mały błąd,
- większy atak daje większy błąd.

## 20. Co to jest heatmapa
Heatmapa to mapa kolorów.

Tutaj pokazuje:
- oś X: siła ataku Eve,
- oś Y: poziom szumu,
- kolor: wartość `QBER`.

Po co to jest:
- żeby naraz zobaczyć dużo wariantów zachowania kanału.

## 21. Co to jest `VQE`
`VQE` to `Variational Quantum Eigensolver`.

Brzmi ciężko, ale intuicja jest taka:

> chcemy znaleźć najniższą energię badanego układu.

W naszym przypadku układem jest cząsteczka `H2`.

## 22. Co to jest energia układu
Energia w fizyce i chemii mówi, jak „korzystny” albo „stabilny” jest dany stan.

W uproszczeniu:
- niższa energia zwykle oznacza bardziej stabilny stan,
- wyższa energia oznacza stan mniej korzystny.

Dlatego szukamy minimum.

## 23. Co to jest `H2`
`H2` to cząsteczka wodoru:
- dwa protony,
- dwa elektrony.

To bardzo popularny przykład w chemii kwantowej, bo jest mały i nadaje się do demonstracji.

## 24. Co to jest długość wiązania `R`
To odległość między atomami w cząsteczce.

Jeśli zmieniamy `R`, zmienia się też energia.

Dlatego projekt liczy energię nie dla jednej liczby, ale dla wielu wartości `R`.

## 25. Co to jest krzywa energii
To wykres:

- oś X: długość wiązania `R`,
- oś Y: energia.

Po co to jest:
- żeby zobaczyć, przy jakiej odległości cząsteczka jest najbardziej stabilna.

## 26. Co to jest minimum krzywej
Minimum krzywej to najniższy punkt wykresu.

Znaczenie:
- to najbardziej stabilna konfiguracja cząsteczki w tym modelu.

## 27. Co to jest Hamiltonian
Hamiltonian to matematyczny obiekt opisujący energię układu.

Najprostsza intuicja:

> jeśli znamy Hamiltonian, możemy policzyć energię różnych stanów.

W tym projekcie Hamiltonian jest uproszczony do małego modelu 2-kubitowego.

## 28. Co to jest stan próbny
W `VQE` nie próbujemy od razu zgadnąć idealnego rozwiązania.

Zamiast tego tworzymy stan próbny, czyli:

> kandydat na rozwiązanie.

Potem sprawdzamy, jaką ma energię.

## 29. Co to jest ansatz
Ansatz to sposób budowania stanu próbnego.

W tym projekcie ansatz to parametryzowany obwód kwantowy.

Czyli:
- mamy obwód,
- ma on parametry,
- zmieniamy parametry,
- patrzymy, czy energia spada.

## 30. Co to jest optymalizacja
Optymalizacja to proces poprawiania parametrów tak, aby wynik był jak najlepszy.

Tutaj:
- celem jest jak najniższa energia,
- optymalizator próbuje kolejnych ustawień parametrów,
- wybiera lepsze.

## 31. Co to znaczy `Exact`
`Exact` to wynik dokładny.

W projekcie liczymy go klasycznie, żeby mieć punkt odniesienia.

Znaczenie:
- `VQE` daje przybliżenie,
- `Exact` mówi nam, jak blisko prawdy jesteśmy.

## 32. Co to jest błąd `|E_vqe - E_exact|`
To różnica między:
- wynikiem przybliżonym,
- wynikiem dokładnym.

Jeśli różnica jest mała, to dobrze.

## 33. Co to jest wartość bezwzględna
Wartość bezwzględna oznacza, że nie interesuje nas znak, tylko wielkość różnicy.

Przykłady:
- `|3| = 3`
- `|-3| = 3`

Czyli:
- `|E_vqe - E_exact|` mówi, jak bardzo te liczby się różnią,
- bez pytania, która jest większa.

## 34. Co to jest `SHA-256`
To funkcja skrótu.

Najprościej:
- bierze dane wejściowe,
- robi z nich wynik o stałej długości.

W tym projekcie:
- bierze materiał kluczowy z `BB84`,
- daje 32-bajtowy klucz do `AES-256`.

## 35. Co to jest `AES-CTR`
To sposób szyfrowania danych.

Najprościej:
- bierzesz dane,
- bierzesz klucz,
- szyfrujesz tak, by bez klucza nie dało się łatwo odczytać treści.

W projekcie:
- szyfrujemy wynik `VQE`.

## 36. Co to jest `XOR`
`XOR` to bardzo prosta operacja logiczna.

Najważniejsza własność:

`A XOR K XOR K = A`

Czyli:
- jeśli zaszyfrujesz dane przez `XOR` z kluczem,
- a potem jeszcze raz użyjesz tego samego klucza,
- odzyskasz oryginał.

W projekcie to tylko tryb awaryjny.

## 37. Jaka matematyka pojawia się w projekcie
Matematyka w projekcie nie jest jedna, tylko kilka rodzajów naraz:

- rachunek prawdopodobieństwa,
- średnia i procent błędów,
- podstawy algebry liniowej,
- pojęcie minimum funkcji,
- różnica między wynikiem przybliżonym i dokładnym.

## 38. Matematyka BB84
Tu najważniejsze są:
- losowość,
- prawdopodobieństwo,
- liczenie błędów.

### Przykład
Jeśli Alice i Bob zachowali 100 bitów, a 7 z nich się różni:

`QBER = 7 / 100 = 0.07 = 7%`

To jest cała najważniejsza matematyka pierwszej fazy.

## 39. Matematyka VQE
Tutaj najważniejsze są:
- funkcja energii,
- minimalizacja,
- porównanie z wynikiem dokładnym.

### Intuicja
Masz wzgórza i doliny.

Szukasz najniższego punktu doliny.

To właśnie robi optymalizator dla energii.

## 40. Matematyka wykresu błędu
Jeśli:
- `E_vqe = -1.05`
- `E_exact = -1.08`

to:

`error = |-1.05 - (-1.08)| = |0.03| = 0.03`

Czyli błąd wynosi `0.03`.

## 41. Co oznacza „wynik jednego etapu wpływa na drugi”
To jedna z najważniejszych rzeczy w projekcie.

Nie jest tak, że:
- BB84 działa osobno,
- VQE działa osobno,
- szyfrowanie działa osobno.

U nas:
- `QBER` decyduje, czy w ogóle wolno iść dalej,
- klucz z `BB84` służy do szyfrowania wyników `VQE`.

To właśnie skleja projekt w jedną całość.

## 42. Jak czytać tabelę walkthrough
Jeśli widzisz kolumny:
- `alice_bit`
- `alice_basis`
- `bob_basis`
- `bob_bit`
- `kept`

to czytaj je tak:

### `alice_bit`
Co Alice chciała wysłać.

### `alice_basis`
W jaki sposób Alice to zakodowała.

### `bob_basis`
W jaki sposób Bob próbował to odczytać.

### `bob_bit`
Co Bob finalnie dostał po pomiarze.

### `kept`
Czy ten przypadek został zachowany do dalszego liczenia.

Jeśli `kept = 1`, to baza Alice i Boba była zgodna.
Jeśli `kept = 0`, to przypadek jest odrzucany.

## 43. Dlaczego część wyników jest odrzucana
Bo w BB84 nie wolno mieszać razem pomiarów wykonanych w różnych bazach.

Tylko zgodne bazy dają sensowny materiał do porównania i budowy klucza.

## 44. Dlaczego projekt może zatrzymać się przed `VQE`
Bo bezpieczeństwo jest tu ważniejsze niż samo obliczenie.

Jeśli `QBER` jest za duży, aplikacja mówi:

> ten kanał jest zbyt ryzykowny, nie idziemy dalej.

To jest poprawne zachowanie projektu.

## 45. Co powinieneś zapamiętać na sam koniec
Jeśli nic więcej nie zostanie, zapamiętaj te zdania:

- bit to `0` albo `1`,
- bit Alice to informacja, którą Alice chce wysłać,
- baza mówi, w jaki sposób informacja jest zakodowana albo mierzona,
- `QBER` mówi, ile błędów jest w komunikacji,
- `VQE` szuka najniższej energii układu,
- `Exact` to wynik dokładny,
- `AES-CTR` szyfruje wynik końcowy,
- cały projekt działa jako jeden ciąg: bezpieczeństwo, obliczenie, zabezpieczenie wyniku.
