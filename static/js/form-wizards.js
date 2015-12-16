var handleBootstrapWizardsValidation = function() {
    "use strict";
    $("#mysubmit").removeClass( "btn-primary" ).attr("disabled", "disabled");
    $("#wizard").bwizard({ validating: function (e, ui) { 
            if (ui.index == 0) {
                // step-1 validation
                if (false === $('form[name="form-wizard"]').parsley().validate('primary')) {
                    return false;
                }
            } else if (ui.index == 1) {
                // step-2 validation
                  if (false === $('form[name="form-wizard"]').parsley().validate('primary1')) {
                    return false;
                }
            } else if (ui.index == 2) {
                // step-3 validation
                if (false === $('form[name="form-wizard"]').parsley().validate('primary2')) {
                    return false;
                }else{
                    $("#mysubmit").addClass( "btn-primary" ).removeAttr("disabled");
                }
            } else if (ui.index == 3) {
                // step-4 validation
                $("#mysubmit").addClass( "btn-primary" ).removeAttr("disabled");
                if (false === $('form[name="form-wizard"]').parsley().validate('primary3')) {
                    return false;
                }
            }
        } 
    });
};

var FormWizardValidation = function () {
    "use strict";
    return {
        //main function
        init: function () {
            handleBootstrapWizardsValidation();
        }
    };
}();