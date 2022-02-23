
tables = [];
editTableId = -1;

function loadTables(){
    tables = [];
    $.getJSON('/get_tables',(data) => {
      
      for(var i in data ){
        var v = data[i]
        tables[i] = v;
      }
      updateTableView();
    })
}

   
function updateTableView(){
    
    //Remove all rows first
    $("tbody tr").remove()

    for(table of tables){
        var row = createRow(table)
        $('tbody').append(row)
    }
}


function addTable(id){
    closeAddForm();
    $.ajaxSetup({beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }});
    var data = $('#'+id).serialize()
    $.post('add_table/',data,(data) => {
        if(data){
            notify('table');
            loadTables();
        }
    })

    document.getElementById('addTableButton').onclick=openAddForm;

}
function copyCurrentTable(){
    $.getJSON('copy_table/'+currentTid+'/',(data)=>{
        tables.push(data);
        notifyShare('table');
    })
}


// Main function



function createRow(table){
    var row = 
    `<tr style="background-color:whitesmoke;">
          <td>${table['fields']['user']}</td>
          <td> 
            <a style="outline: none;" href="/table_view/${table['pk']}"> ${table['fields']['name']}</a>
          </td> <br/>
          <td>Monday</td>
          <td>Endday</td>
          <td>8.${table['fields']['slotOffset']}</td>
          <td>${table['fields']['is_shared']}</td>
          <td>14.01.1999</td>
          
          <td>
          <div>
              <button id = "deleteButton#${table['pk']}" onclick="delTable(${table['pk']})"     style="padding:10px;margin:10px;width:40px"  class="delete-button"><i class="fa fa-trash"></i></button>
              <button id = "editTableButton#${table['pk']}" onclick="openEditForm(${table['pk']})" style="padding:10px;margin:10px;width:40px"  class="edit-button" ><i class="fa fa-edit"></i></button>
          </div>
          </td>
  
    </tr>`
  
  
      return row
      
  }

function editTable(id){
    closeEditForm();
    $.ajaxSetup({beforeSend: function(xhr, settings) {
			xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
			}});
    var data = $('#'+id).serialize()+'&'+'pk='+editTableId
    $.post('edit_table/',data,(data) => {
        notify('table')
        loadTables()
    })
    
    document.getElementById('editTableButton').onclick=openEditForm;

  
}

function delTable(pk){
    $.ajaxSetup({beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }});
    var data = {pk:pk}
    $.post('del_table/',data,(data) => {
        notify('table')
        loadTables();
    })

}

function openAddForm() {
    $('#addTableForm').trigger('reset')
    $('#addTableFormDiv').css('display','block');
}

function closeAddForm() {
    $('#addTableFormDiv').css('display','none');
}
function openEditForm(id) {
    // $('#editTableForm')
    fillForm(id)
    $('#editTableFormDiv').css('display','block');
    editTableId = id
}
function fillForm(id){
    var table = getTableFromId(id)
    $('#editTableFormDiv').remove()
    var form = `
        <div id="editTableFormDiv" style = "left:1300px;top:95px" class="form-popup" style="display: none;" >
        <form id = "editTableForm" onsubmit="return false;"  class="form-container" style="max-height: 500px;">
            <input type="text" placeholder="Name" name="name" value= ${table['fields']['name']} required><br/><br/>
            <input type="number" placeholder=" Day Number" name="days" value= ${table['fields']['days']} required> <br/><br/>
            <input type="number" placeholder="Slots Per Day " name="slotsPerDay" value= ${table['fields']['slotsPerDay']} required> <br/><br/>
            <input type="number" placeholder="Slot Offset" name="slotOffset" value= ${table['fields']['slotOffset']} required> <br/><br/>
            <!-- Shared? <input type="checkbox" name="is_shared"> <br/><br/> -->
            <button onclick = "editTable('editTableForm')" class="accept-button"><i class="fas fa-check"></i></button>
            <button onclick = "closeEditForm()" class="cancel-button"><i class="fas fa-times"></i></button>
            <!-- <input type="hidden" name="user" value={{user}}/> -->
        </form>
        </div>`
    $('body').append(form)
    //sets
    // $('#editTableForm')[0][1] = table.fields.
}
function closeEditForm() {
    $('#editTableFormDiv').css('display','none');
}
function getTableFromId(id){
    for(table of tables){
        if(table.pk==id){
            return table
        }
    }
    return null
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// 
// 
// 
// 
// 
// 
// 
// 






currentTid = -1;

function removeAllNextSiblings(id){
    $('#'+id).nextAll('div.content').remove();
}


rooms = [];
editRoomId = -1;


function loadRooms(){
    rooms = [];
    $.getJSON('get_rooms/'+currentTid+'/',(data) => {
      for(var i in data ){
        var v = data[i]
        rooms[i] = v;
      }
      updateRoomView();
    })
}
 
function updateRoomView(){
    
    //Remove all rows first
    removeAllNextSiblings('roomTitleButton')
    for(room of rooms){
        var row = createRoomRow(room)
        $('#roomDiv').append(row)
    }
}

function createRoomRow(room){
    var row = 
    `<div class="content">
        <button class="row sub_row"> ${room['fields']['description']}
            <button class="delete-button" onclick="deleteRoom(${room['pk']})"><i class="fa fa-trash"></i></button>
            <button class="edit-button" onclick="openEditRoomForm(${room['pk']})"><i class="fa fa-edit"></i></button>
        </button>
    </div>`
    return row
}

function addRoom(id){
    closeAddRoomForm();
    $.ajaxSetup({beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }});
    var data = $('#'+id).serialize()
    $.post('add_room/'+currentTid+'/',data,(data) => {
        // console.log(data);
        notify('rooms');
        loadRooms()
    })
}

