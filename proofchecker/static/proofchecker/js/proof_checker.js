// ---------------------------------------------------------------------------------------------------------------------
// list of variables  to store dom element ids/classes/names (difference between inlineformset vs modelformset
// ---------------------------------------------------------------------------------------------------------------------
const FORMSET_PREFIX = "proofline_set";                         // for modelformset - "form-"
const FORMSET_TOTALFORMS_ID = "id_proofline_set-TOTAL_FORMS";   // for modelformset - "id_form-TOTAL_FORMS"
const FORMSET_TBODY_ID = "proofline-list";                      // for modelformset - "proofline-list"
const FORMSET_TR_CLASS = "proofline_set";                       // for modelformset - "proofline-form"

// ---------------------------------------------------------------------------------------------------------------------

document.addEventListener('DOMContentLoaded', reload_page, false);


// ---------------------------------------------------------------------------------------------------------------------
// functions
// ---------------------------------------------------------------------------------------------------------------------
/**
 * this function will run once DOM contents are loaded
 */
function reload_page() {
    //this function will run on page load

    //will sort proof table based on ORDER field
    sort_table()
    //will decide which button to display between start and restart
    setStartRestartButtonAtBeginning()
}


/**
 * this function decides whether to show START_PROOF button or RESTART_PROOF button
 */
function setStartRestartButtonAtBeginning() {
    //if it finds first rule field and that has some value.. then restart button is displayed.
    if (document.getElementById(`id_${FORMSET_PREFIX}-0-rule`) !== null && document.getElementById(`id_${FORMSET_PREFIX}-0-rule`).value !== '') {
        document.getElementById("btn_start_proof").hidden = true
        document.getElementById("btn_restart_proof").classList.remove("hidden")
    }
}

/**
 * this function starts proof by inserting rows for premises and conclusions.
 */
function start_proof(element) {
    const premises = document.getElementById('id_premises').value;
    const premiseArray = premises.split(",").map(item => item.trim());
    const prooflineTableBody = document.getElementById(FORMSET_TBODY_ID);

    for (let i = 0; i < premiseArray.length; i++) {
        let newRow = insert_form_helper(i)
        let tds = newRow.children

        for (let x = 0; x < tds.length; x++) {
            let input = tds[x].children[0]
            // line_no
            if (x === 0) {
                input.setAttribute("readonly", true)
                input.setAttribute("value", i + 1)
            }
            // formula
            if (x === 1) {
                input.setAttribute("value", `${premiseArray[i]}`)
            }
            // rule
            if (x === 2) {
                input.setAttribute("value", 'Premise')
            }
            // if (i === 0) {
            //     if (x === 4) {
            //         input.style.visibility = 'hidden'
            //     }
            //     if (x === 5) {
            //         input.style.visibility = 'hidden'
            //     }
            //     if (x === 6) {
            //         input.style.visibility = 'hidden'
            //     }
            // }
        }
        prooflineTableBody.appendChild(newRow)
    }
    update_form_count()
    hide_conclude_button()
    element.hidden = true
    document.getElementById("btn_restart_proof").classList.remove("hidden")
    reset_order_fields()
}

/**
 * this function restarts proof by removing all rows and calling startProof method
 */
function restart_proof() {
    const prooflineList = document.getElementById(FORMSET_TBODY_ID);
    //delete all childs from Tbody and calls start_proof method
    delete_children(prooflineList)
    start_proof(document.getElementById("btn_start_proof"))
}


/**
 * Inserts form below current line
 */
function insert_form(obj) {
    //inserts new row with latest index at current object's next position
    insert_row_current_level(get_form_id(obj))
    hide_conclude_button()
    reset_order_fields()
}

/**
 * Inserts form below current line
 */
function create_subproof(obj) {
    const newlyInsertedRow = insert_new_form_at_index(get_form_id(obj) + 1);
    generate_new_subproof_row_number(newlyInsertedRow)
    hide_conclude_button()
    reset_order_fields()
}

/**
 * concludes subproof
 */
function conclude_subproof(obj) {
    insert_row_parent_level(get_form_id(obj))
    hide_conclude_button()
    reset_order_fields()
}

