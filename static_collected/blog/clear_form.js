let clear_forms = (elementID)=> {
    console.log('test message')

    document.getElementById(elementID).getElementsByTagName('input').forEach((input)=>{
        switch(input.type) {
            case 'password':
            case 'text':
            case 'textarea':
            case 'file':
            case 'select-one':
            case 'select-multiple':
            case 'date':
            case 'number':
            case 'tel':
            case 'email':
                input.value = '';
                break;
            case 'checkbox':
            case 'radio':
                input.checked = false;
                break;
        }
    }); 
  }