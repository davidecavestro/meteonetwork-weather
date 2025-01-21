# MeteoNetwork Weather integration for Home Assistant
Home Assistant unofficial integration for MeteoNetwork Weather current conditions

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]
[![Community Forum][forum-shield]][forum]


This integration adds support for retrieving the current conditions from [MeteoNetwork realtime weather data of specific weather stations](https://api.meteonetwork.it/documentation.html#tag/Realtime-Data/paths/~1data-realtime~1%7Bstation_code%7D/get).

A valid Auth token for MeteoNetwork API is required.
You can configure multiple MeteoNetwork weather stations to get observed weather conditions.

#### This integration will set up the following platforms.

Platform | Description
-- | --
`weather` | A Home Assistant `weather` entity, with current data.
`sensor` | A Home Assistant `sensor` entity, with all available sensor from the API.

Minimum required version of Home Assistant is **2024.11.0** as this integration uses the new Weather entity forecast types.

## Installation through HACS (Recommended Method)

If you are not familiar with HACS, or haven't installed it, I would recommend to [look through the HACS documentation](https://hacs.xyz/), before continuing.

Register `davidecavestro/meteonetwork-weather` as an [HACS custom repository](https://www.hacs.xyz/docs/faq/custom_repositories/).

## Manual installation

1. Create a new folder in your configuration folder (where the `configuration.yaml` lives) called `custom_components`
2. Download the [latest version](https://github.com/davidecavestro/meteonetwork-weather/releases) into the `custom_components` folder so that the full path from your config folder is `custom_components/meteonetwork_weather/`
3. Restart Home Assistant.
4. Once Home Assistant is started, from the UI go to Configuration > Integrations > Add Integrations. Search for "MeteoNetwork Weather". After selecting, it could take up to a minute.

## Configuration

To add MeteoNetwork Weather to your installation, do the following:

- Go to Configuration and Integrations
- Click the + ADD INTEGRATION button in the lower right corner.
- Search for *MeteoNetwork Weather** and click the integration.
- When loaded, there will be a configuration wizard, where you must enter:

  | Parameter | Required | Default Value | Description |
  | --------- | -------- | ------------- | ----------- |
  | `Auth Token`   | Yes      | None          | The token provided by MeteoNetwork. You can generate it from the [MeteoNetwork API documentation](https://api.meteonetwork.it/documentation.html#tag/User-Login/paths/~1login/post). |
  | `Station Type` | Yes | Real | Choose the type of Weather Station. Choose a real one near your home, or
  a virtual one based on latitude and longitude to get interpolated data from nearest real stations. |
  | `Station ID` (for real stations) | Yes | None | Choose the Weather Station for getting current conditions among the available ones. Check [the live map](https://www.meteonetwork.it/rete/livemap/) or [the stations list](https://www.meteonetwork.eu/it/stations-list). |
  | `Latitude` (for virtual stations) | Yes | None | Virtual station latitude. |
  | `Longitude` (for virtual stations) | Yes | None | Virtual station longitude. |
  | `Station name` (for virtual stations) | Yes | None | Virtual station name. |

- Complete the wizard to save your data. If all goes well you should now have a new Weather entity with data from MeteoNetwork Forecast
- **Please Note**: You can configure multiple instances of the Integration.

## Enable Debug Logging

If logs are needed for debugging or reporting an issue, use the following configuration.yaml:

```yaml
logger:
  default: error
  logs:
    custom_components.meteonetwork-weather: debug
```

## Disclaimer

This project is not affiliated with, endorsed by, or sponsored by MeteoNetwork (Associazione MeteoNetwork OdV).

The data and information provided through this integration are sourced from the MeteoNetwork API, which is publicly available and licensed under the Creative Commons Attribution 4.0 INternational (CC BY 4.0) license unless otherwise specified.

### Terms of Use

All trademarks, logos, and distinctive signs visible on MeteoNetwork's website are the property of MeteoNetwork and cannot be used without prior authorization.

Any reproduction, distribution, modification, or use of MeteoNetwork's content must attribute the source by citing "MeteoNetwork" and providing the URL: https://meteonetwork.it.

This project utilizes MeteoNetwork's data strictly within the terms of the [Creative Commons Attribution 4.0 INternational license](https://creativecommons.org/licenses/by/4.0/deed).

### Limitations of Liability

MeteoNetwork disclaims all responsibility for the accuracy, completeness, and timeliness of the data provided via their API, and for any issues arising from its use. Users should refer to MeteoNetwork's official site for authoritative information.

For more details about MeteoNetwork's copyright and licensing terms, visit their [website](https://www.meteonetwork.eu/).



***

[commits-shield]: https://img.shields.io/github/commit-activity/y/davidecavestro/meteonetwork-weather.svg?style=flat-square
[commits]: https://github.com/davidecavestro/meteonetwork-weather/commits/main
[hacs]: https://www.hacs.xyz/docs/faq/custom_repositories/
[hacsbadge]: https://img.shields.io/badge/HACS-Default-orange.svg?style=flat-square
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=flat-square
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/davidecavestro/meteonetwork-weather.svg?style=flat-square
[releases-shield]: https://img.shields.io/github/release/davidecavestro/meteonetwork-weather.svg?style=flat-square
[releases]: https://github.com/davidecavestro/meteonetwork-weather/releases