function openAddRoomForm() {
    $('#addRoomForm').trigger('reset')
    $('#addRoomFormDiv').css('display','block');
}

function closeAddRoomForm() {
    $('#addRoomFormDiv').css('display','none');
}

function editRoom(id){
    closeEditRoomForm();
    $.ajaxSetup({beforeSend: function(xhr, settings) {
			xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
			}});
    // ;
    var data = $('#'+id).serialize()+'&'+'pk='+editRoomId
    $.post('edit_room/',data,(data) => {
        notify('rooms')
        loadRooms()
    })
    

  
}

function deleteRoom(pk){
    $.ajaxSetup({beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }});
    var data = {pk:pk}
    $.post('delete_room/',data,(data) => {
        notify('rooms')
        loadRooms();
    })

}

function openEditRoomForm(id) {
    // $('#editTableForm')
    fillRoomForm(id)
    $('#editRoomFormDiv').css('display','block');
    editRoomId = id
}
function fillRoomForm(id){

    var room = getRoomFromId(id)
    $('#editRoomFormDiv').remove()
    var form = 
    `<div id="editRoomFormDiv" class="form-popup">
        <form id="editRoomForm" onsubmit="return false;" class="form-container">
            <input type="text" placeholder="New Capacity" name="capacity" value= ${room['fields']['capacity']} required><br/>
            <input type="text" placeholder="New Description" name="description" value= ${room['fields']['description']} required> <br/>
            <button onclick = "editRoom('editRoomForm')" class="accept-button"><i class="fas fa-check"></i></button>
            <button onclick = "closeEditRoomForm()" class="cancel-button"><i class="fas fa-times"></i></button>
        </form>
    </div>`
    $('body').append(form)
}

function closeEditRoomForm() {
    $('#editRoomFormDiv').css('display','none');
}
function getRoomFromId(id){
    for(room of rooms){
        if(room.pk==id){
            return room
        }
    }
    return null
}



/*

            SECTIONS 

*/
sections = [];
editSectionId = -1;

function loadSections(){
    sections = [];
    $.getJSON('get_sections/'+currentTid+'/',(data) => {
      // console.log(data)
      for(var i in data ){
        var v = data[i]
        sections[i] = v;
      }
      //
      updateSectionView();
    })
}
 
function updateSectionView(){
    
    //Remove all rows first
    removeAllNextSiblings('sectionTitleButton')
    // //;
    for(section of sections){
        var row = createSectionRow(section)
        $('#sectionDiv').append(row)
        //;
    }
}

function createSectionRow(section){
    var row = 
    `<div class="content">
        <button class="row sub_row"> ${section['fields']['description']}
            <button class="delete-button" onclick="deleteSection(${section['pk']})" ><i class="fa fa-trash"></i></button>
            <button class="edit-button" onclick="openEditSectionForm(${section['pk']})"><i class="fa fa-edit"></i></button>
            <button class="edit-button" onclick="openAddPersonForm(${section['pk']})"><i class="fa fa-user-plus" aria-hidden="true"></i></button>
            <button class="edit-button" onclick="showPeople(${section['pk']})"><i class="fa fa-user" aria-hidden="true"></i></button>
        </button>
    </div>`

    return row
        
}


