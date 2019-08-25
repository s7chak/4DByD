const namespace = '/test'
const socket = io(namespace)

const fakeError = { Time: 'Time', ErrorType: 'Error type', ErrorMessage: 'Message' }
const errors = [
    {
        Time: '2015-06-07',
        ErrorType: 'NullPointerException',
        ErrorMessage: 'project.ProjectItems.AddFromFile("C:/Users/sv/Documents/Visual")'
    }
]

socket.on('connect', () => {
    socket.emit('my_event', { data: "I'm connected!" })
})


class Table extends React.Component {
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
        return (
            <table className="table table-striped table-hover table-light mb-0">
                <thead>
                    <Row header={true} error={fakeError}></Row>
                </thead>
                <tbody>
                    {errors.map(error => (
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
        const error = this.props.error
        return (
            <tr className="table" onClick = {() => {this.openStack()}}>
                <Cell oneLine={true} header={header} data={error.Time}></Cell>
                <Cell oneLine={true} header={header} data={error.ErrorType}></Cell>
                <Cell clamped={true} header={header} data={error.ErrorMessage}></Cell>
            </tr>
        )
    }
}

class Cell extends React.Component {
    render() {
        const data = this.props.data
        const oneLine = this.props.oneLine
        if (this.props.header) {
            return <th scope="col">{data}</th>
        } else {
            let classes = ''
            if (oneLine) classes += ' one-line'
            if (this.props.clamped) classes += ' clamped'
            return <td className={classes}>{data}</td>
        }
    }
}

$(document).ready(function() {
    let domContainer = document.querySelector('#app')
    ReactDOM.render(<Table />, domContainer)
})