/**
 * delete current row
 */
function delete_form(obj) {
    delete_row(get_form_id(obj))
}


// ---------------------------------------------------------------------------------------------------------------------
// Helper functions
// ---------------------------------------------------------------------------------------------------------------------

/**
 * generates new subproof row number
 */
function generate_new_subproof_row_number(newlyInsertedRow) {

    // Get the row that the button was clicked
    const previousValidRow = getPreviousValidRow(newlyInsertedRow);
    const original_row_number_of_clicked_button = previousValidRow.children[0].children[0].value

    // Update row number of clicked button
    previousValidRow.children[0].children[0].value = `${original_row_number_of_clicked_button}.1`
    previousValidRow.children[2].children[0].value = 'Assumption'

    // Update the row number of the new row
    newlyInsertedRow.children[0].children[0].value = `${original_row_number_of_clicked_button}.2`
}


/**
 * inserts a row at current level when INSERT ROW button is clicked
 */
function insert_row_current_level(index) {
    const newRow = insert_new_form_at_index(index + 1);
    const prevRowInfo = getObjectsRowInfo(getPreviousValidRow(newRow));

    //get final value of prev row lineno and add 1 to it
    const prevRowLineNumberSegments = prevRowInfo.list_of_line_number;
    const prevRowLastNumberSegment = prevRowLineNumberSegments[prevRowLineNumberSegments.length - 1];
    //generating new row line numbers
    prevRowLineNumberSegments[prevRowLineNumberSegments.length - 1] = Number(prevRowLastNumberSegment) + 1
    newRow.children[0].children[0].value = prevRowLineNumberSegments.join('.')

    renumber_rows(1, newRow)
    reset_order_fields()
}

/**
 * inserts a row at parent level when CONCLUDE SUBPROOF button is clicked
 */
function insert_row_parent_level(index) {
    const newRow = insert_new_form_at_index(index + 1);
    const prevRowInfo = getObjectsRowInfo(getPreviousValidRow(newRow));

    //get final value of prev row lineno and add 1 to it
    const prevRowLineNumberSegments = prevRowInfo.prefix_of_row;
    const prevRowLastNumberSegment = prevRowLineNumberSegments[prevRowLineNumberSegments.length - 1];
    //generating new row line numbers
    prevRowLineNumberSegments[prevRowLineNumberSegments.length - 1] = Number(prevRowLastNumberSegment) + 1
    newRow.children[0].children[0].value = prevRowLineNumberSegments.join('.')

    renumber_rows(1, newRow)
    reset_order_fields()
}

/**
 * deletes the row where obj is located
 */
function delete_row(deleted_row_index) {
    const deleted_row = document.getElementById(FORMSET_PREFIX + '-' + deleted_row_index);
    deleted_row.classList.add("table-secondary")
    //mark checkbox true
    document.getElementById('id_' + FORMSET_PREFIX + '-' + deleted_row_index + '-DELETE').setAttribute("checked", "true")
    document.getElementById('id_' + FORMSET_PREFIX + '-' + deleted_row_index + '-insert-btn').disabled = true
    document.getElementById('id_' + FORMSET_PREFIX + '-' + deleted_row_index + '-create_subproof-btn').disabled = true
    document.getElementById('id_' + FORMSET_PREFIX + '-' + deleted_row_index + '-delete-btn').disabled = true
    document.getElementById('id_' + FORMSET_PREFIX + '-' + deleted_row_index + '-conclude_subproof-btn').disabled = true

    //hide row
    // document.getElementById(FORMSET_PREFIX+'-' + index).hidden = true;
    renumber_rows(-1, deleted_row)
    deleted_row.children[0].children[0].value = '0'

    //if id fields is empty that means this deleted (hidden now) row is a new row.. not existing one.. so we can actually remove it.
    if (document.getElementById('id_' + FORMSET_PREFIX + '-' + deleted_row_index + '-id').value === '') {
        document.getElementById(FORMSET_PREFIX + '-' + deleted_row_index).remove()
        pullupProoflineFormIndex(deleted_row_index)
        update_form_count()
    }
    reset_order_fields()
}



