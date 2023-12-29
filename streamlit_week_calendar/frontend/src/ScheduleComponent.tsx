import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import ScheduleSelector from 'react-schedule-selector'
import Button from '@mui/material/Button'
import './custom.css'

interface State {
  schedule: { [key: string]: Date[] }
  selectedTemplate: string
}

class ScheduleComponent extends StreamlitComponentBase<State> {
  public getData = () => {
    const scheduleData: { [key: string]: string[] } = this.props.args["schedule"];
    let convertedSchedule: { [key: string]: Date[] } = {};
  
    for (let template in scheduleData) {
      convertedSchedule[template] = scheduleData[template].map(dateString => new Date(dateString));
    }
    return convertedSchedule;
  }

  public state = { schedule: this.getData(), selectedTemplate: Object.keys(this.getData())[0] }


  public render = (): ReactNode => {
    // 기존 props
    const numDays = this.props.args["num_days"]
    const minTime = this.props.args["min_time"]
    const maxTime = this.props.args["max_time"]
    const hourlyChunks = this.props.args["hourly_chunks"]
    const dateFormat = this.props.args["date_format"]
    const startDate = this.props.args["start_date"]

    const templates = Object.keys(this.getData())

    return (
      <div>
        <div className="ScheduleBtnWrapper">
          {Object.keys(this.state.schedule).map(template => (
            <Button
              variant="contained"
              key={template}
              style={{
                backgroundColor: this.getSelectedColor(template, templates)
              }}
              onClick={() => this.setState({ selectedTemplate: template })}
            >
              {template}
            </Button>
          ))}
        </div>
        <div className="ScheduleComponentWrapper">
          <ScheduleSelector
            selection={this.state.schedule[this.state.selectedTemplate]}
            numDays={numDays}
            minTime={minTime}
            maxTime={maxTime}
            hourlyChunks={hourlyChunks}
            dateFormat={dateFormat}
            startDate={new Date(startDate)}
            columnGap="2px"
            rowGap="2px"
            onChange={this.handleChange}
            renderDateCell={(date, selected, refSetter) => (
              <div
                style={{
                  backgroundColor: selected 
                    ? this.getSelectedColor(this.state.selectedTemplate, templates)
                      : this.isSelectedInOtherTemplate(date) 
                        ? this.getOtherColorForDate(date, Object.keys(this.state.schedule)) // 다른 템플릿에서 선택된 날짜에 대한 색상
                    : "Gainsboro", // 선택되지 않은 경우의 기본 색상
                  width: "100%",
                  height: "100%",
                }}
              />
            )}
            renderTimeLabel={(time) => (
              <div style={{
                  width: "100%",
                  height: "100%",
                  transform: "rotate(-90deg) scaleX(-1)"
                }}>
                  <p>
                    {new Intl.DateTimeFormat('en-US', {hour:'numeric', hour12:false}).format(time)}
                  </p>
              </div>
            )}
            renderDateLabel={(date) => (
              <div style={{
                  width: "50%",
                  height: "50%",
                  transform: "rotate(-90deg) scaleX(-1)"
                }}>
                  <p>
                    {new Intl.DateTimeFormat('en-US', {weekday:'short'}).format(date)}
                  </p>
              </div>
            )}
          />
        </div>
      </div>
    )
  }

  private getSelectedColor = (template:any, templates:any): string => {
    // 선택된 이벤트에 따라 다른 색상 반환 (색상 코드는 예시입니다)
    switch (template) {
      case templates[0]: return '#FF6C6C';
      case templates[1]: return '#FFBD45';
      case templates[2]: return '#3D9DF3';
      case templates[3]: return '#3df355';
      case templates[4]: return '#b33df3';
      // 추가 이벤트 색상 조건
      default: return '#3d43f3'; // 기본 색상 (연한 파랑)
    }
  }

  private isSelectedInOtherTemplate = (date: Date): boolean => {
    for (let template of Object.keys(this.state.schedule)) {
      if (template !== this.state.selectedTemplate) {
        if (this.state.schedule[template].some(d => d.getTime() === date.getTime())) {
          return true;
        }
      }
    }
    return false;
  }

  private getOtherColorForDate = (date: Date, templates: string[]): string => {
    for (let template of templates) {
      if (this.state.schedule[template].some(d => d.getTime() === date.getTime())) {
        return this.getSelectedColor(template, templates); // 이전에 정의된 getSelectedColor 함수 사용
      }
    }
    return "Gainsboro"; // 기본 색상
  }

  private handleChange = (newSchedule: any) => {
    this.setState(prevState => ({
      schedule: {
        ...prevState.schedule,
        [this.state.selectedTemplate]: newSchedule
      }
    }));
    const jsonDates: { [key: string]: any } = {};

    Object.keys(this.state.schedule).forEach((template) => {
      jsonDates[template] = this.state.schedule[template].reduce((acc: any, date: Date) => {
        const options: Intl.DateTimeFormatOptions = {
          weekday: 'short', hour: 'numeric', minute: 'numeric', hour12: false,
        };
        const formattedDate: string = new Intl.DateTimeFormat('en-US', options).format(date);
        const [weekday, time]: string[] = formattedDate.split(' ');

        if (!acc[weekday]) {
          acc[weekday] = [];
        }
        acc[weekday].push(time);
        return acc;
      }, {});
    });
    Streamlit.setComponentValue(jsonDates)
  }
}

export default withStreamlitConnection(ScheduleComponent)
