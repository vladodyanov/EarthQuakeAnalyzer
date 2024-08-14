from datetime import timedelta

import matplotlib.pyplot as plt
from utils import pearson_correlation, assess_seismic_hazard, depth_magnitude_correlation
from cartopy_maps import visualize_on_map


def analyze_earthquake_data(df):
    result = f"Анализирани {len(df)} земетресения.\n" \
             f"Среден магнитуд: {df['magnitude'].mean():.2f}\n" \
             f"Средна дълбочина: {df['depth'].mean():.2f} км"

    top_earthquakes = df.sort_values('magnitude', ascending=False).head(3)
    top_earthquakes_str = top_earthquakes.apply(lambda row:
                                                f"Магнитуд {row['magnitude']:.1f} - {row['nearest_city']}",
                                                axis=1).str.cat(sep='\n')

    country_counts = df['country'].value_counts()
    if len(country_counts) > 0:
        most_affected_region = country_counts.index[0]
        affected_region_count = country_counts.iloc[0]
    else:
        most_affected_region = "Няма данни"
        affected_region_count = 0

    depth_magnitude_correlation = pearson_correlation(df['depth'], df['magnitude'])

    seismic_hazard_assessment = assess_seismic_hazard(df, most_affected_region)

    aftershocks_analysis = analyze_aftershocks(df)

    return (result, top_earthquakes_str, most_affected_region, affected_region_count,
            depth_magnitude_correlation, seismic_hazard_assessment, aftershocks_analysis)


def analyze_seismic_activity_change(df, start_date, end_date, min_magnitude):
    total_period = (end_date - start_date).days
    mid_date = start_date + timedelta(days=total_period // 2)

    first_half = df[(df['time'] >= start_date) & (df['time'] < mid_date) & (df['magnitude'] >= min_magnitude)]
    second_half = df[(df['time'] >= mid_date) & (df['time'] <= end_date) & (df['magnitude'] >= min_magnitude)]

    first_half_count = len(first_half)
    second_half_count = len(second_half)

    percent_change = ((second_half_count - first_half_count) / first_half_count) * 100 if first_half_count > 0 else 0

    years = total_period / 365

    if percent_change > 0:
        change_type = "повишаване"
    elif percent_change < 0:
        change_type = "намаляване"
    else:
        change_type = "без промяна"

    analysis_result = (f"Анализ за период от {years:.2f} години: "
                       f"За избрания период се наблюдава {change_type} "
                       f"на сеизмичната активност с {abs(percent_change):.2f}%.")

    return analysis_result


def analyze_aftershocks(df):
    sorted_df = df.sort_values('magnitude', ascending=False)

    main_quakes = []
    aftershocks = []

    for _, quake in sorted_df.iterrows():
        is_aftershock = False
        for main_quake in main_quakes:
            # Проверка дали земетресението е в рамките на 7 дни и 100 км от главното земетресение
            time_diff = abs((quake['time'] - main_quake['time']).total_seconds())
            distance = ((quake['latitude'] - main_quake['latitude']) ** 2 +
                        (quake['longitude'] - main_quake['longitude']) ** 2) ** 0.5
            if time_diff <= 7 * 24 * 60 * 60 and distance <= 100 / 111:  # 111 км е приблизително 1 градус
                aftershocks.append((main_quake, quake))
                is_aftershock = True
                break
        if not is_aftershock:
            main_quakes.append(quake)

    # Анализ на афтършоковете
    aftershocks_count = {}
    for main_quake, _ in aftershocks:
        if main_quake['time'] not in aftershocks_count:
            aftershocks_count[main_quake['time']] = 1
        else:
            aftershocks_count[main_quake['time']] += 1

    # Сортиране на земетресенията по брой афтършокове
    sorted_aftershocks = sorted(aftershocks_count.items(), key=lambda x: x[1], reverse=True)

    result = f"За изследвания период има {len(main_quakes)} главни земетресения и {len(aftershocks)} вторични трусове.\n\n"

    result += "Най-голям брой афтършокове се наблюдават след следните земетресения:\n"
    for i, (time, count) in enumerate(sorted_aftershocks[:3], 1):
        main_quake = next(quake for quake in main_quakes if quake['time'] == time)
        result += f"{i}. {main_quake['place']}, {time.strftime('%Y-%m-%d')}, {count} афтършока\n"

    result += "\nНай-малък брой афтършокове се наблюдават след следните земетресения:\n"
    for i, (time, count) in enumerate(sorted_aftershocks[-3:], 1):
        main_quake = next(quake for quake in main_quakes if quake['time'] == time)
        result += f"{i}. {main_quake['place']}, {time.strftime('%Y-%m-%d')}, {count} афтършока\n"

    return result


def visualize_earthquake_data(df, start_date, end_date):
    plt.figure(figsize=(10, 6))
    scatter = plt.scatter(df['time'], df['magnitude'], c=df['depth'], cmap='viridis', alpha=0.4)
    plt.colorbar(scatter, label='Дълбочина (км)')
    plt.title('Земетресения във времето')
    plt.xlabel('Времева ос')
    plt.ylabel('Магнитуд')
    plt.savefig('earthquakes_over_time.png')
    plt.close()

    plt.figure(figsize=(10, 6))
    df['magnitude'].hist(bins=20, edgecolor='black')
    plt.title('Разпределение на магнитудите')
    plt.xlabel('Магнитуд')
    plt.ylabel('Брой земетресения')
    plt.savefig('magnitude_distribution.png')
    plt.close()


def analyze_and_visualize(df, start_date, end_date, min_magnitude):
    analysis_results = analyze_earthquake_data(df)
    visualize_earthquake_data(df, start_date, end_date)

    map_image = visualize_on_map(df, start_date, end_date, min_magnitude)

    (result, top_earthquakes, most_affected_region, affected_region_count,
     correlation, seismic_hazard_assessment, aftershocks_analysis) = analysis_results

    activity_change_analysis = analyze_seismic_activity_change(df, start_date, end_date, min_magnitude)

    return (result, top_earthquakes, most_affected_region, affected_region_count,
            correlation, seismic_hazard_assessment, aftershocks_analysis, map_image, activity_change_analysis)
