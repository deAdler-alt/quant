# PEŁNY SKRYPT DLA PRELEGENTÓW (WERSJA SŁOWO W SŁOWO)

## Założenia wspólne

- Ten dokument ma być czytany praktycznie jak scenariusz.
- Każdy prelegent dostaje pełny tekst i może go przeczytać bez improwizacji.
- Styl: prosto, zrozumiale, ale merytorycznie poprawnie.

## Podział na prelegentów

1. **Kamil** - Slajdy 1-4 (wstęp i architektura)
2. **Dominik** - Slajdy 5-6 (BB84 i QBER)
3. **Marcin** - Slajdy 7-8 (VQE i Hamiltonian)
4. **Ola** - Slajdy 9-10 (biblioteki i szyfrowanie)
5. **Mateusz** - Slajdy 11-18 (demo i zakończenie)

---

## PRELEGENT 1 - Kamil (Slajdy 1-4)

### Slajd 1 - Strona tytułowa

**Tekst do powiedzenia słowo w słowo:**

"Dzień dobry Państwu. Nazywam się Kamil i w imieniu naszego zespołu zapraszam na prezentację projektu QuantumDUO.  
Naszym celem było zbudowanie jednej, spójnej aplikacji, która łączy dwa obszary: bezpieczeństwo komunikacji kwantowej oraz obliczenia chemiczne wykonywane metodami kwantowymi.  
W praktyce wygląda to tak: najpierw sprawdzamy, czy kanał jest bezpieczny, następnie liczymy energię cząsteczki wodoru, a na końcu zabezpieczamy wynik szyfrowaniem."

### Slajd 2 - Agenda

**Tekst do powiedzenia słowo w słowo:**

"Przejdziemy przez prezentację krok po kroku.  
Najpierw pokażemy, po co powstał ten projekt i jak jest zbudowany.  
Następnie wyjaśnimy, jak działa etap bezpieczeństwa, czyli BB84 i wskaźnik QBER.  
Później opowiemy o etapie obliczeniowym VQE, czyli o tym, jak wyznaczamy energię cząsteczki H2.  
Potem omówimy użyte biblioteki i warstwę klasycznego szyfrowania.  
Na końcu pokażemy demo aplikacji Streamlit i podsumujemy najważniejsze wnioski."

### Slajd 3 - Motywacja i cel projektu

**Tekst do powiedzenia słowo w słowo:**

"Dlaczego zrobiliśmy ten projekt?  
Bardzo często projekty kwantowe kończą się na samym obliczeniu i pomijają temat bezpieczeństwa danych.  
My chcieliśmy pokazać pełny łańcuch: od bezpieczeństwa kanału do bezpiecznego wyniku końcowego.  
Dlatego przyjęliśmy prostą zasadę: jeśli kanał nie jest bezpieczny, nie uruchamiamy dalszych obliczeń.  
To oznacza, że bezpieczeństwo nie jest dodatkiem, tylko warunkiem koniecznym."

### Slajd 4 - Architektura

**Tekst do powiedzenia słowo w słowo:**

"Architektura projektu jest modułowa.  
Plik `app.py` odpowiada za interfejs użytkownika i sterowanie przepływem.  
Plik `bb84.py` odpowiada za etap bezpieczeństwa kanału.  
Plik `vqe_h2.py` odpowiada za obliczenia energii cząsteczki H2.  
Plik `crypto_utils.py` odpowiada za szyfrowanie danych.  
Najważniejsza idea architektury jest taka: każdy moduł robi jedną rzecz, więc kod jest czytelny i łatwy do utrzymania."

### Wizualne tłumaczenie koncepcji (do pokazania i omówienia)

```text
Użytkownik -> app.py -> bb84.py -> [QBER <= 0.11 ?]
                               TAK -> vqe_h2.py -> crypto_utils.py -> Wynik
                               NIE -> STOP
```

### Najważniejsze zdania do podkreślenia

- **To jest jeden pipeline, a nie trzy niezależne dema.**
- **Bezpieczeństwo jest bramką wejściową całego systemu.**

---

## PRELEGENT 2 - Dominik (Slajdy 5-6)

### Slajd 5 - BB84

**Tekst do powiedzenia słowo w słowo:**

"Teraz przechodzimy do pierwszego etapu, czyli do BB84.  
BB84 to protokół kwantowej dystrybucji klucza.  
W tym protokole mamy trzy role: Alice, Bob i Eve.  
Alice to nadawca, Bob to odbiorca, a Eve to podsłuchiwacz.  
Alice losuje bity, czyli zera i jedynki, koduje je i wysyła do Boba.  
Bob mierzy otrzymane sygnały.  
Jeśli Eve próbuje podsłuchiwać, wprowadza dodatkowe błędy.  
I właśnie te błędy są dla nas sygnałem, że kanał może być zagrożony."

### Slajd 6 - QBER

**Tekst do powiedzenia słowo w słowo:**

