import pypyodbc
import threading
import queue
import pandas as pd
from bokeh.models import ColumnDataSource
from DataVisualizationWebApp import utility as uHelper
import timeit
import time
import asyncio
from functools import lru_cache

rig_id_str = "rig_id"
job_id_str = 'job_id'
crew_shift_str = 'crew_shift'
depth_ft_str = "depth_ft"

def remove_empty_depth(in_dict):
        out_dict = {}
        out_dict.update([(key, in_dict[key]) for key in in_dict.keys() if ((str(in_dict[depth_ft_str]) != ''))])
    
        return out_dict

#@lru_cache(maxsize=None)
def setup_db_connection():
    uHelper.connection = pypyodbc.connect('Driver={SQL Server};'
                            'Server=SQLWDBP04;'
                            'Database=NOVOS;'
                            'uid=PDPerformance;'
                            'pwd=pTepJ1281S9kpC')
    return uHelper.connection

#@lru_cache(maxsize=None)
#async def retrieve_data(connection, rig_id = -1):
def retrieve_data(rig_id = -1):
    try:
        uHelper.connection = pypyodbc.connect('Driver={SQL Server};'
                            'Server=SQLWDBP04;'
                            'Database=NOVOS;'
                            'uid=PDPerformance;'
                            'pwd=pTepJ1281S9kpC')
    except:
        uHelper.connection.close()
        print("can not connect with database")
    
    connection = uHelper.connection
    cursor_1 = connection.cursor()
    cursor_2 = connection.cursor()
    cursor_3 = connection.cursor()
    cursor_4 = connection.cursor()
        
    rigs_list = []
    select_all_connection = None
    if rig_id == -1:
        select_all_rigs = ("SELECT rig_id FROM all_connection")
        cursor_1.execute(select_all_rigs) 
        rigs = cursor_1.fetchall()
        rigs_set = set()
        for row in rigs:
            rigs_set.add(row[0])
        rigs_list = list(sorted(rigs_set))
        select_all_connection = ("SELECT hole_depth, visualization_depth, connection_type, \
                                         weight_to_weight_time, all_pre_slip_time, slip_to_slip, all_post_slip_time, \
                                         rig_id, job_id, survey_time, \
                                         backream_time, frictiontest_time, pre_slip_time, \
                                         post_slip_time, crew_shift, well_section \
                                  FROM all_connection \
                                  WHERE rig_id = %d;" % (rigs_list[0])) 
    else:
        select_all_connection = ("SELECT hole_depth, visualization_depth, connection_type, \
                                         weight_to_weight_time, all_pre_slip_time, slip_to_slip, all_post_slip_time, \
                                         rig_id, job_id, survey_time, \
                                         backream_time, frictiontest_time, pre_slip_time, \
                                         post_slip_time, crew_shift, well_section \
                                  FROM all_connection \
                                  WHERE rig_id = %d;" % (rig_id)) 
     
    cursor_2.execute(select_all_connection) 
    desc = cursor_2.description
    column_names = [col[0] for col in desc]
    all_connection_dict = [dict(zip(column_names, row)) 
            for row in cursor_2.fetchall()]
    all_connection_dict = {k: [dic[k] for dic in all_connection_dict] for k in all_connection_dict[0]}    
    all_connection_table = pd.DataFrame.from_dict(all_connection_dict)
    
    novos_connection_dict = None
    novos_connection_table = None
    #novos_source = None
    select_novos_connection = None
    if rig_id == -1:
        select_novos_connection = ("SELECT job_id, rig_id, status, type, \
                                           depth_ft, edr_depth_ft, \
                                           connection_phase, connection_type \
                                    FROM novos_connection \
                                    WHERE edr_depth_ft is not NULL and rig_id = %d;" % (rigs_list[0])) 
    else:
        select_novos_connection = ("SELECT job_id, rig_id, status, type, \
                                           depth_ft, edr_depth_ft, \
                                           connection_phase, connection_type \
                                    FROM novos_connection \
                                    WHERE edr_depth_ft is not NULL and rig_id = %d;" % (rig_id)) 

    cursor_3.execute(select_novos_connection)
    if cursor_3.rowcount != 0:
        desc = cursor_3.description
        column_names = [col[0] for col in desc]
        novos_connection_dict = [dict(zip(column_names, row)) 
                for row in cursor_3.fetchall()]
       
        novos_connection_table = pd.DataFrame.from_dict(novos_connection_dict)
        #novos_connection_dict = {}
        #novos_connection_dict["job_id"] = novos_connection_table["job_id"]
        #novos_connection_dict["rig_id"] = novos_connection_table["rig_id"]
        #novos_connection_dict["status"] = novos_connection_table["status"]
        #novos_connection_dict["type"] = novos_connection_table["type"]
        #novos_connection_dict["depth_ft"] = novos_connection_table["depth_ft"]
        #novos_connection_dict["edr_depth_ft"] = novos_connection_table["edr_depth_ft"]
        #novos_connection_dict["connection_phase"] = novos_connection_table["connection_phase"]
        #novos_connection_dict["connection_type"]  = novos_connection_table["connection_type"]
        
    novos_config_dict = None
    novos_config_table =  pd.DataFrame()
    select_novos_config = None
    if rig_id == -1:
        select_novos_config = ("SELECT job_id, rig_id, variable, value, units, hole_depth_ft, change \
                                FROM novos_config \
                                WHERE hole_depth_ft is not NULL and rig_id = %d;" % (rigs_list[0])) 
    else:
        select_novos_config = ("SELECT job_id, rig_id, date_time, variable, value, units, hole_depth_ft, change \
                                FROM novos_config \
                                WHERE hole_depth_ft is not NULL and rig_id = %d;" % (rig_id)) 

    cursor_4.execute(select_novos_config)
    if cursor_4.rowcount != 0:
        desc = cursor_4.description
        column_names = [col[0] for col in desc]
        novos_config_dict = [dict(zip(column_names, row)) 
                for row in cursor_4.fetchall()]
        
        novos_config_table = pd.DataFrame.from_dict(novos_config_dict)
    
    cursor_1.close()
    cursor_2.close()
    cursor_3.close()
    cursor_4.close()    
    connection.close()
    jobs_list = all_connection_table[uHelper.job_id_str].unique().tolist()
    crewshift_list = all_connection_table[uHelper.crew_shift_str].unique().tolist()

    uHelper.all_connection_dict, \
    uHelper.all_connection_table, \
    uHelper.novos_connection_dict, \
    uHelper.novos_connection_table, \
    uHelper.rigs_list, \
    uHelper.jobs_list, \
    uHelper.crewshift_list, \
    uHelper.novos_config_table, \
    uHelper.novos_config_dict = all_connection_dict, \
                                all_connection_table, \
                                novos_connection_dict, \
                                novos_connection_table, \
                                rigs_list, \
                                jobs_list, \
                                crewshift_list, \
                                novos_config_table, \
                                novos_config_dict
    

