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
            'format': 'svg',  # Save as SVG
            'filename': filename,
            'scale': 1,
            'width': 1920,  # 1080p width
            'height': 1080  # 1080p height (16:9 aspect ratio)
        }
    }

    return config