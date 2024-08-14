import numpy as np


def pearson_correlation(depth, magnitude):
    depth = np.array(depth)
    magnitude = np.array(magnitude)

    depth_mean = np.mean(depth)
    magnitude_mean = np.mean(magnitude)

    depth_diff = depth - depth_mean
    magnitude_diff = magnitude - magnitude_mean

    numerator = np.sum(depth_diff * magnitude_diff)
    denominator = np.sqrt(np.sum(depth_diff ** 2) * np.sum(magnitude_diff ** 2))

    correlation = numerator / denominator

    return correlation


def depth_magnitude_correlation(correlation):
    if correlation > 0.7:
        return ("Силна положителна корелация: "
                "С увеличаване на дълбочината, магнитудът значително се увеличава.")
    elif 0.3 < correlation <= 0.7:
        return ("Умерена положителна корелация: "
                "С увеличаване на дълбочината, магнитудът има тенденция да се увеличава.")
    elif -0.3 <= correlation <= 0.3:
        return ("Слаба корелация: "
                "Няма ясна зависимост между дълбочината и магнитуда.")
    elif -0.7 < correlation < -0.3:
        return ("Умерена отрицателна корелация: "
                "С увеличаване на дълбочината, магнитудът има тенденция да намалява.")
    else:
        return ("Силна отрицателна корелация: "
                "С увеличаване на дълбочината, магнитудът значително намалява.")


def assess_seismic_hazard(df, region):
    region_data = df[df['country'] == region]
    mean_magnitude = region_data['magnitude'].mean()

    if mean_magnitude < 4.0:
        risk_level = "Нисък"
        recommendations = [
            "Прилагане на стандартни строителни практики",
            "Спазване на основните изисквания на сеизмичните кодове",
        ]
    elif 4.0 <= mean_magnitude < 5.0:
        risk_level = "Умерен"
        recommendations = [
            "Проектиране на сгради с повишена дуктилност",
            "Укрепване на съществуващи стари сгради",
            "Специално внимание към детайлирането на конструктивните връзки"
        ]
    elif 5.0 <= mean_magnitude < 7.0:
        risk_level = "Висок"
        recommendations = [
            "Използване на сеизмично изолиране за важни и високи сгради",
            "Строго прилагане на съвременни антисеизмични строителни техники",
            "Регулярни инспекции и retrofit на съществуващи конструкции",
            "Ограничаване на височината на сградите в определени зони",
            "Задължителни обучения за аварийно реагиране за всички жители",
            "Създаване на системи за ранно предупреждение"
        ]
    else:
        risk_level = "Много висок"
        recommendations = [
            "Задължително използване на авангардни технологии за сеизмична защита",
            "Строги ограничения върху земеползването и гъстотата на застрояване",
            "Непрекъснат мониторинг на сеизмичната активност",
            "Периодично преразглеждане и обновяване на строителните норми",
            "Масивни кампании за обществена осведоменост и готовност",
            "Разработване на подробни планове за управление на бедствия",
            "Инвестиции в изследвания за подобряване на сеизмичната устойчивост"
        ]

    assessment = (f"Ниво на риск за {region}: {risk_level}\n"
                  f"Препоръки:\n")

    for i, rec in enumerate(recommendations, 1):
        assessment += f"{i}. {rec}\n"

    return assessment


def get_continent(lat, lon):
    if lat > 66.5 or lat < -66.5:
        return 'Антарктика'
    elif -20 <= lon <= 60:
        if lat > 30:
            return 'Европа'
        else:
            return 'Африка'
    elif 60 < lon <= 150:
        return 'Азия'
    elif lon > 150 or lon <= -140:
        return 'Океания'
    elif lat > 0:
        return 'Северна Америка'
    else:
        return 'Южна Америка'