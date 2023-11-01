# -*- coding: utf-8 -*-
import six, os, itertools
import pandas as pd
from sqlalchemy import and_
from sqlalchemy import outerjoin, join
from seleya.utilities.kd_logger import kd_logger
from seleya.utilities.singleton import Singleton
from seleya.data.DataAPI.sqlatom.fetch_engine import FetchEngine


@six.add_metaclass(Singleton)
class FetchKDEngine(FetchEngine):

    def __init__(self):
        super(FetchKDEngine, self).__init__('sly', os.environ['DB_URL'])

    def client(self):
        return self._engine.sql_engine()

    def table_model(self, name):
        return self._base.classes[name]

    def show_indexs(self, name):
        indexs = [ins['column_names'] for ins in self._insp.get_indexes(name)]
        return list(set(itertools.chain.from_iterable(indexs)))

    def customize(self, table, clause_list, columns=None):
        new_list = and_(table.__dict__['flag'] == 1,
                        table.__dict__['flag'].isnot(None))
        indices = self.show_indexs(table.__name__)
        for clause in clause_list:
            if clause.left.name in indices:
                new_list.append(clause)
            else:
                kd_logger.warning("{0} not indices".format(clause.left.name))
        if len(new_list) <= 2:
            kd_logger.error("unconditional query is not allowed")
            return pd.DataFrame()
        return super(FetchKDEngine, self).customize(table=table,
                                                    clause_list=new_list,
                                                    columns=columns)
