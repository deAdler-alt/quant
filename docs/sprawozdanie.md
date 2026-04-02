# Sprawozdanie z projektu `quantumDUO`

## 1. Wstęp
Projekt `quantumDUO` został przygotowany jako demonstracja połączenia dwóch ważnych nurtów informatyki kwantowej: kwantowej kryptografii oraz kwantowej symulacji chemicznej. Główna idea polega na tym, aby najpierw sprawdzić bezpieczeństwo kanału komunikacyjnego przy pomocy protokołu `BB84`, a dopiero później wykonać właściwe obliczenia `VQE` dla cząsteczki wodoru `H2` i bezpiecznie przekazać wynik.

Takie zestawienie nie jest przypadkowe. W praktyce rozwój technologii kwantowych dotyczy jednocześnie dwóch obszarów: bezpiecznej komunikacji oraz przyspieszenia wybranych obliczeń naukowych. Projekt pokazuje, że oba te elementy można połączyć w jeden czytelny i interaktywny pipeline.

## 2. Cel projektu
Celem projektu było zbudowanie aplikacji, która:
- pozwala zasymulować działanie protokołu `BB84`,
- mierzy jakość kanału przez `QBER`,
- uruchamia symulację `VQE` tylko wtedy, gdy kanał jest uznany za bezpieczny,
- szyfruje wynik obliczeń kluczem pochodzącym z fazy `BB84`,
- udostępnia użytkownikowi całość przez prosty interfejs `Streamlit`.

Przyjęto przy tym, że aplikacja ma być:
- zrozumiała dydaktycznie,
- łatwa do pokazania podczas prezentacji,
- możliwa do uruchomienia lokalnie bez dostępu do rzeczywistego sprzętu kwantowego.

## 3. Założenia projektowe
Na początku przyjęto kilka istotnych założeń upraszczających:
- kanał kwantowy modelowany jest przez prosty schemat `intercept-resend` oraz dodatkowy szum typu `bit-flip`,
- bezpieczeństwo kanału oceniamy przez `QBER`,
- graniczny próg bezpieczeństwa przyjmujemy jako `0.11`,
- cząsteczka `H2` opisana jest uproszczonym, 2-kubitowym Hamiltonianem,
- algorytm `VQE` działa na symulatorze stanowym, a nie na fizycznym procesorze kwantowym,
- szyfrowanie wyników ma mieć charakter demonstracyjny, ale technicznie poprawny.

Takie założenia pozwalają skupić się na istocie rozwiązania zamiast na złożonych szczegółach sprzętowych.

## 4. Zastosowane narzędzia i biblioteki
Projekt został napisany w języku Python. Kluczowe biblioteki i ich rola są następujące:

- `streamlit` odpowiada za interfejs użytkownika.
- `numpy` realizuje obliczenia numeryczne, operacje na tablicach oraz część logiki bitowej.
- `matplotlib` generuje wykresy dla `QBER`, energii i błędu.
- `pandas` odpowiada za wygodną prezentację tabel.
- `qiskit` i `qiskit-aer` umożliwiają budowę obwodów kwantowych i ich lokalną symulację.
- `scipy` dostarcza optymalizator używany w `VQE`.
- `cryptography` realizuje szyfrowanie `AES-CTR` oraz skrót `SHA-256`.

Oprócz tego użyto modułów standardowej biblioteki Pythona, takich jak `json`, `csv`, `io`, `os`, `base64` oraz `functools`.

## 5. Opis rozwiązania

### 5.1 Faza pierwsza: BB84
W pierwszym etapie aplikacja uruchamia symulację `BB84`. Alice losuje bity i bazy, Bob losuje własne bazy pomiaru, a opcjonalnie w kanale może pojawić się Eve przechwytująca kubity z określonym prawdopodobieństwem. Dodatkowo modelowany jest prosty szum kanału.

Po wykonaniu pomiarów zachowywane są tylko te pozycje, w których baza Alice i Boba była zgodna. Na tej podstawie liczony jest `QBER`, czyli odsetek błędnych bitów po odsianiu.

Ta faza pełni dwie funkcje:
- buduje materiał kluczowy do dalszego wykorzystania,
- wykrywa, czy kanał jest wystarczająco bezpieczny do kontynuowania procesu.

### 5.2 Faza druga: VQE dla `H2`
Jeżeli kanał przejdzie test bezpieczeństwa, aplikacja uruchamia obliczenia `VQE` dla kilku długości wiązania `R`. Dla każdej z nich budowany jest 2-kubitowy Hamiltonian cząsteczki `H2`, a następnie wyznaczana jest energia:
- metodą wariacyjną `VQE`,
- metodą dokładną przez diagonalizację.

Pozwala to nie tylko uzyskać wynik, ale też od razu porównać jakość rozwiązania przybliżonego z punktem odniesienia.