function addSection(id){
    closeAddSectionForm();
    $.ajaxSetup({beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }});
    var data = $('#'+id).serialize()
    $.post('add_section/'+currentTid+'/',data,(data) => {
        notify('sections')
        notify('events')
        loadSections();
        loadTableDisplay();

    })



}

function openAddSectionForm() {
    $('#addSectionForm').trigger('reset')
    $('#addSectionFormDiv').css('display','block');
}

function closeAddSectionForm() {
    $('#addSectionFormDiv').css('display','none');
}

function editSection(id){
    closeEditSectionForm();
    $.ajaxSetup({beforeSend: function(xhr, settings) {
			xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
			}});
    // ;
    var data = $('#'+id).serialize()+'&'+'pk='+editSectionId
    $.post('edit_section/',data,(data) => {
        notify('sections')
        loadSections()
    })  
}

function deleteSection(pk){
    $.ajaxSetup({beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }});
    var data = {pk:pk}
    $.post('delete_section/',data,(data) => {
        notify('sections')
        loadSections();
    })
}

function openEditSectionForm(id) {
    // $('#editTableForm')
    fillSectionForm(id)
    $('#editSectionFormDiv').css('display','block');
    editSectionId = id
}
function closeEditSectionForm() {
    $('#editSectionFormDiv').css('display','none');
}
function fillSectionForm(id){

    var section = getSectionFromId(id)
    $('#editSectionFormDiv').remove()
    let form = 
    `<div id = "editSectionFormDiv" class="form-popup" id="edit-section">
        <form id="editSectionForm" onsubmit="return false;" class="form-container">
            <input type="text" placeholder = "New Course Id" name="courseId" value=${section['fields']['courseId']} required><br/>
            <input type="text" placeholder = "New Current Section" name="currSec" value=${section['fields']['currSec']} required><br/>
            <input type="text" placeholder = "New Total Section" name="totSection" value=${section['fields']['totSection']} required><br/>
            <input type="text" placeholder = "New Description" name="description" value=${section['fields']['description']} required> <br/>
            <input type="text" placeholder = "New Instructor" name="instructor" value=${section['fields']['instructor']}> <br/>
            <button onclick="editSection('editSectionForm')"  class="accept-button"><i class="fas fa-check"></i></button>
            <button onclick="closeEditSectionForm()" class="cancel-button"><i class="fas fa-times"></i></button>
        </form>
    </div>` 
    // ;
    $('body').append(form)
}

function getSectionFromId(id){
    for(section of sections){
        if(section.pk==id){
            return section
        }
    }
    return null
}



/*

        P E O P L E

*/

people = []
editPersonId = -1;
currentSid = -1;



function loadPeople(){
    people = [];
    $.getJSON('get_people/'+currentTid+'/'+currentSid+'/' ,(data) => {
      // console.log(data)
      for(var i in data ){
        var v = data[i]
        people[i] = v;
      }
      //
      updatePeopleView();
    })
}
 
function updatePeopleView(){
    
    //Remove all rows first
    $('#peopleTableHeader').nextAll('tr').remove();

    for(person of people){
        var row = createPersonRow(person)
        $('#peopleTableBody').append(row)
        //;
    }
}

function createPersonRow(person){
    // ;
    var row = 
        `
        <tr style="height:1cm;">
            <td>${person['pk']}</td>
            <td>${person['fields']['name']}</td>
            <td>${person['fields']['is_instructor']}</td>
            <td> 
            <button style="margin:0" class="delete-button-person" onclick="deletePerson(${person['pk']})" ><i class="fa fa-trash"></i></button>
            </td>
            <td>
            <button style="margin:0" class="edit-button-person" onclick="openEditPersonForm(${person['pk']})"><i class="fa fa-edit"></i></button>
            </td>
        </tr>
        `
    return row
        
}


function addPerson(id){
    closeAddPersonForm();
    $.ajaxSetup({beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }});
    var data = $('#'+id).serialize()
    $.post('add_person/'+currentTid+'/'+currentSid+'/',data,(data) => {
        notify('people');
        notify('sections');
        notify('events')
        loadPeople();
        loadSections();
        loadTableDisplay();

    })

}

