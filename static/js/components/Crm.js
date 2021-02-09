
function Logout() {
    return <div style={{ position: 'absolute', right: '10px', top: '10px', width: '120px' }}>
        <a href="/crm_logout">Secure Log Out</a>
    </div>
}


function Banner() {
    return <div className="logo">
        <br></br><br></br>
        <img src="static/img/GreenstarBanner.png" />
        <br></br>
    </div>

}

function Logo() {
    return <div className=" navbar">
        <h3> Rolodex <i className="far fa-address-card"></i></h3>

    </div>

}


function newContactJSON() {
    var contact = {
        name: userName.value,
        company: userCompany.value,
        phone: userPhone.value,
        email: userEmail.value,
        color: "yellow"
    };
    return contact;
}


function CrmInput(props) {
    function searchFunction() {
        console.log("search function");
    }

    /* Add a contact to the database, and alter the react state */
    function triggerAddContact() {
        $.post("/add_contact", newContactJSON(), props.addContact)
    }

    return <div className="col-lg-3 inp">

        <div>
            <input onKeyUp={searchFunction} id="myInput" className="form-control mt-2" placeholder="search" />
            <span className="icon "><i className="fas fa-search"></i></span>
        </div>
        <h5 className="mt-2">Add New Contact</h5>
        <form id="contactForm">
            <input className="form-control mb-2 mt-3" placeholder="add name" id="userName" />
            <div id="nameAlert" className="alert alert-danger text-justify p-2 ">Please add name</div>

            <input className="form-control mb-3 mt-3" placeholder="add company" id="userCompany" />
            <div id="companyAlert" className="alert alert-danger text-justify p-2 ">Please add company</div>

            <input className="form-control mb-3" placeholder="add phone" id="userPhone" />
            <div id="phoneAlert" className="alert alert-danger text-justify p-2 ">Please add a valid number</div>

            <input className="form-control mb-3" placeholder="add e-mail" id="userEmail" />

            <div id="mailAlert" className="alert alert-danger text-justify p-2 ">Please add a valid e-mail</div>
        </form>
        <button onClick={() => triggerAddContact()} className="btn btn-success w-100 ">Add</button>


    </div>
}

function TopMenu() {
    return <div className="options">
        <button id="statusbutton" className="btn btn-success" onClick={() => {toggleStatus()}}> Viewing Notes </button>
        &nbsp;
    Green <input type="checkbox" onClick={() => statusFilter(this)} id="green" defaultChecked />
    &nbsp;
    Yellow <input type="checkbox" onClick={() => statusFilter(this)} id="yellow" defaultChecked />
    &nbsp;
    Red <input type="checkbox" id="red" onClick={() => statusFilter(this)} defaultChecked />
    </div>

}


function Example() {
  const [show, setShow] = React.useState(false);

  const handleClose = () => setShow(false);
  const handleShow = () => setShow(true);

  return (
    <>
      <button variant="primary" onClick={handleShow}>
        Launch demo modal
      </button>

      <ReactModal show={show} onHide={handleClose} animation={false}>
        <ReactModal.Header closeButton>
          <ReactModal.Title>Modal heading</ReactModal.Title>
        </ReactModal.Header>
        <ReactModal.Body>Woohoo, you're reading this text in a modal!</ReactModal.Body>
        <ReactModal.Footer>
          <button variant="secondary" onClick={handleClose}>
            Close
          </button>
          <button variant="primary" onClick={handleClose}>
            Save Changes
          </button>
        </ReactModal.Footer>
      </ReactModal>
    </>
  );
}


function Modals() {
    function submitLedger() {
        console.log("submit ledger");
    }

    return <div>
        <div className="modal right fade" id="notes" tabIndex="-1" role="dialog" aria-labelledby="myModalLabel">
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
                            <div className="col-6"> Change Date : <input className="form-control" type="date" name="date" maxLength="10" /></div>

                        </div>
                        <br />



                            Add Note Here : <textarea name="newnote" id="newnote" cols="50" rows="4" maxLength="500"
                            placeholder="Add note"></textarea> <br />
                        <div style={{ float: 'right', paddingRight: '50px', paddingTop: '10px' }}> <button type="submit" onClick={() => submitNote()}>Create Entry</button> </div>
                        <br /><br />
                        <div id="note_log"> </div>
                    </div>

                </div>{/*<!-- modal-content -->*/}
            </div>{/* <!-- modal-dialog --> */}
        </div>{/* <!-- modal --> */}


        <div className="modal right fade" id="ledger" tabIndex="-1" role="dialog" aria-labelledby="myModalLabel">
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
                                <div className="col-6"> Date : <input className="form-control" type="date" name="date" maxLength="10" /></div>
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
                                    <button type="button" onClick={submitLedger}>Create Entry</button>
                                </div>
                            </div>
                            <br /><br />
                        </form>
                    </div>
                    <div id="ledger_log"> </div>
                </div>

            </div>{/* <!-- modal-content --> */}
        </div>{/* <!-- modal-dialog --> */}
    </div>
}

function GreenStarFooter() {
    return <footer className="text-center"> Designed by Greenstar Group Inc. &#169; 2020. <br /></footer>

}

function mprint(label, log) {
    console.log(label + ":");
    console.log(log);
}


function Crm() {
    /* State Variables */
    var initColumns = [['name', 'Name'], ['company', 'Company'], ['phone', 'Phone'], ['email', 'Email'], ['remove', '']];
    initColumns = initColumns.map(function (e) { return { 'title': e[1], 'label': e[0] } });
    const [columns, setColumns] = React.useState(initColumns);
    const [data, setData] = React.useState([]);

    function addContact(resp) {
        var newContact = newContactJSON();
        contactForm.reset();
        newContact.id = resp.id;
        let newData = [...data,newContact];
        setData(newData);
    }

    function deleteContact(id) {
        var filtered = data.filter(function(contact) { if (contact.id != id) {return contact;}});
        $.post('/remove_contact', {id:id}, () => setData(filtered));
    }

    /* Converts data entries to contacts */
    function contactFormat(e) {
        function shorten(s) {
            if (s.length > 25) { return s.slice(0, 25) + '...'; }
            else { return s; }
        }
        e.name = <a href="#" data-toggle="modal" data-target="#notes">{e.name}</a>;
        e.email = <a href={"mailto:" + e.email}>{shorten(e.email)}</a>;
        e.remove = <a onClick={() => {deleteContact(e.id)}} className="text-danger"><i className="fas fa-minus-circle"></i></a>;
        return e;
    }

    /* Initialize Contacts List */
    function init_contacts() { $.post('/load_contacts', {}, setData); }
    React.useEffect(init_contacts, []);

    /* Main return statement */
    return <div>
        <Logout />
        <Banner />
        <div className=" jum">
            <Logo />
            <div className="row">
                <CrmInput addContact={addContact} />
                <div className="col-lg-8">
                    <div id="container demo">
                        <TopMenu />
                        <DataTable columns={columns} data={data.map(contactFormat)} />
                    </div>
                </div>
            </div>
            <Example />
        </div>{/* <!-- modal --> */}
        <GreenStarFooter />
    </div>;
}

ReactDOM.render(
    <Crm />,
    document.getElementById('crmReact')
);

