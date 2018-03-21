import React, {Component} from 'react';
import MapGL from 'react-map-gl';
import Papa from 'papaparse';

import DeckGLOverlay from './DeckGLOverlay';

const MAPBOX_TOKEN = process.env.REACT_APP_MAPBOX_TOKEN;

const POLICE_DATA_URL = 'https://raw.githubusercontent.com/filiparag/emergency-crew/master/policija.csv';
const AMBULANCE_DATA_URL = 'https://raw.githubusercontent.com/filiparag/emergency-crew/master/hitna.csv';

class Viz extends Component {
  state = {
    viewport: {
      ...DeckGLOverlay.defaultViewport,
      width: 500,
      height: 500
    },
    policeData: null,
    ambulanceData: null,
  };

  componentDidMount() {
    [
      { url: POLICE_DATA_URL, fieldName: 'policeData' },
      { url: AMBULANCE_DATA_URL, fieldName: 'ambulanceData' },
    ].map((dataset) =>
      Papa.parse(dataset.url, {
        download: true,
        complete: (res) => {
          const fieldData = res.data
            .map(item => 
              [Number(item[1]), Number(item[0]), Number(item[2])]
            )
          this.setState({ [dataset.fieldName]: fieldData  })
        }
      })
    );

    window.addEventListener('resize', this._resize);
    this._resize();
  }

  _resize = () => {
    this._onViewportChange({
      width: window.innerWidth,
      height: window.innerHeight
    });
  }

  _onViewportChange = (viewport) => {
    this.setState({
      viewport: {...this.state.viewport, ...viewport}
    });
  }

  render() {
    const { viewport } = this.state;
    const { dataset } = this.props;

    const data = this.state[dataset];

    return (
      <MapGL
        {...viewport}
        mapStyle={this.props.dark ? "mapbox://styles/mapbox/dark-v9" : "mapbox://styles/mapbox/light-v9" }
        onViewportChange={this._onViewportChange.bind(this)}
        mapboxApiAccessToken={MAPBOX_TOKEN}>
        <DeckGLOverlay
          viewport={viewport}
          data={data || []}
        />
      </MapGL>
    );
  }
}

export default Viz;
