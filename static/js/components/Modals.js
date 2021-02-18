
function LedgerForm(){
    return  <form id="ledgerform">
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
                        <button type="button" onClick={"submitLedger"}>Create Entry</button>
                    </div>
                </div>
                <br /><br />
            </form>

}

function NoteForm(){
    return <div>
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
                
                <div style={{ float: 'right', paddingRight: '50px', paddingTop: '10px' }}> 
                    <button type="submit" onClick={() => submitNote()}>
                    Create Entry</button> 
                </div>
            </div>
}

function ModalHeader(){
    return  <div className="modal-header" id="modalbanner">
                <h4 className="modal-title" id="myModalLabel"></h4>


                <button type="button" className="close" data-dismiss="modal" aria-label="Close"><span
                    aria-hidden="true">&times;</span></button>
            </div>


}

function DataModal(props){
    return  <div className="modal right fade" id = {props.id} tabIndex="-1" role="dialog" aria-labelledby="myModalLabel">
            <div className="modal-dialog" role="document">
                <div className="modal-content">
                    <ModalHeader/>

                    <div className="modal-body">
                        {props.modalForm}                        
                        <br /><br />
                        {props.logs}
                    </div>

                </div>{/*<!-- modal-content -->*/}
            </div>{/* <!-- modal-dialog --> */}
        </div>
}