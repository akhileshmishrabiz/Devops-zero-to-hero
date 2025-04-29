document.addEventListener("DOMContentLoaded", async function() {
  let currentItems = 6; // starting number of items to display
  //let votingServiceAvailable = false; // global variable to store voting service status

  await checkVotingServiceStatus();
  //setInterval(checkVotingServiceStatus, 30000);  // checks voting service status every 30 se

  fetch('/api/products')
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok' + response.statusText);
      }
      return response.json();
    })
    .then(data => {
      // Render initial batch of products
      renderProducts(data.slice(0, currentItems), votingServiceAvailable);

      // Remove loading message
      document.getElementById('loading-message').style.display = 'none';

      // Set up infinite scroll
      window.addEventListener('scroll', function() {
        if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight) {
          currentItems += 6; // add 6 more items each time
          renderProducts(data.slice(0, currentItems), votingServiceAvailable);
        }
      });
    })
    .catch((error) => {
      console.error('There has been a problem with your fetch operation:', error);
    });

  document.addEventListener('click', function(event) {
    if (event.target.classList.contains('read-more')) {
      event.preventDefault();
      
      const descId = event.target.getAttribute('data-desc-id');
      const fullDescId = `full-${descId}`;
      
      document.getElementById(descId).classList.toggle('hidden');
      document.getElementById(fullDescId).classList.toggle('hidden');
    }
  });


  // Fetch and display service status
  fetchServiceStatus();

  // Fetch and display daily origami
  fetchDailyOrigami();

  checkRecommendationStatus()

  // Check status at regular intervals
  // setInterval(checkRecommendationStatus, 5000);
  // setInterval(fetchServiceStatus, 5000);
});

function renderProducts(products, canVote) {
  // Logic to display products on the page
  const productContainer = document.getElementById('products');
  productContainer.innerHTML = ''; // clear the existing items before appending
  products.forEach(product => {
    const productElement = document.createElement('div');
    productElement.className = 'product';
    productElement.innerHTML = `
      <h3>${product.name}</h3>
      <img src="${product.image_url}" alt="${product.name}" />
      <p id="votes-${product.id}">Votes: Loading...</p>
      ${canVote ? `<button onclick="submitVote(${product.id})">Vote 👍</button>` : ''}
      <p class="description" id="desc-${product.id}">${shortenDescription(product.description)}</p>
      <a href="#" class="read-more" data-desc-id="desc-${product.id}">Read More</a>
      <p class="full-description hidden" id="full-desc-${product.id}">${product.description}</p>
    `;
    productContainer.appendChild(productElement);
    // Fetch votes for this origami
    fetchVotesForOrigami(product.id);
  });
}

function fetchVotesForOrigami(origamiId) {
    fetch(`/api/origamis/${origamiId}/votes`)
        .then(response => response.json())
        .then(votes => {
            let votesElem = document.querySelector(`#votes-${origamiId}`);
            votesElem.textContent = `Votes: ${votes}`;
        });
}

function submitVote(productId) {
    fetch(`/api/origamis/${productId}/vote`, {
        method: 'POST'
    })
    .then(response => {
        if(response.ok) {
            // Update UI accordingly
            //alert('Thank you for your vote!');
            // Optionally, re-fetch and update the vote count display
            fetchVotesForOrigami(productId);
        } else {
            alert('Vote did not get registered. Try again later.');
        }
    })
    .catch(error => {
        console.error('Error submitting vote:', error);
        alert('An error occurred while submitting your vote. Please try again later.');
    });
}


function shortenDescription(description, length = 100) {
  if(description.length > length) {
    return `${description.substring(0, length)}...`;
  } else {
    return description;
  }
}

function fetchServiceStatus() {
  fetch('/api/service-status')
    .then(response => response.json())
    .then(data => {
      renderServiceStatus(data);
    })
    .catch((error) => {
      console.error('Error fetching service status:', error);
    });
}

function renderServiceStatus(status) {
  const statusGrid = document.getElementById('status-grid');
  // statusGrid.innerHTML = ''; // clear the existing items
  
  Object.keys(status).forEach(service => {
    const statusBox = document.createElement('div');
    statusBox.className = `status-box ${status[service]}`;
    statusBox.innerHTML = `
      <h4>${capitalizeFirstLetter(service)}</h4>
      <p>${capitalizeFirstLetter(status[service])}</p>
    `;
    statusGrid.appendChild(statusBox);
  });
}

function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}


function fetchDailyOrigami() {
  fetch('/daily-origami')
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok ' + response.statusText);
      }
      return response.json();
    })
    .then(data => {
        renderDailyOrigami(data);
    })
    .catch(error => {
        console.error('Error fetching the daily origami:', error);
        renderDailyOrigamiFallback();
    });
}

function renderDailyOrigami(data) {
    // Get the container where the origami should be displayed
    const origamiContainer = document.getElementById('daily-origami-container');

    // Clear any existing content
    origamiContainer.innerHTML = '';

    // Create and add a header
    const header = document.createElement('h2');
    header.innerText = 'Origami of the Day';
    origamiContainer.appendChild(header);

    // Create new HTML elements and set their properties
    const img = document.createElement('img');
    img.src = data.image_url;
    img.alt = 'Daily Origami';

    const description = document.createElement('p');
    description.innerText = data.description;

    const name = document.createElement('h2');
    name.innerText = data.name;


    // Append the new elements to the container
    origamiContainer.appendChild(img);
    origamiContainer.appendChild(name);
    origamiContainer.appendChild(description);
}


function renderDailyOrigamiFallback() {
    // Get the container where the origami should be displayed
    const origamiContainer = document.getElementById('daily-origami-container');
    
    // Clear any existing content
    origamiContainer.innerHTML = '';
    
    // Add a fallback message
    origamiContainer.innerHTML = '<p>Sorry, the recommendation engine is not available at the moment.</p>';
}


function checkRecommendationStatus() {
    fetch('/recommendation-status')
        .then(response => response.json())
        .then(data => {
            renderRecommendationStatus(data);
        })
        .catch(error => {
            console.error('Error fetching recommendation service status:', error);
        });
}

function renderRecommendationStatus(status) {
  const statusGrid = document.getElementById('status-grid');
  
  const statusBox = document.createElement('div');
  statusBox.className = `status-box ${status.status}`;
  statusBox.innerHTML = `
    <h4>Recommendation</h4>
    <p>${capitalizeFirstLetter(status.status)}</p>
  `;
  statusGrid.appendChild(statusBox);
}

let votingServiceAvailable = false; // global variable to store voting service status

function checkVotingServiceStatus() {
    fetch('/votingservice-status')
	.then(response => {
            if (response.ok) {
                votingServiceAvailable = true;
		return response.json(); 
            } else {
                votingServiceAvailable = false;
                throw new Error('Service not available'); // Throwing an error to be caught in the catch block
            }
        })
        .then(data => {
            renderVotingServiceStatus(data);
        })
        .catch(error => {
            console.error('Error fetching voting service status:', error);
	    votingServiceAvailable = false;
        });
}

function renderVotingServiceStatus(status) {
  const statusGrid = document.getElementById('status-grid');

  const statusBox = document.createElement('div');
  statusBox.className = `status-box ${status.status}`;
  statusBox.innerHTML = `
    <h4>Voting</h4>
    <p>${capitalizeFirstLetter(status.status)}</p>
  `;
  statusGrid.appendChild(statusBox);
}