function openAddPersonForm(sid) {
    currentSid=sid;
    $('#addPersonForm').trigger('reset')
    $('#addPersonFormDiv').css('display','block');
}

function closeAddPersonForm() {
    $('#addPersonFormDiv').css('display','none');
}

function editPerson(id){
    closeEditPersonForm();
    $.ajaxSetup({beforeSend: function(xhr, settings) {
			xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
			}});
    // ;
    var data = $('#'+id).serialize()+'&'+'pk='+editPersonId
    $.post('edit_person/'+currentSid+'/',data,(data) => {
        notify('people');
        notify('sections');
        notify('events')
        loadPeople();
        loadSections();
        loadTableDisplay();
        sid = (getPersonFromId(editPersonId))['fields']['sectionPer']
        showPeople(sid);
    })  
}

function deletePerson(pk){
    $.ajaxSetup({beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }});
    var data = {pk:pk}
    $.post('delete_person/',data,(data) => {
        notify('people');
        notify('sections');
        notify('events')
        loadPeople();
        loadSections();
        loadTableDisplay();
        sid = (getPersonFromId(pk))['fields']['sectionPer']
        showPeople(sid);
    })
}

function showPeople(sid){
    currentSid=sid;
    $('#peopleTable').css('display','block');
    loadPeople();
}

function closePeopleTable(){
    $('#peopleTable').css('display','none');
}

function openEditPersonForm(id) {
    // $('#editTableForm')
    fillPersonForm(id)
    $('#editPersonFormDiv').css('display','block');
    editPersonId = id
}
function closeEditPersonForm() {
    $('#editPersonFormDiv').css('display','none');
}
function fillPersonForm(id){

    var person = getPersonFromId(id)
    $('#editPersonFormDiv').remove()
    let form = 
    `<div id = "editPersonFormDiv" class="form-popup">
        <form id="editPersonForm" onsubmit="return false;" class="form-container">
            <input type="text" placeholder = "New Person Name" name="name" value=${person['fields']['name']} required><br/>
            is instructor? <br/>
            <input type="radio" id="yes" name="is_instructor" value="Yes">
            <label for="yes">YES</label><br>
            <input type="radio" id="no" name="is_instructor" value="No">
            <label for="no"> NO </label><br>            
            <button onclick="editPerson('editPersonForm')"  class="accept-button"><i class="fas fa-check"></i></button>
            <button onclick="closeEditPersonForm()" class="cancel-button"><i class="fas fa-times"></i></button>

        </form>
    </div>` 
    $('body').append(form)
}

function getPersonFromId(id){
    for(person of people){
        if(person.pk==id){
            return person
        }
    }
    return null
}

/* 

        E  V E N T 


*/

currentEvent= -1
currentRow  = -1
currentCell = -1
currentEventObject=undefined

function addEvent(id){
    closeAddEventForm();
    $.ajaxSetup({beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }});
    var data = $('#'+id).serialize()+'&'+'day='+ (currentCell-1) + '&' + 'slot_number=' + (currentRow-1)
    $.post('add_event/'+currentTid+'/',data,(data) => {
        notify('events')
        loadTableDisplay()
    })
}

function openAddEventForm(row,cell) {
    currentRow = row
    currentCell = cell
    $('#addEventForm').trigger('reset')
    $('#addEventFormDiv').css('display','block');
}
function closeAddEventForm() {
    $('#addEventFormDiv').css('display','none');
}

function editEvent(id){
    closeEditEventForm();
    $.ajaxSetup({beforeSend: function(xhr, settings) {
			xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
			}});
    // ;
    var data = $('#'+id).serialize()+'&'+'pk='+currentEventObject[0]['pk']
    $.post('edit_event/',data,(data) => {
        notify('events')
      loadTableDisplay()
    })  
}

function deleteEvent(){
    closeEditEventForm();
    $.ajaxSetup({beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }});
    var data = {pk:currentEventObject[0]['pk']}
    $.post('delete_event/',data,(data) => {
        notify('events')
        loadTableDisplay();
    })
}

function openEditEventForm(row,cell,event) {
    // $('#editTableForm')
    currentRow=row
    currentCell=cell
    currentEvent=event
    getAndFillEvent(tableDisplay[row][cell][event])
}
function closeEditEventForm() {
    $('#editEventFormDiv').css('display','none');
}

