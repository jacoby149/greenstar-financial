
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

function GreenStarFooter() {
    return <footer className="text-center"> Designed by Greenstar Group Inc. &#169; 2020. <br /></footer>

}


function Crm() {
    
    /* Data Table State Variables */
    var initColumns = [['name', 'Name'], ['company', 'Company'], ['phone', 'Phone'], ['email', 'Email'], ['remove', '']];
    initColumns = initColumns.map(function (e) { return { 'title': e[1], 'label': e[0] } });
    const [columns, setColumns] = React.useState(initColumns);
    const [data, setData] = React.useState([]);

    /* Current Contact State Variable */
    const [contactID,setContactID] = React.useState(-1);

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
    
        /* Make a deep copy of e */
        var formatted = {...e};

        formatted.name = <a href="#" 
            data-toggle="modal" 
                data-target="#notes"
                    onClick = {()=>setContactID(e.id)}>
                            {e.name}
                         </a>;
        formatted.email = <a href={"mailto:" + e.email}>{shorten(e.email)}</a>;
        formatted.remove = <a onClick={() => {deleteContact(e.id)}} className="text-danger"><i className="fas fa-minus-circle"></i></a>;
        return formatted;
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
                <DataModal modalForm = {<NoteForm/>} 
                            logs = { <Notes id={contactID}/> } 
                />

                <DataModal modalForm = {<LedgerForm/>} 
                            logs = { <Ledger id = {contactID}/> }     
                />
        </div>{/* <!-- modal --> */}
        <GreenStarFooter />
    </div>;
}

ReactDOM.render(
    <Crm />,
    document.getElementById('crmReact')
);

