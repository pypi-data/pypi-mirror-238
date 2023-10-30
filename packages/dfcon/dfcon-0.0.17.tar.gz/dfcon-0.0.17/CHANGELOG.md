# Change Log
## [0.0.1] - 2023-01-30
### Added
- `Directory` class and its basic fuctions from @MTamon
- `Filter` class and its basic fuctions from @MTamon
- `OverlapedFilter` class and its basic fuctions from @MTamon
- `TiledFilter` class and its basic fuctions from @MTamon
- `DircFilter` class and its basic fuctions from @MTamon
- `FileFilter` class and its basic fuctions from @MTamon
- `EmpFilter` class and its \_\_call\_\_ fuctions from @MTamon

## [0.0.2] - 2023-01-30
### Fixed
- Some functions description typo fixed from @MTamon
- Module import method fixed for module classification from @MTamon

## [0.0.3] - 2023-01-30
### Added
- Some description added from @MTamon

## [0.0.4] - 2023-01-31
### Fixed
- Module import method fixed for module classification from @MTamon

## [0.0.5] - 2023-01-31
### Added
- Supported stability of `Directory`'s `get_file_path()` results from @MTamon

## [0.0.6] - 2023-05-30
### Added
- Supported fuction for changing Directory's name.

## [0.0.7] - 2023-05-30
### Fixed
- Change update_dir_name() return value: None -> self

## [0.0.8] - 2023-05-31
### Added
- Supported fuction for copying files in hierarchy.

## [0.0.9] - 2023-05-31
### Fixed
- Fixed sum bugs. (in Filter.overlap & Filter.tile)

## [0.0.10] - 2023-05-31
### Fixed
- Fixed sum bugs. (in Filter.overlap & Filter.tile)

## [0.0.11] - 2023-05-31
### Fixed
- Fixed Directory.copy_files. (for printer=None)

## [0.0.12] - 2023-05-31
### Added
- Supported tqdm for copy-file() & copy-files().

## [0.0.13] - 2023-05-31
### Fixed
- Fixed Directory.sub_incarnate() (for directory filtering)

## [0.0.14] - 2023-06-01
### Fixed
- Fixed requirements.txt (tqdm)

## [0.0.15] - 2023-06-01
### Fixed
- Fixed DircFilter bug. (about valiable 'target')

## [0.0.16] - 2023-06-01
### Fixed
- Fixed FileFilter bug. (When \_\_call\_\_() called, target=Directory)

## [0.0.17] - 2023-10-30
### Fixed
- Fixed for pylance type check.