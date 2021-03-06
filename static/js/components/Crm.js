
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

    function addContact(resp) {
        const [data,setData] = props.hook;
        var newContact = newContactJSON();
        contactForm.reset();
        newContact.id = resp.id;
        let newData = [...data,newContact];
        setData(newData);
    }

    /* Add a contact to the database, and alter the react state */
    function triggerAddContact() {
        $.post("/add_contact", newContactJSON(), addContact)
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

function TopMenu(props) {
    return <div className="options">
        <button id="statusbutton" className="btn btn-success" onClick={props.toggleViewMode}> Viewing {props.viewMode} </button>
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

function ContactTable(props){

    /* Data Table State Variables */
    var initColumns = [['name', 'Name'], ['company', 'Company'], ['phone', 'Phone'], ['email', 'Email'], ['remove', '']];
    initColumns = initColumns.map(function (e) { return { 'title': e[1], 'label': e[0] } });
    const [columns, setColumns] = React.useState(initColumns);
    const [data,setData] = props.dataHook;
    const [contactID,setContactID] = props.idHook;

    /* Deletes a contact */
    function deleteContact(id) {

        /* function to filter contact with the given id */
        function f(contact) { if (contact.id != id) {return contact;}}
        var filtered = data.filter(f);

        /* Deletion of the contact */
        $.post('/remove_contact', {id:id}, () => setData(filtered));
    }


    /* Properly formats a given contact in the data table. */
    function contactFormat(e) {

        function shorten(s) {
            if (s.length > 25) { return s.slice(0, 25) + '...'; }
            else { return s; }
        }
    
        /* Make a deep copy of e */
        var formatted = {...e};

        formatted.name = <a href="#" 
            data-toggle="modal" 
                data-target={"#" + props.viewMode}
                    onClick = {()=>setContactID(e.id)}>
                            {e.name}
                         </a>;
        formatted.email = <a href={"mailto:" + e.email}>{shorten(e.email)}</a>;
        formatted.remove = <a onClick={() => {deleteContact(e.id)}} className="text-danger"><i className="fas fa-minus-circle"></i></a>;
        return formatted;
    }

    return <DataTable columns={columns} data={data.map(contactFormat)} />

}

function Crm() {
    /* Contact Data */
    const [data, setData] = React.useState([]);

    /* view Mode */
    const [viewMode,setViewMode] = React.useState("notes");
    function toggleViewMode(){
        if (viewMode == "notes"){
            setViewMode("ledger");}
        else{setViewMode("notes")}
    }

    /* Current Contact ID */
    const [contactID,setContactID] = React.useState(-1);
    var contact = data.filter((e) => e.id == contactID );
    contact = contact.length>0?contact[0]:{};
    
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
                
                {/* Search bar + inputs to add contacts. */}
                <CrmInput hook = {[data,setData]}/>

                <div className="col-lg-8">
                    <div id="container demo">
                        <TopMenu
                            viewMode = {viewMode}
                                toggleViewMode = {toggleViewMode} />
                        
                        {/* Main table for viewing and removing contacts. */}
                        <ContactTable 
                            viewMode = {viewMode}
                                dataHook = {[data,setData]}
                                    idHook = {[contactID,setContactID]}
                        />
                    
                    </div>
                </div>
            </div>
                
                {/* Notes Modal */}
                <DataModal contact = {contact}  datahook = {[data,setData]} mode = "notes"
                                mode = {"notes"}
                />

                {/* Ledger Modal */}
                <DataModal contact = {contact} datahook = {[data,setData]} mode = "ledger"
                                mode = {"ledger"}     
                />

        </div>
        <GreenStarFooter />
    </div>;
}

ReactDOM.render(
    <Crm />,
    document.getElementById('crmReact')
);

