import warnings
import json
import os
import pdb
import numpy as np
import pandas as pd
from seleya import SurfaceDBAPI
from seleya import SurfaceMGAPI
from seleya import DBAPI
from seleya.Toolset import blob_service
from seleya.utilities.kd_logger import kd_logger
from joblib import load

# supress sklearn warnings
warnings.filterwarnings(action='ignore', category=UserWarning)


class S2F(object):

    def __init__(self, sector_code):
        self._local_dir = os.environ['local_dir']
        self._db_engine = DBAPI.FetchEngine.create_engine('sly')
        self._blob_svc = blob_service.BlobService()
        self._sector_code = sector_code
        self._probability_cols = [
            'ratingBusinessOutlook', 'ratingRecommendToFriend', 'ratingCeo'
        ]
        self._mean_cols = [
            'ratingWorkLifeBalance', 'ratingCultureAndValues',
            'ratingSeniorLeadership', 'ratingCareerOpportunities',
            'ratingOverall', 'ratingCompensationAndBenefits',
            'ratingDiversityAndInclusion'
        ]
        self._gd_cols = self._probability_cols + self._mean_cols
        self._iso_ems_score_map = {
            'No': 0,
            'ISO 14000': 1,
            'EMS': 1,
            'Both': 2
        }
        self._target_original_list = [
            'return_on_assets', 'return_on_equity', 'debt_to_equity',
            'revenue_total_employees', 'free_cash_flow_margin'
        ]
        self._target_list = []
        for target_original in self._target_original_list:
            for offset in range(1, 4):
                self._target_list.append(f"{target_original}_{offset}y_change")

    def run(self, begin_date='2014-01-01', end_date='2022-01-01'):
        kd_logger.info('Fetching sector data')
        sector_peers = SurfaceDBAPI.Sector().fetch(
            sector_code=self._sector_code, columns=['code', 'sector_id'])
        if sector_peers.empty:
            kd_logger.error('Sector data is empty')
            return None
        kd_logger.info(
            f"{self._sector_code} has {len(sector_peers)} companies")
        codes = sector_peers['code'].unique().tolist()

        sasb_sector = SurfaceDBAPI.SASBMapdom().fetch_sector(
            sector_code=self._sector_code, columns=['column_name', 'trcode'])
        sasb_sector = sasb_sector.dropna(subset=['trcode']).drop_duplicates(
            subset=['trcode'])
        sasb_sector = sasb_sector[~sasb_sector['trcode'].str.startswith('TR.F.'
                                                                        )]
        kd_logger.info(
            f"{self._sector_code} has {len(sasb_sector)} material metrics")

        names = DBAPI.ESGMetricsDetailFactory(self._db_engine).name()
        clause_list = [
            names.index_metric == 1,
            names.trcode.in_(sasb_sector['trcode'].tolist())
        ]
        esg_details_sector = DBAPI.ESGMetricsDetailFactory(
            self._db_engine).customize(
                clause_list=clause_list,
                columns=['trcode', 'category', 'column_name', 'polarity'])
        metrics_list = esg_details_sector['column_name'].unique().tolist()
        kd_logger.info(f"{self._sector_code} esg metrics detail pulled")

        metrics_data = DBAPI.SASBMetricsFactory(self._db_engine).result(
            codes=codes,
            column_name=esg_details_sector['column_name'].tolist(),
            begin_date=begin_date,
            end_date=end_date).drop(['quarter'], axis=1)

        company_data = DBAPI.CompanyFactory(self._db_engine).result(
            codes=codes,
            primary=[1],
            columns=['code', 'region', 'mkt_cap'],
            key='code')

        metrics_data['date'] = metrics_data['date'].apply(
            lambda x: x.strftime('%Y-%m-%d'))
        metrics_data = metrics_data.sort_values(by=['code', 'date'],
                                                ascending=[True, True])
        metrics_data.groupby(['code', 'date']).fillna(method='ffill',
                                                      limit=2,
                                                      inplace=True)

        # metrics_data = metrics_data.dropna(axis=1,
        #                                    thresh=(0.10 * len(metrics_data)))
        metrics_data = metrics_data.dropna(
            axis=0, thresh=2 + ((len(metrics_data.columns) - 2) * 0.2))
        metrics_list = [x for x in metrics_list if x in metrics_data.columns]
        kd_logger.info(f"{self._sector_code} metrics, company data pulled")

        gd_data = SurfaceMGAPI.GDQrankRaw().fetch(
            columns=['date', 'code', 'name', 'value'], codes=codes)
        kd_logger.info(f"{self._sector_code} GD data pulled")

        gd_data = gd_data.pivot_table(values='value',
                                      index=['code', 'date'],
                                      columns='name',
                                      aggfunc='first').reset_index()
        total_data = metrics_data.merge(gd_data,
                                        how='left',
                                        on=['code', 'date'])
        if 'iso_14000_or_ems' in total_data.columns.tolist():
            total_data['iso_14000_or_ems'] = total_data[
                'iso_14000_or_ems'].map(self._iso_ems_score_map)
        total_data = total_data.sort_values(by=['code', 'date'],
                                            ascending=[True, True])

        transform_list = metrics_list + self._gd_cols
        feature_pool = metrics_list + self._gd_cols

        for factor in transform_list:
            for offset in range(1, 4):
                total_data[f"{factor}_{offset}y_change"] = total_data.groupby(
                    ['code'])[factor].pct_change(offset)
                feature_pool.append(f"{factor}_{offset}y_change")
        kd_logger.info(f"{self._sector_code} transformed data shift")
        total_data = total_data.replace([np.inf, -np.inf, 'None'], np.nan)

        result_dict = {}

        for target in self._target_list:
            kd_logger.info(f"{self._sector_code} downloading {target} model")
            local_dir = f'{self._local_dir}/{self._sector_code}/{target}/'
            remote_dir = f'S2F/run01/{self._sector_code}/{target}/'
            try:
                self._blob_svc.download_file(
                    container_name='model',
                    local_file_name=f"{local_dir}model.joblib",
                    remote_file_name=f"{remote_dir}model.joblib",
                    is_refresh=True)
                self._blob_svc.download_file(
                    container_name='model',
                    local_file_name=f"{local_dir}imputer.joblib",
                    remote_file_name=f"{remote_dir}imputer.joblib",
                    is_refresh=True)
            except Exception as e:
                kd_logger.error(
                    f"{self._sector_code} {target} model download failed")
                continue

            current_data = total_data.copy(deep=True)
            # for compatability purpose, to remove in the next train
            current_data['label'] = np.nan
            current_data.columns = current_data.columns.astype(str)

            imputer = load(f"{local_dir}imputer.joblib")
            imputing_columns = imputer.feature_names_in_
            current_data = current_data.set_index(['code', 'date'])
            current_data = current_data[imputing_columns]
            esg_raw_cols = current_data.columns.tolist()
            current_data[esg_raw_cols] = imputer.transform(current_data)
            current_data = current_data.reset_index()

            # only calculate for the recent two years
            current_data = current_data[(current_data['date'] > '2021-01-01') &
                                        (current_data['date'] < '2023-01-01')]

            current_data = current_data.merge(company_data,
                                              how='left',
                                              on='code')
            current_data = current_data.dropna(subset=['region', 'mkt_cap'],
                                               axis=0)

            current_data['region'] = pd.Categorical(current_data['region'])

            ebm = load(f"{local_dir}model.joblib")
            # get the prediction results and individual contributions
            predict_and_contrib = ebm.predict_and_contrib(current_data,
                                                          output='labels')
            # predictions = np.argmax(predict_and_contrib[0], axis=1)
            """
            to interpret the contribution, we can calculate the probability of each class following the formula:
            scores = contribution.sum(axis=1) + intercept
            from sklearn.utils.extmath import softmax
            softmax(np.c_[np.zeros(scores.shape), scores])
            
            alternatively, if we only want the label itself:
            scores = contribution.sum(axis=1) + intercept
            scores = np.c_[np.zeros(scores.shape), scores]
            np.argmax(scores, axis=1)
            """
            predictions = predict_and_contrib[0]
            intercept_ = ebm.intercept_[0]
            contribution = pd.DataFrame(predict_and_contrib[1],
                                        columns=ebm.feature_names_in_)
            contribution['label'] = predictions.tolist()
            contribution['intercept'] = intercept_
            contribution['code'] = current_data['code'].tolist()
            contribution['date'] = current_data['date'].tolist()
            contribution['sector'] = self._sector_code
            contribution['target'] = target

            result_dict[target] = contribution
            break

            kd_logger.info(
                f"{self._sector_code} {target} model explaining done")

        return result_dict
