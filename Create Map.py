from typing import List

import folium
import click
import json
from folium.plugins import Geocoder
import requests

m = folium.Map(tiles='https://a.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}@2x.png', attr='CartoDB, Voyager',
               zoom_control=False, zoom_start=7.4,
               location=[56.05, 10.84])


def load_geojson_file(file_path: str):
    with open(file_path) as f:
        return json.load(f)


base_url_climate = 'https://dmigw.govcloud.dk/v2/climateData/collections/station/items'
base_url_ocean = 'https://dmigw.govcloud.dk/v2/oceanObs/collections/station/items'


def get_station_json(url: str, api_key: str):
    u = url + f'?api-key={api_key}'
    r = requests.get(u)
    return r.json()


style_function_20 = {'fillOpacity': '0.1', 'color': '#0066ff', 'weight': '1.5'}
style_function_10 = {'fillOpacity': '0.1', 'color': '#248f8f', 'weight': '1'}
style_function_kom = {'fillOpacity': '0.1', 'color': '#f73f3f', 'weight': '1'}


def folium_circle_marker(geojson_feature, fill_color: str, color: str, border_color: str, popup: str) -> folium.CircleMarker:
    print(geojson_feature)
    return folium.CircleMarker(location=list(reversed(geojson_feature['geometry']['coordinates'])),
                               fill_color=fill_color,
                               color=color,
                               weight=1,
                               fill=True,
                               fill_opacity=1,
                               radius=5,
                               border_color=border_color,
                               popup=popup
                               )


def station_popup(station_name: str, station_id: str, operation_from: str, operation_to: str, parameter_ids: List[str]) -> folium.Popup:
    html = f""" 
    <html>
      <head>
        <style>
          
          table {{
            font-family: "Roboto", "Helvetica", "Arial", sans-serif;
            height: 81.5%;
            width: 100%;
            
          }}
           
          p {{
            font-family: "Roboto", "Helvetica", "Arial", sans-serif;
            font-size: 1.5em;
            padding: 0;
            font-weight: bold;
           }}
          tr {{
            background-color: #D6EEEE;
            
          }}
          
          tr:hover {{
            background-color: #81caca;
          }}
          
          td {{
            width: 150px;
            padding: 5px;
          }}
           
        </style>
      </head>
      <table>
        <tbody>
          <p>{station_name} {station_id}</p>
          <tr>
            <td>Operation from</td>
            <td>{operation_from}</td>
          </tr>
          <tr>
            <td>Operation to</td>
            <td>{operation_to}</td>
          </tr>
          <tr>
            <td>Parameters measured</td>
            <td>{parameter_ids}</td>
          </tr>
        </tbody>
      </table>
    </html>
    """
    iframe = folium.IFrame(html=html, width=400, height=300)
    return folium.Popup(iframe)


@click.command()
@click.option('--ocean-api-key',
              type=str,
              help="API key to DMI's oceanObs Open Data API, used to pull station data")
@click.option('--climate-api-key',
              type=str,
              help="API key to DMI's climateData Open Data API, used to pull station data")
