
const toggleChatButton = document.getElementById('toggle-chat-button');
const chatBox = document.getElementById('chat-box');

toggleChatButton.addEventListener('click', () => {
    if (chatBox.classList.contains('d-none')) {
        chatBox.classList.remove('d-none');
        toggleChatButton.textContent = 'Close';
    } else {
        chatBox.classList.add('d-none');
        toggleChatButton.textContent = 'Chat';
    }
});

$(document).ready(function() {
      $('#modal_trigger, #modal_trigger2').click(function() {
          $('#modal').fadeIn();
          return false;
      });
  
      $('.modal_close').click(function() {
          $('#modal').fadeOut();
          return false;
      });
  });

const jsonData = {
    servicesHeading: "Amazing <em>Services &amp; Features</em> for you",
    headingLineImageSrc: "{% static 'assets/images/heading-line-dec.png' %}",
    servicesParagraph:
    "If you need the greatest collection of HTML templates for your business, please visit <a rel='nofollow' href='https://www.toocss.com/' target='_blank'>TooCSS</a> Blog. If you need to have a contact form PHP script, go to <a href='https://templatemo.com/contact' target='_parent'>our contact page</a> for more information.",
    headerText: "Get The Latest App From App Stores",
    paragraphText: "Chain App Dev is an app landing page HTML5 template based on Bootstrap v5.1.3 CSS layout provided by TemplateMo, a great website to download free CSS templates.",
    buttonOne: [
      { text: "Free Quote", link: "#contact" },
      { text: "Button One Alternate", link: "#alt-link" }
    ],
    buttonTwo: [
      { text: "Free Quote", link: "#contact" },
      { text: "Button Two Alternate", link: "#alt-link" }
    ],
    mainImage: [
      "{% static 'assets/images/slider-dec.png' %}",
      "{% static 'assets/images/another-image.png' %}"
    ]
  };

  // Function to set data for buttons
  function setButtonData(buttonId, buttonData) {
    const buttonElement = document.getElementById(buttonId);
    if (buttonElement) {
      for (const item of buttonData) {
        const button = document.createElement("a");
        button.textContent = item.text;
        button.setAttribute("href", item.link);
        buttonElement.appendChild(button);
      }
    }
  }

  // Set data for header text and paragraph
  document.getElementById("headerText").textContent = jsonData.headerText;
  document.getElementById("paragraphText").textContent = jsonData.paragraphText;

  // Set data for buttons
  setButtonData("buttonOne", jsonData.buttonOne);
  setButtonData("buttonTwo", jsonData.buttonTwo);

  // Set data for images
  const mainImageElement = document.getElementById("mainImage");
  if (mainImageElement) {
    // Set the src attribute to the first image URL in the jsonData array
    mainImageElement.setAttribute("src", jsonData.mainImage[0]);
    // Set an appropriate alt text
    mainImageElement.setAttribute("alt", "Image Description");
  }
  $(document).ready(function () {
      $('#orderForm').submit(function (e) {
          e.preventDefault();
          $.ajax({
              type: 'POST',
              url: '/order_service_js/',
              data: $('#orderForm').serialize(),
              dataType: 'json',
              success: function (data) {
                  // Close the modal after successful submission
                  $('#orderModal').modal('hide');
                  alert(data.message);
              },
              error: function () {
                  alert('An error occurred. Please try again later.');
              }
          });
      });
  });

  $(document).ready(function () {
      $('#search').submit(function (e) {
          e.preventDefault();
          $.ajax({
              type: 'POST',
              url: '/collect_email/',  // URL to your Django view
              data: $('#search').serialize(),
              dataType: 'json',
              success: function (data) {
                  if (data.message === 'Success') {
                      alert('Thank you for subscribing!');
                  } else {
                      alert('Error: ' + data.errors.email);
                  }
              },
              error: function () {
                  alert('An error occurred. Please try again later.');
              }
          });
      });
  });
