/** @jsx React.DOM */


var SensorBox = React.createClass({
    requestComments: function () {
        this.setState({data: []});
        var socket = new SocketService();
        var sensorName = this.props.sensorName;

        socket.subscribe(sensorName, function (message) {
            if (message.$type === 'dataReceived') {
                this.state.data.push(message);
                this.setState({data: this.state.data});
                console.log('Value "' + message + '" pushed for sensor "' + sensorName + '"');
            }
            if (message.$type === 'subscribedOK') {
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
                <div className="panel-body">
                    <SensorHistoryList data={this.state.data} />
                </div>
            </div>
            );
    }
});

var SensorHistoryList = React.createClass({
    render: function () {
        var sensorHistoryList = this.props.data.map(function (value, index) {
            var date = new Date(value.timestamp);
            var readable;
            if (value.value == '0') {
                readable = "Door is opened"
            } else
            if (value.value == '1') {
                readable = "Door is closed"
            } else {
                readable = "Unknown state... :("
            }

            return (
                        <ul className="value">
                            <li> { date.toString() }: { readable } </li>
                        </ul>
                    );
        });
        return <div className="sensorHistoryList">{sensorHistoryList}</div>;
    }
});
