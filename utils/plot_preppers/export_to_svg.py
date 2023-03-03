def get_svg_config(filename: str = 'custom_image') -> dict:
    """
    Makes sure to export plots as vector graphics.

    Note: It is important to note that any figures containing WebGL traces (i.e. of type scattergl, heatmapgl,
    contourgl, scatter3d, surface, mesh3d, scatterpolargl, cone, streamtube, splom, or parcoords) that are exported
    in a vector format will include encapsulated rasters, instead of vectors, for some parts of the image.
        (see https://plotly.com/python/static-image-export/#vector-formats-svg-and-pdf)
    """

    config = {
        'toImageButtonOptions': {
            'format': 'svg',  # one of png, svg, jpeg, webp
            'filename': filename,
            'scale': 1  # Multiply title/legend/axis/canvas sizes by this factor
        }
    }

    return config