def run(ocean_api_key: str, climate_api_key: str):
    grid10x10 = load_geojson_file("10x10/10x10.geojson")
    grid20x20 = load_geojson_file("20x20/20x20.geojson")
    kommuner = load_geojson_file("Municipalities/Municipalities.geojson")
    # json_climate_stations = get_station_json(base_url_climate, climate_api_key)
    # json_ocean_stations = get_station_json(base_url_ocean, ocean_api_key)

    g20 = folium.GeoJson(grid20x20, name='20x20km', style_function=lambda x: style_function_20)
    g20.add_child(folium.features.GeoJsonPopup(fields=['cellId']))
    g10 = folium.GeoJson(grid10x10, name='10x10km', style_function=lambda x: style_function_10)
    g10.add_child(folium.features.GeoJsonPopup(fields=['cellId']))
    kom_feat = folium.GeoJson(kommuner, name='Kommuner', style_function=lambda x: style_function_kom)
    kom_feat.add_child(folium.features.GeoJsonPopup(fields=('Name', 'MunicipalityID')))

    # all_climate_stations = folium.FeatureGroup(name='Climate stations')
    # temp = folium.FeatureGroup(name='Temperature')
    # humi = folium.FeatureGroup(name='Humidity')
    # pressure = folium.FeatureGroup(name='Pressure')
    # wind = folium.FeatureGroup(name='Wind')
    # sun = folium.FeatureGroup(name='Sun')
    # radi = folium.FeatureGroup(name='Radiation')
    # precip = folium.FeatureGroup(name='Precipitation')
    # snow = folium.FeatureGroup(name='Snow')
    # cloud = folium.FeatureGroup(name='Cloud')
    # all_ocean_stations = folium.FeatureGroup(name='Oceanographic Stations')
    #
    # folium_circle_markers_ocean_stations = map(lambda feature: folium_circle_marker(feature, 'Aquamarine', 'black', 'turquoise', feature['properties']['parameterId']), json_ocean_stations['features'])
    # for circle_marker in folium_circle_markers_ocean_stations:
    #     circle_marker.add_to(all_ocean_stations)
    #
    # climate_stations_popups = list(map(lambda feature: station_popup(feature['properties']['name'],
    #                                                             feature['properties']['stationId'],
    #                                                             feature['properties']['operationFrom'],
    #                                                             feature['properties']['operationTo'],
    #                                                             feature['properties']['parameterId']
    #                                                             ), json_climate_stations['features']))
    #
    # station_popup_pairs = list(zip(json_climate_stations['features'], climate_stations_popups))
    # folium_circle_markers_climate_stations = map(lambda station_popup_pair: folium_circle_marker(station_popup_pair[0], 'DarkCyan', 'black', 'DarkCyan', station_popup_pair[1]), station_popup_pairs)
    # for circle_marker in folium_circle_markers_climate_stations:
    #     circle_marker.add_to(all_climate_stations)
    #
    # temperature_stations = filter(lambda feature: 'mean_temp' in feature['properties']['parameterId'], json_climate_stations['features'])
    # folium_circle_markers_temperature_stations = map(lambda feature: folium_circle_marker(feature, 'Green', 'black', 'Green', feature['properties']['parameterId']), temperature_stations)
    # for circle_marker in folium_circle_markers_temperature_stations:
    #     circle_marker.add_to(temp)
    #
    # humidity_stations = filter(lambda feature: 'mean_relative_hum' in feature['properties']['parameterId'], json_climate_stations['features'])
    # folium_circle_markers_humidity_stations = map(lambda feature: folium_circle_marker(feature, 'Red', 'black', 'Red', feature['properties']['parameterId']), humidity_stations)
    # for circle_marker in folium_circle_markers_humidity_stations:
    #     circle_marker.add_to(humi)
    #
    # pressure_stations = filter(lambda feature: 'mean_pressure' in feature['properties']['parameterId'], json_climate_stations['features'])
    # folium_circle_markers_pressure_stations = map(lambda feature: folium_circle_marker(feature, 'Purple', 'black', 'Purple', feature['properties']['parameterId']), pressure_stations)
    # for circle_marker in folium_circle_markers_pressure_stations:
    #     circle_marker.add_to(pressure)
    #
    # wind_stations = filter(lambda feature: 'mean_wind_speed' in feature['properties']['parameterId'], json_climate_stations['features'])
    # folium_circle_markers_wind_stations = map(lambda feature: folium_circle_marker(feature, 'Black', 'black', 'Black', feature['properties']['parameterId']), wind_stations)
    # for circle_marker in folium_circle_markers_wind_stations:
    #     circle_marker.add_to(wind)
    #
    # sun_stations = filter(lambda feature: 'bright_sunshine' in feature['properties']['parameterId'], json_climate_stations['features'])
    # folium_circle_markers_sun_stations = map(lambda feature: folium_circle_marker(feature, 'Yellow', 'black', 'Yellow', feature['properties']['parameterId']), sun_stations)
    # for circle_marker in folium_circle_markers_sun_stations:
    #     circle_marker.add_to(sun)
    #
    # radiation_stations = filter(lambda feature: 'mean_radiation' in feature['properties']['parameterId'], json_climate_stations['features'])
    # folium_circle_markers_radiation_stations = map(lambda feature: folium_circle_marker(feature, 'Grey', 'black', 'Grey', feature['properties']['parameterId']), radiation_stations)
    # for circle_marker in folium_circle_markers_radiation_stations:
    #     circle_marker.add_to(radi)
    #
    # precipation_stations = filter(lambda feature: 'acc_precip' in feature['properties']['parameterId'], json_climate_stations['features'])
    # folium_circle_markers_precipation_stations = map(lambda feature: folium_circle_marker(feature, 'Blue', 'black', 'Blue', feature['properties']['parameterId']), precipation_stations)
    # for circle_marker in folium_circle_markers_precipation_stations:
    #     circle_marker.add_to(precip)
    #
    # snow_stations = filter(lambda feature: 'snow_depth' in feature['properties']['parameterId'], json_climate_stations['features'])
    # folium_circle_markers_snow_stations = map(lambda feature: folium_circle_marker(feature, 'BlueViolet', 'black', 'BlueViolet', feature['properties']['parameterId']), snow_stations)
    # for circle_marker in folium_circle_markers_snow_stations:
    #     circle_marker.add_to(snow)
    #
    # cloud_stations = filter(lambda feature: 'mean_cloud_cover' in feature['properties']['parameterId'], json_climate_stations['features'])
    # folium_circle_markers_cloud_stations = map(lambda feature: folium_circle_marker(feature, 'Orange', 'black', 'Orange', feature['properties']['parameterId']), cloud_stations)
    # for circle_marker in folium_circle_markers_cloud_stations:
    #     circle_marker.add_to(cloud)

    # all_climate_stations.add_to(m)
    # all_ocean_stations.add_to(m).show = False
    # temp.add_to(m).show = False
    # humi.add_to(m).show = False
    # pressure.add_to(m).show = False
    # wind.add_to(m).show = False
    # sun.add_to(m).show = False
    # radi.add_to(m).show = False
    # precip.add_to(m).show = False
    # snow.add_to(m).show = False
    # cloud.add_to(m).show = False
    g20.add_to(m).show = False
    g10.add_to(m).show = False
    kom_feat.add_to(m).show = False
    Geocoder(add_marker=True).add_to(m)

    lay = folium.LayerControl(collapsed=False)
    lay.add_to(m)

    m.save('index.html')


if __name__ == "__main__":
    run(auto_envvar_prefix='GRID_STATION_CARD_DMI_OPEN_DATA')