// ---------------------------------------------------------------------------------------------------------------------
// Helper functions
// ---------------------------------------------------------------------------------------------------------------------

/**
 * Helper function to set multiple attributes at once
 */
function setAttributes(el, attrs) {
    for (const key in attrs) {
        el.setAttribute(key, attrs[key]);
    }
}


/**
 * Call this at end of any function that changes the amount of forms
 */
function update_form_count() {
    const fomrsetManagerTotalFormCounter = document.getElementById(FORMSET_TOTALFORMS_ID)
    let currentFormCount = document.getElementsByClassName(FORMSET_TR_CLASS).length
    fomrsetManagerTotalFormCounter.setAttribute('value', currentFormCount)
}


/**
 * returns total formset lines by counting number of TR elements that has class name = FORMST_TR_CLASS
 */
function getTotalFormsCount() {
    return document.getElementsByClassName(FORMSET_TR_CLASS).length
}

/**
 * returns total formset lines from formset manager
 */
function getTotalFormsCountFromFormsetManager() {
    return parseInt(document.getElementById(FORMSET_TOTALFORMS_ID).value)
}


/**
 * updates total formset count in formset manager
 */
function setTotalFormsCountInFormsetManager(value) {
    document.getElementById(FORMSET_TOTALFORMS_ID).setAttribute('value', value)
}

/**
 * extract formset index (numeric part) from object's id
 */
function get_form_id(obj) {
    return parseInt(obj.id.replace(/[^0-9]/g, ""))
}


/**
 * delete children from any DOM element
 */
function delete_children(element) {
    let first = element.firstElementChild;
    while (first) {
        first.remove();
        first = element.firstElementChild;
    }
}


/**
 * this function reset ORDER (positional index) for each row. Django displays sorted lines based on this value
 */
function reset_order_fields() {
    const ORDER_fields = document.querySelectorAll('[id $= "-ORDER"]');
    let pos_index = 0;
    let index = null;
    for (let field of ORDER_fields) {
        if (field.id !== null && field.id.indexOf("__prefix__") < 0) {
            index = get_form_id(field)
            if (!document.getElementById(`${FORMSET_PREFIX}-${index}`).hidden) {
                field.value = pos_index++
                document.getElementById(`id_${FORMSET_PREFIX}-${index}-ORDER`).value = field.value
            } else {
                field.value = -1
            }

        }
    }
}


/**
 * this function sorts formset table based on ORDER (input no 9) field.
 */
function sort_table() {
    let switch_flag;
    let i, x, y;
    let switching = true;

    // Run loop until no switching is needed
    while (switching) {
        switching = false;
        const rows = document.getElementsByClassName(FORMSET_TR_CLASS);
        // Loop to go through all rows
        for (i = 1; i < (rows.length - 1); i++) {
            switch_flag = false;

            // Fetch 2 elements that need to be compared
            x = rows[i].getElementsByTagName("input")[9].value
            y = rows[i + 1].getElementsByTagName("input")[9].value
            console.log(x)

            // Check if 2 rows need to be switched
            if (parseInt(x) > parseInt(y)) {
                // If yes, mark Switch as needed and break loop
                switch_flag = true;
                break;
            }
        }
        if (switch_flag) {
            // Function to switch rows and mark switch as completed
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
        }
    }
}


/**
 * Text replacement - replaces escape commands with symbols
 */
function replaceCharacter(ev) {
    let txt = document.getElementById(ev.id).value;
    txt = txt.replace("\\and", "∧");
    txt = txt.replace("\\or", "∨");
    txt = txt.replace("\\implies", "→");
    txt = txt.replace("\\not", "¬");
    txt = txt.replace("\\iff", "↔");
    txt = txt.replace("\\contradiction", "⊥");
    document.getElementById(ev.id).value = txt;
}


/**
 * this function clones empty form and get it ready for insertion at provided index
 */
function insert_form_helper(index) {
    const emptyFormElement = document.getElementById('empty-form').cloneNode(true)
    emptyFormElement.setAttribute("class", FORMSET_TR_CLASS)
    emptyFormElement.setAttribute("id", `${FORMSET_PREFIX}-${index}`)
    const regex = new RegExp('__prefix__', 'g')
    emptyFormElement.innerHTML = emptyFormElement.innerHTML.replace(regex, index)
    return emptyFormElement
}


