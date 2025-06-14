# Sprawdzacz Miejsc KOLEO

Aplikacja webowa w Django do wyszukiwania połączeń kolejowych i sprawdzania dostępności wolnych miejsc w pociągach na podstawie danych z serwisu KOLEO.pl.


## Główne Funkcje

-   **Wyszukiwanie Połączeń**: Znajdź połączenia kolejowe na podstawie stacji początkowej, końcowej, daty i godziny.
-   **Sprawdzanie Miejsc w Czasie Rzeczywistym**: Aplikacja automatycznie sprawdza i wyświetla liczbę wolnych miejsc bezpośrednio w wynikach wyszukiwania.
-   **System Użytkowników**: Pełna obsługa rejestracji, logowania i wylogowywania.
-   **Personalizacja Profilu**: Zalogowani użytkownicy mogą:
    -   Ustawić domyślną stację początkową i końcową.
    -   Spersonalizować, które typy miejsc specjalnych (np. Wagon Ciszy, miejsce na rower) mają być uwzględniane w wynikach.

## Technologie

-   **Backend**: Django
-   **Frontend**: HTML, CSS, Bootstrap 5
-   **Baza Danych**: SQLite (domyślnie w Django)
-   **Zależności Python**: `requests`

## Instalacja i Uruchomienie

Aby uruchomić projekt lokalnie, postępuj zgodnie z poniższymi krokami:

1.  **Sklonuj repozytorium:**
    ```bash
    git clone https://github.com/pawelktk/koleo-seats-checker.git
    cd koleo-checker
    ```

2.  **Stwórz i aktywuj wirtualne środowisko (zalecane):**
    -   **Linux / macOS:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    -   **Windows:**
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Zainstaluj zależności:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Uruchom migracje Django:**
    Ten krok utworzy bazę danych i automatycznie wypełni ją danymi początkowymi (np. typami przedziałów specjalnych).
    ```bash
    python manage.py migrate
    ```

5.  **Uruchom serwer deweloperski:**
    ```bash
    python manage.py runserver
    ```

6.  **Otwórz aplikację w przeglądarce:**
    Przejdź na adres [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

## Ważna Uwaga

Aplikacja korzysta z **wewnętrznego, nieoficjalnego API** serwisu KOLEO.pl. Oznacza to, że:
-   Jest przeznaczona wyłącznie do celów edukacyjnych i osobistego użytku.
-   Jej działanie może zostać zakłócone lub całkowicie uniemożliwione w przypadku jakichkolwiek zmian w API wprowadzonych przez KOLEO.

## Struktura Projektu

-   `koleo_checker/`: Główny folder konfiguracyjny Django.
-   `checker/`: Aplikacja Django odpowiedzialna za główną logikę wyszukiwania i komunikacji z API KOLEO.
-   `users/`: Aplikacja Django obsługująca autentykację i profile użytkowników.
-   `templates/`: Główny folder z szablonami bazowymi i stroną błędu 404.

