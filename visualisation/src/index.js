import 'mapbox-gl/dist/mapbox-gl.css';
import 'normalize.css';

import { render } from 'react-dom';
import React from 'react';

import App from './components/App';

render(<App />, document.body.appendChild(document.createElement('div')));
