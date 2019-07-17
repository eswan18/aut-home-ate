from . import cache, lifx, hue
import lifxlan

def set_color(label, *, rgb=None, hsbk=None):
    '''
    Set the color of a light.

    Automatically forces a refresh if the light doesn't respond.
    '''
    device = get_by_label(label)
    # Call the appropriate functionality based on what time of light it is.
    if isinstance(device, lifxlan.Device):
        lifx.set_color(label, rgb=rgb, hsbk=hsbk)
    else:
        # hue.set_color(label, rgb=rgb, hsbk=hsbk
        pass

def get_by_label(label, refresh=False):
    # If we have a cached copy and don't need to refresh, just return what's
    # in the devices dictionary.
    if label in cache.devices and not refresh:
        return cache.devices[label]
    # Try each company's API until we find the device.
    device = lifx.get_by_label(label, refresh=refresh)
    if device is None:
        device = hue.get_by_label(label, refresh=refresh)
    return device
