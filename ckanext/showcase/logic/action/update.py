import logging

import ckan.lib.uploader as uploader
import ckan.plugins.toolkit as toolkit
import ckanext.showcase.utils as utils


log = logging.getLogger(__name__)

def showcase_update(context, data_dict):

    upload = uploader.get_uploader('showcase', data_dict['image_url'])

    upload.update_data_dict(data_dict, 'image_url',
                            'image_upload', 'clear_upload')

    upload.upload(uploader.get_max_image_size())

    pkg = toolkit.get_action('package_update')(context, data_dict)

    utils.create_thumbnail( data_dict['image_url'] )

    return pkg