### 5.3 Faza trzecia: szyfrowanie wyników
W ostatniej fazie bity uzyskane z `BB84` są przekształcane do postaci bajtowej, a następnie przetwarzane przez `SHA-256`, aby uzyskać 32-bajtowy klucz. Tym kluczem szyfrowany jest wynik `VQE` w trybie `AES-CTR`.

Jeżeli biblioteka kryptograficzna nie jest dostępna albo użytkownik wymusi tryb awaryjny, aplikacja może przełączyć się na prostsze szyfrowanie `XOR`. Rozwiązanie to nie jest bezpieczne produkcyjnie, ale pozwala zachować ciągłość demonstracji.

## 6. Dlaczego rozwiązanie działa

### 6.1 Uzasadnienie fazy BB84
BB84 działa, ponieważ pomiar stanu kwantowego w nieodpowiedniej bazie wprowadza zaburzenie. Oznacza to, że podsłuchująca Eve nie może niezauważalnie przechwycić informacji. Jeśli przechwytuje kubity, zwiększa `QBER`. Z kolei gdy `QBER` jest niski, można uznać, że kanał nie wykazuje śladów silnej ingerencji.

### 6.2 Uzasadnienie fazy VQE
VQE opiera się na zasadzie wariacyjnej. Dla danego Hamiltonianu każda energia policzona dla stanu próbnego jest nie mniejsza niż energia stanu podstawowego. Optymalizator dobiera więc parametry obwodu tak, aby tę energię minimalizować i możliwie zbliżyć się do rozwiązania dokładnego.

### 6.3 Uzasadnienie fazy szyfrowania
Jeżeli strony dysponują wspólnym materiałem kluczowym, mogą użyć go do szyfrowania danych. `SHA-256` pozwala doprowadzić klucz do odpowiedniego formatu dla `AES-256`, a `AES-CTR` daje poprawną technicznie metodę poufnego szyfrowania danych binarnych.

## 7. Wyniki i ich interpretacja
Projekt zwraca trzy grupy wyników:

- wykres `QBER` w funkcji prawdopodobieństwa ataku Eve,
- wykres energii `H2` w funkcji długości wiązania,
- wykres błędu `|E_vqe - E_exact|`.

Interpretacja tych wyników jest następująca:
- wzrost `p_eve` powinien zwiększać `QBER`,
- przy pełnym ataku `QBER` powinien zbliżać się do wartości charakterystycznej dla modelu `intercept-resend`,
- krzywa energii `H2` powinna mieć minimum w pobliżu fizycznej długości wiązania,
- mały błąd względem rozwiązania dokładnego oznacza, że ansatz i optymalizacja działają poprawnie.

Wyniki są więc zgodne z oczekiwaniami teoretycznymi dla modelu demonstracyjnego.

## 8. Najważniejsze zalety projektu
- Projekt łączy dwie różne klasy zastosowań obliczeń kwantowych w jeden spójny scenariusz.
- Aplikacja działa interaktywnie i nadaje się do pokazu na żywo.
- Implementacja jest podzielona na czytelne moduły.
- Użytkownik otrzymuje zarówno wykresy, jak i dane do pobrania.
- Wynik `VQE` jest weryfikowany przez rozwiązanie dokładne.

## 9. Ograniczenia projektu
Projekt ma również wyraźne ograniczenia:
- model `BB84` jest uproszczony i nie zawiera pełnego toru `QKD`,
- nie zaimplementowano korekcji błędów ani privacy amplification,
- model chemiczny `H2` jest pretabelaryzowany i ma charakter edukacyjny,
- `AES-CTR` nie zapewnia integralności danych,
- tryb `XOR` należy traktować wyłącznie jako awaryjną funkcję demonstracyjną.

Ograniczenia te nie przekreślają wartości projektu, lecz wyznaczają granice jego interpretacji.

## 10. Możliwe rozwinięcia
W przyszłości projekt można rozszerzyć o:
- bardziej realistyczne modele szumu i ataków w `BB84`,
- korekcję błędów i privacy amplification,
- dokładniejsze generowanie Hamiltonianu dla większej liczby punktów `R`,
- użycie innych ansatzów i optymalizatorów w `VQE`,
- szyfrowanie zapewniające również integralność, np. `AES-GCM`,
- integrację z rzeczywistym backendem kwantowym.

## 11. Podsumowanie
Projekt `quantumDUO` realizuje założony cel: demonstruje pełny przepływ od kwantowej dystrybucji klucza, przez obliczenie energii cząsteczki wodoru, aż po bezpieczne przygotowanie wyniku do przekazania użytkownikowi. Zastosowane uproszczenia są świadome i uzasadnione dydaktycznie, a sama aplikacja dobrze nadaje się zarówno do nauki, jak i do prezentacji.

Najważniejszą wartością projektu jest pokazanie, że techniki kwantowe nie muszą być prezentowane w oderwaniu od siebie. W `quantumDUO` tworzą one jedną całość: bezpieczeństwo kanału wpływa na to, czy zostaną wykonane dalsze obliczenia, a wynik tych obliczeń jest następnie chroniony za pomocą klucza pochodzącego z fazy kwantowej.
