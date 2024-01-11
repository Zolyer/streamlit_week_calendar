import os
import streamlit.components.v1 as components

_RELEASE = False

if not _RELEASE:
    _component_func = components.declare_component(
        "streamlit_week_calendar",
        url="http://localhost:3001",
    )
else:
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_week_calendar", path=build_dir)


def week_calendar(num_days=7, min_time=0, max_time=24, hourly_chunks=1, date_format='ddd', start_date='2023-12-18', schedule={}, key=None):
    """Create a new instance

    Parameters
    ----------
    num_days: int
        Number of days to display the schedule
    min_time: int
        Number of hours to display start of the schedule
    max_time: int
        Number of hours to display end of the schedule
    hourly_chunks: int
        Number of each hour blocks
    date_format: str
        
    start_date: str
        
    events: list[str]

    schedule: dict[str:dict[str:list[str]]]
        
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    dict[str:dict]

    """
    day_format = {
        'Mon':'2023-12-18',
        'Tue':'2023-12-19',
        'Wed':'2023-12-20',
        'Thu':'2023-12-21',
        'Fri':'2023-12-22',
        'Sat':'2023-12-23',
        'Sun':'2023-12-24'
    }
    time_format = {
        '24:00':'T00:00:00',
        '01:00':'T01:00:00',
        '02:00':'T02:00:00',
        '03:00':'T03:00:00',
        '04:00':'T04:00:00',
        '05:00':'T05:00:00',
        '06:00':'T06:00:00',
        '07:00':'T07:00:00',
        '08:00':'T08:00:00',
        '09:00':'T09:00:00',
        '10:00':'T10:00:00',
        '11:00':'T11:00:00',
        '12:00':'T12:00:00',
        '13:00':'T13:00:00',
        '14:00':'T14:00:00',
        '15:00':'T15:00:00',
        '16:00':'T16:00:00',
        '17:00':'T17:00:00',
        '18:00':'T18:00:00',
        '19:00':'T19:00:00',
        '20:00':'T20:00:00',
        '21:00':'T21:00:00',
        '22:00':'T22:00:00',
        '23:00':'T23:00:00',
    }

    day_convert = {}
    
    for template, schedule in schedule.items():
        li = []
        for week, times in schedule.items():
            for time in times:
                li.append(f"{day_format[week]}{time_format[time]}")
        day_convert[template] = sorted(li)

    component_value = _component_func(
        num_days=num_days, 
        min_time=min_time, 
        max_time=max_time, 
        hourly_chunks=hourly_chunks,
        date_format=date_format,
        start_date=start_date, schedule=day_convert,
        key=key, default=day_convert
        )

    return component_value

if not _RELEASE:
    import streamlit as st
    import pandas as pd
    import json

    data = {
        'Template1': {'Mon': ['08:00', '24:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00'], 'Tue': ['24:00', '01:00', '03:00', '05:00', '09:00', '11:00', '12:00', '13:00', '15:00', '16:00', '17:00', '21:00', '22:00', '23:00'], 'Wed': ['24:00', '01:00', '03:00', '05:00', '07:00', '08:00', '09:00', '11:00', '12:00', '13:00', '15:00', '16:00', '17:00', '19:00', '21:00', '22:00', '23:00'], 'Thu': ['24:00', '01:00', '05:00', '09:00', '11:00', '12:00', '13:00', '15:00', '16:00', '17:00', '19:00', '21:00', '22:00', '23:00'], 'Fri': ['24:00', '01:00', '03:00', '05:00', '07:00', '08:00', '09:00', '11:00', '12:00', '13:00', '15:00', '16:00', '17:00', '19:00', '21:00', '22:00', '23:00'], 'Sat': ['24:00', '01:00', '03:00', '05:00', '09:00', '13:00', '17:00', '21:00', '22:00', '23:00'], 'Sun': ['24:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']}, 
        'Template2': {'Tue': ['02:00', '04:00', '10:00', '18:00', '20:00', '19:00'], 'Wed': ['02:00', '04:00', '10:00', '18:00', '20:00'], 'Fri': ['02:00', '04:00', '10:00', '18:00', '20:00'], 'Sat': ['02:00', '04:00', '10:00', '11:00', '12:00', '18:00', '19:00', '20:00'], 'Thu': ['02:00', '03:00', '04:00', '10:00', '18:00', '20:00']}, 
        'Template3': {'Tue': ['06:00', '07:00', '08:00', '14:00'], 'Wed': ['06:00', '14:00'], 'Thu': ['06:00', '07:00', '08:00', '14:00'], 'Fri': ['06:00', '14:00'], 'Sat': ['06:00', '07:00', '08:00', '14:00', '15:00', '16:00']}
    }
    
    st.set_page_config(layout='wide')

    sel = st.multiselect(
        'Select Templates',
        list(data.keys())
    )

    input_data = {}
    if sel:
        for i in sel:
            input_data[i] = data[i]


    schedule = week_calendar(
        schedule=input_data
    )
    
    if schedule:
        # 데이터를 포함하는 새로운 딕셔너리 생성
        new_data = {}

        for template, values in schedule.items():
            new_data[template] = [values]

        # 새로운 데이터를 pandas DataFrame으로 변환
        df = pd.DataFrame(new_data)

        st.dataframe(df, use_container_width=True)