var $ = django.jQuery;

$(document).ready(function() {
    $('.field-download_answers').click('a', function() {
        var answerText = this.children[1];
        console.log($(this).parent().children('th.field-respondent.nowrap'))
        var a = document.createElement('a');
        a.href = 'data:text;charset=utf-8,' + answerText;
        a.target = '_blank';
        a.download = ''
    })
});