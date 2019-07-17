from . import cache, color

from lifxlan import LifxLAN, WorkflowException
lan = LifxLAN()


def get_by_label(label, refresh=False):
    '''
    Get a device by its label.

    Only uses the formal API the first time, and stores label-device mappings
    in a dictionary to be reused. The `refresh` argument invalidates the
    label in question and forces a call to the API.
    '''
    device = cache.devices.get(label)
    if refresh or (device is None):
        cache.devices[label] = lan.get_device_by_name(label)
        device = cache.devices[label]
    return device

def set_color(label, *, rgb=None, hsbk=None):
    if rgb and hsbk or (not rgb and not hsbk):
        msg = 'Specify exactly one of rgb and hsbk arguments'
        raise ValueError(msg)
    # If the user  provided an RGB value, we need to convert it.
    # There's no danger of overwriting a user-specified HSBK value -- we
    # checked above.
    if rgb:
        hsbk = color.rgb2hsbk(rgb)
    # Get the device and attempt to set its color.
    device = get_by_label(label)
    try:
        device.set_color(hsbk)
    # WorkflowException is thrown when a light can't be contacted properly.
    except WorkflowException:
        device = get_by_label(label, refresh=True)
        device.set_color(hsbk)
    # TODO someday: Add exception handling for devices that aren't lights.
