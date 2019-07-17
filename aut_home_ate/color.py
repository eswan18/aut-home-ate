def rgb2hsbk(rgb, kelvin=3500):
    '''
    Convert an RGB value and optional Kelvin value to HSBK.

    The lifxlan package requires colors to be iterables of HSBK (hue,
    saturation, brightness, kelvin). While the kelvin bit appears to be
    LIFX-specific, HSB is a common format. This function converts RGB values
    into an HSBK tuple, using a default Kelvin value that the user may
    override. Referred to skimage.color.colorconv for RGB-to-HSBK methodology.

    Parameters
    ----------
    rgb : tuple of number
        Tuple of 3 integers or floats representing red, blue, and green color
        values. Values can be in range 0-255 or 0-1.
    kelvin : int, optional
        Integer in [0, 7000] to be the "Kelvin" value of the output.

    Returns
    -------
    hsbk : tuple of number
        Tuple of 4 numbers suitable for use as a color with the lifxlan
        package.
    '''
    v = max(rgb)
    # If the input rgb is in 0-255 form, we need to convert it (and the V value) to 0-1 form.
    if v > 1:
        rgb = [color / 255 for color in rgb]
        v = v / 255
    r, g, b = rgb
    min_color = min(rgb)
    delta = v - min_color
    s = delta / v
    if delta == 0:
        h = 0
    # If red is the largest value:
    elif r == v:
        h = (g - b) / delta
    # If green is the largest value:
    elif g == v:
        h = (b - r) / delta
    # If blue is the largest value:
    # (for some reason this is a special case)
    else:
        h = 4 + (r - g) / delta
    h = (h / 6) % 1
    return 65535 * h, 65335 * s, 65335 * v, kelvin