"Ślad po podsłuchu mierzymy za pomocą QBER.  
QBER to skrót od Quantum Bit Error Rate, czyli po prostu procent błędnych bitów.  
Liczymy go bardzo prosto: liczba błędnych bitów podzielona przez liczbę bitów, które porównujemy.  
W naszym projekcie ustawiliśmy próg bezpieczeństwa na poziomie 11 procent.  
Jeśli QBER jest mniejszy lub równy 11 procent, kanał uznajemy za wystarczająco bezpieczny i przechodzimy dalej.  
Jeśli QBER przekracza 11 procent, system zatrzymuje dalsze etapy."

### Wizualne tłumaczenie koncepcji

```text
Alice (bit 0/1) -----> kanał -----> Bob
             \-----> Eve (podsłuch) ----/

Więcej podsłuchu lub szumu => więcej błędów => wyższy QBER
```

### Mini-objaśnienie dla laików (gdy padnie pytanie)

- **Bit** to 0 albo 1.
- **Bit Alice** to informacja, którą Alice chce wysłać.
- **QBER** to procent niezgodności między tym, co wysłała Alice i co odczytał Bob.

### Najważniejsze zdania do podkreślenia

- **QBER jest miernikiem jakości i bezpieczeństwa kanału.**
- **To QBER decyduje, czy projekt uruchomi dalsze etapy.**

---

## PRELEGENT 3 - Marcin (Slajdy 7-8)

### Slajd 7 - VQE

**Tekst do powiedzenia słowo w słowo:**

"Gdy kanał przejdzie test bezpieczeństwa, uruchamiamy etap obliczeniowy.  
Tutaj używamy algorytmu VQE.  
VQE to skrót od Variational Quantum Eigensolver.  
Najprościej mówiąc, to algorytm, który szuka najniższej energii badanego układu.  
W naszym projekcie tym układem jest cząsteczka wodoru H2.  
Można to porównać do szukania najniższego punktu w terenie: algorytm sprawdza różne ustawienia i dąży do minimum."

### Slajd 8 - Hamiltonian i wynik dokładny

**Tekst do powiedzenia słowo w słowo:**

"Żeby policzyć energię, potrzebujemy opisu matematycznego układu.  
Ten opis nazywa się Hamiltonian.  
Hamiltonian mówi nam, jak zachowuje się energia cząsteczki dla różnych stanów.  
W naszym projekcie używamy uproszczonego modelu 2-kubitowego.  
Dlaczego 2-kubitowego? Bo to dobry kompromis: model jest szybki i nadaje się do demonstracji, a jednocześnie zachowuje sens fizyczny.  
Dodatkowo liczymy też wynik dokładny, czyli tak zwany Exact.  
Porównanie VQE z Exact pokazuje, jak dobre jest nasze przybliżenie."

### Wizualne tłumaczenie koncepcji

```text
Hamiltonian (opis energii) -> VQE (szukanie minimum) -> E_vqe
                                           |
                                           +-> E_exact (wynik dokładny)
                                           |
                                           +-> błąd = |E_vqe - E_exact|
```

### Mini-objaśnienie dla laików

- **Hamiltonian** to matematyczny „przepis” na energię układu.
- **VQE** szuka możliwie najniższej energii.
- **Exact** to wynik referencyjny, żeby nie ufać VQE „na ślepo”.

### Najważniejsze zdania do podkreślenia

- **VQE daje przybliżenie, a Exact pozwala ocenić jego jakość.**
- **Hamiltonian jest konieczny, bo bez niego nie umiemy policzyć energii.**

---

## PRELEGENT 4 - Ola (Slajdy 9-10)

### Slajd 9 - Użyte biblioteki i ich znaczenie

**Tekst do powiedzenia słowo w słowo:**

"Teraz krótko omówię narzędzia, których użyliśmy i dlaczego są ważne.  
Streamlit służy do interfejsu, czyli do panelu ustawień, zakładek i wykresów.  
Qiskit oraz Qiskit Aer służą do części kwantowej i symulacji obwodów.  
NumPy i SciPy obsługują obliczenia numeryczne i optymalizację.  
Matplotlib i Pandas odpowiadają za wizualizacje i tabele.  
Biblioteka Cryptography odpowiada za funkcje bezpieczeństwa, czyli SHA-256 i AES."

### Slajd 10 - Warstwa bezpieczeństwa klasycznego

**Tekst do powiedzenia słowo w słowo:**

"Po etapie BB84 mamy surowe bity.  
Najpierw zamieniamy je do postaci klucza bajtowego.  
Następnie używamy SHA-256, żeby uzyskać klucz o stałej długości 32 bajtów.  
Tego klucza używamy w szyfrowaniu AES-CTR, aby zabezpieczyć wyniki VQE.  
Na końcu robimy test poprawności: szyfrujemy, odszyfrowujemy i porównujemy wynik.  
Jeśli dane są identyczne po powrocie, wiemy, że technicznie wszystko działa poprawnie."

