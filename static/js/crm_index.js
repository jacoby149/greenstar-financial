/* The column labels of DataTable */
function TableHeader(props) {
    console.log("In TableHeader")
    console.log(props.labels)
    const header = [];
    for (let label of props.labels) {
        header.push(<th>{label}</th>);
    }
    return <thead className="tableh1"><tr>{header}</tr></thead>;
}

/* Entry in the DataTable */
function TableRow(props) {
    console.log("In TableRows")
    const attributes = props.labels.map(label => label.toLowerCase());
    const row = [];
    for (let attribute of attributes) {
        row.push(<td>{props.entry[attribute]}</td>);
    }
    return <tr className={props.entry.color}>{row}</tr>;
}

/* Body of DataTable */
function TableBody(props) {
    console.log("In TableBody")
    console.log(props)
    const body = [];
    for (let entry of props.data) {
        body.push(<TableRow entry={entry} labels={props.labels} />);
    }
    return <tbody id="tableBody">{body}</tbody>;
}

/* DataTable Component */
function DataTable(props) {
    console.log("In DataTable");
    const labels = props.labels;
    const data = props.data;
    return <table id="myTable" className="table text-justify">

        <TableHeader labels={labels} />
        <TableBody labels={labels} data={data} />

    </table>;
}

function Logout() {
    return <div style={{ position: 'absolute', right: '10px', top: '10px', width: '120px' }}>
        <a href="/crm_logout">Secure Log Out</a>
    </div>
}

function Banner() {
    return <div className="logo">
        <img src="static/crm/images/GreenstarBanner.png" />
    </div>

}

function Logo() {
    return <div className=" navbar">
        <h3> Rolodex <i className="far fa-address-card"></i></h3>

    </div>

}

function CrmInput() {
    return <div className="col-lg-3 inp">

        <input onKeyUp="searchFunction()" id="myInput" className="form-control mt-2" placeholder="search" />
        <span className="icon "><i className="fas fa-search"></i></span>

        <h5 className="mt-2">Add New Contact</h5>

        <input className="form-control mb-2 mt-3" placeholder="add name" id="userName" />
        <div id="nameAlert" className="alert alert-danger text-justify p-2 ">Please add name</div>

        <input className="form-control mb-3 mt-3" placeholder="add company" id="userCompany" />
        <div id="companyAlert" className="alert alert-danger text-justify p-2 ">Please add company</div>

        <input className="form-control mb-3" placeholder="add phone" id="userPhone" />
        <div id="phoneAlert" className="alert alert-danger text-justify p-2 ">Please add a valid number</div>

        <input className="form-control mb-3" placeholder="add e-mail" id="userEmail" />
        <div id="mailAlert" className="alert alert-danger text-justify p-2 ">Please add a valid e-mail</div>

        <button onClick="addContact()" className="btn w-100 btn1">Add</button>


    </div>
}

function TopMenu() {
    return <div className="options">
        <button id="statusbutton" onClick="toggleStatus()"> Viewing Notes </button>
    Green <input type="checkbox" onClick="statusFilter(this)" id="green" defaultChecked />
    Yellow <input type="checkbox" onClick="statusFilter(this)" id="yellow" defaultChecked />
    Red <input type="checkbox" id="red" onClick="statusFilter(this)" defaultChecked />
    </div>

}

function Modals() {
    return <div>
        <div className="modal right fade" id="notes" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
            <div className="modal-dialog" role="document">
                <div className="modal-content">

                    <div className="modal-header" id="modalbanner">
                        <h4 className="modal-title" id="myModalLabel"></h4>


                        <button type="button" className="close" data-dismiss="modal" aria-label="Close"><span
                            aria-hidden="true">&times;</span></button>
                    </div>

                    <div className="modal-body">


                        <div className="row">
                            <div className="col-6">
                                Scheduled Status Change : <select name="recurring" className="form-control">
                                    <option value="none">None Scheduled</option>
                                    <option value="green">Green</option>
                                    <option value="yellow">Yellow</option>
                                    <option value="red">Red</option>
                                </select>
                            </div>
                            <div className="col-6"> Change Date : <input className="form-control" type="date" name="date" maxlength="10" /></div>

                        </div>
                        <br />



                            Add Note Here : <textarea name="newnote" id="newnote" cols="50" rows="4" maxlength="500"
                            placeholder="Add note"></textarea> <br />
                        <div style={{ float: 'right', paddingRight: '50px', paddingTop: '10px' }}> <button type="submit" onClick="submitNote()">Create Entry</button> </div>
                        <br /><br />
                        <div id="note_log"> </div>
                    </div>

                </div>{/*<!-- modal-content -->*/}
            </div>{/* <!-- modal-dialog --> */}
        </div>{/* <!-- modal --> */}


        <div className="modal right fade" id="ledger" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
            <div className="modal-dialog" role="document">
                <div className="modal-content">

                    <div className="modal-header" id="modalbanner">
                        <h4 className="modal-title" id="ledgerlabel"> Ledger </h4>


                        <button type="button" className="close" data-dismiss="modal" aria-label="Close"><span
                            aria-hidden="true">&times;</span></button>
                    </div>

                    <div className="modal-body">
                        <form id="ledgerform">

                            <div className="row">
                                <div className="col-6"> Date : <input className="form-control" type="date" name="date" maxlength="10" /></div>
                                <div className="col-6">
                                    Amount ($) : <input className="form-control" type="text" name="amount" />
                                </div>
                                <div className="col-6">
                                    Recurring? : <select name="recurring" className="form-control">
                                        <option value="One">One Time</option>
                                        <option value="Monthly">Monthly</option>
                                        <option value="Yearly">Yearly</option>
                                    </select>
                                </div>
                                <div className="col-6">
                                    Check Number : <input className="form-control" type="text" name="check_number" />
                                </div>
                                <div className="col-6">

                                    Description : <input className="form-control" type="text" name="description" />
                                </div>
                                <div className="col-6" style={{ padding: '24px' }}>
                                    <button type="button" onClick="submitLedger()">Create Entry</button>
                                </div>
                            </div>
                            <br /><br />
                        </form>
                    </div>
                    <div id="ledger_log"> </div>
                </div>

            </div>{/* <!-- modal-content --> */}
        </div>{/* <!-- modal-dialog --> */}
    </div >
}

function GreenStarFooter() {
    return <footer className="text-center"> Designed by Greenstar Group Inc. &#169; 2020. <br /></footer>

}

function Crm() {

    /* State Variables */
    const [firstLoad, setFirstLoad] = React.useState(true);
    const [labels, setLabels] = React.useState(['Name', 'Company', 'Phone', 'Email', '']);
    const [data, setData] = React.useState([]);

    /* Converts data entries to contacts */
    function contact(e) {
        e.name = <a href="/" onClick="">{e.name}</a>;
        /*TODO linkify email, etc. */
        return e;
    }
    /* Setdata wrapper for contacts */
    function setContacts(resp) { setData(resp.map(contact)); }

    /* Initialize Contacts List */
    function init_contacts() { $.post('/load_contacts', {}, setContacts); }
    React.useEffect(init_contacts, []);

    /* Main return statement */
    return <div>
        <Logout />
        <Banner />
        <div className=" jum">
            <Logo />
            <div className="row">
                <CrmInput />
                <div className="col-lg-8">
                    <div id="container demo">
                        <TopMenu />
                        <DataTable labels={labels} data={data} />
                    </div>
                </div>
            </div>
            <Modals />
        </div>{/* <!-- modal --> */}
        <GreenStarFooter />
    </div>;
}

ReactDOM.render(
    <Crm />,
    document.getElementById('crmReact')
);

