import React from 'react';

import Viz from './Viz';

const containerStyle = {
  position: 'relative',
};

const textStyle = {
  background: 'papayawhip',
  position: 'absolute',
  padding: '0 20px',
  zIndex: 1,
  left: 55,
  bottom: 40,

  borderRadius: 2,
  boxShadow: '0 14px 28px rgba(0,0,0,0.25), 0 10px 10px rgba(0,0,0,0.22)',
};

const headerStyle = {
  color: 'palevioletred',
};

class App extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      dataset: 'policeData',
      dark: false
    };
  }

  handleOptionChange = (e) => {
    this.setState({
      dataset: e.target.value
    });
  }
  
  render() {
    return (
      <div style={containerStyle}>
        <div style={textStyle}>
          <h1 onClick={() => this.setState({ dark: !this.state.dark })} style={headerStyle}>Bijeligrad</h1>
          <form style={{ display: 'flex', marginBottom: 10 }}>
            {[
              { label: "Policija", dataset: "policeData" },
              { label: "Hitna", dataset: "ambulanceData" },
            ].map((item) =>
              <div key={item.dataset} className="radio" style={{ marginRight: 10 }}>
                <label>
                  <input type="radio" value={item.dataset} checked={this.state.dataset === item.dataset}  onChange={this.handleOptionChange} style={{marginRight: 5}}/>
                  {item.label}
                </label>
              </div>
            )}
          </form>
        </div>

        <Viz dataset={this.state.dataset} dark={this.state.dark}/>
      </div>
    );
  }
}

export default App;