function getAndFillEvent(description) {

    $.ajaxSetup({beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }});
    var data = {description:description}

    $.post('get_event/'+currentTid+'/',data,(data) => {
        currentEventObject = data
        fillEditEventForm()
    })
    
}

function fillEditEventForm(){
    let event = currentEventObject[0]
    // ;    
    $('#editEventFormDiv').remove()
    let section = getSectionFromId(event['fields']['section'])
    let room = getRoomFromId(event['fields']['room'])
    let form = 
    `<div id = "editEventFormDiv" class="form-popup" id="edit-event">
        <form id="editEventForm" onsubmit="return false;" class="form-container">
            <input type="text" placeholder = "New Section" name="section" value=${section['fields']['description']} required><br/>
            <input type="text" placeholder = "New Room" name="room" value=${room['fields']['description']} required><br/>
            <input type="text" placeholder = "New Description" name="description" value=${event['fields']['description']} required><br/>
            <input type="text" placeholder = "New Length" name="length" value=${event['fields']['length']} required><br/>
            <button onclick="editEvent('editEventForm')" class="accept-button"><i class="fas fa-check"></i></button>
            <button onclick="closeEditEventForm()" class="cancel-button"><i class="fas fa-times"></i></button>
            <button class="accept-button" onclick="deleteEvent()"><i class="fa fa-trash"></i></button>
        </form>
    </div>` 
    // ;
    $('body').append(form)
    $('#editEventFormDiv').css('display','block');

}


/* 

        T A B L E  D I S P L A Y


*/
tableDisplay = [];
conflictsText = '';

function loadTableDisplay(){

    tableDisplay=[];
    $.getJSON('display_table/'+currentTid+'/',(data) => {
        conflictsText = data[0];
        tableDisplay = data[1];
        updateTableDisplay();
        updateConflictsView();
      })

}

function updateConflictsView(){

    $('#conflictReportDiv').empty()
    $('#conflictReportDiv').append(`<text>${conflictsText}</text>`)

}

function updateTableDisplay(){
    $('#tableDisplay').empty();
    tableDisplayHTML = '';
    for(var row in tableDisplay){
        tableDisplayHTML += '<tr>'
        for(var cell in tableDisplay[row]){
            tableDisplayHTML += `<td id=${row}-${cell}>`
            if(cell > 0 && row > 0)
                tableDisplayHTML += `<button id="addEventButton" onclick="openAddEventForm(${row},${cell});"><i class="fa fa-plus"></i></button> <br/>`
            for(var event in tableDisplay[row][cell]){
                tableDisplayHTML += `<text onclick="openEditEventForm(${row},${cell},${event});">` + tableDisplay[row][cell][event] + '<br/> </text>'
            }
            // tableDisplayHTML += tableDisplay[row][cell]
            tableDisplayHTML += '</td>'
        }
        tableDisplayHTML += '</tr>'
    }
    $('#tableDisplay').append(tableDisplayHTML)
    // ;
    

}


function toggleTableShare(option){
    $.ajaxSetup({beforeSend: function(xhr, settings) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }});
    var data;
    if(option=='unshare'){
        data = '&'+'pk='+currentTid + '&'+'is_shared='+'False'
        $.post('edit_table/',data,(data) => {
            notifyShare('share')
            loadTable();
        })
    }
    else{
        data = '&'+'pk='+currentTid + '&'+'is_shared='+'True'
        $.post('edit_table/',data,(data) => {
            notifyShare('share')
            loadTable();
        })
    }
}
function updateSharedView(){
    let table = getTableFromId(currentTid)
    $('#shareContentView').empty()
    let row;
    if(table['fields']['is_shared']){
        row = `
            <button class="row sub_row"> Toggle to Unshare 
                <button class="delete-button" onclick="toggleTableShare('unshare')"><i class="fas fa-toggle-on"></i></button>
            </button>
        `
    }
    else{
        row = `
            <button class="row sub_row"> Toggle to Share 
                <button class="delete-button" onclick="toggleTableShare('share')"><i class="fas fa-toggle-off"></i></button>
            </button>
        `
    }
    $('#shareContentView').append(row)
      
}
function loadTable(){
    tables = [];
    $.getJSON('/get_tables',(data) => {
      // console.log(data)
      for(var i in data ){
        var v = data[i]
        tables[i] = v;
      }
      updateSharedView();
    })
}

