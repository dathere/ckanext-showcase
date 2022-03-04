import ckan.lib.helpers as h
from ckan.plugins import toolkit as tk
from os.path import exists

def facet_remove_field(key, value=None, replace=None):
    '''
    A custom remove field function to be used by the Showcase search page to
    render the remove link for the tag pills.
    '''
    if tk.check_ckan_version(min_version='2.9.0'):
        index_route = 'showcase_blueprint.index'
    else:
        index_route = 'showcase_index'

    return h.remove_url_param(
        key, value=value, replace=replace,
        alternative_url=h.url_for(index_route))


def get_site_statistics():
    '''
    Custom stats helper, so we can get the correct number of packages, and a
    count of showcases.
    '''

    stats = {}
    stats['showcase_count'] = tk.get_action('package_search')(
        {}, {"rows": 1, 'fq': '+dataset_type:showcase'})['count']
    stats['dataset_count'] = tk.get_action('package_search')(
        {}, {"rows": 1, 'fq': '!dataset_type:showcase'})['count']
    stats['group_count'] = len(tk.get_action('group_list')({}, {}))
    stats['organization_count'] = len(
        tk.get_action('organization_list')({}, {}))

    return stats


def get_wysiwyg_editor():
    return tk.config.get('ckanext.showcase.editor', '')

def get_value_from_showcase_extras(extras, key):
    value = ''
    for item in extras:
        if item.get('key') == key:
            value = item.get('value')
    return value

# look for a thumbnail image for image found at path image_url and returns the thumbnail url if it exists
# if no thumbnail exists, the original image_fp is returned
def get_thumbnail( image_name ):

    thumb_name = "";

    # convert image url to file path
    #image_fp = tk.config.get("ckan.storage_path") + '/storage' + image_name

    if image_name != None and "." in image_name:

        if image_name.startswith( 'http' ):
            image_name =  "{1}".format( *image_name.rsplit('/', 1) )

        # convert image_fp to thumb_fp by adding -thumbnail before the file extension
        thumb_name =  "{0}-{2}.{1}".format(*image_name.rsplit('.', 1) + ['thumbnail'])

    if exists( tk.config.get("ckan.storage_path") + '/storage/uploads/showcase/' + thumb_name ):
        return thumb_name
    else:
        return image_name
