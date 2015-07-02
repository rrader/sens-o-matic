/** @jsx React.DOM */


var SensorBox = React.createClass({
    requestComments: function () {
        this.setState({data: []});
        var socket = new SocketService();
        var sensorName = this.props.sensorName;

        socket.subscribe(sensorName, 10, function (message) {
            if (message.$type === 'dataReceived') {
                this.state.data.push(message);
                this.setState({data: this.state.data});
                console.log('Value "' + message + '" pushed for sensor "' + sensorName + '"');
            }
            if (message.$type === 'subscribedOK') {
                this.metadata = message.sensorStaticData;
                this.setState({data: message.history});
                console.log('Subscribed for updates on sensor "' + message.sensorName + '"');
            }
        }.bind(this));
    },
    getInitialState: function () {
        return {data: []};
    },
    componentWillMount: function () {
        this.requestComments();
    },
    render: function () {
        return (
            <div className="panel panel-default sensorBox">
                <div className="panel-heading">Sensor {this.props.sensorName} History</div>
                <img src={"img/" + this.props.sensorName + '.png'}
                     className="img-rounded pull-right" alt="logo"
                     width="100"
                     />
                <div className="panel-body">
                    <SensorHistoryList data={this.state.data} metadata={this.metadata} />
                </div>
            </div>
            );
    }
});

var SensorHistoryList = React.createClass({
    render: function () {
        var self = this;
        var sensorHistoryList = this.props.data.map(function (value, index) {
            var date = new Date(value.timestamp);
            var readable = self.props.metadata['values'][value.value];
            if (readable === undefined) {
                readable = 'unknown value';
            }

            var style = {};
            if (value['$type'] == 'dataReceived') {
              style['color'] = 'gray';
            }
            return <li> <span style={style}> { date.toString() }: { readable } </span> </li>;
        });
        return (<div className="sensorHistoryList">
                  <ul className="value">
                    {sensorHistoryList}
                  </ul>
                </div>
                );
    }
});