### Wizualne tłumaczenie koncepcji

```text
key_bits -> bits_to_key_bytes -> SHA-256 -> klucz 32B -> AES-CTR -> szyfrogram
                                                            |
                                                            +-> decrypt -> porównanie
```

### Mini-objaśnienie dla laików

- **SHA-256**: z danych wejściowych robi stałej długości skrót/klucz.
- **AES-CTR**: szyfr, który ukrywa treść danych.
- **Round-trip**: test „tam i z powrotem”.

### Najważniejsze zdania do podkreślenia

- **Każda biblioteka ma konkretną, uzasadnioną rolę.**
- **Szyfrowanie domyka projekt i zabezpiecza końcowy wynik.**

---

## PRELEGENT 5 - Mateusz (Slajdy 11-18)

### Slajd 11 - Plan demo

**Tekst do powiedzenia słowo w słowo:**

"Teraz pokażę działanie aplikacji na konkretnych scenariuszach.  
Najpierw wariant bezpieczny, potem wyniki VQE, następnie zakładkę Security, a później wariant z atakiem i wariant edukacyjny z tabelą bitów."

### Slajd 12 - Kanał bezpieczny

**Tekst do powiedzenia słowo w słowo:**

"W tym wariancie ustawiliśmy parametry tak, aby kanał był czysty: bez ataku i bez szumu.  
Widzimy niski QBER i zielony komunikat.  
To oznacza, że system uznał kanał za bezpieczny i pozwala przejść do dalszych etapów."

### Slajd 13 - Wyniki VQE

**Tekst do powiedzenia słowo w słowo:**

"Ponieważ kanał przeszedł test, widzimy wyniki VQE.  
Na wykresie energii obserwujemy minimum, czyli najbardziej stabilny punkt układu.  
Na wykresie błędu widzimy różnicę między wynikiem VQE i Exact.  
Im mniejsza ta różnica, tym lepiej działa przybliżenie."

### Slajd 14 - Security

**Tekst do powiedzenia słowo w słowo:**

"W zakładce Security widzimy tryb szyfrowania, rozmiar klucza i wynik testu round-trip.  
Widzimy również opcje pobrania danych w różnych formatach.  
To potwierdza, że wynik końcowy nie tylko jest policzony, ale także zabezpieczony."

### Slajd 15 - Kanał zagrożony

**Tekst do powiedzenia słowo w słowo:**

"Tutaj zwiększamy poziom ataku i zakłóceń.  
QBER rośnie wyraźnie powyżej progu bezpieczeństwa.  
System wyświetla ostrzeżenie i blokuje przejście do VQE oraz Security.  
To nie jest błąd programu, tylko poprawna reakcja bezpieczeństwa."

### Slajd 16 - Walkthrough

**Tekst do powiedzenia słowo w słowo:**

"W tabeli walkthrough widzimy pojedyncze przypadki.  
Kolumna `alice_bit` mówi, co wysłała Alice.  
`alice_basis` i `bob_basis` pokazują, w jakich bazach kodowano i mierzono.  
`bob_bit` pokazuje odczytany wynik.  
`kept` mówi, czy dany przypadek został zachowany do klucza."

### Slajd 17 - Podsumowanie

**Tekst do powiedzenia słowo w słowo:**

"Najważniejszy wniosek jest prosty.  
W tym projekcie bezpieczeństwo kanału steruje całym przepływem.  
Jeśli kanał jest bezpieczny, obliczamy i szyfrujemy wyniki.  
Jeśli nie jest bezpieczny, system zatrzymuje proces."

### Slajd 18 - Zakończenie

**Tekst do powiedzenia słowo w słowo:**

"Dziękujemy za uwagę.  
Jesteśmy gotowi odpowiedzieć na pytania dotyczące zarówno części bezpieczeństwa, jak i części obliczeniowej."

### Wizualne tłumaczenie koncepcji demo

```text
Scenariusz 1: QBER niski  -> VQE działa -> Security działa
Scenariusz 2: QBER wysoki -> STOP (brak dalszych etapów)
```

### Najważniejsze zdania do podkreślenia

- **Zatrzymanie procesu to zamierzona funkcja bezpieczeństwa.**
- **Demo pokazuje pełne zachowanie systemu: sukces i kontrolowane zatrzymanie.**

---

# Szybka ściąga dla całego zespołu

## Trzy zdania, które warto powtarzać

1. **Najpierw bezpieczeństwo kanału, potem obliczenia, na końcu szyfrowanie.**
2. **QBER jest bramką decyzyjną całego projektu.**
3. **VQE porównujemy z Exact, żeby potwierdzić jakość wyników.**

## Czego nie robić podczas wystąpienia

- Nie używać skrótów bez rozwinięcia i wyjaśnienia.
- Nie zakładać, że słuchacze znają pojęcia typu kubit, Hamiltonian, Ansatz.
- Nie przyspieszać zbyt mocno w slajdach matematycznych.

