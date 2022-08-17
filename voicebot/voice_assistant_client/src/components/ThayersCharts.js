/* eslint-disable */
import React from 'react'
import Chart from 'react-google-charts'
import {useSelector} from "react-redux";
import {selectResponses} from "../reducers/media";

const humanGraph = {
  title: 'Human Emotion',
  hAxis: { title: 'Valence', minValue: -1, maxValue: 1 },
  vAxis: { title: 'Arousal', minValue: -1, maxValue: 1 },
  legend: 'none',
}
const botGraph = {
    title: 'Bot Emotion',
    hAxis: { title: 'Valence', minValue: -1, maxValue: 1 },
    vAxis: { title: 'Arousal', minValue: -1, maxValue: 1 },
    legend: 'none',
  }

const toCoordinates = (thayers)=>{
    if (thayers==='n/a'){
        return [0,0]
    }
    return [parseFloat(thayers.split(",")[0]), parseFloat(thayers.split(",")[1])]
}

export const HumanThayers = () => {
    const responses = useSelector(selectResponses)
    return (
      <div>
        <Chart
          width={'280px'}
          height={'280px'}
          chartType="ScatterChart"
          loader={<div>Loading Chart</div>}
          data={[
            ['Valence', 'Arousal'],
            responses[0]? toCoordinates(responses[0].human_thayers):[0,0]
          ]}
          options={humanGraph}
        />
      </div>
    )
}
export const BotThayers = () => {
    const responses = useSelector(selectResponses)

      return (
        <div>
          <Chart
            width={'280px'}
            height={'280px'}
            chartType="ScatterChart"
            loader={<div>Loading Chart</div>}
            data={[
                ['Valence', 'Arousal'],
                responses[0]? toCoordinates(responses[0].bot_thayers):[0,0]
              ]}
            options={botGraph}
          />
        </div>
      )
  }