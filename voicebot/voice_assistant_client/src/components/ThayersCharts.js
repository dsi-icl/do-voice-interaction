import React, { Component } from 'react'
import Chart from 'react-google-charts'

const humanCoordinates = [
  ['Arousal', 'Valence'],
  [-.8, .12]
]
const botCoordinates = [
    ['Arousal', 'Valence'],
    [.8, .72]
  ]


const humanGraph = {
  title: 'Human Emotion',
  hAxis: { title: 'Arousal', minValue: -1, maxValue: 1 },
  vAxis: { title: 'Valence', minValue: -1, maxValue: 1 },
  legend: 'none',
}
const botGraph = {
    title: 'Bot Emotion',
    hAxis: { title: 'Arousal', minValue: -1, maxValue: 1 },
    vAxis: { title: 'Valence', minValue: -1, maxValue: 1 },
    legend: 'none',
  }


export class HumanThayers extends Component {
  render() {
    return (
      <div>
        <Chart
          width={'280px'}
          height={'280px'}
          chartType="ScatterChart"
          loader={<div>Loading Chart</div>}
          data={humanCoordinates}
          options={humanGraph}
        />
      </div>
    )
  }
}
export class BotThayers extends Component {
    render() {
      return (
        <div>
          <Chart
            width={'280px'}
            height={'280px'}
            chartType="ScatterChart"
            loader={<div>Loading Chart</div>}
            data={botCoordinates}
            options={botGraph}
          />
        </div>
      )
    }
  }