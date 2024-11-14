/**
 * Contains code for home page
 */



const reviewContainer = document.querySelector(".review-container")
const reviewSlideShow = new SlideShow(reviewContainer, true, 10000)


const reviewModal = new Modal(document.querySelector("#modal"))

function toggleAccordion(element) {
    // Toggle the expanded class on the clicked element
    element.classList.toggle('expanded');
  
    // Change the arrow direction
    const icon = element.querySelector('.toggle-icon');
    if (element.classList.contains('expanded')) {
      icon.innerHTML = '&#x25B4;'; // Up arrow
      if (window.innerWidth < 768) {
        element.scrollIntoView({behavior: "smooth", block: "start", inline: "nearest"});
      }
    } else {
      icon.innerHTML = '&#x25BE;'; // Down arrow
      if (window.innerWidth < 768) {
        element.scrollIntoView({behavior: "smooth", block: "start", inline: "nearest"});
      }
    }
  
    // Close other accordion items
    const allCards = document.querySelectorAll('.accordion-card');
    allCards.forEach((card) => {
      if (card !== element) {
        card.classList.remove('expanded');
        card.querySelector('.toggle-icon').innerHTML = '&#x25BE;';
      }
    });
  }