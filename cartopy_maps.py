import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter


def create_world_map(df, start_date, end_date, min_magnitude):
    # Създаване на фигура и оси
    plt.figure(figsize=(14, 6))
    ax = plt.axes(projection=ccrs.Mercator())
    # Добавяне на брегова линия
    ax.coastlines('10m')
    # Настройка на осите
    ax.set_global()
    ax.set_xticks(range(-180, 181, 30), crs=ccrs.PlateCarree())
    ax.set_yticks(range(-80, 81, 20), crs=ccrs.PlateCarree())
    ax.tick_params(axis='both', which='major', labelsize=4)
    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)
    # Добавяне на характеристики на картата
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE, edgecolor='gray', linewidth=0.08)
    ax.add_feature(cfeature.BORDERS, edgecolor='gray', linestyle=':', linewidth=0.08)
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)

    # Филтриране на земетресенията
    mask = (df['time'] >= start_date) & (df['time'] <= end_date) & (df['magnitude'] >= min_magnitude)
    filtered_df = df[mask]

    # Визуализиране на земетресенията
    scatter = ax.scatter(filtered_df['longitude'], filtered_df['latitude'],
                         c=filtered_df['magnitude'], cmap='jet',
                         s=filtered_df['magnitude'] ** 0.7, alpha=0.4,
                         transform=ccrs.PlateCarree())

    # Добавяне на цветна лента
    cbar = plt.colorbar(scatter, ax=ax, orientation='vertical', pad=0, shrink=0.3)
    cbar.set_label('Магнитуд на земетресението', fontsize=6)
    cbar.ax.tick_params(labelsize=5)

    # Добавяне на заглавие
    plt.title(
        f'Земетресения\n{start_date.strftime("%Y-%m-%d")} до {end_date.strftime("%Y-%m-%d")}')

    # Запазване на картата като изображение
    plt.savefig('world_map.png', dpi=300, bbox_inches='tight')
    plt.close()


def visualize_on_map(df, start_date, end_date, min_magnitude):
    create_world_map(df, start_date, end_date, min_magnitude)
    return 'world_map.png'
