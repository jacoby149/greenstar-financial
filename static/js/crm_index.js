import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import './static/crm/css/bootstrap.min.css';
import './static/crm/css/all.min.css';
import './static/crm/css/index_style.css';
import './static/crm/css/modal.css';


const e = React.createElement;

class crm extends Component {
    render() {
    return(
        <div style={{position:'absolute',right:'10px',top:'10px',width:'120px'}}>
            <a href="/crm_logout">Secure Log Out</a>
        </div>

        <div className="logo">
            <img src="static/crm/images/GreenstarBanner.png"/>
        </div>

        <div className=" jum">

            <div className=" navbar">
                <h3> Rolodex <i className="far fa-address-card"></i></h3>

            </div>


            <div className="row">


                <div className="col-lg-3 inp">

                    <input onkeyup="searchFunction()" id="myInput" className="form-control mt-2" placeholder="search"/>
                    <span className="icon "><i className="fas fa-search"></i></span>

                    <h5 className="mt-2">Add New Contact</h5>

                    <input className="form-control mb-2 mt-3" placeholder="add name" id="userName"/>
                    <div id="nameAlert" className="alert alert-danger text-justify p-2 ">Please add name</div>

                    <input className="form-control mb-3 mt-3" placeholder="add company" id="userCompany"/>
                    <div id="companyAlert" className="alert alert-danger text-justify p-2 ">Please add company</div>

                    <input className="form-control mb-3" placeholder="add phone" id="userPhone"/>
                    <div id="phoneAlert" className="alert alert-danger text-justify p-2 ">Please add a valid number</div>

                    <input className="form-control mb-3" placeholder="add e-mail" id="userEmail"/>
                    <div id="mailAlert" className="alert alert-danger text-justify p-2 ">Please add a valid e-mail</div>

                    <button onclick="addContact()" className="btn w-100 btn1">Add</button>


                </div>


                <div className="col-lg-8">
                    <div id="container demo">
                        <div className="options">
                            <button id="statusbutton" onclick="toggleStatus()"> Viewing Notes </button>
                            Green <input type="checkbox" onclick="statusFilter(this)" id="green" checked/>
                            Yellow <input type="checkbox" onclick="statusFilter(this)" id="yellow" checked/>
                            Red <input type="checkbox" id="red" onclick="statusFilter(this)" checked/>
                        </div>
                        {/* <!-- table-striped class for striped--> */}
                        <table id="myTable" className="table text-justify">

                            <thead className="tableh1">
                            <th className="">Name</th>
                            <th className="">Company</th>
                            <th className="">Phone</th>
                            <th className="">E-mail</th>
                            <th className="col-1"></th>
                            {/* <!--
                            <th className="col-1"></th>
                            --> */}

                            </thead>

                            <tbody id="tableBody">



                            </tbody>

                        </table>


                    </div>



                </div>
            </div>

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
                                <div className="col-6"> Change Date : <input className="form-control" type="date" name="date" maxlength="10"/></div>

                            </div>
                            <br/>



                            Add Note Here : <textarea name="newnote" id="newnote" cols="50" rows="4" maxlength="500"
                                                    placeholder="Add note"></textarea> <br/>
                            <div style={{float:'right',paddingRight:'50px',paddingTop:'10px'}}> <button type="submit" onclick="submitNote()">Create Entry</button> </div>
                            <br/><br/>
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
                                    <div className="col-6"> Date : <input className="form-control" type="date" name="date" maxlength="10"/></div>
                                    <div className="col-6">
                                        Amount ($) : <input className="form-control" type="text" name="amount"/>
                                    </div>
                                    <div className="col-6">
                                        Recurring? : <select name="recurring" className="form-control">
                                        <option value="One">One Time</option>
                                        <option value="Monthly">Monthly</option>
                                        <option value="Yearly">Yearly</option>
                                    </select>
                                    </div>
                                    <div className="col-6">
                                        Check Number : <input className="form-control" type="text" name="check_number"/>
                                    </div>
                                    <div className="col-6">

                                        Description : <input className="form-control" type="text" name="description"/>
                                    </div>
                                    <div className="col-6" style={{padding:'24px'}}>
                                        <button type="button" onclick="submitLedger()">Create Entry</button>
                                    </div>
                                    </div>
                                    <br/><br/>
                            </form>
                        </div>
                        <div id="ledger_log"> </div>
                    </div>

                </div>{/* <!-- modal-content --> */}
            </div>{/* <!-- modal-dialog --> */}
        </div>{/* <!-- modal --> */}

        <footer className="text-center"> Designed by Greenstar Group Inc. &#169; 2020. <br/></footer>
        );
    }
}

const domContainer = document.querySelector('#crmReact');
ReactDOM.render(e(crm), domContainer);
// export default crm;


