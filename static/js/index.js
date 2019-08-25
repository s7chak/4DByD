const fakeError = { Time: 'Time', ErrorType: 'ErrorType', ErrorMessage: 'ErrorMessage' }
const errors = [
    {
        Time: '2015-06-07',
        ErrorType: 'NullPointerException',
        ErrorMessage:
            'project.ProjectItems.AddFromFile("C:/Users/sv/Documents/Visual Studio 2012/Projects/ConsoleApplication1/ConsoleApplication1/1.txt")' +
            'project.ProjectItems.AddFromFile("C:/Users/sv/Documents/Visual Studio 2012/Projects/ConsoleApplication1/ConsoleApplication1/1.txt")' +
            'project.ProjectItems.AddFromFile("C:/Users/sv/Documents/Visual Studio 2012/Projects/ConsoleApplication1/ConsoleApplication1/1.txt")'
    },
    {
        Time: '2015-06-07',
        ErrorType: 'NullPointerException',
        ErrorMessage:
            'project.ProjectItems.AddFromFile("C:/Users/sv/Documents/Visual Studio 2012/Projects/ConsoleApplication1/ConsoleApplication1/1.txt")'
    },
    {
        Time: '2015-06-07',
        ErrorType: 'NullPointerException',
        ErrorMessage:
            'project.ProjectItems.AddFromFile("C:/Users/sv/Documents/Visual Studio 2012/Projects/ConsoleApplication1/ConsoleApplication1/1.txt")'
    }
]

class Table extends React.Component {
    render() {
        return (
            <table className="table table-striped table-hover table-dark" cellPadding="30">
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
    render() {
        const header = this.props.header
        const error = this.props.error
        return (
            <tr className="table">
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
    const namespace = '/test'

    //     http[s]://<domain>:<port>[/<namespace>]
    const socket = io(namespace)

    socket.on('connect', function() {
        socket.emit('my_event', { data: "I'm connected!" })
    })

    socket.on('err', function(message) {
        window.console.log(message)
    })

    let domContainer = document.querySelector('#app')
    ReactDOM.render(<Table />, domContainer)
})
