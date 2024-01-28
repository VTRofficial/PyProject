import requests
import random
'''
Ehhez az API-hoz nem szükséges API kulcs. Ez a program egy játék, ahol a felhasználónak meg kell adnia egy adott 
ország fővárosát.
A felhasználónak lehetősége van megadni, hogy mennyi kérdésre kell válaszolnia, és hogy milyen kontinensen kell
a programnak országokat kiírni, a városokat angol nyelven kell megadni.
'''


def download_countries_from_api():
    api_url = "https://restcountries.com/v3.1/all"
    response = requests.get(api_url)
    countries_data = response.json()
    return countries_data


def get_countries_from_json(countries_data):
    return [country["name"]["common"] for country in countries_data]


def filter_countries_by_continent(countries_data, continent):
    return [country for country in countries_data if country.get("region") == continent]


def get_random_countries(countries_data, num_countries):
    num_countries = min(max(num_countries, 1), len(countries_data))
    # A program itt kezeli az országok számát
    return random.sample(countries_data, num_countries)


def evaluate_answer(user_answer, correct_answer):
    return user_answer.lower() == correct_answer.lower()


def main():
    print("Ez a program egy játék, ahol meg kell adnia az adott ország fővárosát angolul.")
    countries_data = download_countries_from_api()

    if countries_data:
        num_questions = int(input("Hány ország fővárosát szeretné megkérdezni? "))
        num_questions = min(max(num_questions, 1), len(countries_data))

        continents = set(country.get("region", "") for country in countries_data)
        continent = input(f"Válasszon kontinenst a következők közül: {', '.join(continents)}: ").capitalize()
        # https://www.geeksforgeeks.org/string-capitalize-python/

        if continent == "Antarctica":
            print("Az Antarktiszon nincsenek országok. Az összes ország lesz használva.")
            selected_countries = get_random_countries(get_countries_from_json(countries_data), num_questions)
        elif continent not in continents:
            print("Érvénytelen kontinens. Az összes ország lesz használva.")
            selected_countries = get_random_countries(get_countries_from_json(countries_data), num_questions)
        else:
            continent_countries = filter_countries_by_continent(countries_data, continent)
            country_names = get_countries_from_json(continent_countries)
            selected_countries = get_random_countries(country_names, num_questions)

        correct_answers = 0
        total_questions = len(selected_countries)

        for i, country_name in enumerate(selected_countries):
            country_data = next((country for country in countries_data if country["name"]["common"] == country_name),
                                None)
            # https://www.geeksforgeeks.org/python-next-method/
            if not country_data or not country_data.get("capital"):
                print(f"\nSajnálom, de a {country_name} országnak nincs fővárosa.")
                total_questions -= 1
                continue
            # https://www.geeksforgeeks.org/python-continue-statement/
            print(f"\nKérdés {i + 1}/{total_questions}: Mi {country_name} fővárosa?")
            user_answer = input("Válasz: ").strip()
            correct_answer = country_data["capital"][0]

            if evaluate_answer(user_answer, correct_answer):
                print("Helyes válasz!")
                correct_answers += 1
            else:
                print(f"Sajnálom, a helyes válasz: {correct_answer}")

        accuracy = (correct_answers / total_questions) * 100 if total_questions > 0 else 0
        print(f"\nEredmény: {correct_answers}/{total_questions} helyes válasz. Pontosság: {accuracy:.2f}%")


main()
