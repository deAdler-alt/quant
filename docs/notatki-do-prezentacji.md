# Notatki do prezentacji projektu `quantumDUO`

## 1. Krótkie otwarcie
`quantumDUO` to projekt, który łączy dwa zastosowania informatyki kwantowej: bezpieczną komunikację i symulację chemiczną. Najpierw sprawdzamy, czy kanał komunikacyjny jest bezpieczny dzięki `BB84`, a dopiero potem uruchamiamy `VQE` dla cząsteczki wodoru i szyfrujemy wynik.

## 2. Co pokazuje projekt
- Jak działa protokół `BB84` i jak wykrywa podsłuch.
- Jak działa `VQE` na przykładzie cząsteczki `H2`.
- Jak wynik obliczeń może zostać zabezpieczony kluczem pochodzącym z fazy kwantowej.
- Jak całość można pokazać użytkownikowi w formie działającej aplikacji `Streamlit`.

## 3. Przepływ działania
Najprościej można powiedzieć to tak:

1. Użytkownik ustawia parametry w aplikacji.
2. Symulujemy `BB84` i liczymy `QBER`.
3. Jeśli `QBER` jest wystarczająco niski, uznajemy kanał za bezpieczny.
4. Uruchamiamy `VQE` dla kilku długości wiązania `H2`.
5. Wynik zapisujemy jako `JSON` i `CSV`, a dodatkowo szyfrujemy go kluczem z `BB84`.

## 4. Najważniejsze moduły
- `app.py` spina cały projekt i odpowiada za interfejs.
- `bb84.py` odpowiada za część kryptograficzną i pomiar `QBER`.
- `vqe_h2.py` liczy energię cząsteczki `H2`.
- `crypto_utils.py` odpowiada za szyfrowanie i obsługę klucza.

## 5. Co powiedzieć o BB84
BB84 polega na tym, że Alice wysyła bity zakodowane w dwóch różnych bazach kwantowych. Bob mierzy je w losowo wybranych bazach. Potem obie strony porównują tylko bazy i zostawiają te pozycje, gdzie baza była zgodna.

Najważniejsza intuicja:
- jeśli Eve podsłuchuje, musi mierzyć kubity,
- pomiar w złej bazie zaburza stan,
- to zwiększa `QBER`,
- więc podsłuch daje się wykryć statystycznie.

## 6. Co powiedzieć o `QBER`
`QBER` to odsetek błędnych bitów po odsianiu pozycji z niezgodnymi bazami. Im mniejszy `QBER`, tym lepsza jakość kanału. W projekcie przyjęliśmy próg `0.11`, czyli około 11 procent, jako granicę bezpieczeństwa inspirowaną klasyczną analizą BB84.

## 7. Co powiedzieć o VQE
`VQE` to algorytm hybrydowy:
- część kwantowa przygotowuje stan próbny,
- część klasyczna optymalizuje parametry tego stanu.

Szukamy stanu o jak najniższej energii dla Hamiltonianu cząsteczki `H2`. Dodatkowo porównujemy wynik z rozwiązaniem dokładnym przez diagonalizację, więc od razu widzimy, czy wynik `VQE` jest sensowny.

## 8. Co powiedzieć o wykresach

### Wykres `QBER`
Pokazuje, że im większe prawdopodobieństwo ataku Eve, tym większy błąd kanału. To jest najważniejszy argument, że model wykrywania podsłuchu działa.

### Krzywa energii `H2`
Pokazuje zależność energii od długości wiązania. Minimum tej krzywej odpowiada najbardziej stabilnej konfiguracji cząsteczki.

### Wykres błędu
Pokazuje różnicę między `E_vqe` i `E_exact`. Dzięki temu nie opieramy się wyłącznie na samym przybliżeniu, tylko mamy punkt odniesienia.

## 9. Co powiedzieć o szyfrowaniu
Z bitów pochodzących z `BB84` budujemy materiał kluczowy. Następnie przepuszczamy go przez `SHA-256`, żeby otrzymać 32-bajtowy klucz do `AES-256`. Wynik `VQE` szyfrujemy w trybie `AES-CTR`.

Ważna uwaga do powiedzenia:
- to rozwiązanie zapewnia poufność,
- ale nie daje integralności,
- więc w wersji produkcyjnej lepiej byłoby użyć `AES-GCM`.

## 10. Główne zalety projektu
- Łączy kryptografię kwantową i symulację kwantową w jednym pipeline.
- Ma działający interfejs i dobrze nadaje się do pokazu.
- Wyniki są czytelne i wizualne.
- Projekt jest modularny i łatwy do omówienia.

## 11. Ograniczenia, które warto uczciwie przyznać
- `BB84` jest uproszczoną symulacją.
- `H2` jest opisane małym, demonstracyjnym Hamiltonianem.
- `VQE` działa na symulatorze, nie na prawdziwym urządzeniu.
- `XOR` jest tylko awaryjnym trybem demonstracyjnym.
- Brakuje pełnego toru `QKD`, np. privacy amplification.

## 12. Gotowe odpowiedzi na typowe pytania

### Dlaczego próg `0.11`?
Bo jest to klasyczna granica bezpieczeństwa dla BB84 wynikająca z analizy Shora i Preskilla. W projekcie używamy jej jako jasnego kryterium decyzji, czy kontynuować dalsze obliczenia.

### Skąd bierze się wzrost `QBER`, gdy Eve podsłuchuje?
Bo Eve musi zmierzyć kubit, a jeśli wybierze złą bazę, zaburza stan. Bob może wtedy odczytać inny bit niż Alice.

### Dlaczego `VQE` działa?
Bo opiera się na zasadzie wariacyjnej. Dla każdego stanu próbnego możemy policzyć energię, a optymalizator szuka parametrów, które tę energię minimalizują.

### Dlaczego wybrano `H2`?
Bo to najprostsza i najczęściej pokazywana cząsteczka w demonstracjach chemii kwantowej. Daje się sprowadzić do małego modelu, który nadal ma sens fizyczny.

### Dlaczego `AES-CTR`, a nie `AES-GCM`?
Bo `AES-CTR` jest prosty do pokazania i dobrze nadaje się do demonstracji poufnego szyfrowania danych binarnych. Jednocześnie wiemy, że w systemie produkcyjnym lepsze byłoby rozwiązanie zapewniające też integralność.

### Po co porównanie `VQE` z wynikiem dokładnym?
Żeby pokazać, że algorytm wariacyjny daje sensowny wynik i nie jest tylko czarną skrzynką bez punktu odniesienia.

## 13. Propozycja zakończenia prezentacji
Projekt pokazuje, że technologie kwantowe można przedstawić jako jeden spójny proces: najpierw bezpiecznie uzgadniamy klucz, potem wykonujemy obliczenie kwantowe, a na końcu zabezpieczamy wynik. Dzięki temu `quantumDUO` dobrze nadaje się zarówno jako demonstracja techniczna, jak i materiał edukacyjny.
