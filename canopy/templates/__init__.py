import os
import shutil

TEMPLATE_DIR = os.path.dirname(os.path.abspath(__file__))


def copy_template(template_name, location):
    """
    performs a simple recursive copy of a template to a desired location
    """
    assert not os.path.exists(location)
    shutil.copytree(os.path.join(TEMPLATE_DIR, template_name),
                    location)
