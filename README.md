# streamlit-week-calendar

Streamlit component that allows you to use react-schedule-selector

## Installation instructions

```sh
pip install streamlit-week-calendar
```

## Usage instructions

```python
import streamlit as st
import pandas as pd
import json
from streamlit_week_calendar import schedule_component

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
    new_data = {}
    for template, values in schedule.items():
        new_data[template] = [values]
    df = pd.DataFrame(new_data)
    st.dataframe(df, use_container_width=True)
```