# File management lib

# File classes

## class File

mathods:

get_abspath() -> str

get_base_name() -> str

get_name() -> str

get_extension(self) -> str | None

rename(new_name, force_rewrite) -> None

## class ImageFile : File

mathods:

crop()

save()

## class Directory : File

mathods:

normalize_filenames(force_rewrite=None) -> None
