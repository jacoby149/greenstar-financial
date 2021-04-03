function Logs(props){
    const [log,setLog] = React.useState([]);
    function getLog(){
        if (props.id==-1) return;
        $.post(props.logRoute, { id: props.id },setLog);
    }
    React.useEffect(getLog,[props.id]);
    return props.formattedLog(log)
}

function Notes(props){
    function noteForm(log){
        var formattedLog = [];
        for (const [i, entry] of log.entries()) {
            var currLog = <div><b>{entry.date}</b><p>{entry.note}</p></div>
            formattedLog.push(currLog);
        }
        return formattedLog
    }
    return <Logs id = {props.id} 
                logRoute = {"/load_notes"} 
                    formattedLog = {noteForm} />
}


function Ledger(props){
    function ledgerForm(log){
        var formattedLog = [];
        for (const [i, entry] of log.entries()) {
            var currLedge = <div className = 'ledge'>
                        <p><b>{entry.date}</b></p><p>
                        "Recurring? : " {entry.recurring}</p><p>
                        "Check Num. : " {entry.check_number}</p><p>
                        "Amount ($) : " {entry.amount}</p><p>
                        "Description: " {entry.description}</p>
                        </div > ;
            formattedLog.push(currLedge);
        }
        return formattedLog
    }
    return <Logs id = {props.id} 
                logRoute = {"/load_ledger"} 
                    formattedLog = {ledgerForm} />
}
