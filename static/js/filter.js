var filterdata = {
  lang: [],
  gender: [],
  social: [],
  date: []
};

$(".lang-check").change(function() {
  $(this).val();
  if ($(this).is(":checked")) filterdata.lang.push($(this).val());
  else {
    var tempvar = filterdata.lang.filter(item => {
      return item !== $(this).val();
    });

    filterdata.lang = tempvar.map(item => item);
  }

  makeFilterRequest();
});

$(".gender-check").change(function() {
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

$(".social-check").change(function() {
  $(this).val();
  if ($(this).is(":checked")) filterdata.social.push($(this).val());
  else {
    var tempvar = filterdata.social.filter(item => {
      return item !== $(this).val();
    });

    filterdata.social = tempvar.map(item => item);
  }

  makeFilterRequest();
});

$(".date-check").change(function() {
  $(this).val();
  if ($(this).is(":checked")) filterdata.date.push($(this).val());
  else {
    var tempvar = filterdata.date.filter(item => {
      return item !== $(this).val();
    });

    filterdata.date = tempvar.map(item => item);
  }

  makeFilterRequest();
});

function makeFilterRequest() {
  const project_id = $("input[name=pro_id]").val();
  $(".loader").removeClass("d-none");
  axios
    .post("/dashboard/filter/results", {
      lng: filterdata.lang,
      gen: filterdata.gender,
      social: filterdata.social,
      date: filterdata.date,
      pro_id: project_id
    })
    .then(resp => {
      console.log(resp);
      $(".loader").addClass("d-none");
      $(".comment-container").empty();
      var data = JSON.parse(resp.data);

      $(data).each(function(index, el) {
        var newcom = $(".com-clone").clone();
        $(newcom).removeClass("d-none");
        $(newcom).removeClass("com-clone");
        $(newcom)
          .find(".com-user-img")
          .attr("src", el.fields.user_image);
        if (el.fields.source == "fb")
          $(newcom)
            .find(".com-source")
            .addClass("fa-facebook");
        else if (el.fields.source == "twit")
          $(newcom)
            .find(".com-source")
            .addClass("fa-twitter");

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
      });
    })
    .catch(resp => {
      $(".loader").addClass("d-none");

      console.log(resp);
    });
}

var DoughtnutConfig = {
  type: "doughnut",
  data: {
    datasets: [
      {
        data: [randomScalingFactor(), randomScalingFactor()],
        backgroundColor: ["#CF6766", "#30415D"],
        label: "Dataset 1"
      }
    ],
    labels: [
      "Negative " + randomScalingFactor(),
      "Positive " + randomScalingFactor()
    ]
  },
  options: {
    responsive: true,
    legend: {
      position: "top"
    }
  }
};

window.myDoughnut = new Chart(
  document.getElementById("doughnutChartSentiment"),
  DoughtnutConfig
);
