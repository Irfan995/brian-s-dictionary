function showHidePassword(inputId, iconType) {
    if ($(inputId).attr('type') === 'password') {
        $(inputId).attr('type', 'text');

        if (iconType === 'password') {
            $('#password-hide-icon').hide();
            $('#password-show-icon').show();
        } else {
            $('#confirm-password-hide-icon').hide();
            $('#confirm-password-show-icon').show();
        }
    } else if ($(inputId).attr('type') === 'text') {
        $(inputId).attr('type', 'password');

        if (iconType === 'password') {
            $('#password-show-icon').show();
            $('#password-hide-icon').show();
        } else {
            $('#confirm-password-show-icon').show();
            $('#confirm-password-hide-icon').show();
        }
    }
}