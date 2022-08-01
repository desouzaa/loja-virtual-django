// Step #getIdentificationTypes

// Helper function to append option elements to a select input
function createSelectOptions(elem, options, labelsAndKeys = { label : "name", value : "id"}){
    const {label, value} = labelsAndKeys;
 
    elem.options.length = 0;
 
    const tempOptions = document.createDocumentFragment();
 
    options.forEach( option => {
        const optValue = option[value];
        const optLabel = option[label];
 
        const opt = document.createElement('option');
        opt.value = optValue;
        opt.textContent = optLabel;
 
        tempOptions.appendChild(opt);
    });
 
    elem.appendChild(tempOptions);
 }
 
 // Get Identification Types
 (async function getIdentificationTypes () {
    try {
        const identificationTypes = await mp.getIdentificationTypes();
        const docTypeElement = document.getElementById('docType');
 
        createSelectOptions(docTypeElement, identificationTypes)
    }catch(e) {
        return console.error('Error getting identificationTypes: ', e);
    }
 })()