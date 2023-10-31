import os
import requests
import logging
from auth0.authentication.token_verifier import TokenVerifier, AsymmetricSignatureVerifier

class api(object):
    def __init__(self):
        self.AUTH0_DOMAIN    = os.environ.get('AUTH0_DOMAIN', 'geoinsight.eu.auth0.com')
        self.AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID', 'LVipjRM8ywtUFW0yGy5rQXj8Dgs8Uz8o')
        self.url             = os.environ.get('API_URL', 'https://api.geoinsight.ai')

        self.headers = requests.structures.CaseInsensitiveDict()
        self.headers["Accept"] = "application/json"
        self.headers["Content-Type"] = "application/json"
        self.headers["Accept-Encoding"] = "gzip, deflate, br"
        self.headers["Connection"] = "keep-alive"
        self.headers["Authorization"] = ""

    def is_online(self):
        r = requests.get(self.url)
        if 200 <= r.status_code <= 299:
            return True
        else:
            return False

    def set_access_token(self, _gpt, _apk):
        body = {"grant_type": "refresh_token", "client_id": self.AUTH0_CLIENT_ID, "refresh_token": _gpt, "client_secret": _apk}
        r = requests.post('https://{}/oauth/token'.format(self.AUTH0_DOMAIN), data=body)
        if 200 <= r.status_code <= 299 and self.is_online():
            jwks_url = 'https://{}/.well-known/jwks.json'.format(self.AUTH0_DOMAIN)
            issuer = 'https://{}/'.format(self.AUTH0_DOMAIN)
            sv = AsymmetricSignatureVerifier(jwks_url)
            tv = TokenVerifier(signature_verifier=sv, issuer=issuer, audience=self.AUTH0_CLIENT_ID)
            tv.verify(r.json()['id_token'])
            self.headers["Authorization"] = "Bearer " + '{token}'.format(token=r.json()['access_token'])
            logging.info('Access Token has been set')
        else:
            logging.error('An error occurred: {e}'.format(e=r.json()))
        return

    def aoi_refresh_open(self):
        """ GET aoi_refresh_open



        Returns
        -----------
            response:
                {aoi_refresh_open} response object

        """

        # Endpoint
        endpoint = '/aoi_refresh_open'

        return requests.get(self.url + endpoint, headers=self.headers)

    def atlas_source(self):
        """ GET atlas_source

            The entire list of sources.

        Returns
        -----------
            response:
                {id, dct_title_s, dct_alternative_sm, dct_description_sm, dct_language_sm, dct_creator_sm, dct_publisher_sm, schema_provider_s, gbl_resourceclass_sm, gbl_resourcetype_sm, dcat_theme_sm, dcat_keyword_sm, dct_temporal_sm, dct_issued_s, gbl_indexyear_im, gbl_daterange_drsim, dct_spatial_sm, locn_geometry, dcat_bbox, dcat_centroid, pcdm_memberof_sm, dct_ispartof_sm, dct_rights_sm, dct_license_sm, dct_accessrights_s, dct_format_s, dct_references_s, dct_identifier_sm, gbl_mdmodified_dt, gbl_mdversion_s, gi_destination} response object

        """

        # Endpoint
        endpoint = '/atlas_source'

        return requests.get(self.url + endpoint, headers=self.headers)

    def atlas_source_overview(self):
        """ GET atlas_source_overview

            An overview of the data atlas of the intelligent earth.

        Returns
        -----------
            response:
                {id, dct_title_s, gbl_resourceclass_sm, dct_accessrights_s, gbl_mdmodified_dt, gi_destination} response object

        """

        # Endpoint
        endpoint = '/atlas_source_overview'

        return requests.get(self.url + endpoint, headers=self.headers)

    def auth_get_rt(self):
        """ GET auth_get_rt



        Returns
        -----------
            response:
                {id, auth0_user_id, auth0_refresh_token, date_inserted} response object

        """

        # Endpoint
        endpoint = '/auth_get_rt'

        return requests.get(self.url + endpoint, headers=self.headers)

    def destination_source_overview(self):
        """ GET destination_source_overview



        Returns
        -----------
            response:
                {destination_id, source_id} response object

        """

        # Endpoint
        endpoint = '/destination_source_overview'

        return requests.get(self.url + endpoint, headers=self.headers)

    def dst_refresh_stats_open(self):
        """ GET dst_refresh_stats_open



        Returns
        -----------
            response:
                {dst_refresh_stats_open} response object

        """

        # Endpoint
        endpoint = '/dst_refresh_stats_open'

        return requests.get(self.url + endpoint, headers=self.headers)

    def is_token_valid(self):
        """ GET is_token_valid



        Returns
        -----------
            response:
                {valid} response object

        """

        # Endpoint
        endpoint = '/is_token_valid'

        return requests.get(self.url + endpoint, headers=self.headers)

    def isea3h_data_aoi(self):
        """ GET isea3h_data_aoi



        Returns
        -----------
            response:
                {id, aoi, detail, stats} response object

        """

        # Endpoint
        endpoint = '/isea3h_data_aoi'

        return requests.get(self.url + endpoint, headers=self.headers)

    def isea3h_data_dst(self):
        """ GET isea3h_data_dst



        Returns
        -----------
            response:
                {id, col_name, col_pkey, col_dtype, detail, stats} response object

        """

        # Endpoint
        endpoint = '/isea3h_data_dst'

        return requests.get(self.url + endpoint, headers=self.headers)

    def isea3h_stats(self):
        """ GET isea3h_stats

            Statistics of ISEA3H Discrete Global Grid System.

        Returns
        -----------
            response:
                {resolution, cells, generated, area, spacing, cls} response object

        """

        # Endpoint
        endpoint = '/isea3h_stats'

        return requests.get(self.url + endpoint, headers=self.headers)

    def task_common_status_codes(self):
        """ GET task_common_status_codes

            The status codes and their description

        Returns
        -----------
            response:
                {code_id, code_status, code_description, task_tool} response object

        """

        # Endpoint
        endpoint = '/task_common_status_codes'

        return requests.get(self.url + endpoint, headers=self.headers)

    def task_gendggs_overview(self):
        """ GET task_gendggs_overview

            The overview of task_gendggs with selected columns

        Returns
        -----------
            response:
                {task_id, priority, status} response object

        """

        # Endpoint
        endpoint = '/task_gendggs_overview'

        return requests.get(self.url + endpoint, headers=self.headers)

    def task_gendggs_view(self):
        """ GET task_gendggs_view

            The main view of task_gendggs

        Returns
        -----------
            response:
                {task_id, priority, status, dggrid_operation, verbosity, update_frequency, coord_precision, dggs_type, dggs_aperture, longitude_wrap_mode, unwrap_points, dggs_res_spec, clip_subset_type, input_address_type, clip_cell_res, clip_cell_addresses, output_cell_label_type, output_address_type, cell_output_type, point_output_type, children_output_type, neighbor_output_type, collection_output_gdal_format} response object

        """

        # Endpoint
        endpoint = '/task_gendggs_view'

        return requests.get(self.url + endpoint, headers=self.headers)

    def task_logging_view(self):
        """ GET task_logging_view

            Logging information from all core tools

        Returns
        -----------
            response:
                {task_id, tool, occurred, status, event} response object

        """

        # Endpoint
        endpoint = '/task_logging_view'

        return requests.get(self.url + endpoint, headers=self.headers)

    def task_pipeline_overview(self):
        """ GET task_pipeline_overview

            The overview of task_pipeline with selected columns

        Returns
        -----------
            response:
                {task_id, priority, status, processor, pipe, s3_bucket} response object

        """

        # Endpoint
        endpoint = '/task_pipeline_overview'

        return requests.get(self.url + endpoint, headers=self.headers)

    def task_pipeline_view(self):
        """ GET task_pipeline_view

            The main view of task_pipeline

        Returns
        -----------
            response:
                {task_id, priority, status, processor, pipe, s3_bucket, description, license, start_date, end_date, resolution, bands, ts, ts_interval, nodata, format, value, comment} response object

        """

        # Endpoint
        endpoint = '/task_pipeline_view'

        return requests.get(self.url + endpoint, headers=self.headers)

    def task_ras2dggs_overview(self):
        """ GET task_ras2dggs_overview

            The overview of task_ras2dggs with selected columns

        Returns
        -----------
            response:
                {task_id, priority, status} response object

        """

        # Endpoint
        endpoint = '/task_ras2dggs_overview'

        return requests.get(self.url + endpoint, headers=self.headers)

    def task_ras2dggs_view(self):
        """ GET task_ras2dggs_view

            The main view of task_ras2dggs

        Returns
        -----------
            response:
                {task_id, priority, status, pipeline_id, statistic, res, clip_gid, clip_gid_res} response object

        """

        # Endpoint
        endpoint = '/task_ras2dggs_view'

        return requests.get(self.url + endpoint, headers=self.headers)


    def isea3h_dggs_refresh_stats(self):
        """ POST isea3h_dggs_refresh_stats



        Parameters
        ------------
        none

        Returns
        -----------
            response:
                {response object}

        """

        # Endpoint
        endpoint = '/rpc/isea3h_dggs_refresh_stats'

        # Body
        body = {}

        return requests.post(self.url + endpoint, json=body, headers=self.headers)


    def atlas_source_delete(self, _id):
        """ POST atlas_source_delete

            This deletes a source entry using the source ID

        Parameters
        ------------
            _id : str[]
                str[] | The ID of the source

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/atlas_source_delete'

        # Field type check
        if type(_id) != list:
            logging.error('{}: {} is not {}'.format('_id', _id, 'ARRAY'))

        # Body
        body = {
                 "_id": _id
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def atlas_source_insert(self, _id, _dct_title_s, _gbl_resourceclass_sm, _dct_accessrights_s, _dct_alternative_sm=[], _dct_description_sm=[], _dct_language_sm=[], _dct_creator_sm=[], _dct_publisher_sm=[], _schema_provider_s=None, _gbl_resourcetype_sm=[], _dcat_theme_sm=[], _dcat_keyword_sm=[], _dct_temporal_sm=[], _dct_issued_s=None, _gbl_indexyear_im=None, _gbl_daterange_drsim=[], _dct_spatial_sm=[], _locn_geometry=None, _dcat_bbox=None, _dcat_centroid=None, _pcdm_memberof_sm=[], _dct_ispartof_sm=[], _dct_rights_sm=[], _dct_license_sm=[], _dct_format_s=None, _dct_references_s=None, _dct_identifier_sm=[], _gbl_mdversion_s='Aardvark', _gi_destination=None):
        """ POST atlas_source_insert



        Parameters
        ------------
            _id : str
                str |
            _dct_title_s : str
                str |
            _gbl_resourceclass_sm : str[]
                str[] |
            _dct_accessrights_s : str
                str |
            _dct_alternative_sm : str[]
                str[] | Optional, default is [] |
            _dct_description_sm : str[]
                str[] | Optional, default is [] |
            _dct_language_sm : str[]
                str[] | Optional, default is [] |
            _dct_creator_sm : str[]
                str[] | Optional, default is [] |
            _dct_publisher_sm : str[]
                str[] | Optional, default is [] |
            _schema_provider_s : str
                str | Optional, default is None |
            _gbl_resourcetype_sm : str[]
                str[] | Optional, default is [] |
            _dcat_theme_sm : str[]
                str[] | Optional, default is [] |
            _dcat_keyword_sm : str[]
                str[] | Optional, default is [] |
            _dct_temporal_sm : str[]
                str[] | Optional, default is [] |
            _dct_issued_s : str
                str | Optional, default is None |
            _gbl_indexyear_im : str
                str | Optional, default is None |
            _gbl_daterange_drsim : str[]
                str[] | Optional, default is [] |
            _dct_spatial_sm : str[]
                str[] | Optional, default is [] |
            _locn_geometry : dict
                dict | Optional, default is None |
            _dcat_bbox : dict
                dict | Optional, default is None |
            _dcat_centroid : dict
                dict | Optional, default is None |
            _pcdm_memberof_sm : str[]
                str[] | Optional, default is [] |
            _dct_ispartof_sm : str[]
                str[] | Optional, default is [] |
            _dct_rights_sm : str[]
                str[] | Optional, default is [] |
            _dct_license_sm : str[]
                str[] | Optional, default is [] |
            _dct_format_s : str
                str | Optional, default is None |
            _dct_references_s : str
                str | Optional, default is None |
            _dct_identifier_sm : str[]
                str[] | Optional, default is [] |
            _gbl_mdversion_s : str
                str | Optional, default is 'Aardvark' |
            _gi_destination : str
                str | Optional, default is None |

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/atlas_source_insert'

        # Field type check
        if type(_id) != str and _id is not None:
            logging.error('{}: {} is not {}'.format('_id', _id, 'text'))
        if type(_dct_title_s) != str and _dct_title_s is not None:
            logging.error('{}: {} is not {}'.format('_dct_title_s', _dct_title_s, 'text'))
        if type(_gbl_resourceclass_sm) != list:
            logging.error('{}: {} is not {}'.format('_gbl_resourceclass_sm', _gbl_resourceclass_sm, 'ARRAY'))
        if type(_dct_accessrights_s) != str and _dct_accessrights_s is not None:
            logging.error('{}: {} is not {}'.format('_dct_accessrights_s', _dct_accessrights_s, 'text'))
        if type(_dct_alternative_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_alternative_sm', _dct_alternative_sm, 'ARRAY'))
        if type(_dct_description_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_description_sm', _dct_description_sm, 'ARRAY'))
        if type(_dct_language_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_language_sm', _dct_language_sm, 'ARRAY'))
        if type(_dct_creator_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_creator_sm', _dct_creator_sm, 'ARRAY'))
        if type(_dct_publisher_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_publisher_sm', _dct_publisher_sm, 'ARRAY'))
        if type(_schema_provider_s) != str and _schema_provider_s is not None:
            logging.error('{}: {} is not {}'.format('_schema_provider_s', _schema_provider_s, 'text'))
        if type(_gbl_resourcetype_sm) != list:
            logging.error('{}: {} is not {}'.format('_gbl_resourcetype_sm', _gbl_resourcetype_sm, 'ARRAY'))
        if type(_dcat_theme_sm) != list:
            logging.error('{}: {} is not {}'.format('_dcat_theme_sm', _dcat_theme_sm, 'ARRAY'))
        if type(_dcat_keyword_sm) != list:
            logging.error('{}: {} is not {}'.format('_dcat_keyword_sm', _dcat_keyword_sm, 'ARRAY'))
        # VALUE CHECK MISSING: _dct_temporal_sm
        if type(_dct_issued_s) != str and _dct_issued_s is not None:
            logging.error('{}: {} is not {}'.format('_dct_issued_s', _dct_issued_s, 'timestamp without time zone'))
        # VALUE CHECK MISSING: _gbl_indexyear_im
        # VALUE CHECK MISSING: _gbl_daterange_drsim
        if type(_dct_spatial_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_spatial_sm', _dct_spatial_sm, 'ARRAY'))
        # VALUE CHECK MISSING: _locn_geometry
        # VALUE CHECK MISSING: _dcat_bbox
        # VALUE CHECK MISSING: _dcat_centroid
        if type(_pcdm_memberof_sm) != list:
            logging.error('{}: {} is not {}'.format('_pcdm_memberof_sm', _pcdm_memberof_sm, 'ARRAY'))
        if type(_dct_ispartof_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_ispartof_sm', _dct_ispartof_sm, 'ARRAY'))
        if type(_dct_rights_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_rights_sm', _dct_rights_sm, 'ARRAY'))
        if type(_dct_license_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_license_sm', _dct_license_sm, 'ARRAY'))
        if type(_dct_format_s) != str and _dct_format_s is not None:
            logging.error('{}: {} is not {}'.format('_dct_format_s', _dct_format_s, 'text'))
        if type(_dct_references_s) != str and _dct_references_s is not None:
            logging.error('{}: {} is not {}'.format('_dct_references_s', _dct_references_s, 'text'))
        if type(_dct_identifier_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_identifier_sm', _dct_identifier_sm, 'ARRAY'))
        if type(_gbl_mdversion_s) != str and _gbl_mdversion_s is not None:
            logging.error('{}: {} is not {}'.format('_gbl_mdversion_s', _gbl_mdversion_s, 'text'))
        if type(_gi_destination) != str and _gi_destination is not None:
            logging.error('{}: {} is not {}'.format('_gi_destination', _gi_destination, 'text'))

        # Body
        body = {
                 "_id": _id,
                 "_dct_title_s": _dct_title_s,
                 "_gbl_resourceclass_sm": _gbl_resourceclass_sm,
                 "_dct_accessrights_s": _dct_accessrights_s,
                 "_dct_alternative_sm": _dct_alternative_sm,
                 "_dct_description_sm": _dct_description_sm,
                 "_dct_language_sm": _dct_language_sm,
                 "_dct_creator_sm": _dct_creator_sm,
                 "_dct_publisher_sm": _dct_publisher_sm,
                 "_schema_provider_s": _schema_provider_s,
                 "_gbl_resourcetype_sm": _gbl_resourcetype_sm,
                 "_dcat_theme_sm": _dcat_theme_sm,
                 "_dcat_keyword_sm": _dcat_keyword_sm,
                 "_dct_temporal_sm": _dct_temporal_sm,
                 "_dct_issued_s": _dct_issued_s,
                 "_gbl_indexyear_im": _gbl_indexyear_im,
                 "_gbl_daterange_drsim": _gbl_daterange_drsim,
                 "_dct_spatial_sm": _dct_spatial_sm,
                 "_locn_geometry": _locn_geometry,
                 "_dcat_bbox": _dcat_bbox,
                 "_dcat_centroid": _dcat_centroid,
                 "_pcdm_memberof_sm": _pcdm_memberof_sm,
                 "_dct_ispartof_sm": _dct_ispartof_sm,
                 "_dct_rights_sm": _dct_rights_sm,
                 "_dct_license_sm": _dct_license_sm,
                 "_dct_format_s": _dct_format_s,
                 "_dct_references_s": _dct_references_s,
                 "_dct_identifier_sm": _dct_identifier_sm,
                 "_gbl_mdversion_s": _gbl_mdversion_s,
                 "_gi_destination": _gi_destination
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def atlas_source_update(self, _id, _dct_title_s, _dct_alternative_sm, _dct_description_sm, _dct_language_sm, _dct_creator_sm, _dct_publisher_sm, _schema_provider_s, _gbl_resourceclass_sm, _gbl_resourcetype_sm, _dcat_theme_sm, _dcat_keyword_sm, _dct_temporal_sm, _dct_issued_s, _gbl_indexyear_im, _gbl_daterange_drsim, _dct_spatial_sm, _locn_geometry, _dcat_bbox, _dcat_centroid, _pcdm_memberof_sm, _dct_ispartof_sm, _dct_rights_sm, _dct_license_sm, _dct_accessrights_s, _dct_format_s, _dct_references_s, _dct_identifier_sm, _gbl_mdversion_s, _gi_destination):
        """ POST atlas_source_update



        Parameters
        ------------
            _id : str
                str |
            _dct_title_s : str
                str |
            _dct_alternative_sm : str[]
                str[] |
            _dct_description_sm : str[]
                str[] |
            _dct_language_sm : str[]
                str[] |
            _dct_creator_sm : str[]
                str[] |
            _dct_publisher_sm : str[]
                str[] |
            _schema_provider_s : str
                str |
            _gbl_resourceclass_sm : str[]
                str[] |
            _gbl_resourcetype_sm : str[]
                str[] |
            _dcat_theme_sm : str[]
                str[] |
            _dcat_keyword_sm : str[]
                str[] |
            _dct_temporal_sm : str[]
                str[] |
            _dct_issued_s : str
                str |
            _gbl_indexyear_im : str
                str |
            _gbl_daterange_drsim : str[]
                str[] |
            _dct_spatial_sm : str[]
                str[] |
            _locn_geometry : dict
                dict |
            _dcat_bbox : dict
                dict |
            _dcat_centroid : dict
                dict |
            _pcdm_memberof_sm : str[]
                str[] |
            _dct_ispartof_sm : str[]
                str[] |
            _dct_rights_sm : str[]
                str[] |
            _dct_license_sm : str[]
                str[] |
            _dct_accessrights_s : str
                str |
            _dct_format_s : str
                str |
            _dct_references_s : str
                str |
            _dct_identifier_sm : str[]
                str[] |
            _gbl_mdversion_s : str
                str |
            _gi_destination : str
                str |

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/atlas_source_update'

        # Field type check
        if type(_id) != str and _id is not None:
            logging.error('{}: {} is not {}'.format('_id', _id, 'text'))
        if type(_dct_title_s) != str and _dct_title_s is not None:
            logging.error('{}: {} is not {}'.format('_dct_title_s', _dct_title_s, 'text'))
        if type(_dct_alternative_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_alternative_sm', _dct_alternative_sm, 'ARRAY'))
        if type(_dct_description_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_description_sm', _dct_description_sm, 'ARRAY'))
        if type(_dct_language_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_language_sm', _dct_language_sm, 'ARRAY'))
        if type(_dct_creator_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_creator_sm', _dct_creator_sm, 'ARRAY'))
        if type(_dct_publisher_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_publisher_sm', _dct_publisher_sm, 'ARRAY'))
        if type(_schema_provider_s) != str and _schema_provider_s is not None:
            logging.error('{}: {} is not {}'.format('_schema_provider_s', _schema_provider_s, 'text'))
        if type(_gbl_resourceclass_sm) != list:
            logging.error('{}: {} is not {}'.format('_gbl_resourceclass_sm', _gbl_resourceclass_sm, 'ARRAY'))
        if type(_gbl_resourcetype_sm) != list:
            logging.error('{}: {} is not {}'.format('_gbl_resourcetype_sm', _gbl_resourcetype_sm, 'ARRAY'))
        if type(_dcat_theme_sm) != list:
            logging.error('{}: {} is not {}'.format('_dcat_theme_sm', _dcat_theme_sm, 'ARRAY'))
        if type(_dcat_keyword_sm) != list:
            logging.error('{}: {} is not {}'.format('_dcat_keyword_sm', _dcat_keyword_sm, 'ARRAY'))
        # VALUE CHECK MISSING: _dct_temporal_sm
        if type(_dct_issued_s) != str and _dct_issued_s is not None:
            logging.error('{}: {} is not {}'.format('_dct_issued_s', _dct_issued_s, 'timestamp without time zone'))
        # VALUE CHECK MISSING: _gbl_indexyear_im
        # VALUE CHECK MISSING: _gbl_daterange_drsim
        if type(_dct_spatial_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_spatial_sm', _dct_spatial_sm, 'ARRAY'))
        # VALUE CHECK MISSING: _locn_geometry
        # VALUE CHECK MISSING: _dcat_bbox
        # VALUE CHECK MISSING: _dcat_centroid
        if type(_pcdm_memberof_sm) != list:
            logging.error('{}: {} is not {}'.format('_pcdm_memberof_sm', _pcdm_memberof_sm, 'ARRAY'))
        if type(_dct_ispartof_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_ispartof_sm', _dct_ispartof_sm, 'ARRAY'))
        if type(_dct_rights_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_rights_sm', _dct_rights_sm, 'ARRAY'))
        if type(_dct_license_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_license_sm', _dct_license_sm, 'ARRAY'))
        if type(_dct_accessrights_s) != str and _dct_accessrights_s is not None:
            logging.error('{}: {} is not {}'.format('_dct_accessrights_s', _dct_accessrights_s, 'text'))
        if type(_dct_format_s) != str and _dct_format_s is not None:
            logging.error('{}: {} is not {}'.format('_dct_format_s', _dct_format_s, 'text'))
        if type(_dct_references_s) != str and _dct_references_s is not None:
            logging.error('{}: {} is not {}'.format('_dct_references_s', _dct_references_s, 'text'))
        if type(_dct_identifier_sm) != list:
            logging.error('{}: {} is not {}'.format('_dct_identifier_sm', _dct_identifier_sm, 'ARRAY'))
        if type(_gbl_mdversion_s) != str and _gbl_mdversion_s is not None:
            logging.error('{}: {} is not {}'.format('_gbl_mdversion_s', _gbl_mdversion_s, 'text'))
        if type(_gi_destination) != str and _gi_destination is not None:
            logging.error('{}: {} is not {}'.format('_gi_destination', _gi_destination, 'text'))

        # Body
        body = {
                 "_id": _id,
                 "_dct_title_s": _dct_title_s,
                 "_dct_alternative_sm": _dct_alternative_sm,
                 "_dct_description_sm": _dct_description_sm,
                 "_dct_language_sm": _dct_language_sm,
                 "_dct_creator_sm": _dct_creator_sm,
                 "_dct_publisher_sm": _dct_publisher_sm,
                 "_schema_provider_s": _schema_provider_s,
                 "_gbl_resourceclass_sm": _gbl_resourceclass_sm,
                 "_gbl_resourcetype_sm": _gbl_resourcetype_sm,
                 "_dcat_theme_sm": _dcat_theme_sm,
                 "_dcat_keyword_sm": _dcat_keyword_sm,
                 "_dct_temporal_sm": _dct_temporal_sm,
                 "_dct_issued_s": _dct_issued_s,
                 "_gbl_indexyear_im": _gbl_indexyear_im,
                 "_gbl_daterange_drsim": _gbl_daterange_drsim,
                 "_dct_spatial_sm": _dct_spatial_sm,
                 "_locn_geometry": _locn_geometry,
                 "_dcat_bbox": _dcat_bbox,
                 "_dcat_centroid": _dcat_centroid,
                 "_pcdm_memberof_sm": _pcdm_memberof_sm,
                 "_dct_ispartof_sm": _dct_ispartof_sm,
                 "_dct_rights_sm": _dct_rights_sm,
                 "_dct_license_sm": _dct_license_sm,
                 "_dct_accessrights_s": _dct_accessrights_s,
                 "_dct_format_s": _dct_format_s,
                 "_dct_references_s": _dct_references_s,
                 "_dct_identifier_sm": _dct_identifier_sm,
                 "_gbl_mdversion_s": _gbl_mdversion_s,
                 "_gi_destination": _gi_destination
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def auth_delete_rt(self, _auth0_refresh_token):
        """ POST auth_delete_rt

            This deletes the Auth0 refresh token from the local table

        Parameters
        ------------
            _auth0_refresh_token : str
                str | The Auth0 refresh token

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/auth_delete_rt'

        # Field type check
        if type(_auth0_refresh_token) != str and _auth0_refresh_token is not None:
            logging.error('{}: {} is not {}'.format('_auth0_refresh_token', _auth0_refresh_token, 'text'))

        # Body
        body = {
                 "_auth0_refresh_token": _auth0_refresh_token
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def auth_insert_rt(self, _auth0_refresh_token):
        """ POST auth_insert_rt

            This inserts the auth0_user_id and the auth0_refresh_tocken to the local refresh_token table using the provided Auth0 refresh token

        Parameters
        ------------
            _auth0_refresh_token : str
                str | The Auth0 refresh token

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/auth_insert_rt'

        # Field type check
        if type(_auth0_refresh_token) != str and _auth0_refresh_token is not None:
            logging.error('{}: {} is not {}'.format('_auth0_refresh_token', _auth0_refresh_token, 'text'))

        # Body
        body = {
                 "_auth0_refresh_token": _auth0_refresh_token
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def check_aoi_exists(self, _aoi):
        """ POST check_aoi_exists

            This checks if an AOI exists

        Parameters
        ------------
            _aoi : str
                str | The AOI

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/check_aoi_exists'

        # Field type check
        if type(_aoi) != str and _aoi is not None:
            logging.error('{}: {} is not {}'.format('_aoi', _aoi, 'text'))

        # Body
        body = {
                 "_aoi": _aoi
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def check_dst_exists(self, _id):
        """ POST check_dst_exists

            This checks if a destination exists

        Parameters
        ------------
            _id : str
                str | The destination

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/check_dst_exists'

        # Field type check
        if type(_id) != str and _id is not None:
            logging.error('{}: {} is not {}'.format('_id', _id, 'text'))

        # Body
        body = {
                 "_id": _id
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def columns_without_pkey(self, _col_name, _col_pkey):
        """ POST columns_without_pkey

            Gets all columns that are not a primary key. Removes all elements of array _col_name that are present in array _col_pkey.

        Parameters
        ------------
            _col_name : str[]
                str[] | Array of column names
            _col_pkey : str[]
                str[] | Array of primary key column names

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/columns_without_pkey'

        # Field type check
        if type(_col_name) != list:
            logging.error('{}: {} is not {}'.format('_col_name', _col_name, 'ARRAY'))
        if type(_col_pkey) != list:
            logging.error('{}: {} is not {}'.format('_col_pkey', _col_pkey, 'ARRAY'))

        # Body
        body = {
                 "_col_name": _col_name,
                 "_col_pkey": _col_pkey
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_cell_by_aoi(self, _aoi, _res=2, _data=[], _limit=10000):
        """ POST isea3h_cell_by_aoi

            This endpoint uses an area of interest(`_aoi`) and a cell resolution (`_res`) to find the cells, within that resolution, that intersect that area. It returns the GID of the DGGS cell.

        Parameters
        ------------
            _aoi : str
                str | Area of interest
            _res : int
                int | Optional, default is 2 | Resolution level
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 | Max number of resulting records

        Returns
        -----------
            response:
                {gid, quad, res, center, region, neighbor, children, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_cell_by_aoi'

        # Field type check
        if type(_aoi) != str and _aoi is not None:
            logging.error('{}: {} is not {}'.format('_aoi', _aoi, 'text'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_aoi": _aoi,
                 "_res": _res,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_cell_by_cell(self, _gid, _gid_res, _res=2, _data=[], _limit=10000):
        """ POST isea3h_cell_by_cell

            This endpoint tasks a target resolution(`_res`) and a latitude/longitude(`_y`/`_x`) coordinate pair. It returns the DGGS cell ??

        Parameters
        ------------
            _gid : str[]
                str[] | Grid cell ID
            _gid_res : int
                int | ...
            _res : int
                int | Optional, default is 2 | Resolution level
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 | Max number of resulting records

        Returns
        -----------
            response:
                {gid, quad, res, center, region, neighbor, children, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_cell_by_cell'

        # Field type check
        if type(_gid) != list:
            logging.error('{}: {} is not {}'.format('_gid', _gid, 'ARRAY'))
        if type(_gid_res) != int and _gid_res is not None:
            logging.error('{}: {} is not {}'.format('_gid_res', _gid_res, 'integer'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_gid": _gid,
                 "_gid_res": _gid_res,
                 "_res": _res,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_cell_by_geojson(self, _geojson='{"type":"Polygon","coordinates":[[[-180,90],[180,90],[180,-90],[-180,-90],[-180,90]]]}', _res=4, _srid=4326, _data=[], _limit=10000):
        """ POST isea3h_cell_by_geojson

            This endpoint tasks a target resolution(`_res`) and a geojson geometry. It returns the cell of the DGGS that intersects with a polygon/point given in geojson.

        Parameters
        ------------
            _geojson : dict
                dict | Optional, default is '{"type":"Polygon","coordinates":[[[-180,90],[180,90],[180,-90],[-180,-90],[-180,90]]]}' | polygon feature in geojson format
            _res : int
                int | Optional, default is 4 | Resolution level
            _srid : int
                int | Optional, default is 4326 | Spatial Reference System ID
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 | ...

        Returns
        -----------
            response:
                {gid, quad, res, center, region, neighbor, children, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_cell_by_geojson'

        # Field type check
        if type(_geojson) != dict and _geojson is not None:
            logging.error('{}: {} is not {}'.format('_geojson', _geojson, 'json'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'smallint'))
        if type(_srid) != int and _srid is not None:
            logging.error('{}: {} is not {}'.format('_srid', _srid, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_geojson": _geojson,
                 "_res": _res,
                 "_srid": _srid,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_cell_by_gid(self, _gid, _res, _data=[], _limit=10000):
        """ POST isea3h_cell_by_gid

            This endpoint takes a list of `hex16` global identifiers `[_gid]` and a target resolution  `_res`. It returns the entire cell definition with region, center, children and neighbors of the DGGS cells that match the given GIDs

        Parameters
        ------------
            _gid : str[]
                str[] | Resolution level
            _res : int
                int | Resolution level
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 |

        Returns
        -----------
            response:
                {gid, quad, res, center, region, neighbors, children, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_cell_by_gid'

        # Field type check
        if type(_gid) != list:
            logging.error('{}: {} is not {}'.format('_gid', _gid, 'ARRAY'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_gid": _gid,
                 "_res": _res,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_cell_by_point(self, _x, _y, _res, _srid=4326, _data=[], _limit=10000):
        """ POST isea3h_cell_by_point

            This endpoint tasks a target resolution(`_res`) and a latitude/longitude(`_y`/`_x`) coordinate pair. It returns the cell of the DGGS that intersects with that point.

        Parameters
        ------------
            _x : float
                float | X of the point
            _y : float
                float | Y of the point
            _res : int
                int | Resolution level
            _srid : int
                int | Optional, default is 4326 | Spatial Reference System ID
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 |

        Returns
        -----------
            response:
                {gid, quad, res, center, region, neighbors, children, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_cell_by_point'

        # Field type check
        if type(_x) != float and _x is not None:
            logging.error('{}: {} is not {}'.format('_x', _x, 'numeric'))
        if type(_y) != float and _y is not None:
            logging.error('{}: {} is not {}'.format('_y', _y, 'numeric'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_srid) != int and _srid is not None:
            logging.error('{}: {} is not {}'.format('_srid', _srid, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_x": _x,
                 "_y": _y,
                 "_res": _res,
                 "_srid": _srid,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_center_by_aoi(self, _aoi, _res=2, _data=[], _limit=10000):
        """ POST isea3h_center_by_aoi

            This endpoint uses an area of interest(`_aoi`) and a cell resolution (`_res`) to find the cells, within that resolution, that intersect that area. It returns the GID of the DGGS cell.

        Parameters
        ------------
            _aoi : str
                str | Area of interest
            _res : int
                int | Optional, default is 2 | Resolution level
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 | Max number of resulting records

        Returns
        -----------
            response:
                {gid, quad, res, center, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_center_by_aoi'

        # Field type check
        if type(_aoi) != str and _aoi is not None:
            logging.error('{}: {} is not {}'.format('_aoi', _aoi, 'text'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_aoi": _aoi,
                 "_res": _res,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_center_by_cell(self, _gid, _gid_res, _res=2, _data=[], _limit=10000):
        """ POST isea3h_center_by_cell

            This endpoint tasks a target resolution(`_res`) and a latitude/longitude(`_y`/`_x`) coordinate pair. It returns the center of the DGGS cell.

        Parameters
        ------------
            _gid : str[]
                str[] | Grid cell ID
            _gid_res : int
                int | ...
            _res : int
                int | Optional, default is 2 | Resolution level
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 | Max number of resulting records

        Returns
        -----------
            response:
                {gid, quad, res, center, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_center_by_cell'

        # Field type check
        if type(_gid) != list:
            logging.error('{}: {} is not {}'.format('_gid', _gid, 'ARRAY'))
        if type(_gid_res) != int and _gid_res is not None:
            logging.error('{}: {} is not {}'.format('_gid_res', _gid_res, 'integer'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_gid": _gid,
                 "_gid_res": _gid_res,
                 "_res": _res,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_center_by_geojson(self, _geojson='{"type":"Polygon","coordinates":[[[-180,90],[180,90],[180,-90],[-180,-90],[-180,90]]]}', _res=4, _srid=4326, _data=[], _limit=10000):
        """ POST isea3h_center_by_geojson

            This endpoint tasks a target resolution(`_res`) and a geojson geometry. It returns the center of the DGGS that intersects with a polygon/point given in geojson.

        Parameters
        ------------
            _geojson : dict
                dict | Optional, default is '{"type":"Polygon","coordinates":[[[-180,90],[180,90],[180,-90],[-180,-90],[-180,90]]]}' | polygon feature in geojson format
            _res : int
                int | Optional, default is 4 | Resolution level
            _srid : int
                int | Optional, default is 4326 | Spatial Reference System ID
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 | ...

        Returns
        -----------
            response:
                {gid, quad, res, center, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_center_by_geojson'

        # Field type check
        if type(_geojson) != dict and _geojson is not None:
            logging.error('{}: {} is not {}'.format('_geojson', _geojson, 'json'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'smallint'))
        if type(_srid) != int and _srid is not None:
            logging.error('{}: {} is not {}'.format('_srid', _srid, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_geojson": _geojson,
                 "_res": _res,
                 "_srid": _srid,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_center_by_gid(self, _gid, _res, _data=[], _limit=10000):
        """ POST isea3h_center_by_gid

            This endpoint takes a list of `hex16` global identifiers `[_gid]` and a target resolution  `_res`. It returns the centers of the DGGS cells that match the given GIDs

        Parameters
        ------------
            _gid : str[]
                str[] | Resolution level
            _res : int
                int | Resolution level
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 |

        Returns
        -----------
            response:
                {gid, quad, res, center, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_center_by_gid'

        # Field type check
        if type(_gid) != list:
            logging.error('{}: {} is not {}'.format('_gid', _gid, 'ARRAY'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_gid": _gid,
                 "_res": _res,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_center_by_point(self, _y, _x, _res, _srid=4326, _data=[], _limit=10000):
        """ POST isea3h_center_by_point

            This endpoint tasks a target resolution(`_res`) and a latitude/longitude(`_y`/`_x`) coordinate pair. It returns the center of the DGGS that intersects with that point.

        Parameters
        ------------
            _y : float
                float | Y of the point
            _x : float
                float | X of the point
            _res : int
                int | Resolution level
            _srid : int
                int | Optional, default is 4326 | Spatial Reference System ID
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 |

        Returns
        -----------
            response:
                {gid, quad, res, center, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_center_by_point'

        # Field type check
        if type(_y) != float and _y is not None:
            logging.error('{}: {} is not {}'.format('_y', _y, 'numeric'))
        if type(_x) != float and _x is not None:
            logging.error('{}: {} is not {}'.format('_x', _x, 'numeric'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_srid) != int and _srid is not None:
            logging.error('{}: {} is not {}'.format('_srid', _srid, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_y": _y,
                 "_x": _x,
                 "_res": _res,
                 "_srid": _srid,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_children_by_aoi(self, _aoi, _res=2, _data=[], _limit=10000):
        """ POST isea3h_children_by_aoi

            This endpoint uses an area of interest(`_aoi`) and a cell resolution (`_res`) to find the cells, within that resolution, that intersect that area. It returns the GID of the DGGS cell.

        Parameters
        ------------
            _aoi : str
                str | Area of interest
            _res : int
                int | Optional, default is 2 | Resolution level
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 | Max number of resulting records

        Returns
        -----------
            response:
                {gid, quad, res, children, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_children_by_aoi'

        # Field type check
        if type(_aoi) != str and _aoi is not None:
            logging.error('{}: {} is not {}'.format('_aoi', _aoi, 'text'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_aoi": _aoi,
                 "_res": _res,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_children_by_cell(self, _gid, _gid_res, _res=2, _data=[], _limit=10000):
        """ POST isea3h_children_by_cell

            This endpoint tasks a target resolution(`_res`) and a latitude/longitude(`_y`/`_x`) coordinate pair. It returns the children of the DGGS cell.

        Parameters
        ------------
            _gid : str[]
                str[] | Grid cell ID
            _gid_res : int
                int | ...
            _res : int
                int | Optional, default is 2 | Resolution level
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 | Max number of resulting records

        Returns
        -----------
            response:
                {gid, quad, res, children, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_children_by_cell'

        # Field type check
        if type(_gid) != list:
            logging.error('{}: {} is not {}'.format('_gid', _gid, 'ARRAY'))
        if type(_gid_res) != int and _gid_res is not None:
            logging.error('{}: {} is not {}'.format('_gid_res', _gid_res, 'integer'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_gid": _gid,
                 "_gid_res": _gid_res,
                 "_res": _res,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_children_by_geojson(self, _geojson='{"type":"Polygon","coordinates":[[[-180,90],[180,90],[180,-90],[-180,-90],[-180,90]]]}', _res=4, _srid=4326, _data=[], _limit=10000):
        """ POST isea3h_children_by_geojson

            This endpoint tasks a target resolution(`_res`) and a geojson geometry. It returns the children of the DGGS that intersects with a polygon/point given in geojson.

        Parameters
        ------------
            _geojson : dict
                dict | Optional, default is '{"type":"Polygon","coordinates":[[[-180,90],[180,90],[180,-90],[-180,-90],[-180,90]]]}' | polygon feature in geojson format
            _res : int
                int | Optional, default is 4 | Resolution level
            _srid : int
                int | Optional, default is 4326 | Spatial Reference System ID
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 | ...

        Returns
        -----------
            response:
                {gid, quad, res, children, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_children_by_geojson'

        # Field type check
        if type(_geojson) != dict and _geojson is not None:
            logging.error('{}: {} is not {}'.format('_geojson', _geojson, 'json'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'smallint'))
        if type(_srid) != int and _srid is not None:
            logging.error('{}: {} is not {}'.format('_srid', _srid, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_geojson": _geojson,
                 "_res": _res,
                 "_srid": _srid,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_children_by_gid(self, _gid, _res, _data=[], _limit=10000):
        """ POST isea3h_children_by_gid

            This endpoint takes a list of `hex16` global identifiers `[_gid]` and a target resolution  `_res`. It returns the children of the DGGS cells that match the given GIDs

        Parameters
        ------------
            _gid : str[]
                str[] | Resolution level
            _res : int
                int | Resolution level
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 |

        Returns
        -----------
            response:
                {gid, quad, res, children, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_children_by_gid'

        # Field type check
        if type(_gid) != list:
            logging.error('{}: {} is not {}'.format('_gid', _gid, 'ARRAY'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_gid": _gid,
                 "_res": _res,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_children_by_point(self, _x, _y, _res, _srid=4326, _data=[], _limit=10000):
        """ POST isea3h_children_by_point

            This endpoint tasks a target resolution(`_res`) and a latitude/longitude(`_y`/`_x`) coordinate pair. It returns the children of the DGGS that intersects with that point.

        Parameters
        ------------
            _x : float
                float | X of the point
            _y : float
                float | Y of the point
            _res : int
                int | Resolution level
            _srid : int
                int | Optional, default is 4326 | Spatial Reference System ID
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 |

        Returns
        -----------
            response:
                {gid, quad, res, children, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_children_by_point'

        # Field type check
        if type(_x) != float and _x is not None:
            logging.error('{}: {} is not {}'.format('_x', _x, 'numeric'))
        if type(_y) != float and _y is not None:
            logging.error('{}: {} is not {}'.format('_y', _y, 'numeric'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_srid) != int and _srid is not None:
            logging.error('{}: {} is not {}'.format('_srid', _srid, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_x": _x,
                 "_y": _y,
                 "_res": _res,
                 "_srid": _srid,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_data_aoi_delete(self, _id):
        """ POST isea3h_data_aoi_delete

            Delete an AOI using its ID

        Parameters
        ------------
            _id : str
                str | AOI

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_data_aoi_delete'

        # Field type check
        if type(_id) != str and _id is not None:
            logging.error('{}: {} is not {}'.format('_id', _id, 'text'))

        # Body
        body = {
                 "_id": _id
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_data_aoi_insert(self, _id, _geojson, _detail=''):
        """ POST isea3h_data_aoi_insert

            This endpoint creates an area of interest table.

        Parameters
        ------------
            _id : str
                str | Area ID
            _geojson : dict
                dict | Geojson of the area
            _detail : str
                str | Optional, default is '' |

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_data_aoi_insert'

        # Field type check
        if type(_id) != str and _id is not None:
            logging.error('{}: {} is not {}'.format('_id', _id, 'text'))
        if type(_geojson) != dict and _geojson is not None:
            logging.error('{}: {} is not {}'.format('_geojson', _geojson, 'json'))
        if type(_detail) != str and _detail is not None:
            logging.error('{}: {} is not {}'.format('_detail', _detail, 'text'))

        # Body
        body = {
                 "_id": _id,
                 "_geojson": _geojson,
                 "_detail": _detail
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_data_aoi_refresh(self, _id):
        """ POST isea3h_data_aoi_refresh

            Refreshes the AOI gids using the currently available cells.

        Parameters
        ------------
            _id : str
                str | AOI

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_data_aoi_refresh'

        # Field type check
        if type(_id) != str and _id is not None:
            logging.error('{}: {} is not {}'.format('_id', _id, 'text'))

        # Body
        body = {
                 "_id": _id
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_data_aoi_select(self, _id, _res):
        """ POST isea3h_data_aoi_select

            Delete an AOI using its ID

        Parameters
        ------------
            _id : str
                str | DGGS resolution
            _res : int
                int |

        Returns
        -----------
            response:
                {gid, res, quad} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_data_aoi_select'

        # Field type check
        if type(_id) != str and _id is not None:
            logging.error('{}: {} is not {}'.format('_id', _id, 'text'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'smallint'))

        # Body
        body = {
                 "_id": _id,
                 "_res": _res
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_data_aoi_update_detail(self, _id, _detail):
        """ POST isea3h_data_aoi_update_detail

            This endpoint creates an area of interest table.

        Parameters
        ------------
            _id : str
                str | Area ID
            _detail : str
                str |

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_data_aoi_update_detail'

        # Field type check
        if type(_id) != str and _id is not None:
            logging.error('{}: {} is not {}'.format('_id', _id, 'text'))
        if type(_detail) != str and _detail is not None:
            logging.error('{}: {} is not {}'.format('_detail', _detail, 'text'))

        # Body
        body = {
                 "_id": _id,
                 "_detail": _detail
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_data_destination_dense_join_region(self, _destination, _res):
        """ POST isea3h_data_destination_dense_join_region



        Parameters
        ------------
            _destination : str[]
                str[] |
            _res : int
                int |

        Returns
        -----------
            response:
                {gid, quad, res, region, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_data_destination_dense_join_region'

        # Field type check
        if type(_destination) != list:
            logging.error('{}: {} is not {}'.format('_destination', _destination, 'ARRAY'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))

        # Body
        body = {
                 "_destination": _destination,
                 "_res": _res
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_data_destination_join(self, _destination, _res):
        """ POST isea3h_data_destination_join



        Parameters
        ------------
            _destination : str[]
                str[] |
            _res : int
                int |

        Returns
        -----------
            response:
                {gid, quad, res, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_data_destination_join'

        # Field type check
        if type(_destination) != list:
            logging.error('{}: {} is not {}'.format('_destination', _destination, 'ARRAY'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))

        # Body
        body = {
                 "_destination": _destination,
                 "_res": _res
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_data_destination_join_region(self, _destination, _res):
        """ POST isea3h_data_destination_join_region



        Parameters
        ------------
            _destination : str[]
                str[] |
            _res : int
                int |

        Returns
        -----------
            response:
                {gid, quad, res, region, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_data_destination_join_region'

        # Field type check
        if type(_destination) != list:
            logging.error('{}: {} is not {}'.format('_destination', _destination, 'ARRAY'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))

        # Body
        body = {
                 "_destination": _destination,
                 "_res": _res
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_data_dst_data_upsert(self, _table_name, _values):
        """ POST isea3h_data_dst_data_upsert



        Parameters
        ------------
            _table_name : str
                str |
            _values : dict
                dict |

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_data_dst_data_upsert'

        # Field type check
        if type(_table_name) != str and _table_name is not None:
            logging.error('{}: {} is not {}'.format('_table_name', _table_name, 'text'))
        if type(_values) != dict and _values is not None:
            logging.error('{}: {} is not {}'.format('_values', _values, 'json'))

        # Body
        body = {
                 "_table_name": _table_name,
                 "_values": _values
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_data_dst_delete(self, _id):
        """ POST isea3h_data_dst_delete



        Parameters
        ------------
            _id : str
                str |

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_data_dst_delete'

        # Field type check
        if type(_id) != str and _id is not None:
            logging.error('{}: {} is not {}'.format('_id', _id, 'text'))

        # Body
        body = {
                 "_id": _id
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_data_dst_insert(self, _id, _col_name, _col_dtype, _col_pkey=[]):
        """ POST isea3h_data_dst_insert

            This endpoint creates a destination table.

        Parameters
        ------------
            _id : str
                str | ID
            _col_name : str[]
                str[] | Array of column names
            _col_dtype : str[]
                str[] | Array of column data types
            _col_pkey : str[]
                str[] | Optional, default is [] |

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_data_dst_insert'

        # Field type check
        if type(_id) != str and _id is not None:
            logging.error('{}: {} is not {}'.format('_id', _id, 'text'))
        if type(_col_name) != list:
            logging.error('{}: {} is not {}'.format('_col_name', _col_name, 'ARRAY'))
        if type(_col_dtype) != list:
            logging.error('{}: {} is not {}'.format('_col_dtype', _col_dtype, 'ARRAY'))
        if type(_col_pkey) != list:
            logging.error('{}: {} is not {}'.format('_col_pkey', _col_pkey, 'ARRAY'))

        # Body
        body = {
                 "_id": _id,
                 "_col_name": _col_name,
                 "_col_dtype": _col_dtype,
                 "_col_pkey": _col_pkey
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_data_dst_refresh_stats(self, _id):
        """ POST isea3h_data_dst_refresh_stats



        Parameters
        ------------
            _id : str
                str |

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_data_dst_refresh_stats'

        # Field type check
        if type(_id) != str and _id is not None:
            logging.error('{}: {} is not {}'.format('_id', _id, 'text'))

        # Body
        body = {
                 "_id": _id
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_data_dst_update_detail(self, _id, _detail):
        """ POST isea3h_data_dst_update_detail

            This endpoint creates an area of interest table.

        Parameters
        ------------
            _id : str
                str | Area ID
            _detail : str
                str |

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_data_dst_update_detail'

        # Field type check
        if type(_id) != str and _id is not None:
            logging.error('{}: {} is not {}'.format('_id', _id, 'text'))
        if type(_detail) != str and _detail is not None:
            logging.error('{}: {} is not {}'.format('_detail', _detail, 'text'))

        # Body
        body = {
                 "_id": _id,
                 "_detail": _detail
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_gid_by_aoi(self, _aoi, _res=2, _data=[], _limit=10000):
        """ POST isea3h_gid_by_aoi

            This endpoint uses an area of interest(`_aoi`) and a cell resolution (`_res`) to find the cells, within that resolution, that intersect that area. It returns the GID of the DGGS cell.

        Parameters
        ------------
            _aoi : str
                str | Area of interest
            _res : int
                int | Optional, default is 2 | Resolution level
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 | Max number of resulting records

        Returns
        -----------
            response:
                {gid, quad, res, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_gid_by_aoi'

        # Field type check
        if type(_aoi) != str and _aoi is not None:
            logging.error('{}: {} is not {}'.format('_aoi', _aoi, 'text'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_aoi": _aoi,
                 "_res": _res,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_gid_by_cell(self, _gid, _gid_res, _res=2, _data=[], _limit=10000):
        """ POST isea3h_gid_by_cell

            This endpoint tasks a target resolution(`_res`) and a latitude/longitude(`_y`/`_x`) coordinate pair. It returns the GID of the DGGS cell.

        Parameters
        ------------
            _gid : str[]
                str[] | Grid cell ID
            _gid_res : int
                int | Resolution for children cells
            _res : int
                int | Optional, default is 2 | Resolution level
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 | Max number of resulting records

        Returns
        -----------
            response:
                {gid, quad, res, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_gid_by_cell'

        # Field type check
        if type(_gid) != list:
            logging.error('{}: {} is not {}'.format('_gid', _gid, 'ARRAY'))
        if type(_gid_res) != int and _gid_res is not None:
            logging.error('{}: {} is not {}'.format('_gid_res', _gid_res, 'integer'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_gid": _gid,
                 "_gid_res": _gid_res,
                 "_res": _res,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_gid_by_geojson(self, _geojson='{"type":"Polygon","coordinates":[[[-180,90],[180,90],[180,-90],[-180,-90],[-180,90]]]}', _res=4, _srid=4326, _data=[], _limit=10000):
        """ POST isea3h_gid_by_geojson

            This endpoint tasks a target resolution(`_res`) and a geojson geometry. It returns the GID of the DGGS that intersects with a polygon/point given in geojson.

        Parameters
        ------------
            _geojson : dict
                dict | Optional, default is '{"type":"Polygon","coordinates":[[[-180,90],[180,90],[180,-90],[-180,-90],[-180,90]]]}' | polygon feature in geojson format
            _res : int
                int | Optional, default is 4 | Resolution level
            _srid : int
                int | Optional, default is 4326 | Spatial Reference System ID
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 | ...

        Returns
        -----------
            response:
                {gid, quad, res, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_gid_by_geojson'

        # Field type check
        if type(_geojson) != dict and _geojson is not None:
            logging.error('{}: {} is not {}'.format('_geojson', _geojson, 'json'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'smallint'))
        if type(_srid) != int and _srid is not None:
            logging.error('{}: {} is not {}'.format('_srid', _srid, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_geojson": _geojson,
                 "_res": _res,
                 "_srid": _srid,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_gid_by_gid(self, _gid, _res, _data=[], _limit=10000):
        """ POST isea3h_gid_by_gid

            This endpoint takes a list of `hex16` global identifiers `[_gid]` and a target resolution  `_res`. It returns the centers of the DGGS cells that match the given GIDs

        Parameters
        ------------
            _gid : str[]
                str[] | Resolution level
            _res : int
                int | Resolution level
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 |

        Returns
        -----------
            response:
                {gid, quad, res, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_gid_by_gid'

        # Field type check
        if type(_gid) != list:
            logging.error('{}: {} is not {}'.format('_gid', _gid, 'ARRAY'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_gid": _gid,
                 "_res": _res,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_gid_by_point(self, _x, _y, _res, _srid=4326, _data=[], _limit=10000):
        """ POST isea3h_gid_by_point

            This endpoint tasks a target resolution(`_res`) and a latitude/longitude(`_y`/`_x`) coordinate pair. It returns the GID of the DGGS that intersects with that point.

        Parameters
        ------------
            _x : float
                float | X of the point
            _y : float
                float | Y of the point
            _res : int
                int | Resolution level
            _srid : int
                int | Optional, default is 4326 | Spatial Reference System ID
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 |

        Returns
        -----------
            response:
                {gid, quad, res, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_gid_by_point'

        # Field type check
        if type(_x) != float and _x is not None:
            logging.error('{}: {} is not {}'.format('_x', _x, 'numeric'))
        if type(_y) != float and _y is not None:
            logging.error('{}: {} is not {}'.format('_y', _y, 'numeric'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_srid) != int and _srid is not None:
            logging.error('{}: {} is not {}'.format('_srid', _srid, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_x": _x,
                 "_y": _y,
                 "_res": _res,
                 "_srid": _srid,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_insert_cell(self, _values, _res):
        """ POST isea3h_insert_cell



        Parameters
        ------------
            _values : dict
                dict |
            _res : int
                int |

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_insert_cell'

        # Field type check
        if type(_values) != dict and _values is not None:
            logging.error('{}: {} is not {}'.format('_values', _values, 'json'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))

        # Body
        body = {
                 "_values": _values,
                 "_res": _res
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_neighbor_by_aoi(self, _aoi, _res=2, _data=[], _limit=10000):
        """ POST isea3h_neighbor_by_aoi

            This endpoint uses an area of interest(`_aoi`) and a cell resolution (`_res`) to find the cells, within that resolution, that intersect that area. It returns the GID of the DGGS cell.

        Parameters
        ------------
            _aoi : str
                str | Area of interest
            _res : int
                int | Optional, default is 2 | Resolution level
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 | Max number of resulting records

        Returns
        -----------
            response:
                {gid, quad, res, neighbor, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_neighbor_by_aoi'

        # Field type check
        if type(_aoi) != str and _aoi is not None:
            logging.error('{}: {} is not {}'.format('_aoi', _aoi, 'text'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_aoi": _aoi,
                 "_res": _res,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_neighbor_by_cell(self, _gid, _gid_res, _res=2, _data=[], _limit=10000):
        """ POST isea3h_neighbor_by_cell

            This endpoint tasks a target resolution(`_res`) and a latitude/longitude(`_y`/`_x`) coordinate pair. It returns the neighbors of the DGGS cell.

        Parameters
        ------------
            _gid : str[]
                str[] | Grid cell ID
            _gid_res : int
                int | ...
            _res : int
                int | Optional, default is 2 | Resolution level
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 | Max number of resulting records

        Returns
        -----------
            response:
                {gid, quad, res, neighbor, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_neighbor_by_cell'

        # Field type check
        if type(_gid) != list:
            logging.error('{}: {} is not {}'.format('_gid', _gid, 'ARRAY'))
        if type(_gid_res) != int and _gid_res is not None:
            logging.error('{}: {} is not {}'.format('_gid_res', _gid_res, 'integer'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_gid": _gid,
                 "_gid_res": _gid_res,
                 "_res": _res,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_neighbor_by_geojson(self, _geojson='{"type":"Polygon","coordinates":[[[-180,90],[180,90],[180,-90],[-180,-90],[-180,90]]]}', _res=4, _srid=4326, _data=[], _limit=10000):
        """ POST isea3h_neighbor_by_geojson

            This endpoint tasks a target resolution(`_res`) and a geojson geometry. It returns the neighbors of the DGGS that intersects with a polygon/point given in geojson.

        Parameters
        ------------
            _geojson : dict
                dict | Optional, default is '{"type":"Polygon","coordinates":[[[-180,90],[180,90],[180,-90],[-180,-90],[-180,90]]]}' | polygon feature in geojson format
            _res : int
                int | Optional, default is 4 | Resolution level
            _srid : int
                int | Optional, default is 4326 | Spatial Reference System ID
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 | ...

        Returns
        -----------
            response:
                {gid, quad, res, neighbor, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_neighbor_by_geojson'

        # Field type check
        if type(_geojson) != dict and _geojson is not None:
            logging.error('{}: {} is not {}'.format('_geojson', _geojson, 'json'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'smallint'))
        if type(_srid) != int and _srid is not None:
            logging.error('{}: {} is not {}'.format('_srid', _srid, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_geojson": _geojson,
                 "_res": _res,
                 "_srid": _srid,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_neighbor_by_gid(self, _gid, _res, _data=[], _limit=10000):
        """ POST isea3h_neighbor_by_gid

            This endpoint takes a list of `hex16` global identifiers `[_gid]` and a target resolution  `_res`. It returns the neighbor of the DGGS cells that match the given GIDs

        Parameters
        ------------
            _gid : str[]
                str[] | Resolution level
            _res : int
                int | Resolution level
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 |

        Returns
        -----------
            response:
                {gid, quad, res, neighbor, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_neighbor_by_gid'

        # Field type check
        if type(_gid) != list:
            logging.error('{}: {} is not {}'.format('_gid', _gid, 'ARRAY'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_gid": _gid,
                 "_res": _res,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_neighbor_by_point(self, _x, _y, _res, _srid=4326, _data=[], _limit=10000):
        """ POST isea3h_neighbor_by_point

            This endpoint tasks a target resolution(`_res`) and a latitude/longitude(`_y`/`_x`) coordinate pair. It returns the neighbors of the DGGS that intersects with that point.

        Parameters
        ------------
            _x : float
                float | X of the point
            _y : float
                float | Y of the point
            _res : int
                int | Resolution level
            _srid : int
                int | Optional, default is 4326 | Spatial Reference System ID
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 |

        Returns
        -----------
            response:
                {gid, quad, res, neighbor, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_neighbor_by_point'

        # Field type check
        if type(_x) != float and _x is not None:
            logging.error('{}: {} is not {}'.format('_x', _x, 'numeric'))
        if type(_y) != float and _y is not None:
            logging.error('{}: {} is not {}'.format('_y', _y, 'numeric'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_srid) != int and _srid is not None:
            logging.error('{}: {} is not {}'.format('_srid', _srid, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_x": _x,
                 "_y": _y,
                 "_res": _res,
                 "_srid": _srid,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_region_by_aoi(self, _aoi, _res=2, _data=[], _limit=10000):
        """ POST isea3h_region_by_aoi

            This endpoint uses an area of interest(`_aoi`) and a cell resolution (`_res`) to find the cells, within that resolution, that intersect that area. It returns the GID of the DGGS cell.

        Parameters
        ------------
            _aoi : str
                str | Area of interest
            _res : int
                int | Optional, default is 2 | Resolution level
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 | Max number of resulting records

        Returns
        -----------
            response:
                {gid, quad, res, region, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_region_by_aoi'

        # Field type check
        if type(_aoi) != str and _aoi is not None:
            logging.error('{}: {} is not {}'.format('_aoi', _aoi, 'text'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_aoi": _aoi,
                 "_res": _res,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_region_by_cell(self, _gid, _gid_res, _res=2, _data=[], _limit=10000):
        """ POST isea3h_region_by_cell

            This endpoint tasks a target resolution(`_res`) and a latitude/longitude(`_y`/`_x`) coordinate pair. It returns the region of the DGGS cell.

        Parameters
        ------------
            _gid : str[]
                str[] | Grid cell ID
            _gid_res : int
                int | ...
            _res : int
                int | Optional, default is 2 | Resolution level
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 | Max number of resulting records

        Returns
        -----------
            response:
                {gid, quad, res, region, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_region_by_cell'

        # Field type check
        if type(_gid) != list:
            logging.error('{}: {} is not {}'.format('_gid', _gid, 'ARRAY'))
        if type(_gid_res) != int and _gid_res is not None:
            logging.error('{}: {} is not {}'.format('_gid_res', _gid_res, 'integer'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_gid": _gid,
                 "_gid_res": _gid_res,
                 "_res": _res,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_region_by_cell_ras2dggs(self, _gid, _gid_res, _res=2, _limit=10000):
        """ POST isea3h_region_by_cell_ras2dggs

            This endpoint is specific for ras2dggs

        Parameters
        ------------
            _gid : str
                str | Grid cell ID
            _gid_res : int
                int | ...
            _res : int
                int | Optional, default is 2 | Resolution level
            _limit : int
                int | Optional, default is 10000 | Max number of resulting records

        Returns
        -----------
            response:
                {gid, quad, res, region} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_region_by_cell_ras2dggs'

        # Field type check
        if type(_gid) != str and _gid is not None:
            logging.error('{}: {} is not {}'.format('_gid', _gid, 'text'))
        if type(_gid_res) != int and _gid_res is not None:
            logging.error('{}: {} is not {}'.format('_gid_res', _gid_res, 'integer'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_gid": _gid,
                 "_gid_res": _gid_res,
                 "_res": _res,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_region_by_geojson(self, _geojson='{"type":"Polygon","coordinates":[[[-180,90],[180,90],[180,-90],[-180,-90],[-180,90]]]}', _res=4, _srid=4326, _data=[], _limit=10000):
        """ POST isea3h_region_by_geojson

            This endpoint tasks a target resolution(`_res`) and a geojson geometry. It returns the region of the DGGS that intersects with a polygon/point given in geojson.

        Parameters
        ------------
            _geojson : dict
                dict | Optional, default is '{"type":"Polygon","coordinates":[[[-180,90],[180,90],[180,-90],[-180,-90],[-180,90]]]}' | polygon feature in geojson format
            _res : int
                int | Optional, default is 4 | Resolution level
            _srid : int
                int | Optional, default is 4326 | Spatial Reference System ID
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 | ...

        Returns
        -----------
            response:
                {gid, quad, res, region, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_region_by_geojson'

        # Field type check
        if type(_geojson) != dict and _geojson is not None:
            logging.error('{}: {} is not {}'.format('_geojson', _geojson, 'json'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'smallint'))
        if type(_srid) != int and _srid is not None:
            logging.error('{}: {} is not {}'.format('_srid', _srid, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_geojson": _geojson,
                 "_res": _res,
                 "_srid": _srid,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_region_by_gid(self, _gid, _res, _data=[], _limit=10000):
        """ POST isea3h_region_by_gid

            This endpoint takes a list of `hex16` global identifiers `[_gid]` and a target resolution  `_res`. It returns the regions of the DGGS cells that match the given GIDs

        Parameters
        ------------
            _gid : str[]
                str[] | Resolution level
            _res : int
                int | Resolution level
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 |

        Returns
        -----------
            response:
                {gid, quad, res, region, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_region_by_gid'

        # Field type check
        if type(_gid) != list:
            logging.error('{}: {} is not {}'.format('_gid', _gid, 'ARRAY'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_gid": _gid,
                 "_res": _res,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_region_by_point(self, _x, _y, _res, _srid=4326, _data=[], _limit=10000):
        """ POST isea3h_region_by_point

            This endpoint tasks a target resolution(`_res`) and a latitude/longitude(`_y`/`_x`) coordinate pair. It returns the region of the DGGS that intersects with that point.

        Parameters
        ------------
            _x : float
                float | X of the point
            _y : float
                float | Y of the point
            _res : int
                int | Resolution level
            _srid : int
                int | Optional, default is 4326 | Spatial Reference System ID
            _data : str[]
                str[] | Optional, default is [] |
            _limit : int
                int | Optional, default is 10000 |

        Returns
        -----------
            response:
                {gid, quad, res, region, properties} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_region_by_point'

        # Field type check
        if type(_x) != float and _x is not None:
            logging.error('{}: {} is not {}'.format('_x', _x, 'numeric'))
        if type(_y) != float and _y is not None:
            logging.error('{}: {} is not {}'.format('_y', _y, 'numeric'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))
        if type(_srid) != int and _srid is not None:
            logging.error('{}: {} is not {}'.format('_srid', _srid, 'integer'))
        if type(_data) != list:
            logging.error('{}: {} is not {}'.format('_data', _data, 'ARRAY'))
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_x": _x,
                 "_y": _y,
                 "_res": _res,
                 "_srid": _srid,
                 "_data": _data,
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def isea3h_region_get_1435(self, _gid, _res):
        """ POST isea3h_region_get_1435

            This endpoint takes a list of `hex16` global identifiers `[_gid]` and a target resolution  `_res`. It returns the regions of the DGGS cells that match the given GIDs

        Parameters
        ------------
            _gid : str[]
                str[] | Resolution level
            _res : int
                int | Resolution level

        Returns
        -----------
            response:
                {gid, quad, res, region} response object

        """

        # Endpoint
        endpoint = '/rpc/isea3h_region_get_1435'

        # Field type check
        if type(_gid) != list:
            logging.error('{}: {} is not {}'.format('_gid', _gid, 'ARRAY'))
        if type(_res) != int and _res is not None:
            logging.error('{}: {} is not {}'.format('_res', _res, 'integer'))

        # Body
        body = {
                 "_gid": _gid,
                 "_res": _res
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def public_obfuscation_by_point(self, _hf):
        """ POST public_obfuscation_by_point



        Parameters
        ------------
            _hf : dict]
                dict] |

        Returns
        -----------
            response:
                {obfuscated_hf} response object

        """

        # Endpoint
        endpoint = '/rpc/public_obfuscation_by_point'

        # Field type check
        if type(_hf) != list:
            logging.error('{}: {} is not {}'.format('_hf', _hf, 'ARRAY'))

        # Body
        body = {
                 "_hf": _hf
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_gendggs_batch(self, _limit=1):
        """ POST task_gendggs_batch

            Get a batch of gendggs task IDs

        Parameters
        ------------
            _limit : int
                int | Optional, default is 1 | The number of tasks in the batch

        Returns
        -----------
            response:
                {task_id} response object

        """

        # Endpoint
        endpoint = '/rpc/task_gendggs_batch'

        # Field type check
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_gendggs_by_id(self, _task_id):
        """ POST task_gendggs_by_id

            Get gendggs task by a task_id

        Parameters
        ------------
            _task_id : str
                str | Task ID

        Returns
        -----------
            response:
                {task_id, priority, status, dggrid_operation, verbosity, update_frequency, coord_precision, dggs_type, dggs_aperture, longitude_wrap_mode, unwrap_points, dggs_res_spec, clip_subset_type, input_address_type, clip_cell_res, clip_cell_addresses, output_cell_label_type, output_address_type, cell_output_type, point_output_type, children_output_type, neighbor_output_type, collection_output_gdal_format} response object

        """

        # Endpoint
        endpoint = '/rpc/task_gendggs_by_id'

        # Field type check
        if type(_task_id) != str and _task_id is not None:
            logging.error('{}: {} is not {}'.format('_task_id', _task_id, 'uuid'))

        # Body
        body = {
                 "_task_id": _task_id
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_gendggs_delete(self, _task_id):
        """ POST task_gendggs_delete

            Delete a gendggs task by a task_id

        Parameters
        ------------
            _task_id : str[]
                str[] | Task ID

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/task_gendggs_delete'

        # Field type check
        if type(_task_id) != list:
            logging.error('{}: {} is not {}'.format('_task_id', _task_id, 'ARRAY'))

        # Body
        body = {
                 "_task_id": _task_id
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_gendggs_insert(self, _priority, _dggrid_operation, _verbosity, _dggs_res_spec, _clip_subset_type, _input_address_type, _clip_cell_res, _clip_cell_addresses):
        """ POST task_gendggs_insert

            This endpoint inserts a new gendggs task

        Parameters
        ------------
            _priority : int
                int | Priority
            _dggrid_operation : str
                str | Operation grid
            _verbosity : int
                int | Verbosity
            _dggs_res_spec : int[]
                int[] | Resolution specification
            _clip_subset_type : str
                str | Clip subset type
            _input_address_type : str
                str | Type of address
            _clip_cell_res : int
                int | Cell resolution
            _clip_cell_addresses : str[]
                str[] | Clip cell addresses

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/task_gendggs_insert'

        # Field type check
        if type(_priority) != int and _priority is not None:
            logging.error('{}: {} is not {}'.format('_priority', _priority, 'smallint'))
        if type(_dggrid_operation) != str and _dggrid_operation is not None:
            logging.error('{}: {} is not {}'.format('_dggrid_operation', _dggrid_operation, 'text'))
        if type(_verbosity) != int and _verbosity is not None:
            logging.error('{}: {} is not {}'.format('_verbosity', _verbosity, 'integer'))
        if type(_dggs_res_spec) != list:
            logging.error('{}: {} is not {}'.format('_dggs_res_spec', _dggs_res_spec, 'ARRAY'))
        if type(_clip_subset_type) != str and _clip_subset_type is not None:
            logging.error('{}: {} is not {}'.format('_clip_subset_type', _clip_subset_type, 'text'))
        if type(_input_address_type) != str and _input_address_type is not None:
            logging.error('{}: {} is not {}'.format('_input_address_type', _input_address_type, 'text'))
        if type(_clip_cell_res) != int and _clip_cell_res is not None:
            logging.error('{}: {} is not {}'.format('_clip_cell_res', _clip_cell_res, 'integer'))
        if type(_clip_cell_addresses) != list:
            logging.error('{}: {} is not {}'.format('_clip_cell_addresses', _clip_cell_addresses, 'ARRAY'))

        # Body
        body = {
                 "_priority": _priority,
                 "_dggrid_operation": _dggrid_operation,
                 "_verbosity": _verbosity,
                 "_dggs_res_spec": _dggs_res_spec,
                 "_clip_subset_type": _clip_subset_type,
                 "_input_address_type": _input_address_type,
                 "_clip_cell_res": _clip_cell_res,
                 "_clip_cell_addresses": _clip_cell_addresses
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_gendggs_set_status(self, _task_id, _status):
        """ POST task_gendggs_set_status

            Updating a gendggs task status

        Parameters
        ------------
            _task_id : str[]
                str[] | Task ID
            _status : int
                int | The status of the task

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/task_gendggs_set_status'

        # Field type check
        if type(_task_id) != list:
            logging.error('{}: {} is not {}'.format('_task_id', _task_id, 'ARRAY'))
        if type(_status) != int and _status is not None:
            logging.error('{}: {} is not {}'.format('_status', _status, 'integer'))

        # Body
        body = {
                 "_task_id": _task_id,
                 "_status": _status
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_gendggs_update(self, _task_id, _priority, _dggrid_operation, _verbosity, _dggs_res_spec, _clip_subset_type, _input_address_type, _clip_cell_res, _clip_cell_addresses):
        """ POST task_gendggs_update

            This endpoint updates a gendggs task

        Parameters
        ------------
            _task_id : str
                str | The task ID
            _priority : int
                int | Priority
            _dggrid_operation : str
                str | Operation grid
            _verbosity : int
                int | Verbosity
            _dggs_res_spec : int[]
                int[] | Resolution specification
            _clip_subset_type : str
                str | Clip subset type
            _input_address_type : str
                str | Type of address
            _clip_cell_res : int
                int | Cell resolution
            _clip_cell_addresses : str[]
                str[] | Clip cell addresses

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/task_gendggs_update'

        # Field type check
        if type(_task_id) != str and _task_id is not None:
            logging.error('{}: {} is not {}'.format('_task_id', _task_id, 'uuid'))
        if type(_priority) != int and _priority is not None:
            logging.error('{}: {} is not {}'.format('_priority', _priority, 'smallint'))
        if type(_dggrid_operation) != str and _dggrid_operation is not None:
            logging.error('{}: {} is not {}'.format('_dggrid_operation', _dggrid_operation, 'text'))
        if type(_verbosity) != int and _verbosity is not None:
            logging.error('{}: {} is not {}'.format('_verbosity', _verbosity, 'integer'))
        if type(_dggs_res_spec) != list:
            logging.error('{}: {} is not {}'.format('_dggs_res_spec', _dggs_res_spec, 'ARRAY'))
        if type(_clip_subset_type) != str and _clip_subset_type is not None:
            logging.error('{}: {} is not {}'.format('_clip_subset_type', _clip_subset_type, 'text'))
        if type(_input_address_type) != str and _input_address_type is not None:
            logging.error('{}: {} is not {}'.format('_input_address_type', _input_address_type, 'text'))
        if type(_clip_cell_res) != int and _clip_cell_res is not None:
            logging.error('{}: {} is not {}'.format('_clip_cell_res', _clip_cell_res, 'integer'))
        if type(_clip_cell_addresses) != list:
            logging.error('{}: {} is not {}'.format('_clip_cell_addresses', _clip_cell_addresses, 'ARRAY'))

        # Body
        body = {
                 "_task_id": _task_id,
                 "_priority": _priority,
                 "_dggrid_operation": _dggrid_operation,
                 "_verbosity": _verbosity,
                 "_dggs_res_spec": _dggs_res_spec,
                 "_clip_subset_type": _clip_subset_type,
                 "_input_address_type": _input_address_type,
                 "_clip_cell_res": _clip_cell_res,
                 "_clip_cell_addresses": _clip_cell_addresses
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_pipeline_batch(self, _limit=1):
        """ POST task_pipeline_batch

            Get a batch of pipeline tasks

        Parameters
        ------------
            _limit : int
                int | Optional, default is 1 | The number of tasks in the batch

        Returns
        -----------
            response:
                {task_id} response object

        """

        # Endpoint
        endpoint = '/rpc/task_pipeline_batch'

        # Field type check
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_pipeline_by_id(self, _task_id):
        """ POST task_pipeline_by_id

            Get a pipeline task by its ID

        Parameters
        ------------
            _task_id : str
                str | Task ID

        Returns
        -----------
            response:
                {task_id, priority, status, processor, pipe, s3_bucket, description, license, start_date, end_date, resolution, bands, ts, ts_interval, nodata, format, value, comment} response object

        """

        # Endpoint
        endpoint = '/rpc/task_pipeline_by_id'

        # Field type check
        if type(_task_id) != str and _task_id is not None:
            logging.error('{}: {} is not {}'.format('_task_id', _task_id, 'uuid'))

        # Body
        body = {
                 "_task_id": _task_id
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_pipeline_delete(self, _task_id):
        """ POST task_pipeline_delete

            Delete a pipeline task

        Parameters
        ------------
            _task_id : str[]
                str[] | The ID of the task

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/task_pipeline_delete'

        # Field type check
        if type(_task_id) != list:
            logging.error('{}: {} is not {}'.format('_task_id', _task_id, 'ARRAY'))

        # Body
        body = {
                 "_task_id": _task_id
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_pipeline_insert(self, _priority, _processor, _pipe, _s3_bucket, _description, _license, _start_date, _end_date, _resolution, _bands, _ts, _ts_interval, _nodata, _format, _value, _comment):
        """ POST task_pipeline_insert

            This endpoint inserts a pipeline task.

        Parameters
        ------------
            _priority : int
                int | Priority
            _processor : str
                str | Processor
            _pipe : dict
                dict | Pipe
            _s3_bucket : str
                str | S3 Bucket
            _description : str
                str | Description
            _license : str
                str | License
            _start_date : str
                str | Start date
            _end_date : str
                str | End date
            _resolution : float
                float | Resolution
            _bands : int
                int | Bands
            _ts : bool
                bool | Time Series
            _ts_interval : str
                str | Time Series Interval
            _nodata : int
                int | NoData Value
            _format : str
                str | Format
            _value : str
                str | Value
            _comment : str
                str | Comment

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/task_pipeline_insert'

        # Field type check
        if type(_priority) != int and _priority is not None:
            logging.error('{}: {} is not {}'.format('_priority', _priority, 'smallint'))
        if type(_processor) != str and _processor is not None:
            logging.error('{}: {} is not {}'.format('_processor', _processor, 'text'))
        if type(_pipe) != dict and _pipe is not None:
            logging.error('{}: {} is not {}'.format('_pipe', _pipe, 'json'))
        if type(_s3_bucket) != str and _s3_bucket is not None:
            logging.error('{}: {} is not {}'.format('_s3_bucket', _s3_bucket, 'text'))
        if type(_description) != str and _description is not None:
            logging.error('{}: {} is not {}'.format('_description', _description, 'text'))
        if type(_license) != str and _license is not None:
            logging.error('{}: {} is not {}'.format('_license', _license, 'text'))
        if type(_start_date) != str and _start_date is not None:
            logging.error('{}: {} is not {}'.format('_start_date', _start_date, 'timestamp without time zone'))
        if type(_end_date) != str and _end_date is not None:
            logging.error('{}: {} is not {}'.format('_end_date', _end_date, 'timestamp without time zone'))
        if type(_resolution) != float and _resolution is not None:
            logging.error('{}: {} is not {}'.format('_resolution', _resolution, 'numeric'))
        if type(_bands) != int and _bands is not None:
            logging.error('{}: {} is not {}'.format('_bands', _bands, 'integer'))
        if type(_ts) != bool and _ts is not None:
            logging.error('{}: {} is not {}'.format('_ts', _ts, 'boolean'))
        if type(_ts_interval) != str and _ts_interval is not None:
            logging.error('{}: {} is not {}'.format('_ts_interval', _ts_interval, 'interval'))
        if type(_nodata) != int and _nodata is not None:
            logging.error('{}: {} is not {}'.format('_nodata', _nodata, 'integer'))
        if type(_format) != str and _format is not None:
            logging.error('{}: {} is not {}'.format('_format', _format, 'text'))
        if type(_value) != str and _value is not None:
            logging.error('{}: {} is not {}'.format('_value', _value, 'text'))
        if type(_comment) != str and _comment is not None:
            logging.error('{}: {} is not {}'.format('_comment', _comment, 'text'))

        # Body
        body = {
                 "_priority": _priority,
                 "_processor": _processor,
                 "_pipe": _pipe,
                 "_s3_bucket": _s3_bucket,
                 "_description": _description,
                 "_license": _license,
                 "_start_date": _start_date,
                 "_end_date": _end_date,
                 "_resolution": _resolution,
                 "_bands": _bands,
                 "_ts": _ts,
                 "_ts_interval": _ts_interval,
                 "_nodata": _nodata,
                 "_format": _format,
                 "_value": _value,
                 "_comment": _comment
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_pipeline_s3_bucket_update(self, _task_id, _s3_bucket):
        """ POST task_pipeline_s3_bucket_update

            Update the S3 bucket of a pipeline task

        Parameters
        ------------
            _task_id : str
                str | The ID of the task
            _s3_bucket : str
                str | The S3 bucket

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/task_pipeline_s3_bucket_update'

        # Field type check
        if type(_task_id) != str and _task_id is not None:
            logging.error('{}: {} is not {}'.format('_task_id', _task_id, 'uuid'))
        if type(_s3_bucket) != str and _s3_bucket is not None:
            logging.error('{}: {} is not {}'.format('_s3_bucket', _s3_bucket, 'text'))

        # Body
        body = {
                 "_task_id": _task_id,
                 "_s3_bucket": _s3_bucket
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_pipeline_set_status(self, _task_id, _status):
        """ POST task_pipeline_set_status

            Updating a pipeline task status

        Parameters
        ------------
            _task_id : str[]
                str[] | Task ID
            _status : int
                int | The status of the task

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/task_pipeline_set_status'

        # Field type check
        if type(_task_id) != list:
            logging.error('{}: {} is not {}'.format('_task_id', _task_id, 'ARRAY'))
        if type(_status) != int and _status is not None:
            logging.error('{}: {} is not {}'.format('_status', _status, 'integer'))

        # Body
        body = {
                 "_task_id": _task_id,
                 "_status": _status
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_pipeline_update(self, _task_id, _priority, _processor, _pipe, _s3_bucket, _description, _license, _start_date, _end_date, _resolution, _bands, _ts, _ts_interval, _nodata, _format, _value, _comment):
        """ POST task_pipeline_update

            Update a pipeline task

        Parameters
        ------------
            _task_id : str
                str | The ID of the task
            _priority : int
                int | Priority of the task
            _processor : str
                str | The processor used for the pipeline
            _pipe : dict
                dict | The pipe in json format that contains all variables necessary for the processor
            _s3_bucket : str
                str | The S3 bucket where the input data is stored
            _description : str
                str | The description of the dataset
            _license : str
                str | The license of the dataset
            _start_date : str
                str | The start date of the dataset
            _end_date : str
                str | The end date of the dataset
            _resolution : float
                float | The approxiamte resolution of the dataset in meters
            _bands : int
                int | The number of bands of the dataset
            _ts : bool
                bool | Is it a time series dataset yes/no
            _ts_interval : str
                str | The interval of the time series
            _nodata : int
                int | The NODATA value of the dataset
            _format : str
                str | The format of the dataset
            _value : str
                str | The value of the dataset
            _comment : str
                str | Additional comments about this pipeline

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/task_pipeline_update'

        # Field type check
        if type(_task_id) != str and _task_id is not None:
            logging.error('{}: {} is not {}'.format('_task_id', _task_id, 'uuid'))
        if type(_priority) != int and _priority is not None:
            logging.error('{}: {} is not {}'.format('_priority', _priority, 'smallint'))
        if type(_processor) != str and _processor is not None:
            logging.error('{}: {} is not {}'.format('_processor', _processor, 'text'))
        if type(_pipe) != dict and _pipe is not None:
            logging.error('{}: {} is not {}'.format('_pipe', _pipe, 'json'))
        if type(_s3_bucket) != str and _s3_bucket is not None:
            logging.error('{}: {} is not {}'.format('_s3_bucket', _s3_bucket, 'text'))
        if type(_description) != str and _description is not None:
            logging.error('{}: {} is not {}'.format('_description', _description, 'text'))
        if type(_license) != str and _license is not None:
            logging.error('{}: {} is not {}'.format('_license', _license, 'text'))
        if type(_start_date) != str and _start_date is not None:
            logging.error('{}: {} is not {}'.format('_start_date', _start_date, 'timestamp without time zone'))
        if type(_end_date) != str and _end_date is not None:
            logging.error('{}: {} is not {}'.format('_end_date', _end_date, 'timestamp without time zone'))
        if type(_resolution) != float and _resolution is not None:
            logging.error('{}: {} is not {}'.format('_resolution', _resolution, 'numeric'))
        if type(_bands) != int and _bands is not None:
            logging.error('{}: {} is not {}'.format('_bands', _bands, 'integer'))
        if type(_ts) != bool and _ts is not None:
            logging.error('{}: {} is not {}'.format('_ts', _ts, 'boolean'))
        if type(_ts_interval) != str and _ts_interval is not None:
            logging.error('{}: {} is not {}'.format('_ts_interval', _ts_interval, 'interval'))
        if type(_nodata) != int and _nodata is not None:
            logging.error('{}: {} is not {}'.format('_nodata', _nodata, 'integer'))
        if type(_format) != str and _format is not None:
            logging.error('{}: {} is not {}'.format('_format', _format, 'text'))
        if type(_value) != str and _value is not None:
            logging.error('{}: {} is not {}'.format('_value', _value, 'text'))
        if type(_comment) != str and _comment is not None:
            logging.error('{}: {} is not {}'.format('_comment', _comment, 'text'))

        # Body
        body = {
                 "_task_id": _task_id,
                 "_priority": _priority,
                 "_processor": _processor,
                 "_pipe": _pipe,
                 "_s3_bucket": _s3_bucket,
                 "_description": _description,
                 "_license": _license,
                 "_start_date": _start_date,
                 "_end_date": _end_date,
                 "_resolution": _resolution,
                 "_bands": _bands,
                 "_ts": _ts,
                 "_ts_interval": _ts_interval,
                 "_nodata": _nodata,
                 "_format": _format,
                 "_value": _value,
                 "_comment": _comment
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_ras2dggs_batch(self, _limit=1):
        """ POST task_ras2dggs_batch

            Get a batch of ras2dggs tasks

        Parameters
        ------------
            _limit : int
                int | Optional, default is 1 | The number of tasks in the batch

        Returns
        -----------
            response:
                {task_id} response object

        """

        # Endpoint
        endpoint = '/rpc/task_ras2dggs_batch'

        # Field type check
        if type(_limit) != int and _limit is not None:
            logging.error('{}: {} is not {}'.format('_limit', _limit, 'integer'))

        # Body
        body = {
                 "_limit": _limit
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_ras2dggs_by_id(self, _task_id):
        """ POST task_ras2dggs_by_id

            Get a ras2dggs task by its ID

        Parameters
        ------------
            _task_id : str
                str | Task ID

        Returns
        -----------
            response:
                {task_id, priority, status, pipeline_id, statistic, res, clip_gid, clip_gid_res} response object

        """

        # Endpoint
        endpoint = '/rpc/task_ras2dggs_by_id'

        # Field type check
        if type(_task_id) != str and _task_id is not None:
            logging.error('{}: {} is not {}'.format('_task_id', _task_id, 'uuid'))

        # Body
        body = {
                 "_task_id": _task_id
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_ras2dggs_delete(self, _task_id):
        """ POST task_ras2dggs_delete

            Deleting a ras2dggs task

        Parameters
        ------------
            _task_id : str[]
                str[] | Task ID

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/task_ras2dggs_delete'

        # Field type check
        if type(_task_id) != list:
            logging.error('{}: {} is not {}'.format('_task_id', _task_id, 'ARRAY'))

        # Body
        body = {
                 "_task_id": _task_id
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_ras2dggs_insert(self, _priority, _pipeline_id, _statistic, _res, _clip_gid, _clip_gid_res):
        """ POST task_ras2dggs_insert

            Inserting a ras2dggs task status

        Parameters
        ------------
            _priority : int
                int | Priority of the task
            _pipeline_id : str
                str | The pipeline ID
            _statistic : str
                str | The statistics to be calculated
            _res : int[]
                int[] | The DGGS resolution
            _clip_gid : str[]
                str[] | The gid of the clipping cell
            _clip_gid_res : int
                int | The resolution of the clipping cell

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/task_ras2dggs_insert'

        # Field type check
        if type(_priority) != int and _priority is not None:
            logging.error('{}: {} is not {}'.format('_priority', _priority, 'smallint'))
        if type(_pipeline_id) != str and _pipeline_id is not None:
            logging.error('{}: {} is not {}'.format('_pipeline_id', _pipeline_id, 'uuid'))
        if type(_statistic) != str and _statistic is not None:
            logging.error('{}: {} is not {}'.format('_statistic', _statistic, 'text'))
        if type(_res) != list:
            logging.error('{}: {} is not {}'.format('_res', _res, 'ARRAY'))
        if type(_clip_gid) != list:
            logging.error('{}: {} is not {}'.format('_clip_gid', _clip_gid, 'ARRAY'))
        if type(_clip_gid_res) != int and _clip_gid_res is not None:
            logging.error('{}: {} is not {}'.format('_clip_gid_res', _clip_gid_res, 'integer'))

        # Body
        body = {
                 "_priority": _priority,
                 "_pipeline_id": _pipeline_id,
                 "_statistic": _statistic,
                 "_res": _res,
                 "_clip_gid": _clip_gid,
                 "_clip_gid_res": _clip_gid_res
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_ras2dggs_set_status(self, _task_id, _status):
        """ POST task_ras2dggs_set_status

            Updating a ras2dggs task status

        Parameters
        ------------
            _task_id : str[]
                str[] | Task ID
            _status : int
                int | The status of the task

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/task_ras2dggs_set_status'

        # Field type check
        if type(_task_id) != list:
            logging.error('{}: {} is not {}'.format('_task_id', _task_id, 'ARRAY'))
        if type(_status) != int and _status is not None:
            logging.error('{}: {} is not {}'.format('_status', _status, 'integer'))

        # Body
        body = {
                 "_task_id": _task_id,
                 "_status": _status
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)

    def task_ras2dggs_update(self, _task_id, _priority, _pipeline_id, _statistic, _res, _clip_gid, _clip_gid_res):
        """ POST task_ras2dggs_update

            Updating a ras2dggs task

        Parameters
        ------------
            _task_id : str
                str | Task ID
            _priority : int
                int | Priority of the task
            _pipeline_id : str
                str | The pipeline ID
            _statistic : str
                str | The statistics to be calculated
            _res : int[]
                int[] | The DGGS resolution
            _clip_gid : str[]
                str[] | The gid of the clipping cell
            _clip_gid_res : int
                int | The resolution of the clipping cell

        Returns
        -----------
            response:
                {} response object

        """

        # Endpoint
        endpoint = '/rpc/task_ras2dggs_update'

        # Field type check
        if type(_task_id) != str and _task_id is not None:
            logging.error('{}: {} is not {}'.format('_task_id', _task_id, 'uuid'))
        if type(_priority) != int and _priority is not None:
            logging.error('{}: {} is not {}'.format('_priority', _priority, 'smallint'))
        if type(_pipeline_id) != str and _pipeline_id is not None:
            logging.error('{}: {} is not {}'.format('_pipeline_id', _pipeline_id, 'uuid'))
        if type(_statistic) != str and _statistic is not None:
            logging.error('{}: {} is not {}'.format('_statistic', _statistic, 'text'))
        if type(_res) != list:
            logging.error('{}: {} is not {}'.format('_res', _res, 'ARRAY'))
        if type(_clip_gid) != list:
            logging.error('{}: {} is not {}'.format('_clip_gid', _clip_gid, 'ARRAY'))
        if type(_clip_gid_res) != int and _clip_gid_res is not None:
            logging.error('{}: {} is not {}'.format('_clip_gid_res', _clip_gid_res, 'integer'))

        # Body
        body = {
                 "_task_id": _task_id,
                 "_priority": _priority,
                 "_pipeline_id": _pipeline_id,
                 "_statistic": _statistic,
                 "_res": _res,
                 "_clip_gid": _clip_gid,
                 "_clip_gid_res": _clip_gid_res
                }

        return requests.post(self.url + endpoint, json=body, headers=self.headers)


