var $ = django.jQuery;

$(document).ready(function() {
    $('.field-download_answers').click('a', function() {
        var answerText = this.children[1].textContent;
        var name = $(this).parent().children('th.field-respondent.nowrap').text();
        var a = document.createElement('a');
        a.setAttribute('download', name);
        a.setAttribute('href', 'data:test/plain;charset=utf-8,' + encodeURIComponent(answerText));
        a.click();
    })
});