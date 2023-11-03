#!/usr/bin/env python
# coding: utf-8

# Copyright (c) Saga Inc.
# Distributed under the terms of the GPL License.
from copy import copy
from time import perf_counter
from typing import Any, Dict, List, Optional, Set, Tuple
import pandas as pd
from mitosheet.code_chunks.code_chunk import CodeChunk
from mitosheet.code_chunks.step_performers.column_steps.change_column_dtype_code_chunk import ChangeColumnDtypeCodeChunk

from mitosheet.errors import make_invalid_column_type_change_error, raise_error_if_column_ids_do_not_exist
from mitosheet.is_type_utils import (is_bool_dtype,
                                                   is_datetime_dtype,
                                                   is_float_dtype,
                                                   is_int_dtype, is_number_dtype,
                                                   is_string_dtype,
                                                   is_timedelta_dtype)
from mitosheet.public.v1.sheet_functions.types.utils import get_to_datetime_params
from mitosheet.state import State
from mitosheet.step_performers.step_performer import StepPerformer
from mitosheet.step_performers.utils.utils import get_param
from mitosheet.types import ColumnID


class ChangeColumnDtypeStepPerformer(StepPerformer):
    """"
    A step that allows changing the dtype of a column to a different
    dtype.

    Currently, supports: 'bool', 'int', 'float', 'str', 'datetime', 'timedelta'
    """

    @classmethod
    def step_version(cls) -> int:
        return 4

    @classmethod
    def step_type(cls) -> str:
        return 'change_column_dtype'

    @classmethod
    def saturate(cls, prev_state: State, params: Dict[str, Any]) -> Dict[str, Any]:
        sheet_index: int = params['sheet_index']
        column_ids: List[ColumnID] = params['column_ids']

        # Save all the old dtypes
        old_dtypes = dict()
        for column_id in column_ids:
            column_header = prev_state.column_ids.get_column_header_by_id(sheet_index, column_id)
            old_dtypes[column_id] = str(prev_state.dfs[sheet_index][column_header].dtype)

        params['old_dtypes'] = old_dtypes
        
        return params

    @classmethod
    def execute(cls, prev_state: State, params: Dict[str, Any]) -> Tuple[State, Optional[Dict[str, Any]]]:
        sheet_index: int = get_param(params, 'sheet_index')
        column_ids: List[ColumnID] = get_param(params, 'column_ids')
        old_dtypes: Dict[ColumnID, str] = get_param(params, 'old_dtypes')
        new_dtype: str = get_param(params, 'new_dtype')
        public_interface_version: str = get_param(params, 'public_interface_version')

        raise_error_if_column_ids_do_not_exist(
            'change column dtype',
            prev_state,
            sheet_index,
            column_ids
        )

        if public_interface_version == 1:
            from mitosheet.public.v1 import to_int_series, to_boolean_series, to_float_series, to_timedelta_series, get_datetime_format
        elif public_interface_version == 2:
            from mitosheet.public.v2 import to_int_series, to_boolean_series, to_float_series, to_timedelta_series, get_datetime_format
        elif public_interface_version == 3:
            from mitosheet.public.v3 import to_int_series, to_boolean_series, to_float_series, to_timedelta_series, get_datetime_format
        else:
            raise Exception(f'Please add support for public_interface_version={public_interface_version}')

        post_state = prev_state.copy(deep_sheet_indexes=[sheet_index])
        pandas_processing_time: float = 0

        changed_column_ids: List[ColumnID] = []
        to_datetime_params_map: Dict[ColumnID, Dict[str, Any]] = {}
        for column_id in column_ids:

            old_dtype = old_dtypes[column_id]
            column_header = prev_state.column_ids.get_column_header_by_id(sheet_index, column_id)

            column: pd.Series = prev_state.dfs[sheet_index][column_header]
            new_column = column
            changed_this_column = True
            
            # How we handle the type conversion depends on what type it is
            try:
                pandas_start_time = perf_counter()
                if is_bool_dtype(old_dtype):
                    if is_bool_dtype(new_dtype):
                        changed_this_column = False
                    elif is_int_dtype(new_dtype):
                        new_column = new_column.astype('int')
                    elif is_float_dtype(new_dtype):
                        new_column = column.astype('float')
                    elif is_string_dtype(new_dtype):
                        new_column = column.astype('str')
                    elif is_datetime_dtype(new_dtype):
                        raise make_invalid_column_type_change_error(
                            column_header,
                            old_dtype,
                            new_dtype
                        )
                    elif is_timedelta_dtype(new_dtype):
                        raise make_invalid_column_type_change_error(
                            column_header,
                            old_dtype,
                            new_dtype
                        )
                if is_int_dtype(old_dtype):
                    if is_bool_dtype(new_dtype):
                        new_column = column.fillna(False).astype('bool')
                    elif is_int_dtype(new_dtype):
                        changed_this_column = False
                    elif is_float_dtype(new_dtype):
                        new_column = column.astype('float')
                    elif is_string_dtype(new_dtype):
                        new_column = column.astype('str')
                    elif is_datetime_dtype(new_dtype):
                        new_column = pd.to_datetime(
                            column, 
                            unit='s',
                            errors='coerce'
                        )
                    elif is_timedelta_dtype(new_dtype):
                        new_column = to_timedelta_series(column)
                elif is_float_dtype(old_dtype):
                    if is_bool_dtype(new_dtype):
                        new_column = column.fillna(False).astype('bool')
                    elif is_int_dtype(new_dtype):
                        new_column = column.fillna(0).astype('int')
                    elif is_float_dtype(new_dtype):
                        changed_this_column = False
                    elif is_string_dtype(new_dtype):
                        new_column = column.astype('str')
                    elif is_datetime_dtype(new_dtype):
                        new_column = pd.to_datetime(
                            column, 
                            unit='s',
                            errors='coerce'
                        )
                    elif is_timedelta_dtype(new_dtype):
                        new_column = to_timedelta_series(column)
                elif is_string_dtype(old_dtype):
                    if is_bool_dtype(new_dtype):
                        new_column = to_boolean_series(new_column)
                    elif is_int_dtype(new_dtype):
                        new_column = to_int_series(column)
                    elif is_float_dtype(new_dtype):
                        new_column = to_float_series(column)
                    elif is_string_dtype(new_dtype):
                        changed_this_column = False
                    elif is_datetime_dtype(new_dtype):
                        # We need to detect the correct params to pass to the to_datetime function, and save them for use in the code chunk
                        to_datetime_params = get_to_datetime_params(column)
                        to_datetime_params_map[column_id] = to_datetime_params
                        
                        new_column = pd.to_datetime(
                            column,
                            errors='coerce',
                            **to_datetime_params
                        )
                    elif is_timedelta_dtype(new_dtype):
                        new_column = to_timedelta_series(column)
                elif is_datetime_dtype(old_dtype):
                    if is_bool_dtype(new_dtype):
                        new_column = ~column.isnull()
                    elif is_int_dtype(new_dtype):
                        new_column = column.astype('int') / 10**9
                    elif is_float_dtype(new_dtype):
                        # For some reason, we have to do all the conversions at once
                        new_column = column.astype('int').astype('float') / 10**9
                    elif is_string_dtype(new_dtype):
                        # NOTE: this is the same conversion that we send to the frontend
                        new_column = column.dt.strftime('%Y-%m-%d %X')
                    elif is_datetime_dtype(new_dtype):
                        changed_this_column = False
                    elif is_timedelta_dtype(new_dtype):
                        raise make_invalid_column_type_change_error(
                            column_header,
                            old_dtype,
                            new_dtype
                        )
                elif is_timedelta_dtype(old_dtype):
                    if is_bool_dtype(new_dtype):
                        new_column = ~column.isnull()
                    elif is_int_dtype(new_dtype):
                        new_column = column.dt.total_seconds().astype('int')
                    elif is_float_dtype(new_dtype):
                        new_column = column.dt.total_seconds()
                    elif is_string_dtype(new_dtype):
                        new_column = column.astype('str')
                    elif is_datetime_dtype(new_dtype):
                        raise make_invalid_column_type_change_error(
                            column_header,
                            old_dtype,
                            new_dtype
                        )
                    elif is_timedelta_dtype(new_dtype):
                        changed_this_column = False

                # We update the column, as well as the type of the column
                post_state.dfs[sheet_index][column_header] = new_column
                pandas_processing_time += (perf_counter() - pandas_start_time)

                # Remember which columns we changed
                if changed_this_column:
                    changed_column_ids.append(column_id)

                # If we're changing away from a number column, then we remove the formatting on the column if it exists
                if not is_number_dtype(new_dtype) and column_id in post_state.df_formats[sheet_index]['columns']:
                    del post_state.df_formats[sheet_index]['columns'][column_id]
                    
            except:
                raise make_invalid_column_type_change_error(
                    column_header,
                    old_dtype,
                    new_dtype
                )

        execution_data = {
            'pandas_processing_time': pandas_processing_time,
            'changed_column_ids': changed_column_ids
        }

        if len(to_datetime_params_map) > 0:
            execution_data['to_datetime_params_map'] = to_datetime_params_map

        return post_state, execution_data
        

    @classmethod
    def transpile(
        cls,
        prev_state: State,
        post_state: State,
        params: Dict[str, Any],
        execution_data: Optional[Dict[str, Any]],
    ) -> List[CodeChunk]:
        return [
            ChangeColumnDtypeCodeChunk(
                prev_state, 
                post_state, 
                get_param(params, 'sheet_index'),
                get_param(params, 'column_ids'),
                get_param(params, 'old_dtypes'),
                get_param(params, 'new_dtype'),
                get_param(execution_data if execution_data is not None else {}, 'changed_column_ids'),
                execution_data.get('to_datetime_params_map', None) if execution_data is not None else None,
                get_param(params, 'public_interface_version')
            )
        ]

    @classmethod
    def get_modified_dataframe_indexes(cls, params: Dict[str, Any]) -> Set[int]:
        return {get_param(params, 'sheet_index')}