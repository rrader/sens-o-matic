/** @jsx React.DOM */


var SensorBox = React.createClass({displayName: 'SensorBox',
    requestComments: function () {
        this.setState({data: []});
        var socket = new SocketService();
        var sensorName = this.props.sensorName;

        socket.subscribe(sensorName, function (message) {
            if (message.$type === 'dataReceived') {
                if (!message.data) return;
                this.state.data.push(message.data);
            }
            if (message.$type === 'subscribedOK') {
                console.log('Subscribed for updates on sensor "' + message.sensorName + '"');
            }
//            if (message.$type === 'dataCompleted') {
////                socket.requestComplete(message.$id);
//                this.setState({data: this.state.data});
//            }
            if (message.$type === 'error') {
//                socket.requestComplete(message.$id);
            }
        }.bind(this));
    },
    handleCommentSubmit: function (comment) {
        var comments = this.state.data;
        comments.push(comment);
        this.setState({data: comments});
        console.log('TODO - submit comment');
    },
    getInitialState: function () {
        return {data: []};
    },
    componentWillMount: function () {
        this.requestComments();
    },
    render: function () {
        return (
            React.DOM.div( {className:"commentBox"},
                React.DOM.h1(null, "Comments")
//                React.DOM.input( {type:"submit", value:"Refresh", onClick:this.requestComments} ),
//                CommentList( {data:this.state.data} ),
//                CommentForm( {onCommentSubmit:this.handleCommentSubmit} )
                )
            );
    }
});


React.renderComponent(
    SensorBox({sensorName: 'door'}),
    document.body
);
