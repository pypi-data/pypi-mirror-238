# Routing for Alliance Auth

Routing is a pathfinding plugin for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth/).

## Features

- def route_path(source: int, destination: int, mode="prefer_shortest",  algorithm="astar", edges: list = [], static_cache: bool = False) -> List[int]:
- def route_length(source: int, destination: int, mode="prefer_shortest",  algorithm="astar", edges: List = [], static_cache: bool = False ) -> int:
- def systems_range(source: int, range: int, mode="prefer_shortest", edges: list = [], static_cache: bool = False) -> List:

- A pregenerated optional Graph dict, to reduce DB load and processing for mass use, cannot guarantee accuracy without shipping new versions.

## Implementations
### Planned
AA Drifters
AA Incursions

## Installation

Routing is an App for [Alliance Auth](https://gitlab.com/allianceauth/allianceauth/), Please make sure you have this installed. Routing is not a standalone Django Application

### Step 1 - Install app

```shell
pip install aa-routing
```

### Step 2 - Configure Auth settings

Configure your Auth settings (`local.py`) as follows:

- Add `'routing'` to `INSTALLED_APPS`
- Add below lines to your settings file:

### Step 3 - Maintain Alliance Auth

- Run migrations `python manage.py migrate`
- Gather your staticfiles `python manage.py collectstatic`
- Restart your project `supervisorctl restart myauth:`

### Step 4 - Configuration

In the Admin interface, visit `routing` or `<AUTH-URL>/admin/routing`

## Settings

| Name | Description | Default |
| --- | --- | --- |

## Contributing

Make sure you have signed the [License Agreement](https://developers.eveonline.com/resource/license-agreement) by logging in at <https://developers.eveonline.com> before submitting any pull requests. All bug fixes or features must not include extra superfluous formatting changes.
