
## [0.5.1] - 2025-06-13
### :bug: Bug Fixes
- [`c2344dc`](https://github.com/davidecavestro/meteonetwork-weather/commit/c2344dc44ee0c4cd7133976d8772f0817678760d) - enforce rate limit for requests per minutes, not per second *(commit by [@davidecavestro](https://github.com/davidecavestro))*


## [0.5.0] - 2025-06-12
### :sparkles: New Features
- [`f594aa5`](https://github.com/davidecavestro/meteonetwork-weather/commit/f594aa55f984816bc39504e0948ea14e25b73a6f) - partially fix [#4](https://github.com/davidecavestro/meteonetwork-weather/pull/4) showing config time response errors *(commit by [@davidecavestro](https://github.com/davidecavestro))*
- [`9bc19d6`](https://github.com/davidecavestro/meteonetwork-weather/commit/9bc19d6b43948764f349853ed5ed53dfa58f45ef) - as per [#2](https://github.com/davidecavestro/meteonetwork-weather/pull/2) add rain_rate and rename native_precitpitation to daily_rain *(commit by [@davidecavestro](https://github.com/davidecavestro))*


## [0.4.0] - 2025-06-11
### :sparkles: New Features
- [`98466bc`](https://github.com/davidecavestro/meteonetwork-weather/commit/98466bc24f519cd66740660a8360cb1d97048f0d) - implement [#2](https://github.com/davidecavestro/meteonetwork-weather/pull/2) providing raw data attrs *(commit by [@davidecavestro](https://github.com/davidecavestro))*


## [0.3.2] - 2025-01-25
### :bug: Bug Fixes
- [`709ada0`](https://github.com/davidecavestro/meteonetwork-weather/commit/709ada06b53fbec9482b933dc7b044518a446c0e) - weather entity not available for virtual stations *(commit by [@davidecavestro](https://github.com/davidecavestro))*


## [0.3.1] - 2025-01-21
### :bug: Bug Fixes
- [`07951ea`](https://github.com/davidecavestro/meteonetwork-weather/commit/07951eafa45914cbc771627b1964897abdac19c8) - avoid conflicts on virtual stations ids *(commit by [@davidecavestro](https://github.com/davidecavestro))*

### :wrench: Chores
- [`1b08cf6`](https://github.com/davidecavestro/meteonetwork-weather/commit/1b08cf66a18e5bd7d0a35dafa687117b17628f70) - fix linting *(commit by [@davidecavestro](https://github.com/davidecavestro))*


## [0.3.0] - 2025-01-20
### :sparkles: New Features
- [`e561380`](https://github.com/davidecavestro/meteonetwork-weather/commit/e56138011ed8be80dcb46c57314b7775398a3565) - [#1](https://github.com/davidecavestro/meteonetwork-weather/pull/1) Provide support for virtual/interpolated station *(commit by [@davidecavestro](https://github.com/davidecavestro))*

### :wrench: Chores
- [`13d0129`](https://github.com/davidecavestro/meteonetwork-weather/commit/13d01290ec849dd5b30a175b482bc46b0404c52a) - add iot_class and integration_type to manifest *(commit by [@davidecavestro](https://github.com/davidecavestro))*
- [`62fc5d9`](https://github.com/davidecavestro/meteonetwork-weather/commit/62fc5d928c538940530bb237c73d8ec58e08f520) - restore version into manifest.json for dev time *(commit by [@davidecavestro](https://github.com/davidecavestro))*
- [`f6de7f6`](https://github.com/davidecavestro/meteonetwork-weather/commit/f6de7f6b967244dd87e9458c8b1c1a827d7335a2) - remove the iot_class attribute *(commit by [@davidecavestro](https://github.com/davidecavestro))*


## [0.2.1] - 2025-01-03
### :bug: Bug Fixes
- [`9377148`](https://github.com/davidecavestro/meteonetwork-weather/commit/93771481235277f680d2a3fb3b8b0f6f58c63bf5) - add missing rate_limiter *(commit by [@davidecavestro](https://github.com/davidecavestro))*


## [0.2.0] - 2025-01-02
### :sparkles: New Features
- [`bbd477d`](https://github.com/davidecavestro/meteonetwork-weather/commit/bbd477d49adc8510b6fd31329ebe7a02928c731c) - throttle concurrent requests *(commit by [@davidecavestro](https://github.com/davidecavestro))*

### :bug: Bug Fixes
- [`7dc36c9`](https://github.com/davidecavestro/meteonetwork-weather/commit/7dc36c95458e547c00861c884af425ee1b55c9bb) - broken sensors *(commit by [@davidecavestro](https://github.com/davidecavestro))*


## [0.1.2] - 2025-01-02
### :bug: Bug Fixes
- [`603460b`](https://github.com/davidecavestro/meteonetwork-weather/commit/603460bc63cf04635790427a8029c3d8a9d78a40) - broken sensors *(commit by [@davidecavestro](https://github.com/davidecavestro))*


## [0.1.1] - 2025-01-01
### :bug: Bug Fixes
- [`ca535b1`](https://github.com/davidecavestro/meteonetwork-weather/commit/ca535b1fa7b751dfb42605a555b1202e3537a84f) - avoid exceeding max state size *(commit by [@davidecavestro](https://github.com/davidecavestro))*

[0.1.1]: https://github.com/davidecavestro/meteonetwork-weather/compare/0.1.0...0.1.1
[0.1.2]: https://github.com/davidecavestro/meteonetwork-weather/compare/0.1.1...0.1.2
[0.2.0]: https://github.com/davidecavestro/meteonetwork-weather/compare/0.1.2...0.2.0
[0.2.1]: https://github.com/davidecavestro/meteonetwork-weather/compare/0.2.0...0.2.1
[0.3.0]: https://github.com/davidecavestro/meteonetwork-weather/compare/0.2.1...0.3.0
[0.3.1]: https://github.com/davidecavestro/meteonetwork-weather/compare/0.3.0...0.3.1
[0.3.2]: https://github.com/davidecavestro/meteonetwork-weather/compare/0.3.1...0.3.2
[0.4.0]: https://github.com/davidecavestro/meteonetwork-weather/compare/0.3.2...0.4.0
[0.5.0]: https://github.com/davidecavestro/meteonetwork-weather/compare/0.4.0...0.5.0
[0.5.1]: https://github.com/davidecavestro/meteonetwork-weather/compare/0.5.0...0.5.1