/**
 * this function insert a new form at provided index
 */
function insert_new_form_at_index(index) {
    const getNextIndex = getTotalFormsCount(); //get the latest index
    const emptyFormElement = insert_form_helper(getNextIndex)
    const proof_tbody = document.getElementById(FORMSET_TBODY_ID)
    const proof_table_row = document.getElementById(FORMSET_PREFIX + '-' + (index - 1))
    if (proof_table_row !== null) {
        proof_table_row.after(emptyFormElement)
    } else {
        proof_tbody.append(emptyFormElement)
    }
    update_form_count()
    reset_order_fields()
    return emptyFormElement
}

/**
 * this function gets line no details of row at provided index
 */
function get_row(index) {
    const row_object = document.getElementById(FORMSET_PREFIX + '-' + (index));
    // Get line number of the row
    const line_number_of_row = row_object.children[0].children[0].value;
    // Get list of number of row
    const list_of_line_number = line_number_of_row.split('.');
    // Get the prefix of the row
    const prefix_of_row = list_of_line_number.slice(0, -1);
    // Get the string of the prefix
    const string_of_prefix = prefix_of_row.join('.');
    // Get the final value of row
    const final_value = list_of_line_number.slice(-1);

    return {
        // Get object of the row
        "row_object": row_object,
        // Get line number of the row
        "line_number_of_row": line_number_of_row,
        // Get list of number of row
        "list_of_line_number": list_of_line_number,
        // Get the prefix of the row
        "prefix_of_row": prefix_of_row,
        // Get the string of the prefix
        "string_of_prefix": string_of_prefix,
        // Get the final value of row
        "final_value": final_value,
    }
}

/**
 * this function gets line no details of row at provided object's index
 */
function getObjectsRowInfo(row_object) {
    return get_row(get_form_id(row_object))
}


/**
 * this function finds next row in formset but ignores row(s) that is/are marked for deletion
 */
function getNextValidRow(currRow) {
    let nextRow = null;
    do {
        try {
            nextRow = currRow.nextElementSibling;
            if (nextRow.tagName === 'TR' && nextRow.classList.contains(FORMSET_TR_CLASS) && nextRow.children[7].children[1].getAttribute('checked') !== 'true') {
                break;
            } else {
                currRow = nextRow;
            }
        } catch (Error) {
            break;
        }
    } while (nextRow !== null && nextRow.tagName === 'TR')

    return nextRow;
}


/**
 * this function finds previous row in formset but ignores row(s) that is/are marked for deletion
 */
function getPreviousValidRow(currRow) {
    let prevRow = null;
    do {
        try {
            prevRow = currRow.previousElementSibling;
            if (prevRow.tagName === 'TR' && prevRow.classList.contains(FORMSET_TR_CLASS) && prevRow.children[7].children[1].getAttribute('checked') !== 'true') {
                break;
            } else {
                currRow = prevRow
            }
        } catch (Error) {
            break;
        }
    } while (prevRow !== null && prevRow.tagName === 'TR')

    return prevRow;
}


/**
 * this function reset line numbers in formset
 */
