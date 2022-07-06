let blankForm = document.getElementsByClassName("form")[0].cloneNode(true)
let blankFormInputs = blankForm.getElementsByTagName("input")

for (var i = 0; i < blankFormInputs.length; i++) {
  blankFormInputs[i].value = ""
}

function addNew() {
  let allFormsWrapper = document.getElementById("allForms")
  let allForms = document.getElementsByClassName("form")

  if (allFormsWrapper.length > 99) {
    alert("You can only add 100 students in a time")
    return
  }

  let formInputIds = []
  for (var i = 0; i < allFormsWrapper.length; i++) {
    formInputIds.push(parseInt(allFormsWrapper[i].firstChild.name.split('-')[1]))
  }

  let newFormName = `forms-${Math.max(formInputIds) + 1}-`
  let newForm = blankForm.cloneNode(true)
  let formInputs = newForm.getElementsByTagName("input")

  for (var i = 0; i < formInputs.length; i++) {
    form_name = formInputs[i].name.split('-')[2]
    formInputs[i].setAttribute("name", newFormName + form_name)
    formInputs[i].setAttribute("id", newFormName + form_name)
  }

  allFormsWrapper.appendChild(newForm)
}

function deleteForm(el) {
  el.parentNode.remove()
}

function markAll() {
  var marks = document.getElementsByClassName("mark")
  for (var i = 0; i < marks.length; i++) {
    marks[i].checked = true
  }
}

function unmarkAll() {
  var marks = document.getElementsByClassName("mark")
  for (var i = 0; i < marks.length; i++) {
    marks[i].checked = false
  }
}

function deleteMarked() {
  var marks = document.getElementsByClassName("mark")
  let toRemove = []
  for (var i = 0; i < marks.length; i++) {
    if (marks[i].checked == true) {
      toRemove.push(marks[i])
    }
  }
  for (var i = 0; i < toRemove.length; i++) {
    deleteForm(toRemove[i])
  }
}

function addSeveral() {
  let number = document.getElementById("addSeveralInput").value
  while (number>0) {
    addNew()
    number -= 1
  }
  document.getElementById("addSeveralInput").value = ''
}

function dublicateEverywhere(field, el) {
  var forms = document.getElementsByClassName("form")
  let new_value = el.parentNode.getElementsByClassName(field)[0].value
  for (var i = 0; i < forms.length; i++) {
    forms[i].getElementsByClassName(field)[0].value = new_value
  }
}