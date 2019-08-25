const namespace = '/test'
const socket = io(namespace)

const dom = {}

const errors = []

socket.on('connect', () => {
    socket.emit('my_event', { data: "I'm connected!" })
})

class AppContainer extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            location: 'initial',
            errors: errors
        }
        socket.on('err', message => {
            const newError = JSON.parse(message)
            errors.unshift(newError)
            this.setState({
                errors: errors
            })
        })
    }

    predict() {
        this.setState({
            location: 'predict'
        })
    }

    console() {
        this.setState({
            location: 'console'
        })
    }

    render() {
        if (this.state.location == 'initial') {
            dom.$video.show()
            dom.$mount.css('background', 'rgba(0, 0, 100, 0.5)')
            $('body').css('background-color', '#000000')
            return (
                <div
                    className="container clickable"
                    id="intro-container"
                    onClick={() => {
                        this.setState({ location: 'console' })
                    }}
                >
                    <h1 className="center pb-3">4DByD debugging</h1>
                    <p className="center text-larger pb-3">
                        For developers by developers, to make debugging fast and painless.
                    </p>
                </div>
            )
        } else if (this.state.location == 'console') {
            dom.$video.hide()
            dom.$mount.css('background', '')
            $('body').css('background-color', '#e91e1e54')
            return (
                <TableContainer
                    predict={this.predict.bind(this)}
                    console={this.console.bind(this)}
                    errors={this.state.errors}
                />
            )
        } else {
            dom.$video.hide()
            dom.$mount.css('background', '')
            return (
                <div className="container table-container">
                    <p>The next error message will be:</p>
                    <p className="code-font">
                        error,: couldn\\t connect to server aaa.a.a.a:aaaaa, connection attempt failed: socketexception
                    </p>
                    <button className='btn btn-light'
                        onClick={() => {
                            this.console(this)
                        }}
                    >Back to Console</button>
                </div>
            )
        }
    }
}

class TableContainer extends React.Component {
    render() {
        if (errors.length > 0) {
            return (
                <div className="container table-container">
                    <h2 className="center gray pb-3">4DByD debugger console</h2>
                    <div className="card border shadow rounded" id="table-card">
                        <Table errors={this.props.errors} />
                    </div>
                    <p className="center gray pt-3">Click on an error to open the relevant files</p>
                    <button className='btn btn-light'
                        onClick={() => {
                            this.props.predict()
                        }}
                    >
                        Predict next error
                    </button>
                </div>
            )
        } else {
            return (
                <div>
                    <h4 className="center gray">You have no errors, for now ;)</h4>
                </div>
            )
        }
    }
}

class Table extends React.Component {
    render() {
        return (
            <table className="table table-striped table-hover table-light mb-0">
                <thead>
                    <Row header={true}></Row>
                </thead>
                <tbody className="code-font">
                    {this.props.errors.map(error => (
                        <Row header={false} error={error}></Row>
                    ))}
                </tbody>
            </table>
        )
    }
}

class Row extends React.Component {
    openStack() {
        socket.emit('openfile', this.props.error)
    }

    render() {
        const header = this.props.header
        if (header) {
            return (
                <tr>
                    <th scope="col">Time</th>
                    <th scope="col">Error Type</th>
                    <th scope="col">Error Message</th>
                </tr>
            )
        } else {
            const error = this.props.error
            return (
                <tr
                    onClick={() => {
                        this.openStack()
                    }}
                >
                    <Cell oneLine={true} data={error.Time}></Cell>
                    <Cell oneLine={true} data={error.ErrorType}></Cell>
                    <Cell clamped={true} data={error.ErrorMessage}></Cell>
                </tr>
            )
        }
    }
}

class Cell extends React.Component {
    render() {
        const oneLine = this.props.oneLine
        let classes = 'clickable'
        if (oneLine) classes += ' one-line'
        if (this.props.clamped) classes += ' clamped'
        return <td className={classes}>{this.props.data}</td>
    }
}

$(document).ready(function() {
    dom.$video = $('#background-video')
    dom.$mount = $('#mount')

    let domContainer = document.querySelector('#mount')
    ReactDOM.render(<AppContainer />, domContainer)
})
