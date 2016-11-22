# encoding: utf-8

import ckan.plugins as p
import ckan.plugins.toolkit as tk

def building_codes():
    try:
        tag_list = tk.get_action('tag_list')
        building_codes = tag_list(data_dict={'vocabulary_id': 'building_codes'})
        return building_codes
    except tk.ObjectNotFound:
        return None


class EISMetadataFields(p.SingletonPlugin, tk.DefaultDatasetForm):
    p.implements(p.IDatasetForm)
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)

    def get_helpers(self):
        return {'building_codes': building_codes}

    def _modify_package_schema(self, schema):
        schema.update({
            'asset_code': [tk.get_converter('convert_to_extras')]
            ,'building_code': [tk.get_converter('convert_to_tags')('building_codes')]
        })
        return schema
        

    def create_package_schema(self):
        # let's grab the default schema in our plugin
        schema = super(EISMetadataFields, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        # let's grab the default schema in our plugin
        schema = super(EISMetadataFields, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(EISMetadataFields, self).show_package_schema()
        schema.update({
            'building_code': [tk.get_converter('convert_from_tags')('building_codes')]
            ,'asset_code': [tk.get_converter('convert_from_extras')]
        })
        schema['tags']['__extras'].append(tk.get_converter('free_tags_only'))
        return schema

    def is_fallback(self):
        # Return True to register this plugin as the default handler for
        # package types not handled by any other IDatasetForm plugin.
        return True

    def package_types(self):
        # This plugin doesn't handle any special package types, it just
        # registers itself as the default (above).
        return []

    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        tk.add_template_directory(config, 'templates')
