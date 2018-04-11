
kara.app = Class.extend({
    init: function(opts) {
        $.extend(this, opts);
        this.setupReady();
    },
    setupReady: function() {
        _.flatMap(kara.fun.setup(kara, 'init'), function(clsObj) {
            for (var obj in clsObj) {
                clsObj[obj].init();
            }
        });

        baka.d.on('click', '._action', function(e){
            e.preventDefault();
            kara.ui.actions.do(this);
        });

        $('._action').on('click', function(e){
            e.preventDefault();
            kara.ui.actions.do(this);
        });

        baka.d.on('click', 'form._ajax input[type=submit]', function (e) {
            e.preventDefault();
            baka.logger('kara.app').debug('form._ajax');
            kara.ui.forms.submit($(this).closest('form._ajax'));
        });
//
//        baka.d.on('click', '.flashbar', function(e){
//            e.preventDefault();
//            $('.flashbar').html('');
//        });
    }
});
$(document).ready(function(){new kara.app()});
