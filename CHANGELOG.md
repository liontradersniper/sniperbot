# CHANGELOG.md
 Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Summary CSV export via `save_summary` helper.
### Changed
- `executor.py` trade loop simplified and duplicate imports removed.
- `main.py` now records simulation summary to file.

## [0.1.0] - 2025-06-24
### Changed
- `api.py` refactored with error handling and environment variable validation.
- `executor.py` refactored with logging integration.
- `main.py` improved signal processing and modular integration.
