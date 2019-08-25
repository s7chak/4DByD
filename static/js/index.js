const namespace = '/test'
const socket = io(namespace)

const errors = []

socket.on('connect', () => {
    socket.emit('my_event', { data: "I'm connected!" })
})

class TableContainer extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
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

    render() {
        if (errors.length > 0) {
            return (
                <div class="container" id="app-container">
                    <h2 class="center gray pb-3">4DByD debugger console</h2>
                    <div class="card border shadow rounded" id="app">
                        <Table errors={this.state.errors} />
                    </div>
                    <p class="center gray pt-3">Click on an error to open the relevant files</p>
                </div>
            )
        } else {
            return (
                <div>
                    <h2 class="center gray pb-3">4DByD debugger console</h2>
                    <h4 class="center gray">Hurray! you have no errors!</h4>
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
                <tbody>
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
        let classes = ''
        if (oneLine) classes += ' one-line'
        if (this.props.clamped) classes += ' clamped'
        return <td className={classes}>{this.props.data}</td>
    }
}

$(document).ready(function() {
    let domContainer = document.querySelector('#mount')
    ReactDOM.render(<TableContainer />, domContainer)
})
