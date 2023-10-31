# Metamock

[![PyPI](https://img.shields.io/pypi/v/ssb-metamock.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/ssb-metamock.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/ssb-metamock)][pypi status]
[![License](https://img.shields.io/pypi/l/ssb-metamock)][license]

[![Documentation](https://github.com/statisticsnorway/metamock/actions/workflows/docs.yml/badge.svg)][documentation]
[![Tests](https://github.com/statisticsnorway/metamock/workflows/Tests/badge.svg)][tests]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)][poetry]

[pypi status]: https://pypi.org/project/metamock/
[documentation]: https://statisticsnorway.github.io/metamock
[tests]: https://github.com/statisticsnorway/metamock/actions?workflow=Tests
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black
[poetry]: https://python-poetry.org/

## Features

- Generate synthetic data from a [Datadoc] metadata document.
- Column data types will correspond with those specified in the metadata.
- Where [Statistics Norway]'s classification system [Klass] is referenced, data will be generated from the codes.
- Choose the output file format from `json`, `csv` or `parquet`.
- Placeholder data is used where nothing more specific can be found in the metadata.

### Example

```sh
metamock --datadoc-document tests/data/person_data_v1__DOC.json --output-path ~/metamock/output --output-filename datadoc_example --file-type csv
```

```sh
csvlook --delimiter ";" --max-columns 10 --max-rows 2 ~/metamock/output/datadoc_example.csv

| a | pers_id        |  tidspunkt | sivilstand | alm_inntekt | ... |
| - | -------------- | ---------- | ---------- | ----------- | --- |
| 0 | et             | 1977-08-22 | fugiat     |         696 | ... |
| 1 | nam            | 1986-08-05 | cum        |         692 | ... |
| 2 | exercitationem | 2000-06-17 | illum      |         476 | ... |
| 3 | dignissimos    | 1985-12-12 | ab         |         642 | ... |
| 4 | ipsa           | 2023-02-04 | nihil      |         189 | ... |
| ... | ...            |        ... | ...        |         ... | ... |
```

## Installation

You can install _Metamock_ via [pipx]:

```console
pipx install ssb-metamock
```

## Usage

Please see the [Reference Guide] for details.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_Metamock_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [Statistics Norway]'s [SSB PyPI Template].

[statistics norway]: https://github.com/statisticsnorway
[ssb pypi template]: https://github.com/statisticsnorway/ssb-pypitemplate
[file an issue]: https://github.com/statisticsnorway/metamock/issues
[pipx]: https://pypa.github.io/pipx/
[datadoc]: https://github.com/statisticsnorway/datadoc
[klass]: https://www.ssb.no/en/metadata/om-klass

<!-- github-only -->

[license]: https://github.com/statisticsnorway/metamock/blob/main/LICENSE
[contributor guide]: https://github.com/statisticsnorway/metamock/blob/main/CONTRIBUTING.md
[reference guide]: https://statisticsnorway.github.io/metamock/reference.html
