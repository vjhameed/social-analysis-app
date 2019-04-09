$(function () {
  $('#menu1').metisMenu();
});

  $('.hash-section').click(function () {
      $('.hash-section').removeClass('selected')
      $(this).addClass('selected')
    })



  var filterdata = {
      lang: [],
      gender: [],
      social: [],
      date: [],
      sent: '',
      daterange:''
    };

    $('.date-range-filter').change(function(){
      filterdata.daterange = $(this).val()
      console.log(filterdata)
      makeFilterRequest()
    })

    $("input[type=range]").change(function () {
      console.log($(this).val())
      if($(this).val() == 1){
        filterdata.sent = 'Negative'
      }else if ($(this).val() == 3) {
        filterdata.sent = 'Positive'
      }else{
        filterdata.sent = ''
      }
      makeFilterRequest();
    });

    $(".lang-check").change(function () {
      if ($(this).is(":checked")) filterdata.lang.push($(this).val());
      else {
        var tempvar = filterdata.lang.filter(item => {
          return item !== $(this).val();
        });

        filterdata.lang = tempvar.map(item => item);
      }

      makeFilterRequest();
    });

    $(".gender-check").change(function () {
      $(this).val();
      if ($(this).is(":checked")) filterdata.gender.push($(this).val());
      else {
        var tempvar = filterdata.gender.filter(item => {
          return item !== $(this).val();
        });

        filterdata.gender = tempvar.map(item => item);
      }

      makeFilterRequest();
    });

    $(".social-check").change(function () {
      if ($(this).is(":checked")) filterdata.social.push($(this).val());
      else {
        var tempvar = filterdata.social.filter(item => {
          return item !== $(this).val();
        });

        filterdata.social = tempvar.map(item => item);
      }

      makeFilterRequest();
    });

    $(".date-check").change(function () {
      if ($(this).is(":checked")) filterdata.date.push($(this).val());
      else {
        var tempvar = filterdata.date.filter(item => {
          return item !== $(this).val();
        });

        filterdata.date = tempvar.map(item => item);
      }

      makeFilterRequest();
    });


    function createComment(el){
var newcom = $(".com-clone").clone();
$(newcom).removeClass("d-none");
$(newcom).removeClass("com-clone");
$(newcom)
.find(".com-user-img")
.attr("src", el.fields.user_image);
if (el.fields.source == "fb") {
  $(newcom)
    .find(".com-source")
    .addClass("fa-facebook");
  $(newcom).find('.social-source-name').text('facebook.com')
} else if (el.fields.source == "twit") {
  $(newcom)
    .find(".com-source")
    .addClass("fa-twitter");
  $(newcom).find('.social-source-name').text('twitter.com')
}
$(newcom)
  .find(".com-user-name")
  .text(el.fields.user_name);
$(newcom)
  .find(".com-user-follow")
  .text(el.fields.user_followers);

$(newcom)
  .find(".com-date")
  .text(el.fields.created_at);
$(newcom)
  .find(".mention_text")
  .text(el.fields.message);

$(newcom).appendTo(".comment-container");
}


function assignSidebar(data){

  var nomale,nofemale,nopositive,nonegative,nonuetral,noen,nofr,noar,noarz = ' '

  $(data).each(function(index, el) {
    if (el.fields.sentiment == "Positive") nopositive = nopositive + 1;
    else if (el.fields.sentiment == "Negative") nonegative = nonegative + 1;
    else nonuetral = nonuetral + 1;
    if (el.fields.gender == "Male") nomale = nomale + 1;
    else if (el.fields.gender == "Female") nofemale = nofemale + 1;
    if (el.fields.language == "en") noen = noen + 1;
    else if (el.fields.language == "fr") nofr = nofr + 1;
    else if (el.fields.language == "ar") noar = noar + 1;
    else if (el.fields.language == "arz") noarz = noarz + 1;
  })


  $("#filter-neg-count").text(nonegative)
  $("#filter-pos-count").text(nopositive)
  $("#filter-neu-count").text(nonuetral)

  $("#filter-male-count").text(nomale)
  $("#filter-female-count").text(nofemale)

  $("#filter-en-count").text(noen)
  $("#filter-fr-count").text(nofr)
  $("#filter-ar-count").text(noar)
  $("#filter-arz-count").text(noarz)

}