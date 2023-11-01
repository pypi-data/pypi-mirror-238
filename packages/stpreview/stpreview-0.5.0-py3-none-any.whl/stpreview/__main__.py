from pathlib import Path
from typing import Optional

import asdf
import typer
from typing_extensions import Annotated

from stpreview.downsample import (
    OBSERVATORIES,
    downsample_asdf_by,
    downsample_asdf_to,
    known_asdf_observatory,
)
from stpreview.image import north_pole_angle, write_image

app = typer.Typer()


@app.command()
def by(
    input: Annotated[Path, typer.Argument(help="path to ASDF file with 2D image data")],
    output: Annotated[Path, typer.Argument(help="path to output image file")],
    factor: Annotated[
        tuple[int, int],
        typer.Argument(help="block size by which to downsample image data"),
    ],
    observatory: Annotated[
        Optional[str], typer.Argument(help=f"observatory, one of {OBSERVATORIES}")
    ] = None,
    compass: Annotated[
        Optional[bool], typer.Option(help="whether to draw a north arrow on the image")
    ] = False,
):
    """
    downsample the given ASDF image by the given factor
    """

    if observatory is None:
        observatory = known_asdf_observatory(input)

    data = downsample_asdf_by(input=input, factor=factor, observatory=observatory)

    if compass:
        with asdf.open(input) as file:
            wcs = file[observatory]["meta"]["wcs"]
        north_arrow_angle = north_pole_angle(wcs).degree - 90
    else:
        north_arrow_angle = None

    write_image(
        data,
        output,
        north_arrow_angle=north_arrow_angle,
    )


@app.command()
def to(
    input: Annotated[Path, typer.Argument(help="path to ASDF file with 2D image data")],
    output: Annotated[Path, typer.Argument(help="path to output image file")],
    shape: Annotated[
        tuple[int, int], typer.Argument(help="desired pixel resolution of output image")
    ],
    observatory: Annotated[
        Optional[str], typer.Argument(help=f"observatory, one of {OBSERVATORIES}")
    ] = None,
    compass: Annotated[
        Optional[bool], typer.Option(help="whether to draw a north arrow on the image")
    ] = False,
):
    """
    downsample the given ASDF image to the desired shape

    the output image may be smaller than the desired shape, if no even factor exists
    """

    if observatory is None:
        observatory = known_asdf_observatory(input)

    data = downsample_asdf_to(input=input, shape=shape, observatory=observatory)

    if compass:
        with asdf.open(input) as file:
            wcs = file[observatory]["meta"]["wcs"]
        north_arrow_angle = north_pole_angle(wcs).degree - 90
    else:
        north_arrow_angle = None

    write_image(
        data,
        output,
        shape=shape,
        north_arrow_angle=north_arrow_angle,
    )


def main():
    app()


if __name__ == "__main__":
    main()
