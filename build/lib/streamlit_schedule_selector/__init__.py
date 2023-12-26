import os
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "streamlit_schedule_selector",
        url="http://localhost:3001",
    )
else:
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_schedule_selector", path=build_dir)


def schedule_component(num_days=7, min_time=0, max_time=24, hourly_chunks=1, date_format='ddd', start_date='2023-12-18', schedule=[], key=None):
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
    component_value = _component_func(
        num_days=num_days, 
        min_time=min_time, 
        max_time=max_time, 
        hourly_chunks=hourly_chunks,
        date_format=date_format,
        start_date=start_date, schedule=schedule,
        key=key, default=0
        )

    return component_value

if not _RELEASE:
    import streamlit as st
    import pandas as pd
    import json

    data = {
        "Template1":[
                "2023-12-18T00:00:00Z",
                "2023-12-18T01:00:00Z",
                "2023-12-18T02:00:00Z",
            ],
        "Template2":[
                "2023-12-18T03:00:00Z",
                "2023-12-18T04:00:00Z",
                "2023-12-18T05:00:00Z",
            ],
        "Template3":[
                "2023-12-18T06:00:00Z",
                "2023-12-18T07:00:00Z",
                "2023-12-18T08:00:00Z",
            ],
    }
    
    st.set_page_config(layout='wide')

    schedule = schedule_component(
        schedule=data
    )

    if schedule:
        # 데이터를 포함하는 새로운 딕셔너리 생성
        new_data = {}

        for template, values in schedule.items():
            new_data[template] = [values]

        # 새로운 데이터를 pandas DataFrame으로 변환
        df = pd.DataFrame(new_data)

        st.dataframe(df, use_container_width=True)