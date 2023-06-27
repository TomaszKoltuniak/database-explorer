var showFormButton2 = document.getElementById("showFormButton2");
var addCompanyDialog = document.getElementById("addCompanyDialog");
var addCompanyForm = document.getElementById("addCompanyForm");
var addCompanySubmitButton = document.getElementById(
    "addCompanySubmitButton"
);

showFormButton2.addEventListener("click", function () {
    addCompanyDialog.showModal();
});

addCompanyForm.addEventListener("close", function () {
    addCompanyDialog.submit();
});

function closeDialog() {
    addCompanyDialog.close();
}

function addCommentField(content='', parent_id='comments') {
    var commentSections = document.getElementById(parent_id);
    // commentSections.innerHTML = null;
    var newCommentField = document.createElement("input");
    newCommentField.type = "text";
    newCommentField.name = "comment";
    newCommentField.value = content;
    commentSections.appendChild(newCommentField);
}

function showEditDialog(id, record) {
    document.getElementById("editCompanyDialog").showModal();
    console.log(record['Comments']);
    if (!record['Comments']) {
        record['Comments'] = []
    }
    var formated_record = JSON.parse(record.replaceAll("'", '"'))
    console.log(formated_record);
    
    document.getElementById("e_id").value = id;
    document.getElementById("e_company_name").value = formated_record['Company name'];
    document.getElementById("e_field_of_work").value = formated_record['Field of work'];
    document.getElementById("e_address").value = formated_record['Address'];
    document.getElementById("e_mentor").value = formated_record['Name of Mentor/ Contact person'];
    document.getElementById("e_phone_number").value = formated_record['Phone number'];
    document.getElementById("e_email").value = formated_record['Email'];
    document.getElementById("e_website").value = formated_record['Website'];
    document.getElementById("e_max_students").value = formated_record['Max number of students'];
    document.getElementById("e_current_students").value = formated_record['Current student count'];
    document.getElementById("e_status").value = formated_record['Status'];
    document.getElementById("e_commute").value = formated_record['Commute'];
    document.getElementById("e_equipment").value = formated_record['Required additional equipment/ clothes'];
    document.getElementById("e_info").value = formated_record['Important information'];

    document.getElementById("e_comments").innerHTML = null;
    formated_record['Comments'].map((comment) => {
        addCommentField(comment.Content, 'e_comments');
    })
}


