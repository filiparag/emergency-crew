import React, { Component } from 'react';
import DeckGL, { HexagonLayer } from 'deck.gl';

const LIGHT_SETTINGS = {
  lightsPosition: [
    20.44051978167588,
    44.80657971403727,
    8000,
    17.44051978167588,
    49.80657971403727,
    8000,
  ],
  ambientRatio: 0.4,
  diffuseRatio: 0.6,
  specularRatio: 0.2,
  lightsStrength: [0.8, 0.0, 0.8, 0.0],
  numberOfLights: 2,
};

const colorRange = [
  [1, 152, 189],
  [73, 227, 206],
  [216, 254, 181],
  [254, 237, 177],
  [254, 173, 84],
  [209, 55, 78],
];

const elevationScale = { min: 1, max: 50 };

const defaultProps = {
  radius: 50,
  upperPercentile: 100,
  lowerPercentile: 25,
  coverage: 0.66,
};

class DeckGLOverlay extends Component {
  static get defaultColorRange() {
    return colorRange;
  }

  static get defaultViewport() {
    return {
      longitude: 20.44051978167588,
      latitude: 44.80657971403727,
      zoom: 13,
      minZoom: 5,
      maxZoom: 15,
      pitch: 53.12686794634536,
      bearing: -9.63433962949328,
      altitude: 1.5,
    };
  }

  constructor(props) {
    super(props);
    this.startAnimationTimer = null;
    this.intervalTimer = null;
    this.state = {
      elevationScale: elevationScale.min,
    };

    this._startAnimate = this._startAnimate.bind(this);
    this._animateHeight = this._animateHeight.bind(this);
  }

  componentDidMount() {
    this._animate();
  }

  componentWillReceiveProps(nextProps) {
    if (nextProps.data.length !== this.props.data.length) {
      this._animate();
    }
  }

  componentWillUnmount() {
    this._stopAnimate();
  }

  _animate() {
    this._stopAnimate();

    this.startAnimationTimer = window.setTimeout(this._startAnimate, 1500);
  }

  _startAnimate() {
    this.intervalTimer = window.setInterval(this._animateHeight, 20);
  }

  _stopAnimate() {
    window.clearTimeout(this.startAnimationTimer);
    window.clearTimeout(this.intervalTimer);
  }

  _animateHeight() {
    if (this.state.elevationScale === elevationScale.max) {
      this._stopAnimate();
    } else {
      this.setState({ elevationScale: this.state.elevationScale + 1 });
    }
  }

  _initialize(gl) {
    gl.enable(gl.DEPTH_TEST);
    gl.depthFunc(gl.LEQUAL);
  }

  _getColorValue = points => points[0][2];

  _getPosition = d => d;

  render() {
    const { viewport, data, radius, coverage, upperPercentile } = this.props;

    if (!data) {
      return null;
    }

    const layers = [
      new HexagonLayer({
        id: 'heatmap',
        getPosition: this._getPosition,
        getColorValue: this._getColorValue,
        elevationScale: this.state.elevationScale,
        onHover: this.props.onHover,
        lightSettings: LIGHT_SETTINGS,
        pickable: Boolean(this.props.onHover),
        elevationRange: [3, 60],
        extruded: true,
        opacity: 1,
        radius,
        upperPercentile,
        colorRange,
        coverage,
        data,
      }),
    ];

    return (
      <DeckGL
        {...viewport}
        layers={layers}
        onWebGLInitialized={this._initialize}
      />
    );
  }
}

DeckGLOverlay.displayName = 'DeckGLOverlay';
DeckGLOverlay.defaultProps = defaultProps;

export default DeckGLOverlay;