function renumber_rows(direction, newlyChangedRow) {

    //getting currentRow that just got changed
    const currRow = newlyChangedRow;
    //getting the following valid row (ignoring rows that are already marked for deletion)
    let nextRow = getNextValidRow(currRow);

    //if there's no next row then no need to renumber the rows
    if (nextRow !== null) {
        //getting line no info of current row
        const currRowInfo = getObjectsRowInfo(newlyChangedRow);
        //getting line no info of next row
        let nextRowInfo = getObjectsRowInfo(nextRow);

        //finding out the index of changed element in line number list. if line number has 3 levels like 3.1 need to know which index got updated
        //for new rows that is the last item
        //next sets of rows that has the same prefix as inserted row... we'll update their line number element that is on the same level (index) .. i.e. 3.*
        const index_of_changing_element = currRowInfo.list_of_line_number.length - 1;
        const prefix_values_string = currRowInfo.prefix_of_row.join('.');  // Get the prefix value string

        //will loop thru all the succeeding rows in formset
        while (nextRow !== null && nextRow.tagName === 'TR' && nextRow.classList.contains(FORMSET_TR_CLASS)) {

            //for insertion -- if current row is 3.1.1 and we do not have to increase line no for row that is on higher level than current row.. so 3.2 will not get updated.
            if (direction === 1 && currRowInfo.list_of_line_number.length > nextRowInfo.list_of_line_number.length) {
                break;
            }

            // get next form line no and line no list
            const next_row_line_no = nextRowInfo.line_number_of_row;
            const next_row_line_no_list = nextRowInfo.list_of_line_number;

            //if next row starts with current row's prefix then we will increase (for insert / direction 1) or decrease (for deletion / direction -1) next row's line number
            if (next_row_line_no.startsWith(prefix_values_string)) {
                next_row_line_no_list[index_of_changing_element] = Number(next_row_line_no_list[index_of_changing_element]) + direction
                const new_row_number = next_row_line_no_list.join('.');
                nextRow.children[0].children[0].value = new_row_number
            }

            //setting up next for for next loop
            nextRow = getNextValidRow(nextRow)
            nextRowInfo = (nextRow !== null) ? getObjectsRowInfo(nextRow) : null;
        }

    }
}


/**
 * this function reset line numbers in formset
 */
function pullupProoflineFormIndex(to_index) {
    const last_form_element_id = getTotalFormsCountFromFormsetManager() - 1;
    for (let i = to_index + 1; i <= last_form_element_id; i++) {
        updateFormsetId(i, i - 1)
    }
}


/**
 * this function updates formset id. When a newly created row is deleted from DOM (in create and update scenario) we will need to pull up the indexes of succeeding rows.
 * in case of deleting rows that is currently in DB we are not deleting them from DOM so no need to update formset ids in that case.
 */
function updateFormsetId(old_id, new_id) {
    const targeted_element = document.getElementById(FORMSET_PREFIX + '-' + old_id)
    if (targeted_element !== null) {
        document.getElementById(FORMSET_PREFIX + '-' + old_id).setAttribute('id', `${FORMSET_PREFIX}-${new_id}`)
        const fields = ['line_no', 'formula', 'rule', 'insert-btn', 'create_subproof-btn', 'conclude_subproof-btn', 'delete-btn', 'id', 'DELETE', 'ORDER']
        fields.forEach(function (field) {
            document.getElementById('id_' + FORMSET_PREFIX + '-' + old_id + '-' + field).setAttribute('name', `${FORMSET_PREFIX}-${new_id}-${field}`)
            document.getElementById('id_' + FORMSET_PREFIX + '-' + old_id + '-' + field).setAttribute('id', `id_${FORMSET_PREFIX}-${new_id}-${field}`)

            //this is temporary for debugging purpose. added index in INSERT ROW button value
            if (field === 'insert-btn') document.getElementById(`id_${FORMSET_PREFIX}-${new_id}-${field}`).setAttribute('value', `Insert Row ${new_id}`)
        })
    }
}



/**
 * hides conclude subproof button wherever applicable
 * ***** NEED TO WORK ON IT *****
 */
function hide_conclude_button() {
    const forms = document.getElementsByClassName(FORMSET_TBODY_ID)
    const number_of_forms = forms.length - 1;

    for (let current_form = 0; current_form <= number_of_forms; current_form++) {
        const current_row = get_row(current_form);
        if (current_form === 0) {
            document.getElementById(`${FORMSET_PREFIX}-${current_form}`).children[6].children[0].style.visibility = 'hidden'
        } else if (current_form < number_of_forms) {
            const next_row = get_row(current_form + 1);
            if (current_row.string_of_prefix == next_row.string_of_prefix) {
                document.getElementById(`${FORMSET_PREFIX}-${current_form}`).children[6].children[0].style.visibility = 'hidden'
            }
        } else if (current_row.list_of_line_number.length <= 1) {
            document.getElementById(`${FORMSET_PREFIX}-${current_form}`).children[6].children[0].style.visibility = 'hidden'
            break
        }
    }
}

// ---------------------------------------------------------------------------------------------------------------------
