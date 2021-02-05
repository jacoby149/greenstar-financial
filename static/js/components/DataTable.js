/* The column columns of DataTable */
function TableHeader(props) {
    const header = [];
    for (let column of props.columns) {
        header.push(<th>{column.title}</th>);
    }
    return <thead className="tableh1"><tr>{header}</tr></thead>;
}

/* Entry in the DataTable */
function TableRow(props) {
    const attributes = props.columns.map(column => column.label.toLowerCase());

    const row = [];
    for (let attribute of attributes) {
        row.push(<td>{props.entry[attribute]}</td>);
    }
    return <tr className={props.entry.color}>{row}</tr>;
}

/* Body of DataTable */
function TableBody(props) {
    const body = [];
    for (let entry of props.data) {
        body.push(<TableRow entry={entry} columns={props.columns} />);
    }
    return <tbody id="tableBody">{body}</tbody>;
}

/* DataTable Component */
function DataTable(props) {
    const columns = props.columns;
    const data = props.data;
    return <table id="myTable" className="table text-justify">

        <TableHeader columns={columns} />
        <TableBody columns={columns} data={data} />

    </table>;
}